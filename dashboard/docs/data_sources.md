# Data Sources Reference

## Important Disclaimer

The resistance matrix values are approximate global medians compiled from multiple surveillance reports. The time series data is synthetic but calibrated to published trends. No raw patient-level or isolate-level data is used directly; all values are derived from published aggregate statistics, modeled estimates, or calibrated synthetic generation.

---

## Source 1: Murray et al., Lancet 2022 (GBD-AMR)

**Full citation:** Murray CJL, Ikuta KS, Sharara F, et al. "Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis." *The Lancet*, 399(10325):629-655, 2022.

**URL:** https://doi.org/10.1016/S0140-6736(21)02724-0

**What we extract:**
- 1.27 million deaths directly attributable to bacterial AMR in 2019 (used as the 2019 anchor in `MORTALITY_DATA`)
- 4.95 million deaths associated with bacterial AMR in 2019 (used as the 2019 associated deaths figure)
- Resistance index anchor point: 58 for year 2019 in `OBSERVED_DATA`
- Pathogen-level burden rankings informing the resistance matrix weighting

**Data quality:** Observed/modeled. This is a Bayesian hierarchical model applied to a comprehensive database of clinical isolate data. The estimates carry uncertainty but represent the most authoritative global AMR burden assessment available.

---

## Source 2: O'Neill Review on Antimicrobial Resistance (2016)

**Full citation:** O'Neill J. "Tackling drug-resistant infections globally: final report and recommendations." *Review on Antimicrobial Resistance*, 2016.

**URL:** https://amr-review.org/sites/default/files/160518_Final%20paper_with%20cover.pdf

**What we extract:**
- Projection of 10 million AMR deaths per year by 2050 (used as the 2050 endpoint in `MORTALITY_DATA`)
- Forecast trajectory anchor: resistance index 93 at 2040, used in `FORECAST_DATA`
- The 2045 mortality interpolation point (7,200K deaths) bridges between GRAM and O'Neill estimates

**Data quality:** Projection. The 10 million figure is a widely cited but contested projection based on extrapolation from limited regional data. It serves as an upper-bound scenario rather than a precise forecast.

---

## Source 3: GRAM Project (Global Research on Antimicrobial Resistance) / IHME

**Full citation:** Institute for Health Metrics and Evaluation (IHME). "Global Research on Antimicrobial Resistance (GRAM) Project." University of Washington, 2024.

**URL:** https://www.healthdata.org/research-analysis/health-risks-issues/antimicrobial-resistance-amr

**Related CIDRAP coverage:** https://www.cidrap.umn.edu/antimicrobial-stewardship/study-forecasts-more-39-million-deaths-antimicrobial-resistance-2050

**What we extract:**
- Resistance index projection for 2025: 70 (from `OBSERVED_DATA`, sourced as "CIDRAP/GRAM projection")
- Forecast data points for 2030 (80) and 2035 (88) in `FORECAST_DATA`
- Mortality projections for 2025 (1,500K) and 2030 (2,100K) in `MORTALITY_DATA`
- GRAM coverage timeline (1990-2021, 204 countries) in the Data Sources page catalog

**Data quality:** Mixed observed and projected. The GRAM project uses hierarchical Bayesian models fitted to observed surveillance data; forecasts beyond 2021 are model-based extrapolations.

---

## Source 4: WHO GLASS (Global Antimicrobial Resistance and Use Surveillance System)

**Full citation:** World Health Organization. "Global Antimicrobial Resistance and Use Surveillance System (GLASS) Report: 2022." WHO, Geneva, 2022.

**URL:** https://www.who.int/initiatives/glass

**What we extract:**
- Regional resistance data for K. pneumoniae, E. coli, S. aureus, and A. baumannii across six WHO regions (used in `REGIONAL_DATA` in `pathogen_data.py`)
- Resistance matrix values for individual pathogen-antibiotic combinations, particularly carbapenem resistance in Gram-negatives
- Coverage timeline (2015-present, 127 countries) shown on the Data Sources page

**Data quality:** Observed (laboratory-based surveillance). GLASS data is the most authoritative international surveillance source, but enrollment and reporting quality vary by country. Low- and middle-income countries are underrepresented in early years.

---

## Source 5: ECDC EARS-Net (European Antimicrobial Resistance Surveillance Network)

**Full citation:** European Centre for Disease Prevention and Control. "Antimicrobial resistance in the EU/EEA (EARS-Net) — Annual epidemiological report." ECDC, Stockholm, 2023.

**URL:** https://www.ecdc.europa.eu/en/antimicrobial-resistance/surveillance-and-disease-data/data-ecdc

**What we extract:**
- MRSA prevalence trends informing the `TEMPORAL_TRENDS` data (the MRSA decline pattern from ~42% in 2005 to ~21% by 2025 is calibrated to European trends)
- Regional resistance data for Europe in `REGIONAL_DATA`
- Long-running time series (1998-present) providing the temporal backbone for trend calibration

**Data quality:** Observed (invasive isolate surveillance from blood/CSF). High-quality standardized data from 30 EU/EEA countries. Not globally representative — European trends (e.g., successful MRSA reduction) may not reflect global patterns.

---

## Source 6: CDC Antibiotic Resistance Threats Report

**Full citation:** Centers for Disease Control and Prevention. "Antibiotic Resistance Threats in the United States, 2019." US Department of Health and Human Services, 2019. Updated 2022.

**URL:** https://www.cdc.gov/antimicrobial-resistance/data-research/threats/index.html

**What we extract:**
- US-specific resistance rates used as cross-validation for the resistance matrix
- Threat classification (urgent, serious, concerning) as a complement to WHO priority rankings
- Coverage timeline (2013-2022) shown on the Data Sources page

**Data quality:** Observed (US national estimates). High quality but limited to the United States. Used for validation rather than as a primary data source for the global model.

---

## Source 7: Oxford Vaccine Group AMR Timeline

**Full citation:** Oxford Vaccine Group. "Antibiotic Resistance." University of Oxford, 2023.

**URL:** https://www.ovg.ox.ac.uk/news/antibiotic-resistance

**What we extract:**
- Historical baseline resistance index values for 1990 (12), 1995 (18), 2000 (23), and 2005 (28) in `OBSERVED_DATA`
- These serve as early anchors for the sigmoid curve construction

**Data quality:** Observed (narrative review of historical data). These values represent our interpretation of the qualitative and semi-quantitative historical record compiled by OVG. They are approximate.

---

## Source 8: IHME GBD (Global Burden of Disease) Updates

**Full citation:** Institute for Health Metrics and Evaluation. "GBD Results." University of Washington, 2021.

**URL:** https://www.healthdata.org/research-analysis/diseases-injuries-risks/factsheets/2021-amr-factsheet

**What we extract:**
- Resistance index anchor for 2010 (35) and 2015 (45) in `OBSERVED_DATA`, sourced as "Lancet GBD"
- The 2021 update anchor point: resistance index 63

**Data quality:** Modeled. GBD estimates use extensive statistical modeling with uncertainty quantification. The AMR-specific estimates are among the most rigorous available.

---

## Source 9: ResistanceMap (CDDEP / One Health Trust)

**Full citation:** Center for Disease Dynamics, Economics & Policy. "ResistanceMap: Antibiotic Resistance." One Health Trust, 2024.

**URL:** https://resistancemap.onehealthtrust.org/

**What we extract:**
- Cross-validation of resistance percentages in the pathogen-antibiotic matrix
- Listed as an available data source on the Data Sources page (40+ countries, 2000-present)

**Data quality:** Observed (aggregated from national surveillance systems). Quality varies by country. Used for validation rather than as a primary input.

---

## Data Categories Summary

### Observed Data
- `OBSERVED_DATA` years 1990-2021: Anchored to published values from the sources above
- `RESISTANCE_MATRIX`: Approximate global medians compiled from WHO GLASS, EARS-Net, Murray et al., and CDC reports
- `REGIONAL_DATA`: Based on WHO GLASS 2022 regional breakdowns
- `TEMPORAL_TRENDS`: Calibrated to published trends (MRSA decline, E. coli and CRE increase) but with simplified trajectories

### Projections
- `OBSERVED_DATA` year 2025: CIDRAP/GRAM projection (not yet fully observed)
- `FORECAST_DATA` (2025-2060): Model-based extrapolations from GRAM and O'Neill trajectories
- `MORTALITY_DATA` years 2025-2050: Interpolated between GRAM near-term projections and O'Neill long-term scenario

### Synthetic Data
- `MONTHLY_DATA` in `timeseries_data.py`: Entirely synthetic monthly resistance time series generated with `np.random.default_rng(seed=42)`. These are deterministic (reproducible) but do not correspond to any specific real-world dataset. They combine logistic/polynomial trends, sinusoidal seasonality, and Gaussian noise to produce plausible-looking series for SARIMA demonstration purposes.

### Constructed/Composite
- The "Resistance Pressure Index" (0-100 scale) is a conceptual composite metric, not a raw epidemiological measurement. It normalizes and aggregates across multiple resistance indicators to provide a single trajectory visualization.
- Confidence bounds in `OBSERVED_DATA` and `FORECAST_DATA` are manually specified based on the range of estimates across sources, not derived from a formal statistical model.
