# ============================================================
# PUBLIC ECONOMICS PROJECT - SPAIN PENSION REFORM AND AGEING
# Clean R script for tables and appendix figures
# Course: Public Economics ECON2607 - UCLouvain
# Author: Andrea Garrido
# ============================================================

# Notes:
# - This script creates the tables and figures used in the report appendix.
# - Population data source: UN World Population Prospects 2024, Median variant.
# - Pension expenditure and replacement-rate values are entered manually from
#   AIReF, OECD, FEDEA, and European Commission sources cited in the report.

# 0. Clear environment ---------------------------------------------------

rm(list = ls())

# 1. Packages ------------------------------------------------------------

# Run this line only once if packages are not installed:
# install.packages(c("tidyverse", "readxl", "scales", "writexl"))

library(tidyverse)
library(readxl)
library(scales)
library(writexl)

# 2. Project folders -----------------------------------------------------

# All outputs are saved in these folders.
dir.create("outputs", showWarnings = FALSE)
dir.create("figures", showWarnings = FALSE)

# 3. Import UN population data ------------------------------------------

# Option A: choose the downloaded UN Excel file manually.
# This is the easiest option if the file is not stored in the project folder.
file_path <- file.choose()

# Option B: use a reproducible relative path instead.
# Uncomment and adapt this line if you keep the UN file inside a data folder.
# file_path <- "data/un_wpp_spain_population.xlsx"

# Check sheet names if needed.
print(excel_sheets(file_path))

# The downloaded UN Excel file contains several header rows.
# The relevant table starts after the first 5 rows.
pop_raw <- read_excel(
  path = file_path,
  sheet = "Data",
  skip = 5,
  col_names = FALSE
)

# Rename columns manually.
# These columns correspond to location, year, and broad age groups.
names(pop_raw) <- c(
  "loc_id",
  "location",
  "year",
  "population_0_14",
  "population_15_64",
  "population_65plus",
  "population_80plus"
)

# 4. Clean population data ----------------------------------------------

pop <- pop_raw %>%
  mutate(
    year = as.numeric(year),
    population_0_14 = as.numeric(population_0_14),
    population_15_64 = as.numeric(population_15_64),
    population_65plus = as.numeric(population_65plus),
    population_80plus = as.numeric(population_80plus)
  ) %>%
  filter(location == "Spain")

# Key years used in the report.
years_keep <- c(2025, 2050, 2070)

pop_3years <- pop %>%
  filter(year %in% years_keep) %>%
  mutate(
    total_population = population_0_14 + population_15_64 + population_65plus,
    old_age_dependency_ratio = population_65plus / population_15_64 * 100,
    share_0_14 = population_0_14 / total_population * 100,
    share_15_64 = population_15_64 / total_population * 100,
    share_65plus = population_65plus / total_population * 100,
    share_80plus = population_80plus / total_population * 100
  )

# Full demographic table for the appendix.
demographic_table <- pop_3years %>%
  select(
    location,
    year,
    total_population,
    population_0_14,
    population_15_64,
    population_65plus,
    population_80plus,
    old_age_dependency_ratio,
    share_0_14,
    share_15_64,
    share_65plus,
    share_80plus
  ) %>%
  mutate(
    across(
      c(
        total_population,
        population_0_14,
        population_15_64,
        population_65plus,
        population_80plus
      ),
      ~ round(.x, 0)
    ),
    across(
      c(
        old_age_dependency_ratio,
        share_0_14,
        share_15_64,
        share_65plus,
        share_80plus
      ),
      ~ round(.x, 1)
    )
  )

# Same table with short column names for Excel/appendix use.
demographic_table_short <- demographic_table %>%
  rename(
    country = location,
    total_pop = total_population,
    pop_0_14 = population_0_14,
    pop_15_64 = population_15_64,
    pop_65p = population_65plus,
    pop_80p = population_80plus,
    dep_ratio = old_age_dependency_ratio,
    sh_0_14 = share_0_14,
    sh_15_64 = share_15_64,
    sh_65p = share_65plus,
    sh_80p = share_80plus
  )

print(demographic_table_short)

# 5. PAYG pension scenario simulation -----------------------------------

# Simple PAYG formula used in the report:
# required contribution rate = benefit ratio * old-age dependency ratio
# This is a pressure exercise, not a legal forecast of Spanish contribution rates.

benefit_scenarios <- tibble(
  scenario = c("Low adequacy", "Medium adequacy", "High adequacy"),
  benefit_ratio = c(0.40, 0.50, 0.60)
)

payg_scenarios <- demographic_table %>%
  select(year, old_age_dependency_ratio) %>%
  crossing(benefit_scenarios) %>%
  mutate(
    dependency_ratio_decimal = old_age_dependency_ratio / 100,
    required_contribution_rate = benefit_ratio * dependency_ratio_decimal * 100
  )

payg_table <- payg_scenarios %>%
  select(
    year,
    scenario,
    old_age_dependency_ratio,
    benefit_ratio,
    required_contribution_rate
  ) %>%
  mutate(
    benefit_ratio = benefit_ratio * 100,
    required_contribution_rate = round(required_contribution_rate, 1)
  ) %>%
  rename(
    dep_ratio = old_age_dependency_ratio,
    benefit = benefit_ratio,
    contrib_rate = required_contribution_rate
  )

print(payg_table)

# 6. Existing pension expenditure projections ---------------------------

# Values manually entered from sources cited in the report:
# - AIReF 2025: pension expenditure rule / long-term sustainability report
# - OECD 2025: OECD Economic Survey Spain and Pensions at a Glance
# - FEDEA 2024: analysis of Spanish pension reform and sustainability
# - European Commission 2024: Ageing Report

pension_cost <- tibble(
  source = c(
    "AIReF 2025",
    "AIReF 2025",
    "OECD 2025",
    "OECD 2025",
    "FEDEA 2024",
    "FEDEA 2024",
    "EU Ageing Report 2024",
    "EU Ageing Report 2024"
  ),
  year = c(
    2022, 2050,
    2023, 2050,
    2023, 2050,
    2022, 2070
  ),
  period = c(
    "Current", "2050",
    "Current", "2050",
    "Current", "2050",
    "Current", "2070"
  ),
  pension_gdp = c(
    12.7, 16.1,
    12.9, 16.1,
    12.9, 17.1,
    13.1, 16.7
  )
)

print(pension_cost)

# 7. Replacement rates ---------------------------------------------------

# Source: OECD Pensions at a Glance 2025.
# Indicator: gross pension replacement rate for a full-career average-wage worker.

replacement_rates <- tibble(
  country_group = c("Spain", "OECD average"),
  gross_replacement_rate = c(80.0, 52.0)
)

print(replacement_rates)

# 8. Save tables ---------------------------------------------------------

write_xlsx(
  list(
    demographic_indicators = demographic_table_short,
    payg_scenarios = payg_table,
    pension_cost = pension_cost,
    replacement_rates = replacement_rates
  ),
  "outputs/spain_pension_tables.xlsx"
)

write_csv(demographic_table_short, "outputs/table_A1_demographic_indicators.csv")
write_csv(payg_table, "outputs/table_A2_payg_scenarios.csv")
write_csv(pension_cost, "outputs/supporting_pension_cost.csv")
write_csv(replacement_rates, "outputs/supporting_replacement_rates.csv")

# 9. Appendix figures ----------------------------------------------------

# Figure A1: Old-age dependency ratio
figure_A1 <- ggplot(
  demographic_table,
  aes(x = year, y = old_age_dependency_ratio)
) +
  geom_line(linewidth = 1) +
  geom_point(size = 3) +
  scale_x_continuous(breaks = years_keep) +
  labs(
    title = "Figure A1. Old-age dependency ratio in Spain",
    subtitle = "People aged 65+ per 100 people aged 15-64",
    x = "Year",
    y = "Old-age dependency ratio",
    caption = "Source: Own calculations based on UN World Population Prospects 2024, Median variant."
  ) +
  theme_minimal()

print(figure_A1)
ggsave(
  "figures/figure_A1_old_age_dependency_ratio.png",
  figure_A1,
  width = 7,
  height = 5,
  dpi = 300
)

# Figure A2: Age structure
age_shares_long <- demographic_table %>%
  select(year, share_0_14, share_15_64, share_65plus) %>%
  pivot_longer(
    cols = c(share_0_14, share_15_64, share_65plus),
    names_to = "age_group",
    values_to = "share"
  ) %>%
  mutate(
    age_group = case_when(
      age_group == "share_0_14" ~ "0-14",
      age_group == "share_15_64" ~ "15-64",
      age_group == "share_65plus" ~ "65+",
      TRUE ~ age_group
    )
  )

figure_A2 <- ggplot(
  age_shares_long,
  aes(x = factor(year), y = share, fill = age_group)
) +
  geom_col(position = "dodge") +
  labs(
    title = "Figure A2. Age structure of Spain's population",
    subtitle = "Share of total population by broad age group",
    x = "Year",
    y = "Share of total population (%)",
    fill = "Age group",
    caption = "Source: Own calculations based on UN World Population Prospects 2024, Median variant."
  ) +
  theme_minimal()

print(figure_A2)
ggsave(
  "figures/figure_A2_age_structure.png",
  figure_A2,
  width = 7,
  height = 5,
  dpi = 300
)

# Figure A3: Population aged 80+
figure_A3 <- ggplot(
  demographic_table,
  aes(x = year, y = share_80plus)
) +
  geom_line(linewidth = 1) +
  geom_point(size = 3) +
  scale_x_continuous(breaks = years_keep) +
  labs(
    title = "Figure A3. Population aged 80+ in Spain",
    subtitle = "Share of total population aged 80 or older",
    x = "Year",
    y = "Share of total population (%)",
    caption = "Source: Own calculations based on UN World Population Prospects 2024, Median variant."
  ) +
  theme_minimal()

print(figure_A3)
ggsave(
  "figures/figure_A3_population_80plus.png",
  figure_A3,
  width = 7,
  height = 5,
  dpi = 300
)

# Figure A4: PAYG scenario simulation
figure_A4 <- ggplot(
  payg_table,
  aes(x = year, y = contrib_rate, color = scenario, group = scenario)
) +
  geom_line(linewidth = 1) +
  geom_point(size = 3) +
  scale_x_continuous(breaks = years_keep) +
  labs(
    title = "Figure A4. PAYG pension pressure under adequacy scenarios",
    subtitle = "Required contribution rate implied by pension generosity and ageing",
    x = "Year",
    y = "Required contribution rate (%)",
    color = "Scenario",
    caption = "Source: Own calculations based on UN World Population Prospects 2024."
  ) +
  theme_minimal()

print(figure_A4)
ggsave(
  "figures/figure_A4_payg_scenarios.png",
  figure_A4,
  width = 7,
  height = 5,
  dpi = 300
)

# Figure A5: Pension expenditure projections
figure_A5 <- ggplot(
  pension_cost,
  aes(x = factor(year), y = pension_gdp, fill = source)
) +
  geom_col(position = position_dodge(width = 0.9)) +
  geom_text(
    aes(label = paste0(pension_gdp, "%")),
    position = position_dodge(width = 0.9),
    vjust = -0.3,
    size = 3.5
  ) +
  labs(
    title = "Figure A5. Projected public pension expenditure in Spain",
    subtitle = "Pension expenditure as a share of GDP under existing projections",
    x = "Year",
    y = "Pension expenditure (% of GDP)",
    fill = "Projection",
    caption = "Sources: AIReF 2025, OECD 2025, FEDEA 2024, European Commission Ageing Report 2024."
  ) +
  ylim(0, 19) +
  theme_minimal()

print(figure_A5)
ggsave(
  "figures/figure_A5_pension_expenditure_gdp.png",
  figure_A5,
  width = 8,
  height = 5,
  dpi = 300
)

# Figure A6: Gross replacement rate
figure_A6 <- ggplot(
  replacement_rates,
  aes(x = country_group, y = gross_replacement_rate, fill = country_group)
) +
  geom_col(width = 0.6) +
  geom_text(
    aes(label = paste0(gross_replacement_rate, "%")),
    vjust = -0.3,
    size = 4
  ) +
  labs(
    title = "Figure A6. Gross pension replacement rate",
    subtitle = "Spain compared with the OECD average",
    x = "",
    y = "Gross replacement rate (%)",
    caption = "Source: OECD Pensions at a Glance 2025."
  ) +
  ylim(0, 90) +
  theme_minimal() +
  theme(legend.position = "none")

print(figure_A6)
ggsave(
  "figures/figure_A6_replacement_rate.png",
  figure_A6,
  width = 7,
  height = 5,
  dpi = 300
)

# 10. End message --------------------------------------------------------

message("Done. Tables saved in the 'outputs' folder and figures saved in the 'figures' folder.")
