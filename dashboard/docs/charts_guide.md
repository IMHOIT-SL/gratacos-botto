# Charts Guide

This document describes every chart in the dashboard: what it shows, how to read it, where its data comes from, and how to export it.

---

## 1. AMR Resistance Curve (super-exponential)

**Page:** Overview (`/`)

**What it shows:** The primary visualization of the project — a closed-form **super-exponential** curve plotting the "Resistance Pressure Index" (0-100) from 1990 to 2060, expressing the paper's "rate of increase is itself growing" thesis (UPDATE v.A-29 párr. 22). The observed segment (1990-2025) is drawn as a solid blue line; the forecast segment (2025-2060) is a dashed red line. A faint dotted grey line shows the constant-r reference logistic for visual contrast. Published data points are blue circle markers. A shaded band shows the ±3-year temporal envelope. A dotted red horizontal line marks the critical threshold at ~95, and a red-shaded vertical band highlights the critical point window **2040-2047** (matching paper párr. 19 milestones).

**How to interpret it:**
- The y-axis is a normalized conceptual composite, not a raw measurement.
- The super-exponential curve crosses the critical threshold (95) in **2047**; the constant-r reference crosses it in **2051**. The 4-year advance is the paper's central forecasting claim.
- The shaded ±3y band represents the paper's stated uncertainty (párr. 5: "fourteen years (±3)") — it is a temporal shift, not a statistical CI.
- Hover over markers to see source citations.

**Data sources:** `compute_super_exponential_curve()` and `compute_reference_logistic_curve()` in `data/amr_data.py` — closed-form, hardcoded coefficients (K=100, A≈7.333, r=0.0705, b=3.05·10⁻⁴), no fitting. Anchored to Murray et al. (Lancet 2022), O'Neill Review, GRAM Project, Tai 2025 IJAA, Oxford Vaccine Group, and IHME GBD.

**Export:** Camera icon → SVG 3x. Filename: `amr_resistance_curve`. Also available in Export Studio with light/B&W themes.

---

## 2. Mortality Projections (three methodologies)

**Page:** Overview (`/`)

**What it shows:** Three projection methodologies overlaid on the same axes. (a) Red+amber stacked bars: GRAM/O'Neill methodology (attributable + associated deaths, escalating to ~10M associated by 2050). (b) Dashed blue line with diamond markers: **Tai et al. 2025** (paper ref 10) — a more conservative GBD-hierarchical methodology projecting ~1.91M attributable deaths by 2040.

**How to interpret it:**
- The 2019 bar is the only fully observed data point (1,270K attributable, 4,950K associated, from Murray et al.).
- Tai 2025 (~1.91M @ 2040) and O'Neill (~10M @ 2050) are legitimate methodological alternatives — the gap between them is itself a measure of model uncertainty in long-horizon AMR mortality forecasting.
- "Attributable" deaths would not have occurred without the resistant infection; "associated" includes all deaths in patients with resistant infections.

**Data sources:** `MORTALITY_DATA` from `data/amr_data.py` with `tai_2025_deaths_k` column. Anchored to Murray et al. (2019 baseline), GRAM (2025-2035), O'Neill (2040-2050), and Tai et al. IJAA 2025.

**Export:** Camera icon → SVG 3x. Filename: `amr_mortality`. Also in Export Studio.

---

## 3. ESKAPEE Resistance Heatmap

**Page:** Pathogens (`/pathogens`)

**What it shows:** An 11×10 heatmap with the **ESKAPEE** pathogens (E. coli explicit per paper párr. 11) plus **S. maltophilia** (paper párr. 65) plus reference pathogens (rows) and 10 antibiotic classes (columns). Each cell shows the approximate percentage of resistant isolates. Color scale: dark teal (0%) → blue → amber → red (100%). Em-dash cells = intrinsic resistance or insufficient data. Each row is annotated with two badges: WHO priority (Critical/High/Medium/Special) **and** Magiorakos isolate-level phenotype (MDR/XDR/PDR documented).

**How to interpret it:**
- Darker red cells indicate higher resistance — the most concerning pathogen-drug combinations.
- S. maltophilia has 6/10 NaN cells (β-lactams, aminoglycosides, vancomycin, macrolides) — this reflects intrinsic biology (L1 metallo-β-lactamase, etc.), not missing data.
- MDR/XDR/PDR badges are isolate-level (Magiorakos 2012). Saying "K. pneumoniae = PDR" is shorthand for "PDR strains are documented in literature" — most clinical isolates remain susceptible to at least some drugs.
- Hover any cell for the resistance percentage and modification flag (when overridden via Sensitivity Analysis).

**Data sources:** `RESISTANCE_MATRIX`, `PATHOGENS`, `ANTIBIOTIC_CLASSES`, `WHO_PRIORITY`, `MDR_XDR_PDR` from `data/pathogen_data.py`. Anchored to WHO GLASS 2022/2023, ECDC EARS-Net, Murray et al. Lancet 2022, CDC AR Threats Report, Magiorakos 2012, paper UPDATE v.A-29 párrs. 51-65.

**Export:** Camera icon → SVG 3x. Also in Export Studio.

---

## 3a. Sensitivity Analysis (companion panel)

**Page:** Pathogens (`/pathogens`) — directly below the heatmap

**What it shows:** A research-mode "what-if" panel that lets you override any cell of the heatmap transiently. Two dropdowns (Pathogen, Antibiotic class), a slider (0–100% override value), and Apply / Reset buttons. A live preview line shows the currently selected cell with its default and proposed value. A status line below shows how many cells are currently modified.

**How to interpret it:**
- Defaults are anchored to peer-reviewed surveillance data. Overrides are **transient** (per-session, reset on page reload) by design — preserves reproducibility for publication.
- Intrinsic-R (NaN) cells **refuse override** and the preview marks them with a warning — biological correctness preserved.
- The heatmap above re-renders immediately when Apply is clicked. Modified cells are flagged in their hover tooltip.

**Data sources:** Reads `RESISTANCE_MATRIX` defaults; writes overrides to `dcc.Store(storage_type="memory")` — never persisted.

---

## 4. Regional Variation

**Page:** Pathogens (`/pathogens`)

**What it shows:** A grouped bar chart comparing resistance rates across six WHO regions (Africa, Americas, SE Asia, Europe, E. Mediterranean, W. Pacific) for four key pathogens: K. pneumoniae (3rd-gen cephalosporin resistance), E. coli (3rd-gen cephalosporin resistance), S. aureus (MRSA prevalence), and A. baumannii (carbapenem resistance).

**How to interpret it:**
- Bars are grouped by region, with each color representing a different pathogen.
- E. Mediterranean and SE Asia generally show the highest resistance rates.
- Europe shows relatively lower rates, reflecting more established stewardship programs.
- The y-axis runs from 0-100% resistant isolates.
- These are regional aggregates and mask significant within-region variation.

**Data sources:** `REGIONAL_DATA` from `data/pathogen_data.py`. Based on WHO GLASS 2022 regional breakdowns and EARS-Net for European data.

**Export:** Camera icon, SVG at 3x scale. Also available in Export Studio.

---

## 5. Temporal Trends

**Page:** Pathogens (`/pathogens`)

**What it shows:** Line chart tracking the prevalence of three key resistance phenotypes from 2000 to 2025: MRSA (amber), 3GC-R E. coli (blue), and CRE K. pneumoniae (red). Each line has small markers at annual data points.

**How to interpret it:**
- MRSA shows a distinctive pattern: rising to ~42% around 2005, then gradually declining to ~21% by 2025. This reflects the success of hospital infection control interventions in many countries.
- 3GC-R E. coli shows a steady linear increase from ~5% to ~32%, driven by community-acquired ESBL-producing strains.
- CRE K. pneumoniae shows an accelerating increase from ~1% to ~35%, representing one of the most alarming resistance trends globally.
- The divergent trajectories illustrate that AMR is not a single problem — different pathogens have different dynamics and respond differently to interventions.

**Data sources:** `TEMPORAL_TRENDS` from `data/pathogen_data.py`. Trends are calibrated to published surveillance data from EARS-Net and GLASS but are simplified representations (smooth trajectories rather than raw annual data).

**Export:** Camera icon, SVG at 3x scale. Also available in Export Studio.

---

## 6. SARIMA Forecast

**Page:** Time Series (`/timeseries`)

**What it shows:** The main forecast chart on the Time Series page. It displays historical monthly resistance rate data (solid colored line) for the selected pathogen, with a dashed line showing the SARIMA model forecast extending into the future. A shaded band shows the 95% confidence interval around the forecast. The forecast horizon is user-adjustable (6, 12, 24, or 36 months).

**How to interpret it:**
- The historical data shows monthly granularity with visible seasonality and noise.
- The forecast continues the trend and seasonal pattern identified by the SARIMA model.
- The 95% CI band widens over time, reflecting increasing uncertainty in longer-range forecasts.
- For MRSA, expect a roughly flat or gently declining forecast. For 3GC-R E. coli and CRE K. pneumoniae, expect upward trends.
- The model label below the chart title confirms which method was used (SARIMAX or linear fallback).

**Data sources:** `MONTHLY_DATA` from `data/timeseries_data.py`. This is entirely synthetic data generated with deterministic randomness (seed=42). See `data_sources.md` for details.

**Export:** Camera icon, SVG at 3x scale.

---

## 7. Scenario Comparison

**Page:** Time Series (`/timeseries`)

**What it shows:** A comparison of two forecast scenarios for the selected pathogen. The historical data is shown in grey. The "Business as usual" (BAU) forecast is a dashed red line. The "Intervention (-30%)" scenario is a dotted green line showing the projected trajectory if interventions reduce the trend component by 30%.

**How to interpret it:**
- The gap between the red and green lines represents the potential impact of effective stewardship and infection control interventions.
- The intervention scenario applies a 30% reduction to the delta between each forecast point and the last observed value (see `models.md` for details).
- For pathogens with strong upward trends (CRE K. pneumoniae), the gap between scenarios is most dramatic.
- This is a simplified scenario model — real interventions would have more complex dynamics.

**Data sources:** Same synthetic monthly data as the SARIMA Forecast chart. BAU uses the standard SARIMA forecast; intervention uses `fit_intervention_sarima()`.

**Export:** Camera icon, SVG at 3x scale.

---

## 8. ACF/PACF Correlogram

**Page:** Time Series (`/timeseries`)

**What it shows:** Two bar charts showing the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF) of the selected pathogen's raw monthly resistance series. Dotted horizontal lines mark the 95% significance bounds (plus/minus 1.96 / sqrt(N)).

**How to interpret it:**
- **ACF** — Shows the correlation between the series and lagged versions of itself. For AMR data, expect significant autocorrelation at lag 12 (annual seasonality) and slowly decaying positive correlations at early lags (trend component).
- **PACF** — Shows the partial correlation after removing the effect of intermediate lags. Significant spikes at specific lags suggest AR order. A significant spike at lag 12 supports the seasonal AR component.
- Bars extending beyond the dotted significance lines are statistically significant at the 5% level.
- These plots justify the SARIMAX(1,1,1)(1,1,0,12) model specification: the ACF/PACF patterns are consistent with an ARIMA(1,1,1) process with seasonal differencing at period 12.
- The number of lags shown is min(36, N/3) where N is the series length.

**Data sources:** Computed from `MONTHLY_DATA` using `statsmodels.tsa.stattools.acf` and `pacf` (or a manual fallback if statsmodels is unavailable).

**Export:** Camera icon, SVG at 3x scale.

---

## 9. Residuals

**Page:** Time Series (`/timeseries`)

**What it shows:** A bar chart of the SARIMA model residuals (observed minus fitted values) over time. Positive residuals are green; negative residuals are red. Diagnostic statistics (AIC, BIC, residual standard deviation) are displayed above the chart as badges.

**How to interpret it:**
- Well-behaved residuals should appear random with no visible pattern or trend.
- If residuals show a trend, the model is not adequately capturing the data dynamics.
- If residuals show periodic spikes, the seasonal component may need adjustment.
- The residual standard deviation gives a rough sense of typical model error in percentage points.
- AIC and BIC values are useful for comparing alternative model specifications (lower is better).

**Data sources:** Computed by `fit_sarima()` in `pages/timeseries.py` from the SARIMAX model residuals.

**Export:** Camera icon, SVG at 3x scale.

---

## 10. Data Coverage Timeline

**Page:** Data Sources (`/datasources`)

**What it shows:** A horizontal bar (Gantt-style) chart showing the temporal coverage of each data source used in the project. Each bar represents a data source, with its length proportional to the year range covered.

**How to interpret it:**
- Longer bars indicate data sources with deeper historical coverage (e.g., GRAM 1990-2021, EARS-Net 1998-2025).
- Single-year sources (Murray et al. reference year 2019) appear as thin bars.
- This visualization helps identify temporal gaps and overlaps in data coverage.

**Data sources:** `DATA_SOURCES` list in `pages/datasources.py`, with manually specified year ranges for each source.

**Export:** Camera icon, SVG at 3x scale.

---

## 11. Carbapenem 2035 Spotlight

**Page:** Overview (`/`)

**What it shows:** Stacked area chart of carbapenem-resistant mortality through 2035: CRE (Enterobacterales) + CRAB (A. baumannii) + CRPA (P. aeruginosa). A vertical dotted line at 2025 marks the observed → forecast boundary; a second dotted line at 2035 marks the Tai 2025 horizon.

**How to interpret it:**
- Operationalises paper UPDATE v.A-29 párr. 9 / Tai 2025: "carbapenem-resistant deaths are projected to escalate sharply by 2035 even as overall age-standardized mortality declines".
- The per-pathogen split is illustrative — refer to Tai 2025 for the underlying figures.

**Data sources:** `CARBAPENEM_PROJECTION` in `data/amr_data.py`. Anchored to Murray 2022 (2019 baseline) + Tai 2025 IJAA (paper ref 10).

**Export:** Camera icon → SVG 3x. Filename: `carbapenem_2035`. Also in Export Studio.

---

## 12. PubMed Scientometric Trend

**Page:** Industry (`/industry`)

**What it shows:** Annual publication counts for the search term "antibiotic resistance" on PubMed, 1990-2025. Bar chart, ~253K cumulative results.

**How to interpret it:**
- Closely matches the 250,267 results visible in the PubMed query screenshot embedded in the paper (image 3, párr. 25).
- Annual count derived from the closed-form `count(y) = round(500·exp(0.115·(y-1990)))` — calibrated to reproduce the visual envelope of the PubMed search results.

**Data sources:** `compute_pubmed_annual()` in `data/bibliometrics_data.py`. Anchored to PubMed search "antibiotic resistance".

**Export:** Camera icon → SVG 3x. Also in Export Studio.

---

## 13. Antibiotic-Resistance Market Growth

**Page:** Industry (`/industry`)

**What it shows:** Market size projection 2022-2032 with **CAGR 5.4%** (Univdatos report). Spline line + filled area, with annotated start ($5.5B 2023) and end ($8.83B 2032).

**How to interpret it:**
- Univdatos "Antibiotic Resistance Market 2024-2032" report applied with uniform CAGR.
- The chart supports the paper's párr. 25 thesis: market grows but efficacy doesn't.

**Data sources:** `MARKET_GROWTH` in `data/bibliometrics_data.py`. Anchored to Univdatos.

**Export:** Camera icon → SVG 3x. Also in Export Studio.

---

## 14. Drug Class Breakdown

**Page:** Industry (`/industry`)

**What it shows:** Grouped bar chart comparing 2023 vs 2032 USD revenue across four drug classes: Oxazolidinones (linezolid), Lipoglycopeptides (dalbavancin/oritavancin), Tetracyclines (tigecycline/eravacycline/omadacycline), and Others (β-lactam/inhibitor combos and novel agents).

**How to interpret it:**
- Per-class shares are visual approximations of the Univdatos drug-class figure embedded in the paper (image 2).
- Revenue allocation, not therapeutic effectiveness — same molecules face the same resistance pressures.

**Data sources:** `DRUG_CLASS_SHARE`, `class_size_2023()`, `class_size_2032()` in `data/bibliometrics_data.py`. Anchored to Univdatos.

**Export:** Camera icon → SVG 3x. Also in Export Studio.

---

## 15. Awareness vs Effectiveness — Divergence

**Page:** Industry (`/industry`)

**What it shows:** Two series indexed to **1990 = 1.0** on a **log scale**. Awareness (blue solid) tracks cumulative PubMed publications and reaches ~500× by 2025. Effectiveness (red dashed) tracks `(100 − resistance index)` and declines to ~0.34× by 2025. The two curves move in opposite directions.

**How to interpret it:**
- Direct visualisation of paper UPDATE v.A-29 párr. 25: "increase in volume of sales, but no increase in efficacy is discernible".
- Structural, not cyclical, divergence — awareness alone has not solved the problem.

**Data sources:** `AWARENESS_EFFECTIVENESS` in `data/bibliometrics_data.py`. Combines PubMed annual counts and the super-exponential resistance model.

**Export:** Camera icon → SVG 3x. Also in Export Studio. **This is the central industry chart — recommended for the paper's párr. 25 figure.**

---

## 16. Paradigm Comparison (classical vs antimetabolic)

**Page:** Metabolic (`/metabolic`)

**What it shows:** Conceptual chart contrasting two trajectories. The red curve is the data-driven classical antibiotic effectiveness (100 − super-exp resistance index). The blue band is a **qualitative working-hypothesis envelope** — explicitly NOT a forecast — representing the paper's claim that an antimetabolic line of treatment could sustain effectiveness. A note inside the figure marks this as qualitative.

**How to interpret it:**
- This is the **only** chart in the dashboard that includes a non-empirical series. The convention is enforced everywhere else.
- The blue band is intended only to visualise the paradigm shift the paper proposes (subtitle + párrs. 5, 24). Once authors specify the molecular mechanism and supply quantitative inputs, this band can be replaced with a quantitative trajectory.

**Data sources:** `compute_super_exponential_curve()` for the classical curve; the qualitative band is hand-drawn (years 2025–2060, fixed bounds 55–75).

**Export:** Camera icon → SVG 3x. Also in Export Studio.

---

## Export Studio

**Page:** Export (`/export`)

The Export Studio page provides a unified interface for exporting any of the **11 charts** in the dashboard with customisable settings, grouped by source page in the dropdown:

- **Overview** — Resistance Pressure Trajectory (super-exp), Mortality Projections (Murray + Tai 2025), Carbapenem 2035 Spotlight
- **Pathogens** — ESKAPEE Resistance Heatmap, Regional Variation, Temporal Trends
- **Industry** — PubMed Scientometric, Market Growth (CAGR 5.4%), Drug Class Breakdown, Awareness vs Effectiveness divergence
- **Metabolic** — Paradigm Comparison

Settings:

- **Color schemes:** Dashboard Dark (default), Publication Light (white background, journal-friendly), Print B&W (grayscale)
- **Formats:** SVG (recommended for publications), PNG (presentations & web). For PDF, export as SVG and convert with Inkscape or `cairosvg`.
- **Resolution:** 1x (screen), 2x (presentations), 3x (publication quality, ~300 DPI)

To export, configure settings, then click the camera icon in the Plotly modebar of the preview chart. The file downloads with a descriptive filename.
