# Charts Guide

This document describes every chart in the dashboard: what it shows, how to read it, where its data comes from, and how to export it.

---

## 1. AMR Resistance Curve

**Page:** Overview (`/`)

**What it shows:** The primary visualization of the project. A sigmoid-shaped curve plotting the "Resistance Pressure Index" (0-100) from 1990 to 2060. The observed segment (1990-2025) is drawn as a solid blue line; the forecast segment (2025-2060) is a dashed red line. Published data points are shown as blue circle markers. A shaded band shows the uncertainty range. A dotted red horizontal line marks the critical threshold at ~95, and a shaded vertical band highlights the projected critical point window (2040-2045).

**How to interpret it:**
- The y-axis (Resistance Pressure Index) is a normalized conceptual composite, not a raw measurement. A value of 70 means approximately 70% of the way toward total first-line antibiotic ineffectiveness for hospital-acquired Gram-negative infections.
- The transition from solid to dashed at 2025 marks the boundary between anchored data and model-based forecasts.
- The shaded uncertainty band widens in the forecast period, reflecting increasing uncertainty.
- Hover over any point to see the exact index value and, for data point markers, the published source.
- The critical point zone (2040-2045) is where the curve approaches 95, indicating near-total resistance for key pathogen-drug combinations.

**Data sources:** `OBSERVED_DATA` and `FORECAST_DATA` from `data/amr_data.py`, interpolated by `compute_sigmoid_curve()`. Anchored to Murray et al. (Lancet 2022), O'Neill Review, GRAM Project, Oxford Vaccine Group, and IHME GBD.

**Export:** Click the camera icon in the Plotly modebar (top-right of chart). Default format: SVG at 3x scale. Filename: `amr_resistance_curve`. Also available through the Export Studio page with alternative color schemes.

---

## 2. Mortality Projections

**Page:** Overview (`/`)

**What it shows:** A stacked bar chart showing projected AMR deaths per year (in thousands) from 2019 to 2050. The red bars represent deaths directly attributable to bacterial AMR; the amber bars represent additional associated deaths (total associated minus attributable).

**How to interpret it:**
- The 2019 bar is the only fully observed data point (1,270K attributable, 4,950K associated, from Murray et al.).
- Subsequent bars are projections that escalate toward the O'Neill scenario of 10 million attributable deaths by 2050.
- The distinction between "attributable" and "associated" is methodologically important: attributable deaths are those that would not have occurred without the resistant infection, while associated deaths include all deaths in patients with resistant infections regardless of whether resistance was the proximate cause.
- Hover to see exact values for each component.

**Data sources:** `MORTALITY_DATA` from `data/amr_data.py`. Anchored to Murray et al. (2019 baseline), GRAM projections (2025-2035), and O'Neill trajectory (2040-2050).

**Export:** Camera icon, SVG at 3x scale. Filename: `amr_mortality`. Also available in Export Studio.

---

## 3. Resistance Heatmap

**Page:** Pathogens (`/pathogens`)

**What it shows:** A 10x10 heatmap matrix with 10 pathogens (rows) and 10 antibiotic classes (columns). Each cell shows the approximate percentage of resistant isolates (global median). The color scale runs from dark teal (0%) through blue and amber to red (100%). Cells marked with an em-dash represent intrinsic resistance or insufficient data (NaN). Each pathogen row is annotated with its WHO priority classification (Critical, High, Medium, or Special).

**How to interpret it:**
- Darker red cells indicate higher resistance rates — these are the most concerning pathogen-drug combinations.
- A. baumannii and E. faecium (VRE) show the broadest patterns of high resistance.
- Em-dash cells (e.g., P. aeruginosa vs. Penicillins) indicate intrinsic resistance — the antibiotic class was never effective against that organism.
- The WHO priority labels help contextualize which organisms pose the greatest public health threat.
- Hover over any cell for a detailed tooltip showing the pathogen, antibiotic class, and resistance percentage.

**Data sources:** `RESISTANCE_MATRIX`, `PATHOGENS`, `ANTIBIOTIC_CLASSES`, and `WHO_PRIORITY` from `data/pathogen_data.py`. Values are approximate global medians compiled from WHO GLASS 2022/2023, ECDC EARS-Net, Murray et al. (Lancet 2022), and CDC AR Threats Report 2019/2022.

**Export:** Camera icon, SVG at 3x scale. Also available in Export Studio with light and B&W themes.

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

## Export Studio

**Page:** Export (`/export`)

The Export Studio page provides a unified interface for exporting any of the five main charts (AMR Resistance Curve, Mortality Projections, Resistance Heatmap, Regional Variation, Temporal Trends) with customizable settings:

- **Color schemes:** Dashboard Dark (default), Publication Light (white background), Print B&W (grayscale)
- **Formats:** SVG (recommended for publications), PNG, PDF
- **Resolution:** 1x (screen), 2x (presentations), 3x (publication quality, ~300 DPI)

To export, configure your desired settings, then click the camera icon in the Plotly modebar of the preview chart. The file will be downloaded with a descriptive filename (e.g., `amr_main_curve_light.svg`).
