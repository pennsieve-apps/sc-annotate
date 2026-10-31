# Third-party software and data

This app is Apache-2.0 (see `LICENSE`). The images it builds contain the following third-party
components, installed from PyPI at the pinned versions in `requirements.txt` (and
`requirements-cpu.txt` / `requirements-cuda.txt`); their licences apply to the images. Each
licence was read in the project's own LICENSE file at the pinned tag. **Nothing in the images is
GPL**: celltypist declares `leidenalg` (GPL-3.0-or-later) and `igraph` (GPL-2.0) for its
over-clustering, which this app never runs, so they (and igraph's `texttable`) are not installed
(`pip install --no-deps`). They are in `requirements-dev.txt` only, for the real-data stand-in in
`tests/make_fixture.py`, which is not part of the images.

| Component | What | Licence | Source |
|---|---|---|---|
| scvi-tools 1.5.2 | scVI, scANVI, scArches query mapping (reference mode, `METHOD=scanvi`). Called as a library. | BSD-3-Clause | https://github.com/scverse/scvi-tools |
| celltypist 1.7.1 | `celltypist.train` / `celltypist.annotate` (reference mode, `METHOD=celltypist`). Code only: **no pretrained model is bundled or downloaded**. | MIT | https://github.com/Teichlab/celltypist |
| PyTorch 2.15.0 (cpu variant: `+cpu` build; gpu variant: CUDA 13.2 build with triton 3.9.0) | Tensor computation for scvi-tools. | BSD-3-Clause style (bundle: Apache-2.0, BSD, MIT, ...); triton MIT | https://pytorch.org |
| nvidia-cublas, -cuda-runtime, -cudnn-cu13, -cufft, -cusolver, -cusparse, -cusparselt-cu13, -nccl-cu13, -nvjitlink, -nvshmem-cu13, -nvtx, -cuda-nvrtc, -cuda-cupti, -cuda-cccl, -cufile; cuda-toolkit 13.2.2, cuda-bindings 13.4.4, cuda-pathfinder 1.8.5 | gpu variant only: CUDA runtime libraries. | NVIDIA proprietary, redistributable (licence in each wheel); cuda-bindings/pathfinder Apache-2.0 | https://developer.nvidia.com/cuda-toolkit |
| Pyro 1.9.2 (pyro-ppl, pyro-api 0.1.2) | Dependency of scvi-tools. | Apache-2.0 | https://github.com/pyro-ppl/pyro |
| Lightning 2.6.6 (lightning, pytorch-lightning, lightning-utilities 0.15.3, torchmetrics 1.9.0) | Training loop of scvi-tools. | Apache-2.0 | https://github.com/Lightning-AI/pytorch-lightning |
| scanpy 1.12.5 | Normalization, `highly_variable_genes`, `score_genes`. | BSD-3-Clause | https://github.com/scverse/scanpy |
| anndata 0.13.4, mudata 0.4.1 | `.h5ad` reading and writing. | BSD-3-Clause | https://github.com/scverse |
| scikit-learn 1.7.2 | CellTypist's logistic regression (kept below 1.8, which removed an argument celltypist 1.7.1 passes). | BSD-3-Clause | https://scikit-learn.org |
| scikit-misc 0.5.3 | loess for `seurat_v3` variable genes. | BSD-3-Clause | https://github.com/has2k1/scikit-misc |
| NumPy 2.5.4, SciPy 1.18.1, pandas 3.1.0, h5py 3.16.0 | Arrays, sparse matrices, tables, HDF5. | BSD-3-Clause (NumPy also 0BSD/MIT/Zlib/CC0 parts) | https://numpy.org, https://scipy.org, https://pandas.pydata.org, https://www.h5py.org |
| Matplotlib 3.11.2, Pillow 13.0.0 | PNG figures. | Matplotlib licence (PSF-based); MIT-CMU | https://matplotlib.org |
| openpyxl 3.1.5, et_xmlfile, click, requests, urllib3, charset-normalizer, idna, certifi | Dependencies of celltypist (imported, unused: no network at run time). | MIT / BSD / Apache-2.0 / MPL-2.0 (certifi) | PyPI |
| xarray, sparse, ml_collections, docrep, rich, tensorboard (+ tensorboard-data-server, absl-py, grpcio, protobuf, Markdown, Werkzeug), pydantic (+ pydantic-core, pydantic-settings, annotated-types, typing-inspection, python-dotenv), formulaic, interface_meta, narwhals, msgspec, opt_einsum, cloudpickle, fsspec, aiohttp (+ aiosignal, aiohappyeyeballs, frozenlist, multidict, propcache, yarl, attrs), Jinja2, MarkupSafe, sympy, mpmath, networkx, filelock, setuptools | Dependencies of scvi-tools, torch and Lightning (versions in `requirements.txt`). | Apache-2.0 / BSD / MIT | PyPI |
| numba, llvmlite, umap-learn, pynndescent, statsmodels, patsy, seaborn, joblib, threadpoolctl, natsort, fast-array-utils, legacy-api-wrap, session-info2, scverse-misc, zarr, numcodecs, donfig, google-crc32c, array-api-compat | Dependencies of scanpy / anndata. | BSD-2/3-Clause, MIT, Apache-2.0, MPL-2.0 | PyPI |
| contourpy, cycler, fonttools, kiwisolver, packaging, pyparsing, python-dateutil, six, tqdm, typing_extensions, tzdata, wrapt, PyYAML, Pygments, markdown-it-py, mdurl | Dependencies of the above. | MIT / BSD / Apache-2.0 / MPL-2.0+MIT (tqdm) / PSF-2.0 | PyPI |
| python:3.12.16-slim-bookworm | Base image (Debian 12 + CPython 3.12). | PSF (Python); Debian packages under their own free licences | https://hub.docker.com/_/python |

## Bundled data: built-in marker sets

`processor/markers/{drg-human,knee-human,broad}.csv` list cell type names and HGNC gene symbols
(facts taken from published tables and text, with the source per gene); no text, figure or table
of the articles is reproduced.

| Set | Source articles (licence of the article) |
|---|---|
| `drg-human` | Bhuiyan et al. 2024, Sci Adv, doi:10.1126/sciadv.adj9173 (CC BY-NC 4.0); Tavares-Ferreira et al. 2022, Sci Transl Med, doi:10.1126/scitranslmed.abj8186 (NIH author manuscript); Avraham et al. 2022, Pain, doi:10.1097/j.pain.0000000000002628 (author manuscript) |
| `knee-human` | Ji et al. 2019, Ann Rheum Dis, doi:10.1136/annrheumdis-2017-212863 (CC BY-NC 4.0); Chou et al. 2020, Sci Rep, doi:10.1038/s41598-020-67730-y (CC BY 4.0); Zhang et al. 2019, Nat Immunol, doi:10.1038/s41590-019-0378-1; Emont et al. 2022, Nature, doi:10.1038/s41586-022-04518-2 |
| `broad` | PanglaoDB (Franzén et al. 2019, Database, doi:10.1093/database/baz046; CC BY 4.0), marker table as redistributed by OmniPath (downloaded 2026-10-31) |

## Not bundled

- **CellTypist pretrained models** (https://celltypist.org/models): pickled scikit-learn models
  hosted by the Wellcome Sanger Institute. Neither `models.json`, the model descriptions, the
  celltypist README nor celltypist.org states a licence for them; the site's terms point to the
  Sanger default (CC BY-NC-ND 4.0 for content it hosts), and each model is trained on third-party
  data with its own terms. Redistribution in an image is therefore not clearly allowed, loading a
  pickle from an input would run code, and no model covers DRG or joint tissue: none is bundled,
  and none is downloaded (no network at run time).
- **Demo data** (not in the image or the repository): Pennsieve Discover 475 v1
  (doi:10.26275/cxuf-ftav) and 480 v1 (doi:10.26275/9qsp-i8dh), both CC BY 4.0.
