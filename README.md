# sc-annotate

Cell types for **single-cell and single-nucleus RNA-seq** (10x 3'/5', Flex, the RNA half of
Multiome; human, mouse, rat). It is the fourth step of the *Single-nucleus Atlas Mapping &
Condition Comparison* workflow
(`sc-prep → sc-qc → sc-integrate → sc-annotate → {sc-markers, st-compare} → sc-report`), and its
labels feed the *Multiome Gene Regulation* workflow (`atac-regulome`).

**For a biologist.** After integration every nucleus belongs to a cluster (`C01`, `C02`, ...).
This app gives each nucleus a cell type name, in one of two ways:

- **With a reference** you trust (an annotated atlas of the same tissue, for example from
  CELLxGENE, or the output of an earlier run of this app), the reference's labels are transferred
  to every nucleus, one by one. Nuclei that resemble no reference type well enough stay
  `Unassigned`. Only cell types that are in the reference can be found.
- **Without a reference**, each cluster is named after the cell type whose marker genes it
  expresses most, from your own `markers.csv` or from a built-in table taken from published
  atlases: **human dorsal root ganglion** (neuron subtypes including nociceptors,
  proprioceptors, LTMRs, pruritogen receptors, cold neurons; satellite glia; Schwann cells;
  fibroblasts, endothelium, pericytes, macrophages, T cells), **human knee joint** (chondrocyte
  states, lining and sublining synovial fibroblasts, synovial macrophages, immune cells,
  vasculature, adipocytes) or **broad** types for any tissue. A cluster whose best two types are
  too close stays `Unassigned`, so you can look at it yourself.

Each nucleus then carries `cell_type`, a confidence `cell_type_score` (0-1) and where the label
came from (`cell_type_source`). The app also writes a reusable **model**: a labelled reference
(`reference.h5ad`), the scANVI model when it trained one, and per-type expression signatures for
the spatial deconvolution app cell2location. Run it once with markers, check the result, then use
the model as the reference of the next dataset.

**For a computational analyst.** Reference mode transfers labels per cell with CellTypist
(`METHOD=celltypist`, default on CPU: logistic regression on the reference's 3,000 most variable
genes, log1p of counts per 10,000) or scANVI (`METHOD=scanvi`, default on the GPU variant: an
scVI model of the reference counts with the scArches architecture, fine-tuned as scANVI on the
labels, the query mapped by scArches surgery with the query samples as new batches, exactly as in
the scvi-tools tutorial "Reference mapping with SCVI-Tools"). Genes are matched by Ensembl id when
both sides have ids, else by symbol; the call is the most probable label, `Unassigned` below
`MIN_SCORE`. Markers mode scores every gene of every marker set per sample with
`scanpy.tl.score_genes` (expression minus a control set from the same expression bin; Satija et
al. 2015, Tirosh et al. 2016), averages them with the set's weights, z-scores each set over all
nuclei and calls each cluster the set with the highest mean z when it is positive and ahead of the
runner-up by `MARGIN`.

## Method

1. **Inputs.** Every `<sample_id>.h5ad` on `cells` is read twice, one sample at a time: once for
   its `obs`, gene list and UMAP (backed, no matrix), once for the work. Genes present in every
   sample are used (logged; `summary.json → n_genes_common`). `obs["cluster"]` is required.
2. **Mode.** `MODE=auto` picks reference mode when a reference is linked, else markers mode.
3. **Reference mode.**
   - The reference's `obs` is read first; at most `MAX_CELLS_PER_TYPE` cells per type are drawn
     (seeded), types with fewer than 10 cells and unlabelled cells (`Unassigned`, `Unknown`,
     empty) are dropped, and only those rows of the counts are loaded (`layers["counts"]`, `X` or
     `raw.X`, the first that is integer-valued).
   - Genes are matched to the query (Ensembl ids, else symbols ignoring case); fewer than 200
     shared genes stops the run. The 3,000 most variable genes of the reference counts
     (`seurat_v3`, over all reference cells; per-batch selection fails on batches of a few hundred
     nuclei) are the model's genes.
   - `celltypist`: `celltypist.train` on log1p(counts per 10,000) of those genes (one-vs-rest
     logistic regression, CellTypist's default), then `celltypist.annotate` per sample on all its
     genes (`majority_voting` off: clusters come from sc-integrate). Score: the probability of the
     best label.
   - `scanvi`: `SCVI(use_layer_norm="both", use_batch_norm="none", encode_covariates=True,
     dropout_rate=0.2, n_layers=2)` on the reference counts with `REFERENCE_BATCH_COLUMN` as the
     batch, `MAX_EPOCHS` epochs (0 = scvi-tools' rule: 400, fewer above 20,000 cells);
     `SCANVI.from_scvi_model` + 20 epochs with 100 samples per label; the query counts (genes of
     the model) are mapped with `SCANVI.prepare_query_anndata` / `load_query_data` and trained
     `QUERY_EPOCHS` epochs without weight decay; `predict(soft=True)` gives each label's
     probability. A linked sc-annotate model with `scanvi/` skips the reference training.
   - Device: the GPU when torch sees one (logged and recorded), else the CPU.
4. **Markers mode.** Marker sets come from a linked `markers.csv` or the built-in `MARKER_SET`.
   Sets with fewer than `MIN_GENES_PRESENT` positively weighted genes in the data are skipped
   (logged). Per sample, each gene gets `score_genes([gene], ctrl_size=50, n_bins=25)`; a set's
   score is `sum(w * score) / sum(|w|)`; scores are z-scored per set over all nuclei; per cluster
   the mean z of each set decides. `cell_type_score` is the cluster's *agreement*: the fraction of
   its nuclei whose own best set is the cluster's best set. It is reported, not used for the call:
   with many related subtypes (eleven DRG neuron sets) single nuclei disagree even in a clean
   cluster.
5. **Outputs.** Each sample is rewritten with the three new `obs` columns (nothing else changes:
   same `obs` order, genes, layers, embeddings; `uns["pennsieve"]["annotation"]` records the run).
   The model's `reference.h5ad` is the training reference subsample (reference mode) or up to
   `MAX_CELLS_PER_TYPE` labelled nuclei per type, never `Unassigned` (markers mode), with counts
   on the shared genes.

Deviations from the single-cell best-practices guide (Heumos et al. 2023): it recommends
automated annotation followed by manual curation; this app does the automated part and leaves
ambiguous clusters `Unassigned` (and reports runner-up types, agreement and scores) for that
curation. Marker-based typing is done at cluster level, as the guide suggests for marker genes,
not per cell.

## Ports

| Port | Direction | Content |
|---|---|---|
| `cells` | in (required, subfolder) | sc-integrate's `<sample_id>.h5ad` (X log-normalized, `layers["counts"]`, `obs["cluster"]`, `obsm["X_umap"]`) |
| `reference` | in (optional, subfolder) | a labelled `.h5ad` with counts, or an sc-annotate `model` output |
| `markers` | in (optional, subfolder) | `markers.csv`: `cell_type, gene[, weight]` |
| `cells` | out | the same files with `obs["cell_type"]`, `obs["cell_type_score"]`, `obs["cell_type_source"]` |
| `labels` | out | `labels.csv` |
| `model` | out | `reference.h5ad`, `signatures.csv`, `reference_summary.csv`, `scanvi/` |
| `annotation` | out | `summary.json`, tables and figures |

Without links, files are found by name anywhere under `INPUT_DIR`: `markers.csv`, a reference as
`reference.h5ad` (with its `scanvi/` beside it) or any `.h5ad` in a `reference/` folder; every
other `.h5ad` is a sample.

## Parameters

| Parameter | Default | Effect |
|---|---|---|
| `MODE` | `auto` | `auto`, `reference`, `markers` (above). |
| `METHOD` | `celltypist` (gpu variant: `scanvi`) | Reference mode's label transfer. |
| `MARKER_SET` | `broad` | Built-in set when no `markers.csv` is linked: `drg-human`, `knee-human`, `broad`, `none`. |
| `CELL_TYPE_COLUMN` | `cell_type` | The reference's label column (an sc-annotate model always uses `cell_type`). |
| `REFERENCE_BATCH_COLUMN` | empty | The reference's batch column for scVI (donor, sample, chemistry). |
| `MIN_SCORE` | `0.5` | Reference mode: below this probability a nucleus is `Unassigned`. |
| `MARGIN` | `0.2` | Markers mode: the best set's mean z must lead the runner-up by this much. |
| `MIN_GENES_PRESENT` | `2` | Markers mode: genes a set needs in the data to be scored. |
| `MAX_CELLS_PER_TYPE` | `2000` | Reference (and model) cells per type. |
| `MAX_EPOCHS` | `0` | Reference scVI epochs (0 = scvi-tools' rule). |
| `QUERY_EPOCHS` | `100` | scArches query epochs. |
| `SEED` | `42` | Subsampling, control genes, training. |
| `THREADS` | `0` | CPU threads (0 = the container's CPU quota). |

Bad values exit with code 2; no usable input (no samples, no reference in `MODE=reference`, every
sample failed, too few shared genes) exits with code 1.

## Outputs

- `cells/<sample_id>.h5ad`: as read, plus `obs["cell_type"]` (categorical), `obs["cell_type_score"]`
  (float32, 0-1), `obs["cell_type_source"]` (`reference`, `model` or `markers`).
- `labels/labels.csv`: `sample_id, obs_id, cluster, cell_type, cell_type_score`.
- `model/reference.h5ad` (X = counts, `obs["cell_type"]`, `obs["batch"]`, `var["gene_ids"]`),
  `model/signatures.csv` (`gene, gene_id`, one column per type: mean counts per cell, the format
  the cell2location app reads), `model/reference_summary.csv` (`cell_type, n_cells, n_used,
  status`), `model/scanvi/` (`model.pt` for `scvi.model.SCANVI.load` in a notebook; `weights.pt` +
  `setup.json`, what a later run of this app reads).
- `annotation/summary.json` (mode, method, counts, fraction `Unassigned`, per-type counts and mean
  score, gene matching, marker sets used and skipped, training settings),
  `cell_types_by_sample.csv` (`sample_id, cell_type, n_obs, fraction`), `confusion.csv`
  (`cluster, cell_type, n_obs, mean_score, fraction_of_cluster`), `clusters.csv` (markers mode:
  `cluster, n_obs, cell_type, best, best_z, second, second_z, agreement, reason`; reference mode:
  each cluster's majority type), `marker_scores.csv` (markers mode: `cluster, marker_set,
  mean_z`), `umap_cell_type.png`, `cell_types_by_sample.png`, `score_histogram.png`.
- `provenance.json` in every folder (app, version, tools, parameters, inputs, timings, per-sample
  status, peak memory, citations).

## Built-in marker sets

`processor/markers/*.csv` (`cell_type, gene, source`). Every gene was checked against the cited
paper's tables or text (and its HGNC symbol); no gene is listed for two types of the same set.

| Set | Types | Sources |
|---|---|---|
| `drg-human` | 20: Neuron (pan-neuronal, used when no subtype leads), Proprioceptor (PVALB+), A-beta LTMR, A-delta LTMR, two A-delta HTMR, PEP and NP nociceptors, Pruritogen receptor (SST+), Cold thermoreceptor, C-LTMR, Injured neuron (ATF3+), Satellite glia, Myelinating and Non-myelinating Schwann cell, Fibroblast, Endothelial, Pericyte / smooth muscle, Macrophage, T cell | Bhuiyan et al. 2024 (Tables S2 and S6, human DRG), Tavares-Ferreira et al. 2022, Avraham et al. 2022 |
| `knee-human` | 14: effector, prehypertrophic and hypertrophic chondrocytes; lining (PRG4+) and sublining synovial fibroblasts; synovial macrophages; CD1C+ dendritic cells; T, B, plasma and mast cells; endothelial; pericyte / smooth muscle; adipocytes | Ji et al. 2019 (OA cartilage), Chou et al. 2020 (OA synovium), Zhang et al. 2019 (synovium), Emont et al. 2022 (adipose) |
| `broad` | 16: T, NK, B, plasma, macrophages, mast, neutrophils, endothelial, fibroblasts, smooth muscle / pericytes, epithelial, neurons, Schwann cells, oligodendrocytes, adipocytes, erythroid | PanglaoDB (Franzén et al. 2019), human markers of low ubiquitousness |

Bhuiyan et al.'s neuron type names are their cross-species harmonized names (`SMR2` has no human
gene; it names the type). Left out for lack of specific human markers: the rarer peptidergic
subtypes, rapidly vs slowly adapting A-beta LTMRs, perineurial vs endoneurial fibroblasts
(DRG); regulatory/proliferative/fibrocartilage chondrocytes, osteoblasts, osteoclasts,
meniscus-specific cells, TREM2+ lining macrophages, NK cells (knee). Knee adipocyte markers come
from subcutaneous/visceral fat, not the infrapatellar fat pad.

## Results on the demo data

**Markers mode on the C2 DRG data** (Discover 475; sc-prep → sc-qc → sc-integrate outputs in
`workflow-single-cell/data/work/drg-c2/`, 12 samples, 18,439 nuclei, 15 clusters;
`MARKER_SET=drg-human`; outputs in `data/work/drg-c2/annotate/`): 10 types called, 34.6 % of
nuclei `Unassigned`. Called: Fibroblast (C02, C06; 3,581), Satellite glia (C03; 1,878), Neuron
(C04; 1,852), Endothelial (C09; 1,042), Proprioceptor (PVALB+) (C10; 874), Macrophage (C11; 858),
Pruritogen receptor (SST+) (C12; 688), PEP nociceptor (C13; 593), Myelinating Schwann cell (C14;
537), Pericyte / smooth muscle (C15; 147). Unassigned: C07 (1,318; CALCA-high, between the PEP
nociceptor and A-delta HTMR sets, margin 0.11), C01 (2,182; low expression of every set, mostly
sample CC0048), C05 and C08 (mixed glial and neuronal markers, likely neuron-glia doublets or
ambient RNA). The eight neuron-rich samples are 38-65 % neuronal types; **CC0032, CC0037, CC0048
and CC0050 are 0-7 % neuronal** (CC0037: none; fibroblasts 50 %, endothelial 19 %, macrophages
16 %), i.e. these biopsies are mostly nerve root / connective tissue rather than ganglion; compare
conditions on them with care.

**Reference mode, atlas split** (Discover 480; 8 donors, 4 per half, at most 3,000 nuclei per
sample; a stand-in for sc-qc/sc-integrate from `tests/make_fixture.py --from-cellranger`): half A
was annotated with `drg-human` markers, its `model/` linked as the reference of half B (10,046
nuclei), and the transferred labels compared with half B's own marker labels. Half A's reference
held 10 types (A-beta LTMR, SST+ pruritogen receptor and eight non-neuronal types; the other
neuron subtypes were not called in half A, so cannot be transferred). On the 8,001 half-B nuclei
whose marker label is one of those 10 types: scANVI agreed on 72.9 % (0.8 % `Unassigned`
overall), CellTypist on 50.8 % with 40.4 % `Unassigned`, and 76.8 % of the nuclei CellTypist did
label. Most disagreement is between the neighbouring stromal / glial types (satellite glia vs
non-myelinating Schwann, fibroblast vs macrophage in low-quality clusters), where the marker calls
themselves are cluster-level. This measures consistency between the two modes, not accuracy.

**Synthetic fixture** (`tests/make_fixture.py`: 3 samples, 6 planted types): markers 100 %,
CellTypist 95.9 %, scANVI 98.7 % of nuclei get their planted type; the scANVI model reused as a
reference gives the same.

## Runtime

Measured in the linux/amd64 cpu image under emulation on an M-series Mac (Docker, `--cpus 4`,
`--memory 4g`); expect native amd64 to be several times faster.

| Run | Nuclei | Wall time | Peak memory (cgroup) |
|---|---|---|---|
| markers, C2 DRG, 18,082 genes | 18,439 | 37 s | 1.36 GB |
| CellTypist, atlas split (8,468 reference nuclei) | 10,046 | 63 s | 3.56 GB |
| scANVI, atlas split (400 + 20 + 100 epochs; native arm64, 4 threads) | 10,046 | 549 s | 1.63 GB (process RSS) |

Memory: markers mode holds one sample plus a nuclei × sets score table; reference mode holds the
reference subsample (`MAX_CELLS_PER_TYPE` × types, all genes, CSR) and, for scANVI, the query's
counts on 3,000 genes (about 1 GB per 100,000 nuclei). CellTypist densifies the reference
subsample on the 3,000 genes for training (8 bytes × cells × 3,000: 1.4 GB for 60,000 cells).
`runtime.memory` is 16 GiB, enough for 300,000 query nuclei with a 40-type reference. On a CPU,
scANVI takes minutes per 10,000 nuclei and epoch count; use the gpu variant for large data.

## GPU variant

`variants` in `app.yml`: the `gpu` variant is built with `TORCH_FLAVOUR=cuda` (CUDA 13.2 PyTorch
wheels), runs on `computeTypes: [gpu]` and defaults to `METHOD=scanvi`. Its image was built and
imports checked locally (no GPU here, so it was not run on one; `torch.cuda.is_available()`
decides at run time and the device is logged).

## Running it locally

```sh
python3.12 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
make test PYTHON=.venv/bin/python        # pytest on the synthetic fixture (no Docker)
make run PYTHON=.venv/bin/python         # cpu image over data/fixture/linked/ -> data/output/
make validate PYTHON=.venv/bin/python    # app.yml schema, CITATION.cff
```

See `sample-input/README.md` for the inputs and real data.

## Limitations

- Reference mode can only find types in the reference; a type missing there is forced onto the
  nearest reference type unless its probability falls below `MIN_SCORE`. Use a reference of the
  same tissue, species and (ideally) nuclei rather than whole cells.
- CellTypist probabilities are one-vs-rest and not calibrated across references; scANVI's are
  softmax probabilities of a model trained a fixed number of epochs. Neither is a statistical
  confidence.
- Markers mode labels clusters, not nuclei: a cluster that mixes types (doublets, ambient RNA,
  low quality) gets one label or `Unassigned`. Its quality depends on sc-qc's ambient removal
  (neuronal transcripts leak into every DRG nucleus) and on sc-integrate's resolution.
- Built-in markers are human; mouse/rat symbols match by case, but marker specificity differs
  between species (Bhuiyan et al. 2024 show this for DRG neurons).
- No CellTypist pretrained model is bundled (see Licences); none covers DRG or joint tissue.

## Licences

Our code is Apache-2.0 (`LICENSE`). scvi-tools, scanpy and anndata are BSD-3-Clause, CellTypist
MIT, PyTorch BSD-style, Pyro and Lightning Apache-2.0. The gpu image contains the NVIDIA CUDA
libraries of the CUDA build of PyTorch (proprietary, redistributable). Nothing in either image is
GPL: igraph and leidenalg (GPL), which celltypist declares for its over-clustering, are not
installed. **CellTypist pretrained models are not bundled**: they are pickles hosted by the
Wellcome Sanger Institute without an explicit model licence (the site's default terms are CC
BY-NC-ND 4.0), and none fits the target tissues. The built-in marker tables are lists of gene
symbols with their sources; the source articles' licences are in `THIRD_PARTY.md`. Details in
`THIRD_PARTY.md`.

## Credits

- **scvi-tools** (Gayoso et al. 2022, scverse) provides scVI (Lopez et al. 2018), scANVI (Xu et
  al. 2021) and scArches query mapping (Lotfollahi et al. 2022), which this app uses for
  reference-based label transfer.
- **CellTypist** (Domínguez Conde et al. 2022, Teichmann lab) trains and applies the logistic
  regression classifier of the CPU label transfer.
- **Scanpy** (Wolf, Angerer and Theis 2018) and **anndata** (Virshup et al. 2024) read and write
  the data, normalize it, select variable genes and score marker genes (`score_genes`, the
  method of Satija et al. 2015 and Tirosh et al. 2016).
- **PyTorch** (Paszke et al. 2019) runs the scvi-tools models on CPU or GPU.
- **Marker sets**: Bhuiyan, Xu, Renthal and colleagues' harmonized DRG/trigeminal atlas,
  Tavares-Ferreira, Price and colleagues' human DRG spatial atlas, Avraham, Cavalli and
  colleagues' human DRG single-nucleus data (`drg-human`); Ji, Wang and colleagues' human OA
  cartilage atlas, Chou, Lotz and colleagues' human OA synovium data, Zhang, Raychaudhuri and the
  AMP RA/SLE network's synovial atlas, Emont, Rosen and colleagues' human adipose atlas
  (`knee-human`); Franzén, Gan and Björkegren's PanglaoDB (`broad`).
- **Demo data**: Arendt-Tranholm, Sankaranarayanan and Price (C2 DRG single-nucleus data,
  Discover 475, described by Arendt-Tranholm et al. 2026) and Sankaranarayanan and Price (human
  DRG atlas, Discover 480), NIH PRECISION Human Pain Network.
- **Method guidance**: Heumos et al. 2023, single-cell best practices.

## Citations

Full entries (all authors, PMIDs) in `CITATION.cff`.

- Heumos L et al. (2023). Best practices for single-cell analysis across modalities. *Nat Rev Genet* 24:550-572. doi:10.1038/s41576-023-00586-w
- Gayoso A et al. (2022). A Python library for probabilistic analysis of single-cell omics data. *Nat Biotechnol* 40:163-166. doi:10.1038/s41587-021-01206-w
- Lopez R et al. (2018). Deep generative modeling for single-cell transcriptomics. *Nat Methods* 15:1053-1058. doi:10.1038/s41592-018-0229-2
- Xu C et al. (2021). Probabilistic harmonization and annotation of single-cell transcriptomics data with deep generative models. *Mol Syst Biol* 17:e9620. doi:10.15252/msb.20209620
- Lotfollahi M et al. (2022). Mapping single-cell data to reference atlases by transfer learning. *Nat Biotechnol* 40:121-130. doi:10.1038/s41587-021-01001-7
- Domínguez Conde C et al. (2022). Cross-tissue immune cell analysis reveals tissue-specific features in humans. *Science* 376:eabl5197. doi:10.1126/science.abl5197
- Wolf FA, Angerer P, Theis FJ (2018). SCANPY: large-scale single-cell gene expression data analysis. *Genome Biol* 19:15. doi:10.1186/s13059-017-1382-0
- Virshup I et al. (2024). anndata: Access and store annotated data matrices. *J Open Source Softw* 9:4371. doi:10.21105/joss.04371
- Satija R et al. (2015). Spatial reconstruction of single-cell gene expression data. *Nat Biotechnol* 33:495-502. doi:10.1038/nbt.3192
- Tirosh I et al. (2016). Dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq. *Science* 352:189-196. doi:10.1126/science.aad0501
- Paszke A et al. (2019). PyTorch: An Imperative Style, High-Performance Deep Learning Library. NeurIPS 32. doi:10.48550/arXiv.1912.01703
- Bhuiyan SA et al. (2024). Harmonized cross-species cell atlases of trigeminal and dorsal root ganglia. *Sci Adv* 10:eadj9173. doi:10.1126/sciadv.adj9173
- Tavares-Ferreira D et al. (2022). Spatial transcriptomics of dorsal root ganglia identifies molecular signatures of human nociceptors. *Sci Transl Med* 14:eabj8186. doi:10.1126/scitranslmed.abj8186
- Avraham O et al. (2022). Profiling the molecular signature of satellite glial cells at the single cell level reveals high similarities between rodents and humans. *Pain* 163:2348-2364. doi:10.1097/j.pain.0000000000002628
- Ji Q et al. (2019). Single-cell RNA-seq analysis reveals the progression of human osteoarthritis. *Ann Rheum Dis* 78:100-110. doi:10.1136/annrheumdis-2017-212863
- Chou CH et al. (2020). Synovial cell cross-talk with cartilage plays a major role in the pathogenesis of osteoarthritis. *Sci Rep* 10:10868. doi:10.1038/s41598-020-67730-y
- Zhang F et al. (2019). Defining inflammatory cell states in rheumatoid arthritis joint synovial tissues by integrating single-cell transcriptomics and mass cytometry. *Nat Immunol* 20:928-942. doi:10.1038/s41590-019-0378-1
- Emont MP et al. (2022). A single-cell atlas of human and mouse white adipose tissue. *Nature* 603:926-933. doi:10.1038/s41586-022-04518-2
- Franzén O, Gan LM, Björkegren JLM (2019). PanglaoDB: a web server for exploration of mouse and human single-cell RNA sequencing data. *Database* 2019:baz046. doi:10.1093/database/baz046
- Kleshchevnikov V et al. (2022). Cell2location maps fine-grained cell types in spatial transcriptomics. *Nat Biotechnol* 40:661-671. doi:10.1038/s41587-021-01139-4 (the consumer of `signatures.csv`)
- Arendt-Tranholm A, Sankaranarayanan I, Price TJ (2025). Single nucleus sequencing of human C2 dorsal root ganglia tissue from fusion surgeries [dataset]. Pennsieve Discover 475 v1. doi:10.26275/cxuf-ftav (CC BY 4.0)
- Arendt-Tranholm A et al. (2026). Transcriptome of the human C2 dorsal root ganglia in C1–2 arthrodesis surgery: insight for neck pain. *Brain* 149:1349-1364. doi:10.1093/brain/awaf370
- Sankaranarayanan I, Price TJ (2025). Single nucleus sequencing atlas of human dorsal root ganglion [dataset]. Pennsieve Discover 480 v1. doi:10.26275/9qsp-i8dh (CC BY 4.0)
