# Mathematical Models Reference

This document describes the mathematical models used in the dashboard, their parameters, and their limitations.

---

## 1. Sigmoid / Logistic Resistance Curve

### Formula

The conceptual model underlying the resistance pressure trajectory is a logistic (sigmoid) function:

```
R(t) = L / (1 + exp(-k * (t - x0)))
```

where:
- `R(t)` is the Resistance Pressure Index at year `t`
- `L = 100` is the carrying capacity (maximum possible index)
- `k = 0.15` is the steepness parameter (growth rate)
- `x0 = 2010` is the inflection point (year of fastest growth)

### Parameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `L`       | 100   | Upper asymptote — represents theoretical total ineffectiveness of first-line antibiotics |
| `k`       | 0.15  | Growth rate — higher values produce a steeper S-curve. 0.15 gives a ~50-year transition from low to high resistance |
| `x0`      | 2010  | Inflection year — the midpoint where the growth rate is highest. Chosen because the 2010s saw the sharpest acceleration in carbapenem resistance and XDR-TB |

### Implementation in the Dashboard

The standalone script (`docs/antibiotics.py`) uses the pure logistic formula with manual overrides for the historical segment. The dashboard (`data/amr_data.py`) takes a different approach: it **does not use the logistic formula directly**. Instead, it performs piecewise linear interpolation between manually specified anchor points:

- **Observed segment (1990-2025):** Interpolated from `OBSERVED_DATA` using `np.interp()`. Each anchor point is derived from a published source (see `data_sources.md`).
- **Forecast segment (2025-2060):** Interpolated from `FORECAST_DATA` using `np.interp()`. These points follow a logistic-like trajectory but are individually calibrated to published forecasts (GRAM, O'Neill).

The result is a curve that has the qualitative shape of a sigmoid but is anchored to real-world data rather than fitted to the logistic formula.

### Confidence Bounds

The upper and lower bounds in `OBSERVED_DATA` and `FORECAST_DATA` are manually specified for each anchor point. They represent the range of estimates across different published sources rather than a formal statistical confidence interval. In the forecast period, the bounds widen to reflect increasing uncertainty, following the spread between optimistic and pessimistic published scenarios.

### Interpretation

The Resistance Pressure Index is a **conceptual composite metric** on a 0-100 scale:
- 0 = no clinically significant resistance
- ~70 (current, 2025) = widespread resistance to multiple first-line agents; carbapenems increasingly compromised
- ~95 (critical threshold) = near-total ineffectiveness of first-line antibiotics for hospital-acquired Gram-negative infections
- 100 = theoretical complete pan-resistance (asymptotic, never fully reached)

This index does not correspond to any single measured quantity. It synthesizes trends in MRSA prevalence, ESBL/3GC-R rates, carbapenem resistance, and other indicators into a single trajectory for communication purposes.

---

## 2. SARIMA Model

### Specification

The time series page fits a **SARIMAX(1,1,1)(1,1,0,12)** model to monthly synthetic resistance data.

Full notation: SARIMAX(p,d,q)(P,D,Q,s)

### Parameter Breakdown

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `p = 1`  | Non-seasonal AR order | One autoregressive lag: the current value depends linearly on the previous month's value |
| `d = 1`  | Non-seasonal differencing | First-order differencing to remove the trend; the model is fit to month-over-month changes |
| `q = 1`  | Non-seasonal MA order | One moving-average lag: the current value depends on the previous month's forecast error |
| `P = 1`  | Seasonal AR order | One seasonal autoregressive lag at period 12: this year's January depends on last year's January |
| `D = 1`  | Seasonal differencing | Seasonal differencing at period 12 to remove the annual cycle; the model operates on year-over-year changes |
| `Q = 0`  | Seasonal MA order | No seasonal moving-average component |
| `s = 12` | Seasonal period | 12 months (annual seasonality) |

### Mathematical Form

After differencing, the model can be written as:

```
(1 - phi_1 * B)(1 - Phi_1 * B^12)(1 - B)(1 - B^12) * y_t = (1 + theta_1 * B) * epsilon_t
```

where:
- `B` is the backshift operator: `B * y_t = y_{t-1}`
- `phi_1` is the non-seasonal AR(1) coefficient
- `Phi_1` is the seasonal AR(1) coefficient
- `theta_1` is the non-seasonal MA(1) coefficient
- `epsilon_t ~ N(0, sigma^2)` is white noise

### Fitting

The model is fit using `statsmodels.tsa.statespace.sarimax.SARIMAX` with:
- `enforce_stationarity=False` — allows the optimizer to explore a wider parameter space
- `enforce_invertibility=False` — relaxes the invertibility constraint on MA parameters
- `maxiter=200` — maximum optimization iterations
- `disp=False` — suppresses optimizer output

The fitting procedure uses maximum likelihood estimation (MLE) via the Kalman filter.

### Forecasting

Forecasts are generated using `results.get_forecast(steps=horizon)` which produces:
- **Point forecast** (`.predicted_mean`): the expected value at each future time step
- **95% confidence interval** (`.conf_int(alpha=0.05)`): based on the cumulative forecast error variance, which grows with the forecast horizon

### Fallback

If statsmodels is not available or the SARIMAX fit fails (convergence issues), the code falls back to simple **linear extrapolation**:

```python
coeffs = np.polyfit(t, series.values, 1)  # linear regression
forecast = np.polyval(coeffs, t_future)
CI = forecast +/- 1.96 * std(residuals)
```

The fallback is indicated in the model label displayed on the chart.

### Diagnostics

The Time Series page provides several diagnostic outputs:

- **AIC (Akaike Information Criterion):** Measures model fit penalized by complexity. Lower is better. Useful for comparing model specifications.
- **BIC (Bayesian Information Criterion):** Similar to AIC but with a stronger penalty for model complexity.
- **Residual standard deviation:** The typical magnitude of one-step-ahead prediction errors.
- **Residual plot:** Visual inspection for remaining patterns (should appear random).
- **ACF/PACF correlograms:** Autocorrelation structure of the raw series, used to validate model order selection.

---

## 3. Intervention Scenario

### Approach

The intervention scenario models a hypothetical 30% reduction in the resistance trend, representing the combined effect of stewardship programs, infection control measures, and new drug development.

### Implementation

The intervention forecast is computed in `fit_intervention_sarima()` as follows:

```python
# Fit the same SARIMAX model and get the BAU forecast
bau_mean = forecast.predicted_mean.values

# Compute the delta from the last observed value
last_val = series.iloc[-1]
deltas = bau_mean - last_val

# Apply 30% reduction to the deltas
intervention_mean = last_val + deltas * 0.7
```

This means:
- If the BAU forecast predicts the resistance rate will increase by 10 percentage points, the intervention scenario predicts an increase of only 7 percentage points.
- If the BAU forecast predicts a decrease (as for MRSA), the intervention scenario predicts a less steep decrease (the 30% reduction applies to the magnitude of change, not the direction).
- The intervention scenario shares the same starting point as BAU (the last observed value).

### Interpretation

The 30% figure is illustrative rather than evidence-based. It is meant to demonstrate the general principle that coordinated interventions can alter resistance trajectories, not to quantify the exact impact of any specific policy. Real-world intervention effects would depend on the specific pathogen, the intervention type, geographic scope, and implementation quality.

---

## 4. Confidence Intervals

### SARIMA Forecast CI

The 95% confidence intervals on the SARIMA forecast are computed analytically from the model's forecast error variance:

```
CI = forecast_mean +/- z_{0.025} * sqrt(cumulative_forecast_variance)
```

where `z_{0.025} = 1.96` and the cumulative forecast variance grows with each step because each future prediction depends on the (uncertain) prediction before it.

Key properties:
- The CI is symmetric around the point forecast.
- The CI widens monotonically with the forecast horizon.
- At step 1, the CI width is approximately `+/- 1.96 * sigma` (the one-step-ahead prediction standard error).
- At longer horizons, the CI width approaches that of an unconditional forecast (essentially the historical variance of the series).

### ACF/PACF Significance Bounds

The horizontal dashed lines on the ACF and PACF plots are at:

```
+/- 1.96 / sqrt(N)
```

where `N` is the number of observations in the series. This is the standard Bartlett bound for testing whether individual autocorrelation coefficients are significantly different from zero under the null hypothesis of white noise.

### Sigmoid Curve Uncertainty Bands

As noted above, the confidence bounds on the main resistance curve are **not statistically derived**. They are manually specified ranges representing the spread across different published estimates and scenarios. They should be interpreted as a plausible range rather than a formal confidence interval.

---

## 5. Limitations and Assumptions

### General Limitations

1. **Conceptual index, not a measurement.** The Resistance Pressure Index is a constructed composite for visualization purposes. It cannot be directly validated against any single observable quantity.

2. **Aggregation masks heterogeneity.** Global aggregates conceal enormous regional, pathogen-level, and healthcare-setting-level variation. A global index of 70 could mean 90 in South Asia and 40 in Scandinavia.

3. **Synthetic time series data.** The monthly data used for SARIMA modeling is entirely synthetic. While calibrated to approximate real-world trends, the seasonal patterns, noise characteristics, and long-term trajectories may not match any real surveillance dataset. Results should be interpreted as demonstrations of methodology, not as real forecasts.

### Sigmoid Curve Assumptions

4. **Logistic growth model.** The assumption that resistance follows a sigmoid (S-curve) trajectory implies a saturation effect near 100%. In reality, resistance dynamics are far more complex, with potential for reversals (as seen with MRSA in Europe), new drug introductions, and evolutionary constraints.

5. **Fixed inflection point.** The inflection point at 2010 is based on expert judgment. If the true inflection is earlier or later, the entire trajectory shifts accordingly.

6. **Independence of pathogens.** The composite index treats all resistance types as additive. In reality, resistance mechanisms interact — for example, plasmid-mediated carbapenem resistance can spread between species.

### SARIMA Assumptions

7. **Stationarity after differencing.** The SARIMAX(1,1,1)(1,1,0,12) model assumes that after one regular and one seasonal difference, the series is stationary. If the underlying trend is nonlinear (e.g., exponential acceleration), the model may underestimate future resistance.

8. **Gaussian errors.** The model assumes normally distributed innovations. Resistance data can exhibit skewness and outliers (e.g., during outbreaks).

9. **Constant parameters.** The model parameters are estimated from the full historical series and assumed constant. In reality, the dynamics of resistance emergence may be changing (e.g., accelerating due to increased antibiotic consumption in LMICs).

10. **No exogenous variables.** The model uses only the historical resistance series itself. It does not incorporate antibiotic consumption data, infection control policy changes, new drug approvals, or other covariates that influence resistance trends.

### Intervention Scenario Assumptions

11. **Linear proportional reduction.** The 30% trend reduction is applied uniformly across the forecast horizon. Real interventions would likely have delayed onset, variable effectiveness, and potential resistance to the intervention itself.

12. **No feedback effects.** The intervention scenario does not account for behavioral responses (e.g., reduced investment in stewardship if resistance appears to be declining).
