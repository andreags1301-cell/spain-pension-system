"""Build the report tables from the demographic indicators and fixed sources."""
from __future__ import annotations

import pandas as pd

from . import config

# Short column names used for the Excel / appendix tables (Table A1).
_SHORT_NAMES = {
    "location": "country", "total_population": "total_pop",
    "population_0_14": "pop_0_14", "population_15_64": "pop_15_64",
    "population_65plus": "pop_65p", "population_80plus": "pop_80p",
    "old_age_dependency_ratio": "dep_ratio", "share_0_14": "sh_0_14",
    "share_15_64": "sh_15_64", "share_65plus": "sh_65p", "share_80plus": "sh_80p",
}


def demographic_table_short(demographic: pd.DataFrame) -> pd.DataFrame:
    """Table A1 - demographic indicators with short column names."""
    return demographic.rename(columns=_SHORT_NAMES)


def payg_scenarios(demographic: pd.DataFrame) -> pd.DataFrame:
    """Table A2 - PAYG pressure: required contribution rate by adequacy scenario.

    contribution rate = benefit ratio x (dependency ratio / 100) x 100.
    """
    base = demographic[["year", "old_age_dependency_ratio"]]
    df = base.merge(config.BENEFIT_SCENARIOS, how="cross")
    df["required_contribution_rate"] = (
        df["benefit_ratio"] * df["old_age_dependency_ratio"] / 100 * 100)
    df = df.rename(columns={"old_age_dependency_ratio": "dep_ratio",
                            "benefit_ratio": "benefit",
                            "required_contribution_rate": "contrib_rate"})
    df["benefit"] = df["benefit"] * 100
    df["contrib_rate"] = df["contrib_rate"].round(1)
    return df[["year", "scenario", "dep_ratio", "benefit", "contrib_rate"]]


def build(demographic: pd.DataFrame) -> dict:
    """Return every report table keyed by name."""
    return {
        "demographic_indicators": demographic_table_short(demographic),
        "payg_scenarios": payg_scenarios(demographic),
        "pension_cost": config.PENSION_COST.copy(),
        "replacement_rates": config.REPLACEMENT_RATES.copy(),
    }
