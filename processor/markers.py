"""
Marker mode: cluster-level cell typing from marker gene sets (as in st-celltype).

A marker set is a cell type and its genes, each with a weight (default 1; a negative weight marks
a gene the type should not express). Sets come from markers.csv on the `markers` input
(`cell_type, gene[, weight]`, one gene per row) or from a built-in table (processor/markers/*.csv,
chosen by MARKER_SET). Symbols are matched case-insensitively, so the human tables also match
mouse and rat symbols (CD3E ~ Cd3e).

Per sample, each gene gets scanpy.tl.score_genes (its log-normalized expression minus that of
control genes drawn from the same expression bin; Satija et al. 2015, Tirosh et al. 2016) and a
set's score is the weighted mean of its genes' scores. Every set's score is then z-scored over
all cells of all samples. A cluster is called the set with the highest mean z-score when that
mean is positive and beats the runner-up by MARGIN; otherwise it is Unassigned. The
cell_type_score of its cells is the cluster's agreement: the fraction of its cells whose own
highest-scoring set is the cluster's best set (reported, not used for the call: single nuclei are
sparse, so per-cell calls among many related subtypes disagree even in a clean cluster).
"""
from __future__ import annotations

import csv
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

log = logging.getLogger("sc-annotate")

BUILTIN_DIR = Path(__file__).resolve().parent / "markers"
UNASSIGNED = "Unassigned"
MAX_MARKERS_BYTES = 5 * 2**20
SAFE = re.compile(r"[^A-Za-z0-9_+./()' -]+")


@dataclass
class MarkerSet:
    cell_type: str
    weights: dict[str, float]                                   # gene as given -> weight
    present: dict[str, float] = field(default_factory=dict)     # var_name -> weight
    missing: list[str] = field(default_factory=list)


def builtin_names() -> list[str]:
    return sorted(p.stem for p in BUILTIN_DIR.glob("*.csv"))


def read_markers_csv(path: Path) -> list[MarkerSet]:
    """cell_type, gene[, weight]: one gene per row; extra columns (e.g. source) are ignored."""
    if path.stat().st_size > MAX_MARKERS_BYTES:
        raise ValueError(f"{path.name} is larger than {MAX_MARKERS_BYTES // 2**20} MB")
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        cols = {c.strip().lower(): c for c in (reader.fieldnames or []) if c}
        if "cell_type" not in cols or "gene" not in cols:
            raise ValueError(f"{path.name}: needs the columns cell_type and gene (and optionally weight); found {list(cols)}")
        sets: dict[str, dict[str, float]] = {}
        for i, row in enumerate(reader, start=2):
            ct = re.sub(r"\s+", " ", SAFE.sub("", row[cols["cell_type"]] or "")).strip()
            gene = (row[cols["gene"]] or "").strip()
            if not ct or not gene:
                continue
            raw = (row.get(cols["weight"]) or "").strip() if "weight" in cols else ""
            try:
                w = float(raw) if raw else 1.0
            except ValueError as exc:
                raise ValueError(f"{path.name} line {i}: weight {raw!r} is not a number") from exc
            if not np.isfinite(w):
                raise ValueError(f"{path.name} line {i}: weight must be finite")
            if w != 0:
                sets.setdefault(ct, {})[gene] = w
    out = [MarkerSet(ct, w) for ct, w in sets.items() if any(v > 0 for v in w.values())]
    if not out:
        raise ValueError(f"{path.name}: no cell type with a positively weighted gene")
    return out


def load_sets(marker_set: str, markers_csv: Path | None) -> tuple[list[MarkerSet], str]:
    """A linked markers.csv wins over MARKER_SET; else the built-in table MARKER_SET names."""
    if markers_csv is not None:
        return read_markers_csv(markers_csv), "markers.csv"
    return read_markers_csv(BUILTIN_DIR / f"{marker_set}.csv"), f"builtin:{marker_set}"


def resolve(sets: list[MarkerSet], var_names, min_genes: int) -> tuple[list[MarkerSet], list[MarkerSet]]:
    """Match genes case-insensitively; keep the sets with >= min_genes positively weighted genes present."""
    lookup: dict[str, str] = {}
    for name in map(str, var_names):
        lookup.setdefault(name.upper(), name)
    kept, skipped = [], []
    for s in sets:
        s.present, s.missing = {}, []
        for g, w in s.weights.items():
            hit = lookup.get(g.upper())
            if hit is None:
                s.missing.append(g)
            else:
                s.present.setdefault(hit, w)
        n_pos = sum(1 for w in s.present.values() if w > 0)
        (kept if n_pos >= min_genes else skipped).append(s)
    return kept, skipped


def score_sample(adata, sets: list[MarkerSet], seed: int) -> pd.DataFrame:
    """Weighted mean of per-gene score_genes scores, one column per set (log-normalized X)."""
    import scanpy as sc

    genes = sorted({g for s in sets for g in s.present})
    per_gene = {}
    for g in genes:
        sc.tl.score_genes(adata, [g], score_name="_score", ctrl_size=50, n_bins=25, random_state=seed, use_raw=False)
        per_gene[g] = adata.obs.pop("_score").to_numpy(dtype=np.float64)
    out = pd.DataFrame(index=adata.obs_names)
    for s in sets:
        total = sum(abs(w) for w in s.present.values())
        out[s.cell_type] = sum(w * per_gene[g] for g, w in s.present.items()) / total
    return out


def zscore(scores: pd.DataFrame) -> pd.DataFrame:
    sd = scores.std(axis=0, ddof=0).replace(0, 1.0)
    return (scores - scores.mean(axis=0)) / sd


def call_clusters(z: pd.DataFrame, clusters: np.ndarray, margin: float):
    """(cell_type per cell, score per cell, one row per cluster)."""
    names = np.array(z.columns, dtype=object)
    values = z.to_numpy(dtype=np.float64)
    own_best = values.argmax(axis=1)
    cell_type = np.empty(len(z), dtype=object)
    score = np.empty(len(z), dtype=np.float64)
    rows = []
    for cl in sorted(set(clusters)):
        m = clusters == cl
        means = values[m].mean(axis=0)
        order = np.argsort(-means, kind="stable")
        best = order[0]
        second = order[1] if len(order) > 1 else None
        gap = means[best] - means[second] if second is not None else float("inf")
        agreement = float((own_best[m] == best).mean())
        ok = means[best] > 0 and gap >= margin
        call = names[best] if ok else UNASSIGNED
        cell_type[m], score[m] = call, agreement
        rows.append({"cluster": cl, "n_obs": int(m.sum()), "cell_type": call, "best": names[best],
                     "best_z": float(means[best]), "second": names[second] if second is not None else "",
                     "second_z": float(means[second]) if second is not None else float("nan"),
                     "agreement": agreement,
                     "reason": "" if ok else "; ".join(r for r, bad in (
                         ("best mean z-score not positive", means[best] <= 0),
                         (f"margin {gap:.2f} < {margin}", gap < margin)) if bad)})
    return cell_type, score, rows
