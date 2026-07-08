#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path

from isotope_analysis.config import load_analysis_config
from isotope_analysis.analysis import run_analysis
from isotope_analysis.grid import run_grid_analysis


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyse a single FLUKA simulation directory (RESNUCLEi isotopes)."
    )
    parser.add_argument("config", type=Path, help="path to analysis.yaml")
    args = parser.parse_args()

    config = load_analysis_config(args.config)
    if config.grid:
        run_grid_analysis(config)
    else:
        run_analysis(config)


if __name__ == "__main__":
    main()
