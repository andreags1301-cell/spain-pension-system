"""End-to-end pipeline: build the pension-report tables and appendix figures.

Run from the repository root with the project environment active:

    python -m src.main

Reproduces the legacy R script: clean the UN WPP data for Spain, compute the
ageing indicators and the PAYG simulation, and export the appendix tables
(CSV + one Excel workbook) and figures A1-A6.
"""
from __future__ import annotations

import warnings

import pandas as pd

from . import analysis, config, data_prep, plots

warnings.simplefilter("ignore")

_RULE = "=" * 64


def _header(title: str) -> None:
    print(f"\n{_RULE}\n{title}\n{_RULE}")


def main() -> None:
    # 1. Data + indicators -------------------------------------------------
    demographic = data_prep.demographic_indicators(data_prep.load_population())
    tables = analysis.build(demographic)

    _header("TABLE A1 - Demographic (ageing) indicators")
    print(tables["demographic_indicators"].to_string(index=False))
    _header("TABLE A2 - PAYG scenarios")
    print(tables["payg_scenarios"].to_string(index=False))
    _header("Pension expenditure (% GDP) and replacement rates")
    print(tables["pension_cost"].to_string(index=False))
    print()
    print(tables["replacement_rates"].to_string(index=False))

    # 2. Persist tables ----------------------------------------------------
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)
    tables["demographic_indicators"].to_csv(
        config.TABLES_DIR / "table_A1_demographic_indicators.csv", index=False)
    tables["payg_scenarios"].to_csv(
        config.TABLES_DIR / "table_A2_payg_scenarios.csv", index=False)
    tables["pension_cost"].to_csv(
        config.TABLES_DIR / "supporting_pension_cost.csv", index=False)
    tables["replacement_rates"].to_csv(
        config.TABLES_DIR / "supporting_replacement_rates.csv", index=False)

    # One Excel workbook with every table on its own sheet.
    with pd.ExcelWriter(config.TABLES_DIR / "spain_pension_tables.xlsx") as writer:
        tables["demographic_indicators"].to_excel(writer, sheet_name="demographic_indicators", index=False)
        tables["payg_scenarios"].to_excel(writer, sheet_name="payg_scenarios", index=False)
        tables["pension_cost"].to_excel(writer, sheet_name="pension_cost", index=False)
        tables["replacement_rates"].to_excel(writer, sheet_name="replacement_rates", index=False)

    # 3. Figures -----------------------------------------------------------
    saved = plots.save_all(demographic, tables)

    _header("OUTPUTS WRITTEN")
    for path in sorted(config.TABLES_DIR.glob("*")):
        print(f"  {path.relative_to(config.ROOT)}")
    for path in saved:
        print(f"  {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
