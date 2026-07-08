from __future__ import annotations
import shutil
from pathlib import Path


def discover_combos(results_dir: Path, units: list[int]) -> list[Path]:
    """Immediate subdirs of results_dir that contain a raw *.<unit> file anywhere inside."""
    results_dir = Path(results_dir)
    combos: list[Path] = []
    for sub in sorted(p for p in results_dir.iterdir() if p.is_dir()):
        if any(next(iter(sub.glob(f"**/*.{u}")), None) is not None for u in units):
            combos.append(sub)
    return combos


def collect_combo(combo_dir: Path, units: list[int]) -> Path:
    """Symlink (or copy) every run's raw *.<unit> files into <combo>/_collected/."""
    combo_dir = Path(combo_dir)
    collected = combo_dir / "_collected"
    if collected.exists():
        shutil.rmtree(collected)
    collected.mkdir(parents=True)
    for u in units:
        for f in sorted(combo_dir.glob(f"**/*.{u}")):
            if f.is_dir() or collected in f.parents:
                continue
            dest = collected / f.name
            if dest.exists():
                dest = collected / f"{f.parent.name}__{f.name}"
            try:
                dest.symlink_to(f.resolve())
            except OSError:
                shutil.copy2(f, dest)
    return collected
