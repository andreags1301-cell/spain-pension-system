# Data

`unpopulation_dataportal_20260512100840.xlsx` — export from the **UN World
Population Prospects 2024** data portal (Online Edition): population of **Spain**,
both sexes, **median variant**, by broad age group and year. **Not committed**
(`data/` is git-ignored; re-download it from the UN portal to reproduce).

## Structure

The real table is on the **`Data`** sheet and starts after **5 header rows**.
The analysis reads seven unnamed columns in this order:

| Position | Meaning                          |
|----------|----------------------------------|
| 1        | Location id (724 = Spain)        |
| 2        | Location name (`Spain`)          |
| 3        | Year                             |
| 4        | Population aged 0-14 (persons)   |
| 5        | Population aged 15-64 (persons)  |
| 6        | Population aged 65+ (persons)    |
| 7        | Population aged 80+ (persons)    |

Figures are in **persons**. The analysis keeps the benchmark years 2025, 2050
and 2070 (see [`src/config.py`](../src/config.py)) and computes the old-age
dependency ratio and age-group shares from these columns.

## Other inputs

Pension-expenditure projections and replacement rates are **not** in this file —
they are entered by hand in [`src/config.py`](../src/config.py) from AIReF (2025),
OECD (2025), FEDEA (2024) and the EU Ageing Report (2024), as cited in the report.
