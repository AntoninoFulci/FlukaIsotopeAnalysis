from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class AnalysisConfig:
    directory: Path
    units: list[int]
    isotopes: list[tuple[int, int]]
    volume: float
    executable: str = "usrsuw"
    output: str = "isotopes.xlsx"
    grid: bool = False
    summary_output: str = "isotopes_summary.xlsx"


def _parse_isotopes(raw: dict) -> list[tuple[int, int]]:
    """Accept `Z: A` (single) or `Z: [A1, A2, ...]` (multiple per element).

    Returns a flat, sorted list of unique (Z, A) pairs.
    """
    pairs: list[tuple[int, int]] = []
    for z, a in raw.items():
        zi = int(z)
        alist = a if isinstance(a, (list, tuple)) else [a]
        for ai in alist:
            pair = (zi, int(ai))
            if pair not in pairs:
                pairs.append(pair)
    return sorted(pairs)


def load_analysis_config(path: Path) -> AnalysisConfig:
    raw = yaml.safe_load(Path(path).read_text())
    if not raw or "analysis" not in raw:
        raise ValueError("config must contain a top-level 'analysis' section")
    a = raw["analysis"]

    for field in ("directory", "units", "volume", "isotopes"):
        if field not in a:
            raise ValueError(f"analysis.{field} is required")

    directory = Path(a["directory"])
    if not directory.exists():
        raise ValueError(f"analysis.directory does not exist: {directory}")

    units = [int(u) for u in a["units"]]
    if not units:
        raise ValueError("analysis.units must list at least one unit number")

    isotopes = _parse_isotopes(a["isotopes"])
    if not isotopes:
        raise ValueError("analysis.isotopes must list at least one Z: A pair")

    return AnalysisConfig(
        directory=directory,
        units=units,
        isotopes=isotopes,
        volume=float(a["volume"]),
        executable=a.get("executable", "usrsuw"),
        output=a.get("output", "isotopes.xlsx"),
        grid=bool(a.get("grid", False)),
        summary_output=a.get("summary_output", "isotopes_summary.xlsx"),
    )
