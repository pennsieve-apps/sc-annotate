"""
sc-annotate: cell types for single-cell / single-nucleus RNA-seq.

Reads sc-integrate's <sample_id>.h5ad files (port `cells`, with obs["cluster"]), an optional
labelled reference (port `reference`: an .h5ad, or a previous run's `model` folder) and an
optional markers.csv (port `markers`), and labels every cell:

  reference mode  label transfer from the reference (METHOD: celltypist or scanvi), per cell,
                  Unassigned below MIN_SCORE (processor/transfer.py)
  markers mode    marker-set scores, one call per cluster (processor/markers.py)

MODE=auto picks reference mode when a reference is linked, else markers mode. Writes

  cells/       every <sample_id>.h5ad with obs cell_type, cell_type_score, cell_type_source
  labels/      labels.csv (sample_id, obs_id, cluster, cell_type, cell_type_score)
  model/       reference.h5ad, signatures.csv, scanvi/ (when scANVI ran), reference_summary.csv
  annotation/  summary.json, cell_types_by_sample.csv, confusion.csv, clusters.csv,
               marker_scores.csv (markers mode), figures

each with a provenance.json.
"""
from __future__ import annotations

import json
import logging
import math
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from processor import threads as T

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger("sc-annotate")
for noisy in ("matplotlib", "PIL", "fontTools", "numba", "h5py", "anndata"):
    logging.getLogger(noisy).setLevel(logging.WARNING)

APP_NAME = "sc-annotate"
REPO_ROOT = Path(__file__).resolve().parent.parent
BUILTIN_SETS = sorted(p.stem for p in (Path(__file__).resolve().parent / "markers").glob("*.csv"))

DEFAULTS = {
    "MODE": "auto",
    "METHOD": "celltypist",
    "MARKER_SET": "broad",
    "CELL_TYPE_COLUMN": "cell_type",
    "REFERENCE_BATCH_COLUMN": "",
    "MIN_SCORE": "0.5",
    "MARGIN": "0.2",
    "MIN_GENES_PRESENT": "2",
    "MAX_CELLS_PER_TYPE": "2000",
    "MAX_EPOCHS": "0",
    "QUERY_EPOCHS": "100",
    "SEED": "42",
    "THREADS": "0",
}
PARAMETERS = tuple(DEFAULTS)
CHOICES = {"MODE": ("auto", "reference", "markers"), "METHOD": ("celltypist", "scanvi"),
           "MARKER_SET": tuple(BUILTIN_SETS) + ("none",)}
CITATIONS = {
    "best_practices": ("10.1038/s41576-023-00586-w", "37002403", "Heumos L et al. Nat Rev Genet 2023"),
    "scanpy": ("10.1186/s13059-017-1382-0", "29409532", "Wolf FA et al. Genome Biol 2018"),
    "anndata": ("10.21105/joss.04371", None, "Virshup I et al. J Open Source Softw 2024"),
    "satija": ("10.1038/nbt.3192", "25867923", "Satija R et al. Nat Biotechnol 2015"),
    "tirosh": ("10.1126/science.aad0501", "27124452", "Tirosh I et al. Science 2016"),
    "scvi_tools": ("10.1038/s41587-021-01206-w", "35132262", "Gayoso A et al. Nat Biotechnol 2022"),
    "scvi": ("10.1038/s41592-018-0229-2", "30504886", "Lopez R et al. Nat Methods 2018"),
    "scanvi": ("10.15252/msb.20209620", "33491336", "Xu C et al. Mol Syst Biol 2021"),
    "scarches": ("10.1038/s41587-021-01001-7", "34462589", "Lotfollahi M et al. Nat Biotechnol 2022"),
    "pytorch": ("10.48550/arXiv.1912.01703", None, "Paszke A et al. NeurIPS 2019"),
    "celltypist": ("10.1126/science.abl5197", "35549406", "Domínguez Conde C et al. Science 2022"),
    "tavares_ferreira": ("10.1126/scitranslmed.abj8186", "35171654", "Tavares-Ferreira D et al. Sci Transl Med 2022"),
    "bhuiyan": ("10.1126/sciadv.adj9173", "38905344", "Bhuiyan SA et al. Sci Adv 2024"),
    "avraham": ("10.1097/j.pain.0000000000002628", "35503034", "Avraham O et al. Pain 2022"),
    "ji": ("10.1136/annrheumdis-2017-212863", "30026257", "Ji Q et al. Ann Rheum Dis 2019"),
    "chou": ("10.1038/s41598-020-67730-y", "32616761", "Chou CH et al. Sci Rep 2020"),
    "zhang": ("10.1038/s41590-019-0378-1", "31061532", "Zhang F et al. Nat Immunol 2019"),
    "emont": ("10.1038/s41586-022-04518-2", "35296864", "Emont MP et al. Nature 2022"),
    "panglaodb": ("10.1093/database/baz046", "30951143", "Franzén O et al. Database (Oxford) 2019"),
}
MARKER_SOURCES = {"drg-human": ["tavares_ferreira", "bhuiyan", "avraham"], "knee-human": ["ji", "chou", "zhang", "emont"],
                  "broad": ["panglaodb"]}


def citations(keys: list[str]) -> list[dict]:
    out = []
    for k in keys:
        doi, pmid, text = CITATIONS[k]
        out.append({"doi": doi, **({"pmid": pmid} if pmid else {}), "text": text})
    return out


class ParameterError(ValueError):
    pass


def read_parameters(env=os.environ) -> dict:
    raw = {k: (env.get(k) if env.get(k) not in (None, "") else v) for k, v in DEFAULTS.items()}
    p: dict = {}
    for name, choices in CHOICES.items():
        value = raw[name].strip().lower()
        if value not in choices:
            raise ParameterError(f"{name} must be one of {', '.join(choices)}, got {raw[name]!r}")
        p[name] = value
    p["CELL_TYPE_COLUMN"] = raw["CELL_TYPE_COLUMN"].strip()
    p["REFERENCE_BATCH_COLUMN"] = raw["REFERENCE_BATCH_COLUMN"].strip()
    try:
        for name in ("MIN_SCORE", "MARGIN"):
            p[name] = float(raw[name])
        for name in ("MIN_GENES_PRESENT", "MAX_CELLS_PER_TYPE", "MAX_EPOCHS", "QUERY_EPOCHS", "SEED", "THREADS"):
            p[name] = int(raw[name])
    except ValueError as exc:
        raise ParameterError(f"bad numeric parameter: {exc}") from exc
    if not 0 <= p["MIN_SCORE"] <= 1 or not math.isfinite(p["MARGIN"]) or p["MARGIN"] < 0:
        raise ParameterError("MIN_SCORE must be within 0-1 and MARGIN >= 0")
    if p["MIN_GENES_PRESENT"] < 1 or p["MAX_CELLS_PER_TYPE"] < 10 or p["MAX_EPOCHS"] < 0 or p["QUERY_EPOCHS"] < 1 \
            or p["THREADS"] < 0:
        raise ParameterError("MIN_GENES_PRESENT >= 1, MAX_CELLS_PER_TYPE >= 10, MAX_EPOCHS >= 0, QUERY_EPOCHS >= 1, THREADS >= 0")
    if not p["CELL_TYPE_COLUMN"]:
        raise ParameterError("CELL_TYPE_COLUMN must not be empty")
    return p


def _clean_json(obj):
    if isinstance(obj, float):
        return None if math.isnan(obj) or math.isinf(obj) else obj
    if isinstance(obj, dict):
        return {str(k): _clean_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean_json(v) for v in obj]
    if hasattr(obj, "item"):
        return _clean_json(obj.item())
    return obj


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(_clean_json(data), indent=2) + "\n")


def tool_versions() -> dict:
    from importlib.metadata import PackageNotFoundError, version

    out = {"python": platform.python_version()}
    for pkg in ("scanpy", "anndata", "scvi-tools", "torch", "lightning", "celltypist", "scikit-learn", "scikit-misc",
                "numpy", "scipy", "pandas", "h5py", "matplotlib"):
        try:
            out[pkg] = version(pkg)
        except PackageNotFoundError:
            out[pkg] = None
    return out


def peak_rss_mb() -> float | None:
    import resource

    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(peak / (1024 * 1024 if sys.platform == "darwin" else 1024), 1)


def cgroup_peak_mb() -> float | None:
    try:
        return round(int(Path("/sys/fs/cgroup/memory.peak").read_text()) / 2**20, 1)
    except (OSError, ValueError):
        return None


def app_version() -> str:
    try:
        return (REPO_ROOT / "VERSION").read_text().strip()
    except OSError:
        return "unknown"


def read_sample(path: Path, sample_id: str):
    """One sample, checked against the contract: unique obs_names, obs["cluster"]."""
    import anndata as ad

    a = ad.read_h5ad(path)
    if "cluster" not in a.obs.columns:
        raise ValueError("no obs['cluster'] (link sc-integrate's cells output)")
    if not a.obs_names.is_unique:
        raise ValueError("obs_names are not unique")
    a.var_names_make_unique()
    a.obs["sample_id"] = sample_id
    return a


def main() -> int:
    started = datetime.now(timezone.utc)
    t0 = time.monotonic()
    input_dir, output_dir = os.environ.get("INPUT_DIR"), os.environ.get("OUTPUT_DIR")
    if not input_dir or not output_dir:
        log.error("INPUT_DIR and OUTPUT_DIR must be set")
        return 2
    input_dir, output_dir = Path(input_dir).absolute(), Path(output_dir)   # safe_inputs takes relative paths under INPUT_DIR
    if not input_dir.is_dir():
        log.error("INPUT_DIR %s is not a folder", input_dir)
        return 2
    try:
        params = read_parameters()
    except ParameterError as exc:
        log.error("%s", exc)
        return 2
    from processor.safe_inputs import cpu_threads

    n_threads = cpu_threads(params["THREADS"])
    T.set_env(n_threads)
    log.info("threads: %d", n_threads)
    if os.environ.get("TORCH_FLAVOUR") == "cuda":     # the gpu variant never runs on the CPU unnoticed
        from processor import transfer as X

        problem = X.cuda_problem()
        if problem:
            log.error("GPU variant: %s; run it on a GPU node (computeTypes gpu) or use the cpu variant", problem)
            return 1
        log.info("GPU: %s", X.cuda_description())

    import numpy as np
    import pandas as pd

    from processor import markers as M
    from processor import reference as R
    from processor.inputs import discover

    found = discover(input_dir)
    rel = found.input_dir.rel
    for name, reason in found.skipped.items():
        log.warning("%s: skipped, %s", name, reason)
    if not found.samples:
        log.error("no <sample_id>.h5ad found on the cells input under %s", input_dir)
        return 1
    mode = params["MODE"]
    if mode == "auto":
        mode = "reference" if found.reference else "markers"
    if mode == "reference" and found.reference is None:
        log.error("MODE=reference but no reference .h5ad or model folder is linked")
        return 1
    sets, marker_source = [], None
    if mode == "markers":
        if params["MARKER_SET"] == "none" and found.markers_csv is None:
            log.error("markers mode needs a markers.csv on the markers input or a built-in MARKER_SET")
            return 2
        try:
            sets, marker_source = M.load_sets(params["MARKER_SET"], found.markers_csv, found.input_dir)
        except (OSError, ValueError) as exc:
            log.error("marker sets: %s", exc)
            return 1
    method = params["METHOD"] if mode == "reference" else "markers"
    source = ("model" if found.reference.is_model else "reference") if mode == "reference" else "markers"
    log.info("%d samples; mode %s (%s)%s", len(found.samples), mode, method,
             f", marker sets from {marker_source} ({len(sets)})" if sets else f", reference {found.reference.path.name}"
             + (" (sc-annotate model)" if found.reference.is_model else ""))

    # --- headers: obs, var and the UMAP of every sample (backed, no matrices) ------------------
    import anndata as ad

    statuses: dict[str, dict] = {}
    obs_parts, umap_parts, var_of = [], [], {}
    for sid, path in found.samples.items():
        try:
            a = ad.read_h5ad(path, backed="r")
            try:
                if "cluster" not in a.obs.columns:
                    raise ValueError("no obs['cluster'] (link sc-integrate's cells output)")
                if not a.obs_names.is_unique:
                    raise ValueError("obs_names are not unique")
                obs_parts.append(pd.DataFrame({"sample_id": sid, "obs_id": a.obs_names.astype(str),
                                               "cluster": a.obs["cluster"].astype(str).to_numpy()}))
                umap_parts.append(np.asarray(a.obsm["X_umap"])[:, :2] if "X_umap" in a.obsm else None)
                var = a.var.copy()
                var.index = var.index.astype(str)
                var_of[sid] = var[~var.index.duplicated()]
                statuses[sid] = {"sample_id": sid, "file": rel(path), "status": "ok",
                                 "n_obs": int(a.n_obs), "n_genes": int(a.n_vars)}
            finally:
                a.file.close()
        except Exception as exc:
            statuses[sid] = {"sample_id": sid, "file": rel(path), "status": "failed",
                             "error": f"{type(exc).__name__}: {exc}"}
            log.error("%s: skipped: %s", sid, exc)
    ok = [sid for sid in found.samples if statuses[sid]["status"] == "ok"]
    if not ok:
        log.error("every sample failed")
        return 1
    frame = pd.concat(obs_parts, ignore_index=True)
    if frame["obs_id"].duplicated().any():
        log.error("obs_names repeat across samples (they must be <sample_id>:<barcode>)")
        return 1
    common = var_of[ok[0]].index
    for sid in ok[1:]:
        common = common.intersection(var_of[sid].index, sort=False)
    query_var = var_of[ok[0]].loc[common]
    log.info("%d cells in %d samples; %d genes in every sample", len(frame), len(ok), len(common))

    def load_ok(sid):
        a = read_sample(found.samples[sid], sid)
        return a[:, common].copy() if a.n_vars != len(common) else a

    # --- calls ----------------------------------------------------------------------------------
    t_calls = time.monotonic()
    info: dict = {"mode": mode, "method": method, "cell_type_source": source, "n_genes_common": int(len(common))}
    model_ref, ref_summary, scanvi_model, marker_rows, z = None, None, None, None, None
    try:
        if mode == "markers":
            used, skipped_sets = M.resolve(sets, common, params["MIN_GENES_PRESENT"])
            for s in skipped_sets:
                log.info("marker set %s skipped: %d of %d genes present", s.cell_type, len(s.present), len(s.weights))
            if not used:
                log.error("no marker set has %d genes among the data's genes", params["MIN_GENES_PRESENT"])
                return 1
            parts = []
            for sid in ok:
                t = time.monotonic()
                parts.append(M.score_sample(load_ok(sid), used, params["SEED"]))
                log.info("%s: %d cells scored for %d marker sets, %.1fs", sid, len(parts[-1]), len(used), time.monotonic() - t)
            z = M.zscore(pd.concat(parts))
            cell_type, score, marker_rows = M.call_clusters(z, frame["cluster"].to_numpy(), params["MARGIN"])
            for r in marker_rows:
                log.info("%s: %d cells -> %s (z %.2f, then %s %.2f; agreement %.2f)%s", r["cluster"], r["n_obs"], r["cell_type"],
                         r["best_z"], r["second"], r["second_z"], r["agreement"], f"; {r['reason']}" if r["reason"] else "")
            info["marker_sets"] = {"source": marker_source, "n_given": len(sets), "n_used": len(used),
                                   "used": {s.cell_type: {"genes_used": list(s.present), "genes_missing": s.missing} for s in used},
                                   "skipped": {s.cell_type: {"genes_present": list(s.present), "genes_missing": s.missing} for s in skipped_sets}}
        else:
            from processor import transfer as X

            X.quiet()
            accelerator, device_text = X.device()
            log.info("device: %s", device_text)
            info["device"] = device_text
            ref_path = found.reference.path
            ct_col, batch_col = ("cell_type", "batch") if found.reference.is_model else (params["CELL_TYPE_COLUMN"], params["REFERENCE_BATCH_COLUMN"])
            ref, ref_summary = R.load(ref_path, ct_col, batch_col, params["MAX_CELLS_PER_TYPE"], params["SEED"])
            mapping, how = R.align(ref.var, query_var)
            info.update(reference=rel(ref_path), reference_source=ref.uns.get("source", {}), gene_match=how, n_genes_reference=int(ref.n_vars),
                        n_genes_shared=len(mapping))
            log.info("genes shared with the reference: %d of %d (matched by %s)", len(mapping), ref.n_vars, how)
            if len(mapping) < 200:
                log.error("only %d genes are shared with the reference; is it the same species and gene naming?", len(mapping))
                return 1
            probs = None
            if params["METHOD"] == "scanvi" and found.reference.scanvi is not None:
                scanvi_model = X.load_scanvi(ref, found.reference.scanvi, found.input_dir)
                model_ref = scanvi_model.adata.copy()
                genes = list(model_ref.var_names)
                info["training"] = {"reused": "scanvi/ of the reference model"}
                cols = {r: q for r, q in mapping.items() if r in set(genes)}
            else:
                model_ref = ref[:, list(mapping)].copy()
                model_ref.var_names = [mapping[g] for g in mapping]
                model_ref.var["gene_ids"] = query_var.loc[model_ref.var_names, "gene_ids"].astype(str).to_numpy() \
                    if "gene_ids" in query_var.columns else model_ref.var["gene_ids"].to_numpy()
                genes = X.select_genes(model_ref)
                cols = {g: g for g in genes}
            info["n_genes_model"] = len(genes)
            if params["METHOD"] == "scanvi":
                if scanvi_model is None:
                    scanvi_model, info["training"] = X.train_scanvi(model_ref[:, genes].copy(), params["MAX_EPOCHS"], accelerator, params["SEED"])
                parts = []
                for sid in ok:
                    a = load_ok(sid)
                    counts, _, _ = R.counts_of(a)
                    q = ad.AnnData(X=counts[:, [a.var_names.get_loc(c) for c in cols.values()]],
                                   obs=pd.DataFrame({"batch": sid}, index=a.obs_names), var=pd.DataFrame(index=list(cols)))
                    parts.append(q)
                    log.info("%s: %d cells, counts of %d model genes", sid, q.n_obs, q.n_vars)
                query = ad.concat(parts, merge="same")
                del parts
                probs = X.map_query(scanvi_model, query, params["QUERY_EPOCHS"], accelerator, params["SEED"])
                info["training"]["query_epochs"] = params["QUERY_EPOCHS"]
            else:
                ct_model = X.train_celltypist(model_ref[:, genes].copy(), n_threads, params["SEED"])
                parts = []
                for sid in ok:
                    a = load_ok(sid)
                    counts, _, _ = R.counts_of(a)
                    t = time.monotonic()
                    parts.append(X.annotate_celltypist(ct_model, ad.AnnData(X=counts, obs=pd.DataFrame(index=a.obs_names),
                                                                             var=pd.DataFrame(index=a.var_names))))
                    log.info("%s: %d cells annotated, %.1fs", sid, a.n_obs, time.monotonic() - t)
                probs = pd.concat(parts)
            probs = probs.loc[frame["obs_id"].to_numpy()]
            best = probs.to_numpy().argmax(axis=1)
            score = probs.to_numpy()[np.arange(len(probs)), best]
            cell_type = np.asarray(probs.columns, dtype=object)[best]
            cell_type[score < params["MIN_SCORE"]] = M.UNASSIGNED
    except (OSError, ValueError, KeyError) as exc:
        log.error("annotation failed: %s", exc)
        return 1
    frame["cell_type"] = cell_type
    frame["cell_type_score"] = np.asarray(score, dtype=np.float64)
    t_calls = time.monotonic() - t_calls

    # --- cells and model ------------------------------------------------------------------------
    dirs = {name: output_dir / name for name in ("cells", "labels", "model", "annotation")}
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    t_write = time.monotonic()
    annotation_uns = {"mode": mode, "method": method, "app_version": app_version(),
                      **({"min_score": params["MIN_SCORE"]} if mode == "reference" else {"margin": params["MARGIN"]}),
                      **({"marker_sets": marker_source} if marker_source else {})}
    model_pick = None
    if mode == "markers":
        labelled = frame.index[frame["cell_type"] != M.UNASSIGNED]
        try:
            pick, ref_summary = R.select_cells(frame.loc[labelled, "cell_type"], params["MAX_CELLS_PER_TYPE"], params["SEED"])
            model_pick = set(frame.loc[labelled[pick], "obs_id"])
        except ValueError as exc:
            log.warning("model: no reference.h5ad (%s)", exc)
    model_parts = []
    by_sample = {sid: g for sid, g in frame.groupby("sample_id", sort=False)}
    for sid in ok:
        t = time.monotonic()
        try:
            a = read_sample(found.samples[sid], sid)
            rows = by_sample[sid].set_index("obs_id").loc[a.obs_names.astype(str)]
            a.obs["cell_type"] = pd.Categorical(rows["cell_type"].to_numpy())
            a.obs["cell_type_score"] = rows["cell_type_score"].to_numpy(dtype=np.float32)
            a.obs["cell_type_source"] = pd.Categorical([source] * a.n_obs)
            pen = dict(a.uns.get("pennsieve", {})) if isinstance(a.uns.get("pennsieve"), dict) else {}
            pen["annotation"] = annotation_uns
            a.uns["pennsieve"] = pen
            a.write_h5ad(dirs["cells"] / f"{sid}.h5ad", compression="gzip")
            if model_pick:
                m = a.obs_names.isin(list(model_pick))
                if m.any():
                    sub = a[m][:, common]
                    counts, _, _ = R.counts_of(sub)
                    model_parts.append(ad.AnnData(X=counts, obs=pd.DataFrame(
                        {"cell_type": sub.obs["cell_type"].astype(str).to_numpy(), "batch": sid}, index=sub.obs_names),
                        var=pd.DataFrame({"gene_ids": query_var["gene_ids"].astype(str).to_numpy() if "gene_ids" in query_var
                                          else ""}, index=common)))
            n_un = int((rows["cell_type"] == M.UNASSIGNED).sum())
            statuses[sid].update(n_unassigned=n_un, n_cell_types=int(rows["cell_type"].nunique()))
            log.info("%s: %d cells, %d cell types, %d unassigned, written in %.1fs", sid, a.n_obs,
                     rows["cell_type"].nunique(), n_un, time.monotonic() - t)
        except Exception as exc:
            statuses[sid].update(status="failed", error=f"{type(exc).__name__}: {exc}")
            log.error("%s: writing failed: %s", sid, exc)
    if all(statuses[s]["status"] != "ok" for s in ok):
        log.error("every sample failed")
        return 1
    if model_parts:
        model_ref = ad.concat(model_parts, merge="same")
    if model_ref is not None:
        model_ref.obs["cell_type"] = pd.Categorical(model_ref.obs["cell_type"].astype(str))
        model_ref.obs["batch"] = pd.Categorical(model_ref.obs["batch"].astype(str))
        source_of_ref = info.get("reference_source") or {}
        model_ref.uns = {"pennsieve": {"model_of": APP_NAME, "version": app_version(), "mode": mode, "method": method},
                         **({"source": source_of_ref} if source_of_ref else {})}
        model_ref.write_h5ad(dirs["model"] / "reference.h5ad", compression="gzip")
        R.signatures(model_ref).to_csv(dirs["model"] / "signatures.csv", float_format="%.6g")
        if scanvi_model is not None:
            from processor import transfer as X

            (dirs["model"] / "scanvi").mkdir(exist_ok=True)
            X.save_scanvi(scanvi_model, dirs["model"] / "scanvi")
        pd.DataFrame(ref_summary).to_csv(dirs["model"] / "reference_summary.csv", index=False)
    t_write = time.monotonic() - t_write

    # --- labels and annotation tables -----------------------------------------------------------
    frame = frame[frame["sample_id"].isin([s for s in ok if statuses[s]["status"] == "ok"])]
    frame.to_csv(dirs["labels"] / "labels.csv", index=False, columns=["sample_id", "obs_id", "cluster", "cell_type", "cell_type_score"],
                 float_format="%.4g")
    counts = frame.groupby(["sample_id", "cell_type"], sort=False).size()
    totals = frame.groupby("sample_id", sort=False).size()
    by_sample_rows = pd.DataFrame({"n_obs": counts}).reset_index()
    by_sample_rows["fraction"] = by_sample_rows["n_obs"] / totals.loc[by_sample_rows["sample_id"]].to_numpy()
    by_sample_rows.to_csv(dirs["annotation"] / "cell_types_by_sample.csv", index=False, float_format="%.4g")
    conf = frame.groupby(["cluster", "cell_type"]).agg(n_obs=("obs_id", "size"), mean_score=("cell_type_score", "mean")).reset_index()
    conf["fraction_of_cluster"] = conf["n_obs"] / conf.groupby("cluster")["n_obs"].transform("sum")
    conf.to_csv(dirs["annotation"] / "confusion.csv", index=False, float_format="%.4g")
    if marker_rows is not None:
        pd.DataFrame(marker_rows).to_csv(dirs["annotation"] / "clusters.csv", index=False, float_format="%.4g")
        means = z.groupby(frame["cluster"].to_numpy()).mean()
        means.index.name = "cluster"
        means.reset_index().melt(id_vars="cluster", var_name="marker_set", value_name="mean_z").to_csv(
            dirs["annotation"] / "marker_scores.csv", index=False, float_format="%.4g")
    else:
        top = conf.sort_values(["cluster", "n_obs"], ascending=[True, False]).groupby("cluster").head(1)
        top = top.rename(columns={"fraction_of_cluster": "fraction"})[["cluster", "cell_type", "n_obs", "fraction", "mean_score"]]
        top.insert(1, "n_cells", frame.groupby("cluster").size().loc[top["cluster"]].to_numpy())
        top.to_csv(dirs["annotation"] / "clusters.csv", index=False, float_format="%.4g")

    # --- figures --------------------------------------------------------------------------------
    from processor import figures as F

    figures = []
    order = [t for t in frame["cell_type"].value_counts().index if t != M.UNASSIGNED]
    order += [M.UNASSIGNED] if (frame["cell_type"] == M.UNASSIGNED).any() else []
    try:
        if all(u is not None for u in umap_parts):
            coords = np.vstack(umap_parts)[frame.index.to_numpy()]
            figures.append(F.scatter_categorical(coords, frame["cell_type"].to_numpy(), order,
                                                 f"UMAP by cell type ({len(frame):,} cells)", dirs["annotation"] / "umap_cell_type.png"))
        else:
            log.warning("no obsm['X_umap'] in every sample: no UMAP figure")
        samples_ok = list(dict.fromkeys(frame["sample_id"]))
        table = {s: dict(zip(g["cell_type"], g["fraction"])) for s, g in by_sample_rows.groupby("sample_id")}
        figures.append(F.stacked_bar(table, samples_ok, order, "Cell types by sample", dirs["annotation"] / "cell_types_by_sample.png"))
        xlabel = "cell_type_score (fraction of the cluster's cells whose best marker set is the call)" if mode == "markers" \
            else f"cell_type_score ({method} probability of the best label)"
        figures.append(F.score_histogram(frame["cell_type_score"], params["MIN_SCORE"] if mode == "reference" else None, "Annotation confidence",
                                         dirs["annotation"] / "score_histogram.png", xlabel))
    except Exception as exc:
        log.exception("figures failed: %s", exc)

    # --- summary and provenance -----------------------------------------------------------------
    overall = frame["cell_type"].value_counts()
    summary = {
        "mode": mode, "method": method, "cell_type_source": source,
        "n_samples": int(frame["sample_id"].nunique()), "n_cells": int(len(frame)), "n_clusters": int(frame["cluster"].nunique()),
        "n_cell_types": int(sum(1 for t in overall.index if t != M.UNASSIGNED)),
        "fraction_unassigned": float(overall.get(M.UNASSIGNED, 0) / len(frame)),
        "mean_score": float(frame["cell_type_score"].mean()),
        "cell_types": [{"cell_type": t, "n_obs": int(overall[t]), "fraction": float(overall[t] / len(frame)),
                        "mean_score": float(frame.loc[frame["cell_type"] == t, "cell_type_score"].mean())} for t in order],
        **info, "figures": [p.name for p in figures],
    }
    write_json(dirs["annotation"] / "summary.json", summary)
    keys = ["best_practices", "scanpy", "anndata"]
    if mode == "markers":
        keys += ["satija", "tirosh"] + (MARKER_SOURCES.get(params["MARKER_SET"], []) if marker_source != "markers.csv" else [])
    elif method == "scanvi":
        keys += ["scvi_tools", "scvi", "scanvi", "scarches", "pytorch"]
    else:
        keys.append("celltypist")
    n_failed = sum(1 for s in statuses.values() if s["status"] != "ok")
    provenance = {
        "app": APP_NAME, "version": app_version(), "tools": tool_versions(), "parameters": params,
        "threads": n_threads, "method": info, "citations": citations(keys),
        "inputs": [rel(p) for p in [*found.samples.values(),
                                    *([found.reference.path, *(found.reference.scanvi or {}).values()] if found.reference else []),
                                    *([found.markers_csv] if found.markers_csv else [])]],
        "skipped_inputs": found.skipped,
        "started": started.isoformat(timespec="seconds"),
        "finished": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "timings_seconds": {"annotate": round(t_calls, 2), "write": round(t_write, 2), "total": round(time.monotonic() - t0, 2)},
        "peak_rss_mb": peak_rss_mb(), "cgroup_peak_mb": cgroup_peak_mb(),
        "samples": list(statuses.values()), "n_ok": len(statuses) - n_failed, "n_failed": n_failed,
    }
    for d in dirs.values():
        write_json(d / "provenance.json", {**provenance, "outputs": sorted(p.name for p in d.iterdir())})
    log.info("done: %d samples (%d failed), %d cells, %d cell types (%.1f%% unassigned), %.1fs, peak RSS %s MB",
             summary["n_samples"], n_failed, summary["n_cells"], summary["n_cell_types"], 100 * summary["fraction_unassigned"],
             time.monotonic() - t0, peak_rss_mb())
    return 0


if __name__ == "__main__":
    sys.exit(main())
