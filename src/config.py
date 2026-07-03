"""Project configuration: paths, benchmark years and the manually-entered data.

Public Economics project on Spain's pension system and ageing. Demographic
indicators come from UN World Population Prospects 2024 (median variant);
the pension-expenditure and replacement-rate values are entered by hand from
the official sources cited in the report.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

# --- Paths -------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data" / "unpopulation_dataportal_20260512100840.xlsx"
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"
ASSETS_DIR = ROOT / "assets"

# --- Benchmark years used throughout the report ------------------------------
# 2025 = current, 2050 = baby-boom retirement peak, 2070 = long-term horizon.
YEARS_KEEP = [2025, 2050, 2070]

# --- PAYG simulation: benefit-ratio (adequacy) scenarios ---------------------
# Required contribution rate = benefit ratio x old-age dependency ratio.
BENEFIT_SCENARIOS = pd.DataFrame({
    "scenario": ["Low adequacy", "Medium adequacy", "High adequacy"],
    "benefit_ratio": [0.40, 0.50, 0.60],
})

# --- Public pension expenditure projections (% of GDP) -----------------------
# Manually entered from AIReF 2025, OECD 2025, FEDEA 2024, EU Ageing Report 2024.
PENSION_COST = pd.DataFrame({
    "source": ["AIReF 2025", "AIReF 2025", "OECD 2025", "OECD 2025",
               "FEDEA 2024", "FEDEA 2024", "EU Ageing Report 2024", "EU Ageing Report 2024"],
    "year": [2022, 2050, 2023, 2050, 2023, 2050, 2022, 2070],
    "period": ["Current", "2050", "Current", "2050", "Current", "2050", "Current", "2070"],
    "pension_gdp": [12.7, 16.1, 12.9, 16.1, 12.9, 17.1, 13.1, 16.7],
})

# --- Gross replacement rate: Spain vs OECD (OECD Pensions at a Glance 2025) ---
REPLACEMENT_RATES = pd.DataFrame({
    "country_group": ["Spain", "OECD average"],
    "gross_replacement_rate": [80.0, 52.0],
})
