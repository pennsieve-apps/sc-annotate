"""
Reference mode: label transfer from a labelled reference to the query cells.

scanvi (scvi-tools; Xu et al. 2021, Lotfollahi et al. 2022), as in the scvi-tools tutorial
"Reference mapping with SCVI-Tools": an scVI model of the reference counts (scArches
architecture: layer norm, no batch norm, covariates encoded, 2 layers, dropout 0.2), turned into
scANVI with the reference labels (20 epochs, 100 samples per label), then the query is mapped by
scArches surgery (new batches = the query samples; 100 epochs without weight decay) and each
cell gets scANVI's class probabilities (predict(soft=True)).

celltypist (Dominguez Conde et al. 2022): a CellTypist logistic-regression model trained on the
reference's N_TOP_GENES most variable genes (log1p of counts normalized to 10,000), applied to each query
sample in turn; the score is the probability of the best label.

A trained scANVI model is saved three ways in scanvi/: model.pt (scvi-tools' own format, for
SCANVI.load in a notebook), and weights.pt (the module's tensors only) + setup.json (the settings
to rebuild it). A later run reads only weights.pt (torch.load(weights_only=True)) and setup.json,
never model.pt, which is a pickle and so unsafe to load from an input.
"""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import pandas as pd

log = logging.getLogger("sc-annotate")

UNLABELED = "__unlabeled__"
N_TOP_GENES = 3000
SCVI_KWARGS = {"use_layer_norm": "both", "use_batch_norm": "none", "encode_covariates": True, "dropout_rate": 0.2, "n_layers": 2}
SCANVI_EPOCHS = 20
MAX_SETUP_BYTES = 2**20
MAX_WEIGHTS_BYTES = 2**30
# init parameters a setup.json may set when a model is rebuilt (scalars only)
INIT_KEYS = {"n_hidden", "n_latent", "n_layers", "dropout_rate", "dispersion", "gene_likelihood", "use_observed_lib_size",
             "linear_classifier", "latent_distribution", "use_layer_norm", "use_batch_norm", "encode_covariates",
             "deeply_inject_covariates"}


def device() -> tuple[str, str]:
    """('gpu' | 'cpu', description); the GPU when torch sees one."""
    import torch

    if torch.cuda.is_available():
        return "gpu", f"cuda ({torch.cuda.get_device_name(0)})"
    return "cpu", "cpu (no CUDA device)"


def quiet() -> None:
    import scvi

    scvi.settings.verbosity = logging.WARNING
    for name in ("scvi", "lightning", "lightning.pytorch", "lightning_fabric", "lightning.fabric", "pytorch_lightning", "celltypist", "py.warnings"):
        logging.getLogger(name).setLevel(logging.ERROR)


def select_genes(ref) -> list[str]:
    """The N_TOP_GENES most variable genes of the reference counts (seurat_v3 over all reference
    cells: per-batch selection fails on batches of a few hundred cells, where loess cannot fit)."""
    import scanpy as sc

    n = min(N_TOP_GENES, ref.n_vars)
    sc.pp.highly_variable_genes(ref, flavor="seurat_v3", n_top_genes=n, subset=False)
    genes = list(ref.var_names[ref.var["highly_variable"].to_numpy()])
    ref.var.drop(columns=[c for c in ref.var.columns if c != "gene_ids"], inplace=True)
    return genes


def _train_kwargs(epochs: int, accelerator: str, label: str) -> dict:
    from lightning.pytorch.callbacks import Callback

    class EpochLog(Callback):
        def __init__(self):
            self.t0, self.every = time.monotonic(), max(1, epochs // 10)

        def on_train_epoch_end(self, trainer, pl_module):
            e = trainer.current_epoch + 1
            if e % self.every == 0 or e == epochs:
                log.info("%s: epoch %d/%d, %.0fs", label, e, epochs, time.monotonic() - self.t0)

    return {"max_epochs": int(epochs), "accelerator": accelerator, "devices": 1, "enable_progress_bar": False,
            "enable_model_summary": False, "enable_checkpointing": False, "logger": False, "callbacks": [EpochLog()]}


def train_scanvi(ref, epochs: int, accelerator: str, seed: int):
    """scVI then scANVI on the reference (X = counts, obs cell_type and batch)."""
    import scvi

    scvi.settings.seed = seed
    scvi.model.SCVI.setup_anndata(ref, batch_key="batch")
    vae = scvi.model.SCVI(ref, **SCVI_KWARGS)
    epochs = epochs or min(round(20000 / ref.n_obs * 400), 400)   # scvi-tools' default rule (get_max_epochs_heuristic)
    t = time.monotonic()
    vae.train(**_train_kwargs(epochs, accelerator, "reference scVI"))
    log.info("reference scVI: %d epochs, %.0fs", epochs, time.monotonic() - t)
    model = scvi.model.SCANVI.from_scvi_model(vae, unlabeled_category=UNLABELED, labels_key="cell_type")
    t = time.monotonic()
    model.train(n_samples_per_label=100, **_train_kwargs(SCANVI_EPOCHS, accelerator, "reference scANVI"))
    log.info("reference scANVI: %d epochs, %.0fs", SCANVI_EPOCHS, time.monotonic() - t)
    return model, {"scvi_epochs": int(epochs), "scanvi_epochs": SCANVI_EPOCHS}


def save_scanvi(model, folder: Path) -> None:
    import torch

    model.save(str(folder), overwrite=True, save_anndata=False)
    torch.save(model.module.state_dict(), folder / "weights.pt")
    init = model.init_params_
    params = {k: v for k, v in {**init["non_kwargs"], **init["kwargs"].get("model_kwargs", {})}.items() if k in INIT_KEYS}
    setup = {"format": "sc-annotate scanvi v1", "init_params": params, "var_names": list(map(str, model.adata.var_names)),
             "labels": [str(c) for c in model.adata_manager.get_state_registry("labels").categorical_mapping],
             "batches": [str(c) for c in model.adata_manager.get_state_registry("batch").categorical_mapping]}
    (folder / "setup.json").write_text(json.dumps(setup, indent=2) + "\n")


def load_scanvi(ref, folder: Path):
    """Rebuild a saved scANVI model on its reference (reference.h5ad: X counts, obs cell_type, batch)."""
    import scvi
    import torch

    for name, cap in (("setup.json", MAX_SETUP_BYTES), ("weights.pt", MAX_WEIGHTS_BYTES)):
        if (folder / name).stat().st_size > cap:
            raise ValueError(f"scanvi/{name} is larger than {cap} bytes")
    setup = json.loads((folder / "setup.json").read_text())
    if setup.get("format") != "sc-annotate scanvi v1":
        raise ValueError("scanvi/setup.json is not an sc-annotate model description")
    params = {k: v for k, v in setup["init_params"].items()
              if k in INIT_KEYS and isinstance(v, (bool, int, float, str))}
    genes = [str(g) for g in setup["var_names"]]
    missing = set(genes) - set(ref.var_names)
    if missing:
        raise ValueError(f"reference.h5ad lacks {len(missing)} of the model's genes")
    ref = ref[:, genes].copy()
    ref.obs["cell_type"] = ref.obs["cell_type"].astype(str)
    scvi.model.SCANVI.setup_anndata(ref, labels_key="cell_type", unlabeled_category=UNLABELED, batch_key="batch")
    model = scvi.model.SCANVI(ref, **params)
    labels = [str(c) for c in model.adata_manager.get_state_registry("labels").categorical_mapping]
    batches = [str(c) for c in model.adata_manager.get_state_registry("batch").categorical_mapping]
    if labels != setup["labels"] or batches != setup["batches"]:
        raise ValueError("reference.h5ad does not match the saved model's labels or batches")
    state = torch.load(folder / "weights.pt", map_location="cpu", weights_only=True)
    model.module.load_state_dict(state)
    model.is_trained_ = True
    log.info("scANVI model rebuilt from scanvi/: %d genes, %d cell types", len(genes), len(labels) - 1)
    return model


def map_query(model, query, epochs: int, accelerator: str, seed: int) -> pd.DataFrame:
    """scArches surgery of the query (X counts, obs batch = sample) into the model; class probabilities per cell."""
    import scvi

    scvi.settings.seed = seed
    query.obs["cell_type"] = UNLABELED
    n_ref = len(model.adata.var_names)
    n_shared = len(query.var_names.intersection(model.adata.var_names))
    scvi.model.SCANVI.prepare_query_anndata(query, model)
    qmodel = scvi.model.SCANVI.load_query_data(query, model, accelerator=accelerator)
    t = time.monotonic()
    qmodel.train(plan_kwargs={"weight_decay": 0.0}, **_train_kwargs(epochs, accelerator, "query scANVI"))
    log.info("query mapping: %d of the model's %d genes in the query, %d epochs, %.0fs", n_shared, n_ref, epochs, time.monotonic() - t)
    probs = qmodel.predict(soft=True)
    return probs.drop(columns=[c for c in probs.columns if c == UNLABELED])


def lognorm(adata):
    """log1p of counts normalized to 10,000 per cell (X must be counts)."""
    import scanpy as sc

    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    return adata


def train_celltypist(ref, threads: int, seed: int):
    """CellTypist model of the reference (X counts on the selected genes, obs cell_type)."""
    import celltypist

    data = lognorm(ref.copy())
    t = time.monotonic()
    # CellTypist's default one-vs-rest logistic regression (it needs scikit-learn < 1.8, which
    # removed the multi_class argument celltypist 1.7.1 passes; requirements.txt pins 1.7.2).
    model = celltypist.train(data, labels="cell_type", check_expression=False, n_jobs=threads, random_state=seed)
    log.info("CellTypist model: %d cell types, %d genes, %.0fs", len(model.cell_types), len(model.features), time.monotonic() - t)
    return model


def annotate_celltypist(model, sample) -> pd.DataFrame:
    """Probabilities of the CellTypist labels for one sample (X counts, all genes)."""
    import celltypist

    result = celltypist.annotate(lognorm(sample), model=model, majority_voting=False)
    return result.probability_matrix
