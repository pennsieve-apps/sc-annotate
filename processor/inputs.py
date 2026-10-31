"""
Finding the inputs.

Linked layout (placement: subfolder): INPUT_DIR/cells/<sample_id>.h5ad, optionally
INPUT_DIR/reference/ (an .h5ad, or a previous sc-annotate `model` folder: reference.h5ad and
scanvi/) and INPUT_DIR/markers/markers.csv. Without links the same files are found by name
anywhere under INPUT_DIR: markers.csv by name, a reference as reference.h5ad (or an .h5ad in a
folder named reference/), every other .h5ad is a sample.

Symlinks are followed (the platform links each input entry to an upstream output), but a file
must resolve inside INPUT_DIR or inside the target of one of those platform links (an entry of
INPUT_DIR, or of a real INPUT_DIR/<port>/ folder): a link planted inside upstream data that points
anywhere else (/proc, /etc, ...) is refused.
"""
from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

log = logging.getLogger("sc-annotate")

SAMPLE_ID = re.compile(r"^[A-Za-z0-9_-]+$")
PORTS = ("cells", "reference", "markers")


@dataclass
class Reference:
    path: Path                    # the .h5ad (reference.h5ad of a model folder)
    is_model: bool                # a previous sc-annotate model folder
    scanvi_dir: Path | None       # its scanvi/ folder, when scANVI ran


@dataclass
class Inputs:
    samples: dict[str, Path]
    reference: Reference | None
    markers_csv: Path | None
    skipped: dict[str, str] = field(default_factory=dict)


def _within(path: Path, roots: list[Path]) -> bool:
    return any(path == r or path.is_relative_to(r) for r in roots)


def walk(root: Path) -> list[Path]:
    """Every regular file under root (symlinks followed), sorted; anything that resolves outside
    root and the targets of the platform's links (depth 1 and 2) is skipped with a warning."""
    base = root.resolve()
    roots = [base]
    for entry in sorted(root.iterdir()):
        if entry.is_symlink():
            roots.append(entry.resolve())
        elif entry.is_dir() and entry.name in PORTS:      # a real port folder the platform filled with links
            roots.extend(e.resolve() for e in sorted(entry.iterdir()) if e.is_symlink())
    found: list[Path] = []
    seen: set[Path] = set()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        real = Path(dirpath).resolve()
        if real in seen or not _within(real, roots):
            if real not in seen:
                log.warning("%s: links outside the input, ignored", Path(dirpath).relative_to(root))
            dirnames[:] = []
            continue
        seen.add(real)
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for f in sorted(filenames):
            p = Path(dirpath) / f
            if f.startswith("."):
                continue
            if not _within(p.resolve(), roots):
                log.warning("%s: links outside the input, ignored", p.relative_to(root))
                continue
            if p.is_file():
                found.append(p)
    return found


def _reference_in(files: list[Path]) -> Reference | None:
    h5ads = [p for p in files if p.suffix.lower() == ".h5ad"]
    if not h5ads:
        return None
    named = [p for p in h5ads if p.name == "reference.h5ad"]
    path = (named or h5ads)[0]
    if len(h5ads) > 1:
        log.warning("%d .h5ad files on the reference input; using %s", len(h5ads), path.name)
    scanvi = path.parent / "scanvi"
    has_scanvi = (scanvi / "setup.json").is_file() and (scanvi / "weights.pt").is_file()
    is_model = path.name == "reference.h5ad" and (has_scanvi or (path.parent / "signatures.csv").is_file())
    return Reference(path, is_model, scanvi if has_scanvi else None)


def discover(input_dir: Path) -> Inputs:
    files = walk(input_dir)

    def under(port: str) -> list[Path] | None:
        folder = input_dir / port
        if not folder.is_dir():
            return None
        return [p for p in files if p.is_relative_to(folder)]

    ref_files, marker_files, cell_files = under("reference"), under("markers"), under("cells")
    if ref_files is None:   # no links: reference.h5ad (with its model folder), or .h5ad files in a reference/ folder
        ref_files = [p for p in files if p.name == "reference.h5ad" or "reference" in p.relative_to(input_dir).parts[:-1]]
    reference = _reference_in(ref_files)
    ref_folder = reference.path.parent if reference else None
    markers = [p for p in (marker_files if marker_files is not None else files) if p.name.lower() == "markers.csv"]
    if len(markers) > 1:
        log.warning("%d markers.csv files; using %s", len(markers), markers[0])
    if cell_files is None:
        cell_files = [p for p in files if ref_folder is None or not p.is_relative_to(ref_folder)]

    samples: dict[str, Path] = {}
    skipped: dict[str, str] = {}
    for p in cell_files:
        if p.suffix.lower() != ".h5ad":
            continue
        sid = p.stem
        if not SAMPLE_ID.match(sid):
            skipped[p.name] = "file name is not a sample id ([A-Za-z0-9_-]+)"
        elif sid in samples:
            skipped[str(p.relative_to(input_dir))] = f"a second .h5ad for sample {sid}"
        else:
            samples[sid] = p
    return Inputs(samples, reference, markers[0] if markers else None, skipped)
