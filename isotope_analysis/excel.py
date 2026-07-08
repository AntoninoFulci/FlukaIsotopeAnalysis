from __future__ import annotations
from pathlib import Path

import pandas as pd

from .physics import isotope_symbol


def write_activity_workbook(
    rows: list[dict],
    isotopes: dict[int, int],
    volume: float,
    output_path: Path,
) -> None:
    rows_sorted = sorted(rows, key=lambda r: r["_tdecay_s"])
    syms = [isotope_symbol(z, a) for z, a in sorted(isotopes.items())]

    records: list[dict] = []
    for r in rows_sorted:
        rec: dict = {"CoolingTime": r["CoolingTime"]}
        for sym in syms:
            bq = r.get(f"{sym} (Bq)", 0.0)
            rec[f"{sym} (Bq)"] = bq
            rec[f"{sym} (Bq/cm³)"] = bq / volume if volume else 0.0
            rec[f"{sym} (% Error)"] = r.get(f"{sym} (% Error)", 0.0)
            rec[f"{sym} (µg)"] = r.get(f"{sym} (µg)", 0.0)
        records.append(rec)

    df = pd.DataFrame(records)
    with pd.ExcelWriter(str(output_path), engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Activity", index=False)


def write_summary_workbook(
    rows: list[dict],
    isotopes: dict[int, int],
    volume: float,
    output_path: Path,
) -> None:
    rows_sorted = sorted(rows, key=lambda r: (r.get("Configuration", ""), r["_tdecay_s"]))
    syms = [isotope_symbol(z, a) for z, a in sorted(isotopes.items())]

    records: list[dict] = []
    for r in rows_sorted:
        rec: dict = {"Configuration": r.get("Configuration", ""), "CoolingTime": r["CoolingTime"]}
        for sym in syms:
            rec[f"{sym} (Bq)"] = r.get(f"{sym} (Bq)", 0.0)
            rec[f"{sym} (µg)"] = r.get(f"{sym} (µg)", 0.0)
        records.append(rec)

    df = pd.DataFrame(records)
    with pd.ExcelWriter(str(output_path), engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Summary", index=False)
