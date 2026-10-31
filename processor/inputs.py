"""
Finding the inputs (through processor/safe_inputs.py, the shared walker of the workflow).

Linked layout (placement: subfolder): INPUT_DIR/cells/<sample_id>.h5ad, optionally
INPUT_DIR/reference/ (an .h5ad, or a previous sc-annotate `model` folder: reference.h5ad and
scanvi/) and INPUT_DIR/markers/markers.csv. Without links the same files are found by name
anywhere under INPUT_DIR: markers.csv by name, a reference as reference.h5ad (or an .h5ad in a
folder named reference/), every other .h5ad is a sample. Every .h5ad is checked with check_h5
(no external links, external storage or virtual datasets) before it is used.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from processor.safe_inputs import InputDir, UnsafeInput

log = logging.getLogger("sc-annotate")

SAMPLE_ID = re.compile(r"^[A-Za-z0-9_-]+$")


@dataclass
class Reference:
    path: Path                    # the .h5ad (reference.h5ad of a model folder)
    is_model: bool                # a previous sc-annotate model folder
    scanvi: dict[str, Path] | None = None    # {"setup.json": ..., "weights.pt": ...} when scANVI ran


@dataclass
class Inputs:
    input_dir: InputDir
    samples: dict[str, Path]
    reference: Reference | None
    markers_csv: Path | None
    skipped: dict[str, str] = field(default_factory=dict)


def _reference_in(files: list[Path], skipped: dict[str, str], inp: InputDir) -> Reference | None:
    h5ads = []
    for p in files:
        if p.suffix.lower() == ".h5ad":
            try:
                inp.check_h5(p)
                h5ads.append(p)
            except UnsafeInput as exc:
                skipped[inp.rel(p)] = str(exc)
    if not h5ads:
        return None
    named = [p for p in h5ads if p.name == "reference.h5ad"]
    path = (named or h5ads)[0]
    if len(h5ads) > 1:
        log.warning("%d .h5ad files on the reference input; using %s", len(h5ads), path.name)
    scanvi = {p.name: p for p in files if p.parent == path.parent / "scanvi" and p.name in ("setup.json", "weights.pt")}
    has_scanvi = len(scanvi) == 2
    is_model = path.name == "reference.h5ad" and (has_scanvi or any(p == path.parent / "signatures.csv" for p in files))
    return Reference(path, is_model, scanvi if has_scanvi else None)


def discover(input_dir: Path) -> Inputs:
    inp = InputDir(input_dir)
    files = inp.walk()
    skipped: dict[str, str] = {}

    def under(port: str) -> list[Path] | None:
        folder = input_dir / port
        if not folder.is_dir():
            return None
        return [p for p in files if p.is_relative_to(folder)]

    ref_files, marker_files, cell_files = under("reference"), under("markers"), under("cells")
    if ref_files is None:   # no links: reference.h5ad (with its model folder), or files in a reference/ folder
        ref_files = [p for p in files if p.name == "reference.h5ad" or "reference" in p.relative_to(input_dir).parts[:-1]]
    reference = _reference_in(ref_files, skipped, inp)
    ref_folder = reference.path.parent if reference else None
    markers = [p for p in (marker_files if marker_files is not None else files) if p.name.lower() == "markers.csv"]
    if len(markers) > 1:
        log.warning("%d markers.csv files; using %s", len(markers), inp.rel(markers[0]))
    if cell_files is None:
        cell_files = [p for p in files if ref_folder is None or not p.is_relative_to(ref_folder)]

    samples: dict[str, Path] = {}
    for p in cell_files:
        if p.suffix.lower() != ".h5ad":
            continue
        sid = p.stem
        if not SAMPLE_ID.match(sid):
            skipped[inp.rel(p)] = "file name is not a sample id ([A-Za-z0-9_-]+)"
        elif sid in samples:
            skipped[inp.rel(p)] = f"a second .h5ad for sample {sid}"
        else:
            try:
                inp.check_h5(p)
                samples[sid] = p
            except UnsafeInput as exc:
                skipped[inp.rel(p)] = str(exc)
    return Inputs(inp, samples, reference, markers[0] if markers else None, skipped)
