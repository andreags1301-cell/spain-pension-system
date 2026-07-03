# Legacy R implementation

`public_economics_pension_clean.R` is the **original** script, written in R for
the Public Economics report (ECON2607). It cleans the UN WPP file, computes the
ageing indicators and PAYG scenarios, and exports the appendix tables and
figures. It is kept here as the reference implementation.

The Python pipeline in [`../src/`](../src) reproduces its tables and figures.
New work should go in the Python code; this script is preserved for provenance.

## Running it

Requires R with: `tidyverse`, `readxl`, `scales`, `writexl`. The script reads the
data through an interactive file picker (`file.choose()`) — select the UN WPP
Excel file at `../data/` when prompted.
