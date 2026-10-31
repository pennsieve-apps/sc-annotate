# sample-input

This app reads sc-integrate's `cells` output (`<sample_id>.h5ad`: X log-normalized,
`layers["counts"]`, `obs["cluster"]`, `obsm["X_umap"]`), optionally a labelled reference on
`reference` and a `markers.csv` on `markers`. The contract is in
`workflow-single-cell/docs/conventions.md`.

## Synthetic fixture (no download)

```sh
make fixture PYTHON=.venv/bin/python   # data/fixture/{linked,flat}/
make run PYTHON=.venv/bin/python       # Docker over data/fixture/linked/ -> data/output/
```

Three samples (`s1`-`s3`, sequenced progressively shallower) of 500 nuclei and 260 genes. Six
cell types are planted (Neuron, Satellite glia, Fibroblast, Endothelial, Macrophage, T cell), each
with three markers and a program of 12 other genes; satellite glia span two clusters. The truth is
in `truth.csv`. `reference/reference_atlas.h5ad` is a CELLxGENE-like reference of the same types
(1,200 cells, Ensembl `var_names` with symbols in `var["feature_name"]`, counts in `X`,
`obs["cell_type"]`, `obs["donor"]`; set `REFERENCE_BATCH_COLUMN=donor`), and
`markers/markers.csv` lists the planted markers. With all three linked, `MODE=auto` uses the
reference; `MODE=markers` uses the markers.

## A markers.csv

```csv
cell_type,gene,weight
Satellite glia,FABP7,1
Satellite glia,KCNJ10,1
Satellite glia,SNAP25,-1
Fibroblast,DCN,
Fibroblast,LUM,
```

`weight` is optional (default 1); a negative weight marks a gene the type should not express, 0
drops the gene. Other columns (such as `source`) are ignored. Symbols match case-insensitively.

## Real data

Run sc-prep, sc-qc and sc-integrate on the workflow's demo data (`scripts/fetch-sample-data.sh
snrna` in the workflow repository), e.g. the C2 DRG data (Discover 475), then:

```sh
docker run --rm --platform linux/amd64 --memory 4g --network none --read-only --tmpfs /tmp \
  -e INPUT_DIR=/data/input -e OUTPUT_DIR=/data/output -e MARKER_SET=drg-human \
  -v /path/to/integrate/cells:/data/input/cells:ro -v "$PWD/data/output:/data/output" sc-annotate:cpu
```

Add `-v /path/to/model:/data/input/reference:ro` to transfer labels from a reference or an earlier
run's `model` output.

Without the upstream apps, `python -m tests.make_fixture DIR --from-cellranger
<folder with *filtered_feature_bc_matrix.h5>` (or `--from-prep <sc-prep cells>`) is a stand-in:
it keeps nuclei with >= 300 genes and < 10 % mitochondrial reads, normalizes, and computes a joint
PCA, Leiden clusters and a UMAP (no ambient removal, doublet removal or batch correction).
