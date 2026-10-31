"""
Fixtures that follow the workflow contract (cells/<sample_id>.h5ad as sc-integrate writes them).

  python -m tests.make_fixture data/fixture [--layout both|linked|flat]
      synthetic: three samples of 500 nuclei, 260 genes, six planted cell types (truth in
      truth.csv), clusters, a UMAP; reference/reference_atlas.h5ad (a labelled reference of the
      same types, raw counts, another gene naming: Ensembl var_names + feature_name) and
      markers/markers.csv
  python -m tests.make_fixture data/demo --from-prep DIR | --from-cellranger DIR [--samples N] [--max-obs 3000]
      a stand-in for sc-qc + sc-integrate (and sc-prep) on real data: sc-prep's cells output, or
      Cell Ranger .h5 files (SPARC layout); see integrate_like()
"""
from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path

import numpy as np

PLANTED = {
    "Neuron": ["SNAP25", "PRPH", "SCN10A"],
    "Satellite glia": ["FABP7", "KCNJ10", "GLUL"],
    "Fibroblast": ["DCN", "LUM", "COL1A1"],
    "Endothelial": ["PECAM1", "VWF", "CDH5"],
    "Macrophage": ["CD68", "CD163", "MRC1"],
    "T cell": ["CD3E", "CD2", "TRAC"],
}
TYPES = list(PLANTED)
FRACTIONS = [0.15, 0.3, 0.2, 0.15, 0.12, 0.08]
N_GENES = 260
SAMPLES = ["s1", "s2", "s3"]
TARGET_SUM = 1e4


def gene_table(rng):
    markers = [g for gs in PLANTED.values() for g in gs]
    genes = markers + [f"GENE{i + 1:03d}" for i in range(N_GENES - len(markers))]
    ids = [f"ENSG{i + 1:011d}" for i in range(len(genes))]
    # each type also has its own program of 12 filler genes (signal beyond the markers)
    filler = np.arange(len(markers), len(genes))
    programs = {t: rng.choice(filler, 12, replace=False) for t in TYPES}
    return genes, ids, programs


def simulate(rng, n, genes, programs, depth):
    labels = rng.choice(TYPES, size=n, p=FRACTIONS)
    base = rng.lognormal(-1.0, 1.0, size=len(genes))
    mean = np.tile(base, (n, 1))
    for t in TYPES:
        rows = labels == t
        for g in PLANTED[t]:
            j = genes.index(g)
            mean[:, j] = 0.05
            mean[rows, j] = 3.0
        mean[np.ix_(rows, programs[t])] *= 4.0
    size = rng.lognormal(0, 0.3, n)[:, None] * depth
    return rng.poisson(mean * size).astype(np.float32), labels


def write_sample(path: Path, sid: str, counts, labels, genes, ids, rng) -> None:
    import anndata as ad
    import pandas as pd
    import scanpy as sc
    import scipy.sparse as sp

    n = counts.shape[0]
    codes = np.array([TYPES.index(t) for t in labels])
    cluster = np.array([f"C{c + 1:02d}" for c in codes], dtype=object)
    split = (codes == 1) & (rng.random(n) < 0.5)                  # satellite glia in two clusters
    cluster[split] = f"C{len(TYPES) + 1:02d}"
    centres = rng.normal(0, 8, size=(len(TYPES) + 1, 2))
    umap = centres[[int(c[1:]) - 1 for c in cluster]] + rng.normal(0, 1, size=(n, 2))
    obs = pd.DataFrame({"sample_id": pd.Categorical([sid] * n), "cluster": pd.Categorical(cluster),
                        "condition": pd.Categorical(["demo"] * n)}, index=[f"{sid}:BC{i + 1:05d}" for i in range(n)])
    var = pd.DataFrame({"gene_ids": ids, "feature_types": "Gene Expression", "mt": False, "ribo": False}, index=genes)
    a = ad.AnnData(X=sp.csr_matrix(counts), obs=obs, var=var)
    a.layers["counts"] = sp.csr_matrix(counts)
    sc.pp.normalize_total(a, target_sum=TARGET_SUM)
    sc.pp.log1p(a)
    a.X = sp.csr_matrix(a.X, dtype=np.float32)
    a.obsm["X_umap"] = umap
    a.obsm["X_integrated"] = rng.normal(size=(n, 10)).astype(np.float32)
    a.uns["pennsieve"] = {"organism": "human", "chemistry": "flex", "source": sid, "prep_version": "fixture"}
    path.parent.mkdir(parents=True, exist_ok=True)
    a.write_h5ad(path)


def write_reference(path: Path, rng, genes, ids, programs, n=1200) -> None:
    """A CELLxGENE-like reference: Ensembl var_names, symbols in var['feature_name'], counts in X,
    labels in obs['cell_type'], two donors."""
    import anndata as ad
    import pandas as pd
    import scipy.sparse as sp

    counts, labels = simulate(rng, n, genes, programs, depth=1.2)
    obs = pd.DataFrame({"cell_type": pd.Categorical(labels), "donor": pd.Categorical(rng.choice(["d1", "d2"], n))},
                       index=[f"ref{i}" for i in range(n)])
    var = pd.DataFrame({"feature_name": genes}, index=ids)
    path.parent.mkdir(parents=True, exist_ok=True)
    ad.AnnData(X=sp.csr_matrix(counts), obs=obs, var=var).write_h5ad(path)


def write_markers(path: Path, sets: dict[str, list[str]] | None = None, weights: bool = False) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["cell_type", "gene", "weight"] if weights else ["cell_type", "gene"])
        for ct, gs in (sets or PLANTED).items():
            for g in gs:
                w.writerow([ct, g, 1] if weights else [ct, g])
    return path


def make_synthetic(root: Path, seed: int = 7) -> Path:
    rng = np.random.default_rng(seed)
    genes, ids, programs = gene_table(rng)
    truth = []
    for k, sid in enumerate(SAMPLES):
        counts, labels = simulate(rng, 500, genes, programs, depth=1.0 - 0.2 * k)
        write_sample(root / "cells" / f"{sid}.h5ad", sid, counts, labels, genes, ids, rng)
        truth += [{"obs_id": f"{sid}:BC{i + 1:05d}", "cell_type": t} for i, t in enumerate(labels)]
    write_reference(root / "reference" / "reference_atlas.h5ad", rng, genes, ids, programs)
    write_markers(root / "markers" / "markers.csv")
    with open(root / "truth.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["obs_id", "cell_type"])
        w.writeheader()
        w.writerows(truth)
    return root


def flatten(linked: Path, flat: Path) -> Path:
    """The same files side by side (no links); the reference keeps a reference/ folder."""
    for p in sorted(linked.rglob("*")):
        if p.is_file() and p.name != "truth.csv":
            dest = flat / ("reference" if p.parent.name == "reference" else "") / p.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
    return flat


def make_fixture(root: Path, layout: str = "both") -> dict[str, Path]:
    root = Path(root)
    linked = make_synthetic(root / "linked")
    out = {"linked": linked}
    if layout in ("flat", "both"):
        out["flat"] = flatten(linked, root / "flat")
    return out


# --- a stand-in for sc-qc / sc-integrate on real data ---------------------------------------------

def _read_cellranger(source: Path, n_samples: int):
    import scanpy as sc

    for f in sorted(source.rglob("*filtered_feature_bc_matrix.h5"))[:n_samples]:
        sid = next((p for p in f.parts if p.startswith("sam-")), f.parent.parent.name)
        a = sc.read_10x_h5(f)
        a.var_names_make_unique()
        a.var = a.var[["gene_ids"]]
        a.obs_names = [f"{sid}:{b}" for b in a.obs_names]
        a.obs["sample_id"] = sid
        yield sid, a


def _read_prep(source: Path, n_samples: int):
    import anndata as ad

    for f in sorted(source.glob("*.h5ad"))[:n_samples]:
        yield f.stem, ad.read_h5ad(f)


def integrate_like(root: Path, samples, max_obs: int, resolution: float = 1.0, seed: int = 42) -> Path:
    """Counts in, sc-integrate-like files out: nuclei with >= 300 genes and < 10 % mito reads, a
    seeded subsample, normalize_total + log1p, 2000 HVGs, a joint PCA (no batch correction),
    neighbours, Leiden clusters (C01, ...), UMAP; counts kept in layers['counts']."""
    import anndata as ad
    import pandas as pd
    import scanpy as sc
    import scipy.sparse as sp

    parts = []
    for sid, a in samples:
        a.var["mt"] = a.var_names.str.upper().str.startswith("MT-")
        sc.pp.calculate_qc_metrics(a, qc_vars=["mt"], inplace=True, percent_top=None)
        a = a[(a.obs["n_genes_by_counts"] >= 300) & (a.obs["pct_counts_mt"] < 10)].copy()
        if max_obs and a.n_obs > max_obs:
            a = a[np.sort(np.random.default_rng(seed).choice(a.n_obs, max_obs, replace=False))].copy()
        a.layers["counts"] = sp.csr_matrix(a.X, dtype=np.float32)
        parts.append(a)
        print(f"{sid}: {a.n_obs} nuclei")
    a = ad.concat(parts, merge="same")
    a.var["gene_ids"] = parts[0].var.loc[a.var_names, "gene_ids"].to_numpy()
    a.obs["sample_id"] = pd.Categorical(a.obs["sample_id"].astype(str))
    sc.pp.normalize_total(a, target_sum=TARGET_SUM)
    sc.pp.log1p(a)
    a.X = sp.csr_matrix(a.X, dtype=np.float32)
    sc.pp.highly_variable_genes(a, n_top_genes=2000, batch_key="sample_id")
    hv = a[:, a.var["highly_variable"]].copy()
    sc.pp.pca(hv, n_comps=30, random_state=seed)
    a.obsm["X_pca"] = a.obsm["X_integrated"] = hv.obsm["X_pca"]
    sc.pp.neighbors(a, use_rep="X_integrated", random_state=seed)
    sc.tl.leiden(a, resolution=resolution, flavor="igraph", n_iterations=2, random_state=seed)
    sc.tl.umap(a, random_state=seed)
    a.obs["cluster"] = pd.Categorical([f"C{int(c) + 1:02d}" for c in a.obs["leiden"]])
    del a.obs["leiden"]
    a.uns = {"pennsieve": {"organism": "human", "prep_version": "make_fixture stand-in"}}
    (root / "cells").mkdir(parents=True, exist_ok=True)
    for sid in a.obs["sample_id"].cat.categories:
        a[a.obs["sample_id"] == sid].copy().write_h5ad(root / "cells" / f"{sid}.h5ad")
    print(f"{a.n_obs} nuclei, {a.obs['cluster'].nunique()} clusters -> {root / 'cells'}")
    return root


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out")
    ap.add_argument("--layout", choices=["both", "linked"], default="both")
    ap.add_argument("--from-cellranger", metavar="DIR", help="Cell Ranger output (*filtered_feature_bc_matrix.h5 below DIR)")
    ap.add_argument("--from-prep", metavar="DIR", help="sc-prep's cells output (<sample_id>.h5ad, raw counts in X)")
    ap.add_argument("--samples", type=int, default=4)
    ap.add_argument("--max-obs", type=int, default=3000)
    args = ap.parse_args()
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    if args.from_cellranger:
        integrate_like(out, _read_cellranger(Path(args.from_cellranger), args.samples), args.max_obs)
    elif args.from_prep:
        integrate_like(out, _read_prep(Path(args.from_prep), args.samples), args.max_obs)
    else:
        for layout, path in make_fixture(out, args.layout).items():
            print(f"{layout}: {path}")


if __name__ == "__main__":
    main()
