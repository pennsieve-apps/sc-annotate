"""
The reference: a labelled single-cell .h5ad, or a previous sc-annotate `model` folder.

Only the cells that will be used are read: the obs table first (backed), then the cell type
column picks at most MAX_CELLS_PER_TYPE cells per type (seeded; types with fewer than
MIN_CELLS_PER_TYPE cells are dropped) and only those rows of the count matrix are loaded. Raw
counts come from layers["counts"], X or .raw.X, the first that is integer-valued.

Genes are matched to the query by Ensembl id when both sides carry ids (query var["gene_ids"];
reference var["gene_ids"]/["gene_id"]/["ensembl_id"] or Ensembl var_names), else by symbol
(reference var["feature_name"] (CELLxGENE) or var_names), ignoring case.
"""
from __future__ import annotations

import logging
import re

import anndata as ad
import numpy as np
import pandas as pd
import scipy.sparse as sp

log = logging.getLogger("sc-annotate")

MIN_CELLS_PER_TYPE = 10
SOURCE_KEYS = ("title", "citation", "doi", "license", "licence")
ENSEMBL = re.compile(r"^ENS[A-Z]*G\d+")


def is_integer_valued(X, n_check: int = 200_000) -> bool:
    data = X.data if sp.issparse(X) else np.asarray(X).ravel()
    data = data[:n_check]
    return data.size > 0 and bool(np.all(np.isfinite(data)) and data.min() >= 0 and np.allclose(data, np.round(data)))


def counts_of(adata: ad.AnnData) -> tuple[sp.csr_matrix, pd.DataFrame, str]:
    """(integer counts, CSR float32, the matching var table, where they came from)."""
    candidates = [("layers.counts", adata.layers["counts"], adata.var)] if "counts" in adata.layers else []
    candidates.append(("X", adata.X, adata.var))
    if adata.raw is not None:
        candidates.append(("raw.X", adata.raw.X, adata.raw.var))
    for name, X, var in candidates:
        if X is not None and is_integer_valued(X):
            return sp.csr_matrix(X, dtype=np.float32), var.copy(), name
    raise ValueError("no integer count matrix in layers['counts'], X or raw.X (raw UMI counts are needed)")


def _ids(var: pd.DataFrame) -> pd.Series | None:
    for col in ("gene_ids", "gene_id", "ensembl_id"):
        if col in var.columns:
            return var[col].astype(str).str.replace(r"\.\d+$", "", regex=True)
    names = pd.Series(var.index.astype(str), index=var.index)
    return names.str.replace(r"\.\d+$", "", regex=True) if names.str.match(ENSEMBL).mean() > 0.5 else None


def _symbols(var: pd.DataFrame) -> pd.Series:
    if "feature_name" in var.columns:
        return var["feature_name"].astype(str)
    return pd.Series(var.index.astype(str), index=var.index)


def align(ref_var: pd.DataFrame, query_var: pd.DataFrame) -> tuple[dict[str, str], str]:
    """{reference var_name: query var_name} for the genes both have, and how they were matched."""
    rid, qid = _ids(ref_var), _ids(query_var)
    use_ids = rid is not None and qid is not None and rid.str.match(ENSEMBL).mean() > 0.5 and qid.str.match(ENSEMBL).mean() > 0.5
    rkey = rid if use_ids else _symbols(ref_var).str.upper()
    qkey = qid if use_ids else _symbols(query_var).str.upper()
    q_of: dict[str, str] = {}
    for name, key in zip(query_var.index.astype(str), qkey):
        q_of.setdefault(key, name)
    out, used = {}, set()
    for name, key in zip(ref_var.index.astype(str), rkey):
        q = q_of.get(key)
        if q is not None and q not in used:
            out[name] = q
            used.add(q)
    return out, "ensembl" if use_ids else "symbol"


def select_cells(labels: pd.Series, max_per_type: int, seed: int) -> tuple[np.ndarray, list[dict]]:
    """Row indices (sorted) of at most max_per_type cells per label, and a summary row per label."""
    rng = np.random.default_rng(seed)
    keep, rows = [], []
    values = labels.astype(str).to_numpy()
    for ct in sorted(set(values)):
        idx = np.flatnonzero(values == ct)
        if len(idx) < MIN_CELLS_PER_TYPE:
            rows.append({"cell_type": ct, "n_cells": len(idx), "n_used": 0, "status": f"dropped: fewer than {MIN_CELLS_PER_TYPE} cells"})
            continue
        if max_per_type and len(idx) > max_per_type:
            idx = np.sort(rng.choice(idx, max_per_type, replace=False))
        keep.append(idx)
        rows.append({"cell_type": ct, "n_cells": int((values == ct).sum()), "n_used": len(idx), "status": "used"})
    if len(keep) < 2:
        raise ValueError(f"fewer than two cell types have {MIN_CELLS_PER_TYPE} or more cells")
    return np.sort(np.concatenate(keep)), rows


def load(path, cell_type_col: str, batch_col: str, max_per_type: int, seed: int) -> tuple[ad.AnnData, list[dict]]:
    """The reference subsample: X = counts (CSR float32), obs cell_type and batch, var gene_ids.
    Unlabelled cells (empty, NaN, 'Unassigned', 'Unknown') are not used."""
    backed = ad.read_h5ad(path, backed="r")
    try:
        if cell_type_col not in backed.obs.columns:
            raise ValueError(f"the reference has no obs column {cell_type_col!r} (CELL_TYPE_COLUMN); "
                             f"it has {', '.join(map(str, backed.obs.columns[:30]))}")
        if batch_col and batch_col not in backed.obs.columns:
            raise ValueError(f"the reference has no obs column {batch_col!r} (REFERENCE_BATCH_COLUMN)")
        labels = backed.obs[cell_type_col].astype(str)
        labelled = ~labels.str.strip().isin(["", "nan", "NaN", "None", "Unassigned", "Unknown"]).to_numpy()
        idx, summary = select_cells(labels[labelled], max_per_type, seed)
        idx = np.flatnonzero(labelled)[idx]
        sub = backed[idx].to_memory()
        # where the reference came from (CELLxGENE files carry title and citation in uns): it goes
        # into the model's provenance, since model/reference.h5ad redistributes a subsample of it
        # (a previous sc-annotate model keeps them under uns["source"])
        nested = backed.uns.get("source") if isinstance(backed.uns.get("source"), dict) else {}
        ref_source = {k: str(v)[:2000] for k, v in {**nested, **backed.uns}.items() if k in SOURCE_KEYS and isinstance(v, str)}
    finally:
        backed.file.close()
    X, var, source = counts_of(sub)
    obs = pd.DataFrame({"cell_type": pd.Categorical(sub.obs[cell_type_col].astype(str).to_numpy()),
                        "batch": pd.Categorical(sub.obs[batch_col].astype(str).to_numpy() if batch_col else ["reference"] * sub.n_obs)},
                       index=sub.obs_names.astype(str))
    ids = _ids(var)
    new_var = pd.DataFrame({"gene_ids": ids.to_numpy() if ids is not None else ""}, index=_symbols(var).to_numpy())
    ref = ad.AnnData(X=X, obs=obs, var=new_var)
    ref.var_names_make_unique()
    ref.uns["source"] = ref_source
    log.info("reference: %d cells of %d used, %d genes, counts from %s, %d cell types, %d batches",
             ref.n_obs, len(labels), ref.n_vars, source, ref.obs["cell_type"].nunique(), ref.obs["batch"].nunique())
    return ref, summary


def signatures(ref: ad.AnnData) -> pd.DataFrame:
    """Mean counts per cell of each type (genes x types), the cell2location signature format:
    index gene symbol, column gene_id, then one column per type. Genes never detected are left out."""
    types = list(ref.obs["cell_type"].cat.categories)
    onehot = sp.csr_matrix((np.ones(ref.n_obs, dtype=np.float32), (ref.obs["cell_type"].cat.codes.to_numpy(), np.arange(ref.n_obs))),
                           shape=(len(types), ref.n_obs))
    sums = np.asarray((onehot @ ref.X).todense()).T
    means = sums / np.asarray(onehot.sum(axis=1)).ravel()[None, :]
    detected = sums.sum(axis=1) > 0
    out = pd.DataFrame(means[detected], index=ref.var_names[detected], columns=types)
    out.insert(0, "gene_id", ref.var["gene_ids"].astype(str).to_numpy()[detected])
    out.index.name = "gene"
    return out
