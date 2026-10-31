"""The synthetic fixture through every mode and both input layouts, model reuse, the marker
tables, input safety and parameter handling. No Docker."""
from __future__ import annotations

import csv
import json
import os
import shutil
from pathlib import Path

import anndata as ad
import numpy as np
import pytest

from processor import main as app
from processor import markers as M
from tests.make_fixture import PLANTED, make_fixture

PORTS = ["annotation", "cells", "labels", "model"]


@pytest.fixture(scope="session")
def fixture_root(tmp_path_factory) -> dict[str, Path]:
    return make_fixture(tmp_path_factory.mktemp("fixture"))


def run(input_dir: Path, output_dir: Path, monkeypatch, **params) -> int:
    monkeypatch.setenv("INPUT_DIR", str(input_dir))
    monkeypatch.setenv("OUTPUT_DIR", str(output_dir))
    monkeypatch.setenv("MPLCONFIGDIR", "/tmp/matplotlib")
    for name in app.PARAMETERS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("THREADS", "2")
    for name, value in params.items():
        monkeypatch.setenv(name, str(value))
    return app.main()


def rows(path: Path) -> list[dict[str, str]]:
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def hit_rate(out: Path, root: Path) -> float:
    truth = {r["obs_id"]: r["cell_type"] for r in rows(root / "truth.csv")}
    labels = rows(out / "labels" / "labels.csv")
    return float(np.mean([r["cell_type"] == truth[r["obs_id"]] for r in labels]))


def linked_input(tmp_path: Path, root: Path, **ports: Path) -> Path:
    """An INPUT_DIR as the platform builds it: one folder per port, entries symlinked."""
    inp = tmp_path / "input"
    for port, target in {"cells": root / "cells", **ports}.items():
        (inp / port).mkdir(parents=True)
        for p in sorted(Path(target).iterdir()):
            (inp / port / p.name).symlink_to(p)
    return inp


@pytest.mark.parametrize("layout", ["linked", "flat"])
def test_markers_mode(fixture_root, tmp_path, monkeypatch, layout):
    root = fixture_root[layout]
    out = tmp_path / "out"
    assert run(root, out, monkeypatch, MODE="markers") == 0
    assert sorted(p.name for p in out.iterdir()) == PORTS
    labels = rows(out / "labels" / "labels.csv")
    assert list(labels[0]) == ["sample_id", "obs_id", "cluster", "cell_type", "cell_type_score"]
    assert len(labels) == 1500
    assert hit_rate(out, fixture_root["linked"]) >= 0.95
    assert {"summary.json", "confusion.csv", "clusters.csv", "marker_scores.csv", "cell_types_by_sample.csv",
            "umap_cell_type.png", "cell_types_by_sample.png", "score_histogram.png"} <= {p.name for p in (out / "annotation").iterdir()}
    assert {"reference.h5ad", "signatures.csv", "reference_summary.csv"} <= {p.name for p in (out / "model").iterdir()}
    for port in PORTS:
        prov = json.loads((out / port / "provenance.json").read_text())
        assert {"app", "version", "tools", "parameters", "inputs", "started", "finished", "samples", "peak_rss_mb",
                "citations"} <= set(prov)
        assert all("doi" in c and "text" in c for c in prov["citations"])
    summary = json.loads((out / "annotation" / "summary.json").read_text())
    assert summary["mode"] == "markers" and summary["marker_sets"]["source"] == "markers.csv"


def test_cells_keep_the_contract(fixture_root, tmp_path, monkeypatch):
    out = tmp_path / "out"
    assert run(fixture_root["linked"], out, monkeypatch, MODE="markers") == 0
    before = ad.read_h5ad(fixture_root["linked"] / "cells" / "s2.h5ad")
    after = ad.read_h5ad(out / "cells" / "s2.h5ad")
    assert list(after.obs_names) == list(before.obs_names)
    assert list(after.var_names) == list(before.var_names)
    assert {"cell_type", "cell_type_score", "cell_type_source"} <= set(after.obs.columns)
    assert set(after.obs["cell_type_source"]) == {"markers"}
    assert after.obs["cell_type_score"].between(0, 1).all()
    assert "annotation" in after.uns["pennsieve"] and "counts" in after.layers and "X_umap" in after.obsm
    ref = ad.read_h5ad(out / "model" / "reference.h5ad")
    assert set(ref.obs["cell_type"]) == set(PLANTED) and ref.X.max() > 1 and np.allclose(ref.X.data, np.round(ref.X.data))


def test_reference_celltypist(fixture_root, tmp_path, monkeypatch):
    out = tmp_path / "out"
    assert run(fixture_root["linked"], out, monkeypatch, REFERENCE_BATCH_COLUMN="donor") == 0
    summary = json.loads((out / "annotation" / "summary.json").read_text())
    assert summary["mode"] == "reference" and summary["method"] == "celltypist" and summary["gene_match"] == "ensembl"
    assert hit_rate(out, fixture_root["linked"]) >= 0.9
    assert not (out / "model" / "scanvi").exists()


def test_reference_scanvi_and_model_reuse(fixture_root, tmp_path, monkeypatch):
    root = fixture_root["linked"]
    first = tmp_path / "first"
    assert run(root, first, monkeypatch, METHOD="scanvi", MAX_EPOCHS=30, QUERY_EPOCHS=30, REFERENCE_BATCH_COLUMN="donor") == 0
    assert hit_rate(first, root) >= 0.85
    assert {"model.pt", "weights.pt", "setup.json"} <= {p.name for p in (first / "model" / "scanvi").iterdir()}

    inp = linked_input(tmp_path, root, reference=first / "model")
    second = tmp_path / "second"
    assert run(inp, second, monkeypatch, METHOD="scanvi", QUERY_EPOCHS=30) == 0
    assert hit_rate(second, root) >= 0.85
    after = ad.read_h5ad(second / "cells" / "s1.h5ad")
    assert set(after.obs["cell_type_source"]) == {"model"}
    assert json.loads((second / "annotation" / "summary.json").read_text())["training"]["reused"]


def test_builtin_marker_sets():
    names = M.builtin_names()
    assert set(names) == {"broad", "drg-human", "knee-human"}
    for name in names:
        sets = M.read_markers_csv(M.BUILTIN_DIR / f"{name}.csv")
        assert len(sets) >= 10
        genes = [g for s in sets for g in s.weights]
        assert len(genes) == len(set(genes)), f"{name}: a gene is listed for two cell types"
        assert all(2 <= len(s.weights) <= 8 for s in sets)
        with open(M.BUILTIN_DIR / f"{name}.csv", newline="") as fh:
            assert all(r["source"] for r in csv.DictReader(fh))


def test_markers_csv_weights(tmp_path):
    path = tmp_path / "markers.csv"
    path.write_text("cell_type,gene,weight\nA,G1,2\nA,G2,1\nA,G3,-1\nB,G4,1\nB,G5,0\n")
    sets = {s.cell_type: s.weights for s in M.read_markers_csv(path)}
    assert sets == {"A": {"G1": 2.0, "G2": 1.0, "G3": -1.0}, "B": {"G4": 1.0}}
    path.write_text("cell_type,gene,weight\nA,G1,heavy\n")
    with pytest.raises(ValueError):
        M.read_markers_csv(path)


def test_negative_marker_lowers_the_score(fixture_root):
    a = ad.read_h5ad(fixture_root["linked"] / "cells" / "s1.h5ad")
    plain = M.MarkerSet("T cell", {"CD3E": 1, "CD2": 1})
    negative = M.MarkerSet("T cell", {"CD3E": 1, "CD2": 1, "CD68": -1})
    used, _ = M.resolve([plain, negative], a.var_names, 2)
    s1 = M.score_sample(a, [used[0]], 0)["T cell"]
    s2 = M.score_sample(a, [used[1]], 0)["T cell"]
    macrophages = a.obs["cluster"].astype(str).to_numpy() == "C05"
    assert s2[macrophages].mean() < s1[macrophages].mean()


def test_symlink_out_of_the_input_is_ignored(fixture_root, tmp_path, monkeypatch):
    secret = tmp_path / "elsewhere"
    secret.mkdir()
    shutil.copy(fixture_root["linked"] / "cells" / "s1.h5ad", secret / "stolen.h5ad")
    inp = linked_input(tmp_path, fixture_root["linked"], markers=fixture_root["linked"] / "markers")
    real_cells = Path(os.path.realpath(inp / "cells" / "s1.h5ad")).parent
    planted = tmp_path / "planted"
    shutil.copytree(real_cells, planted)
    (planted / "stolen.h5ad").symlink_to(secret / "stolen.h5ad")
    shutil.rmtree(inp / "cells")
    (inp / "cells").symlink_to(planted)
    out = tmp_path / "out"
    assert run(inp, out, monkeypatch, MODE="markers") == 0
    assert not (out / "cells" / "stolen.h5ad").exists()
    assert len(rows(out / "labels" / "labels.csv")) == 1500


@pytest.mark.parametrize("params", [{"MODE": "guess"}, {"METHOD": "svm"}, {"MARKER_SET": "liver"}, {"MIN_SCORE": "2"},
                                    {"MARGIN": "-1"}, {"MAX_CELLS_PER_TYPE": "3"}, {"QUERY_EPOCHS": "0"}, {"SEED": "x"}])
def test_bad_parameters_exit_2(fixture_root, tmp_path, monkeypatch, params):
    assert run(fixture_root["linked"], tmp_path / "out", monkeypatch, **params) == 2


def test_no_usable_input_exits_1(fixture_root, tmp_path, monkeypatch):
    empty = tmp_path / "empty"
    empty.mkdir()
    assert run(empty, tmp_path / "out", monkeypatch) == 1
    cells_only = linked_input(tmp_path, fixture_root["linked"])
    assert run(cells_only, tmp_path / "out2", monkeypatch, MODE="reference") == 1


def test_markers_mode_without_markers_is_a_parameter_error(fixture_root, tmp_path, monkeypatch):
    cells_only = linked_input(tmp_path, fixture_root["linked"])
    assert run(cells_only, tmp_path / "out", monkeypatch, MARKER_SET="none") == 2
