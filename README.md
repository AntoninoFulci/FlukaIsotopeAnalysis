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

(Optional: `pip install -e .` still works if you want it on your path.)

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

## Library use

```python
from isotope_analysis.reader import read_resnuclei_file
from isotope_analysis.physics import isotope_symbol, half_life
```
