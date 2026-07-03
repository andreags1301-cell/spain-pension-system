"""Appendix figures A1-A6, reproduced from the legacy R script with matplotlib."""
from __future__ import annotations

import pandas as pd
from matplotlib import pyplot as plt

from . import config

_SRC_UN = "Source: Own calculations based on UN World Population Prospects 2024, Median variant."


def _save(fig, path):
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def _line_figure(demographic, y, title, subtitle, ylabel, source, path):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(demographic["year"], demographic[y], color="black", linewidth=1.5,
            marker="o", markersize=8)
    ax.set_xticks(config.YEARS_KEEP)
    ax.set_title(f"{title}\n{subtitle}", fontsize=12)
    ax.set_xlabel("Year")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    fig.text(0.99, -0.02, source, ha="right", fontsize=7, color="#555")
    fig.tight_layout()
    return _save(fig, path)


def figure_A1(demographic, path):
    return _line_figure(
        demographic, "old_age_dependency_ratio",
        "Figure A1. Old-age dependency ratio in Spain",
        "People aged 65+ per 100 people aged 15-64",
        "Old-age dependency ratio", _SRC_UN, path)


def figure_A2(demographic, path):
    long = demographic.melt(
        id_vars="year", value_vars=["share_0_14", "share_15_64", "share_65plus"],
        var_name="age_group", value_name="share")
    labels = {"share_0_14": "0-14", "share_15_64": "15-64", "share_65plus": "65+"}
    colours = {"0-14": "#F08080", "15-64": "#2ca02c", "65+": "#4aa3df"}
    long["age_group"] = long["age_group"].map(labels)

    fig, ax = plt.subplots(figsize=(7, 5))
    years = config.YEARS_KEEP
    width = 0.25
    for i, (grp, colour) in enumerate(colours.items()):
        vals = [long[(long.year == y) & (long.age_group == grp)]["share"].iloc[0] for y in years]
        ax.bar([x + (i - 1) * width for x in range(len(years))], vals, width,
               label=grp, color=colour)
    ax.set_xticks(range(len(years)), years)
    ax.set_title("Figure A2. Age structure of Spain's population\n"
                 "Share of total population by broad age group", fontsize=12)
    ax.set_xlabel("Year")
    ax.set_ylabel("Share of total population (%)")
    ax.legend(title="Age group")
    ax.grid(True, axis="y", alpha=0.3)
    fig.text(0.99, -0.02, _SRC_UN, ha="right", fontsize=7, color="#555")
    fig.tight_layout()
    return _save(fig, path)


def figure_A3(demographic, path):
    return _line_figure(
        demographic, "share_80plus",
        "Figure A3. Population aged 80+ in Spain",
        "Share of total population aged 80 or older",
        "Share of total population (%)", _SRC_UN, path)


def figure_A4(payg, path):
    colours = {"Low adequacy": "#2ca02c", "Medium adequacy": "#4aa3df", "High adequacy": "#d62728"}
    fig, ax = plt.subplots(figsize=(7, 5))
    for scenario, colour in colours.items():
        sub = payg[payg["scenario"] == scenario]
        ax.plot(sub["year"], sub["contrib_rate"], color=colour, linewidth=1.5,
                marker="o", markersize=8, label=scenario)
    ax.set_xticks(config.YEARS_KEEP)
    ax.set_title("Figure A4. PAYG pension pressure under adequacy scenarios\n"
                 "Required contribution rate implied by pension generosity and ageing",
                 fontsize=12)
    ax.set_xlabel("Year")
    ax.set_ylabel("Required contribution rate (%)")
    ax.legend(title="Scenario")
    ax.grid(True, alpha=0.3)
    fig.text(0.99, -0.02, "Source: Own calculations based on UN World Population Prospects 2024.",
             ha="right", fontsize=7, color="#555")
    fig.tight_layout()
    return _save(fig, path)


def figure_A5(pension_cost, path):
    years = sorted(pension_cost["year"].unique())
    sources = list(dict.fromkeys(pension_cost["source"]))
    colours = ["#F08080", "#2ca02c", "#4aa3df", "#b07cd6"]
    fig, ax = plt.subplots(figsize=(8, 5))
    width = 0.2
    for i, source in enumerate(sources):
        xs, ys = [], []
        for j, year in enumerate(years):
            row = pension_cost[(pension_cost.source == source) & (pension_cost.year == year)]
            if not row.empty:
                x = j + (i - 1.5) * width
                xs.append(x)
                ys.append(row["pension_gdp"].iloc[0])
        bars = ax.bar(xs, ys, width, label=source, color=colours[i % len(colours)])
        for rect, v in zip(bars, ys):
            ax.text(rect.get_x() + rect.get_width() / 2, v + 0.15, f"{v}%",
                    ha="center", fontsize=8)
    ax.set_xticks(range(len(years)), years)
    ax.set_ylim(0, 19)
    ax.set_title("Figure A5. Projected public pension expenditure in Spain\n"
                 "Pension expenditure as a share of GDP under existing projections",
                 fontsize=12)
    ax.set_xlabel("Year")
    ax.set_ylabel("Pension expenditure (% of GDP)")
    ax.legend(title="Projection", fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    fig.text(0.99, -0.02, "Sources: AIReF 2025, OECD 2025, FEDEA 2024, European Commission Ageing Report 2024.",
             ha="right", fontsize=7, color="#555")
    fig.tight_layout()
    return _save(fig, path)


def figure_A6(replacement, path):
    colours = {"OECD average": "#F08080", "Spain": "#4aa3df"}
    order = ["OECD average", "Spain"]
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, grp in enumerate(order):
        v = replacement[replacement.country_group == grp]["gross_replacement_rate"].iloc[0]
        ax.bar(i, v, 0.6, color=colours[grp])
        ax.text(i, v + 1, f"{v:.0f}%", ha="center", fontsize=11)
    ax.set_xticks(range(len(order)), order)
    ax.set_ylim(0, 90)
    ax.set_title("Figure A6. Gross pension replacement rate\n"
                 "Spain compared with the OECD average", fontsize=12)
    ax.set_ylabel("Gross replacement rate (%)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.text(0.99, -0.02, "Source: OECD Pensions at a Glance 2025.",
             ha="right", fontsize=7, color="#555")
    fig.tight_layout()
    return _save(fig, path)


def save_all(demographic, tables, figures_dir=config.FIGURES_DIR,
             assets_dir=config.ASSETS_DIR):
    figures_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)
    saved = [
        figure_A1(demographic, figures_dir / "figure_A1_old_age_dependency_ratio.png"),
        figure_A2(demographic, figures_dir / "figure_A2_age_structure.png"),
        figure_A3(demographic, figures_dir / "figure_A3_population_80plus.png"),
        figure_A4(tables["payg_scenarios"], figures_dir / "figure_A4_payg_scenarios.png"),
        figure_A5(tables["pension_cost"], figures_dir / "figure_A5_pension_expenditure_gdp.png"),
        figure_A6(tables["replacement_rates"], figures_dir / "figure_A6_replacement_rate.png"),
    ]
    # Headline figure for the README.
    figure_A1(demographic, assets_dir / "figure_A1_old_age_dependency_ratio.png")
    return saved
