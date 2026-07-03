"""Load and clean the UN World Population Prospects data for Spain.

Mirrors sections 3-4 of the legacy R script: read the WPP export (the real
table starts after five header rows), name the columns, keep Spain and the
three benchmark years, and compute the demographic indicators.
"""
from __future__ import annotations

import pandas as pd

from . import config

_COLUMNS = ["loc_id", "location", "year", "population_0_14",
            "population_15_64", "population_65plus", "population_80plus"]


def load_population(path=config.DATA_FILE) -> pd.DataFrame:
    """Read the WPP 'Data' sheet, name the columns and keep Spain."""
    raw = pd.read_excel(path, sheet_name="Data", skiprows=5, header=None)
    raw.columns = _COLUMNS
    for col in ["year", "population_0_14", "population_15_64",
                "population_65plus", "population_80plus"]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    return raw[raw["location"] == "Spain"]


def demographic_indicators(pop: pd.DataFrame) -> pd.DataFrame:
    """Keep the benchmark years and compute ageing indicators.

    total_population = 0-14 + 15-64 + 65+ (the 80+ group is a subset of 65+).
    old-age dependency ratio = 65+ / 15-64 x 100.
    """
    df = pop[pop["year"].isin(config.YEARS_KEEP)].copy()
    df["total_population"] = (df["population_0_14"] + df["population_15_64"]
                              + df["population_65plus"])
    df["old_age_dependency_ratio"] = df["population_65plus"] / df["population_15_64"] * 100
    df["share_0_14"] = df["population_0_14"] / df["total_population"] * 100
    df["share_15_64"] = df["population_15_64"] / df["total_population"] * 100
    df["share_65plus"] = df["population_65plus"] / df["total_population"] * 100
    df["share_80plus"] = df["population_80plus"] / df["total_population"] * 100

    # Round populations to whole persons and ratios/shares to one decimal.
    pops = ["total_population", "population_0_14", "population_15_64",
            "population_65plus", "population_80plus"]
    ratios = ["old_age_dependency_ratio", "share_0_14", "share_15_64",
              "share_65plus", "share_80plus"]
    df[pops] = df[pops].round(0)
    df[ratios] = df[ratios].round(1)

    cols = ["location", "year"] + pops + ratios
    return df[cols].reset_index(drop=True)
