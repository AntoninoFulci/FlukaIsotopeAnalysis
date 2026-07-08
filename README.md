# FlukaIsotopeAnalysis

Standalone isotope/activation analysis for FLUKA `RESNUCLEi` output.

Reads raw `RESNUCLEi` binaries (`fort.21`, …) and/or already-processed `.rnc`
files (e.g. from FLAIR), computes per-isotope activity (Bq), error, and mass
(µg), and writes an Excel workbook — for a single simulation directory.

## Setup (no installation required)

No `pip install` of this project is needed — run the script directly. Just make
the third-party libraries available:

```bash
pip install pyyaml pandas openpyxl periodictable radioactivedecay
```

## Usage

```bash
python run_analysis.py analysis.yaml
```

`analysis.yaml`:

```yaml
analysis:
  directory: /path/to/simulation
  units: [21, 22, 23]
  executable: usrsuw       # optional, default usrsuw
  volume: 1000             # cm³
  isotopes:                # Z: A
    31: 70
    30: 69
  output: isotopes.xlsx    # optional
```

For each unit: an existing `*<unit>*.rnc` is used as-is; otherwise raw
`*.<unit>`/`fort.<unit>` files are processed with `executable` into
`merged_<unit>.rnc`. Output: an `Activity` sheet, one row per cooling time.

### Grid mode

Point the tool at a whole fluka-grid-search `results/` folder and analyse every
parameter combination at once. Enable it with `grid: true`:

```yaml
analysis:
  directory: /path/to/results   # the grid search's results/ folder
  grid: true
  units: [21, 22, 23]
  volume: 1000
  isotopes: { 31: 70, 30: 69 }
  output: isotopes.xlsx                  # per-combo workbook (in each combo folder)
  summary_output: isotopes_summary.xlsx  # aggregated workbook (in results/)
```

For each combo folder it collects the runs' raw RESNUCLEi files into
`<combo>/_collected/`, merges them with `usrsuw`, writes a per-combo `isotopes.xlsx`,
and finally an aggregated `isotopes_summary.xlsx` (one row per combo × cooling time)
in the `results/` folder.

## Library use

```python
from isotope_analysis.reader import read_resnuclei_file
from isotope_analysis.physics import isotope_symbol, half_life
```
