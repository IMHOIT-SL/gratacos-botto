"""
Time Series page — SARIMA forecasting with diagnostics (Phase 6).
"""

import sys
import os
import warnings

import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import plotly.graph_objects as go
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.timeseries_data import PATHOGEN_CHOICES, MONTHLY_DATA
from components import help_section, chart_title_with_info

dash.register_page(__name__, path="/timeseries", name="Time Series")

# Suppress convergence warnings from statsmodels during fitting
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

CHART_LAYOUT = dict(
    paper_bgcolor="#21232d",
    plot_bgcolor="#21232d",
    font=dict(color="#e8eaed", family="Inter, sans-serif", size=12),
    xaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
    yaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
)

SVG_CONFIG = {
    "toImageButtonOptions": {"format": "svg", "scale": 3},
    "displayModeBar": True,
}

PATHOGEN_COLORS = {
    "MRSA": "#ffb74d",
    "3GC-R E. coli": "#4fc3f7",
    "CRE K. pneumoniae": "#ef5350",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fit_sarima(series, horizon):
    """
    Fit a SARIMAX model and return forecast + diagnostics.
    Falls back to linear extrapolation on failure.
    """
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX

        model = SARIMAX(
            series,
            order=(1, 1, 1),
            seasonal_order=(1, 1, 0, 12),
            enforce_stationarity=False,
            enforce_invertibility=False,
        )
        results = model.fit(disp=False, maxiter=200)

        forecast = results.get_forecast(steps=horizon)
        forecast_mean = forecast.predicted_mean
        conf_int = forecast.conf_int(alpha=0.05)

        residuals = results.resid
        aic = results.aic
        bic = results.bic

        return {
            "mean": forecast_mean.values,
            "lower": conf_int.iloc[:, 0].values,
            "upper": conf_int.iloc[:, 1].values,
            "residuals": residuals.values,
            "aic": aic,
            "bic": bic,
            "method": "SARIMAX(1,1,1)(1,1,0,12)",
        }
    except Exception:
        # Fallback: linear extrapolation
        t = np.arange(len(series))
        coeffs = np.polyfit(t, series.values, 1)
        t_future = np.arange(len(series), len(series) + horizon)
        forecast_mean = np.polyval(coeffs, t_future)
        residuals = series.values - np.polyval(coeffs, t)
        std_resid = np.std(residuals)

        return {
            "mean": forecast_mean,
            "lower": forecast_mean - 1.96 * std_resid,
            "upper": forecast_mean + 1.96 * std_resid,
            "residuals": residuals,
            "aic": np.nan,
            "bic": np.nan,
            "method": "Linear extrapolation (fallback)",
        }


def compute_acf_pacf(series, nlags=36):
    """Compute ACF and PACF values."""
    try:
        from statsmodels.tsa.stattools import acf, pacf

        acf_vals = acf(series, nlags=nlags, fft=True)
        pacf_vals = pacf(series, nlags=nlags, method="ywm")
        return acf_vals, pacf_vals
    except Exception:
        # Simple manual ACF fallback
        n = len(series)
        mean = np.mean(series)
        var = np.var(series)
        acf_vals = np.array([
            np.sum((series[:n - k] - mean) * (series[k:] - mean)) / (n * var)
            if var > 0 else 0.0
            for k in range(nlags + 1)
        ])
        return acf_vals, acf_vals  # PACF approximated by ACF


def forecast_trend(series, bau):
    """Monthly trend of the BAU forecast, free of seasonality.

    Mean year-over-year change across the forecast months (each forecast
    month minus the same month one year earlier, observed or forecast),
    divided by 12. Year-over-year differences cancel the 12-month season.
    """
    full = np.concatenate([np.asarray(series, dtype=float), np.asarray(bau, dtype=float)])
    n_hist = len(series)
    yoy = [full[n_hist + i] - full[n_hist + i - 12] for i in range(len(bau))]
    return float(np.mean(yoy)) / 12.0


def apply_intervention(bau, slope, reduction, delay):
    """Intervention scenario as a closed-form transform of the BAU forecast.

    The first `delay` forecast months follow BAU unchanged. From then on the
    monthly trend `slope` is reduced by `reduction` (fraction), accumulating
    month by month; seasonality is left untouched and the curve does not
    jump at the start month. No refit, no randomness.
    """
    bau = np.asarray(bau, dtype=float)
    months_active = np.clip(np.arange(len(bau)) - delay + 1, 0, None)
    return bau - reduction * slope * months_active


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

layout = html.Div([
    # Help section
    help_section("Time Series", [
        "WHAT IS SARIMA: SARIMA (Seasonal AutoRegressive Integrated Moving Average) is a statistical forecasting method that decomposes time series data into three components: trend (long-term direction), seasonality (repeating cyclical patterns), and noise (random variation). It then uses the patterns found in historical data to project future values. Unlike machine learning approaches, SARIMA provides interpretable parameters and well-defined confidence intervals, making it widely used in epidemiological forecasting including AMR surveillance. The model captures both short-term autocorrelation (this month's value depends on recent months) and seasonal patterns (resistance rates may fluctuate with antibiotic prescribing seasons).",
        "MODEL PARAMETERS EXPLAINED: The notation SARIMAX(1,1,1)(1,1,0,12) describes the model structure. The first group (1,1,1) specifies: p=1 (one autoregressive lag -- the model uses the previous month's value), d=1 (one differencing step -- the model works with month-to-month changes rather than raw values, which removes trend), q=1 (one moving average term -- the model accounts for the previous month's forecast error). The second group (1,1,0,12) specifies the seasonal component: P=1 (one seasonal autoregressive lag -- last year's same-month value matters), D=1 (seasonal differencing -- removing year-over-year seasonal pattern), Q=0 (no seasonal moving average), s=12 (seasonality period is 12 months). In practical terms, this model says: 'predict next month's resistance rate by considering recent trends, recent forecast errors, and what happened at this time last year.'",
        "READING THE FORECAST CHART: The solid line shows historical (observed) monthly resistance rates. The dashed line extending beyond the historical period shows the model's point forecast -- the single most likely predicted value for each future month. The shaded band around the dashed line is the 95% confidence interval: there is approximately a 95% probability that the actual future value falls within this range, assuming the model is correctly specified and the underlying data-generating process remains stable.",
        "CONFIDENCE INTERVAL WIDTH: The confidence interval widens as the forecast extends further into the future. This is a fundamental property of time series forecasting -- uncertainty accumulates with each additional step ahead. A narrow band at 6 months that becomes very wide at 36 months is normal and expected. For policy purposes, this means short-term forecasts (3-12 months) are actionable for resource planning, while longer-term forecasts (24-36 months) are better treated as directional indicators. If the confidence interval is extremely wide even at short horizons, this suggests the data has high volatility or the model is a poor fit.",
        "SCENARIO COMPARISON: The scenario chart overlays two forecasts. The red dashed line ('Business as usual') is the SARIMA forecast. The green dotted line ('Intervention') is a counterfactual: from the start month you choose, the forecast's monthly trend (the average year-over-year change, which cancels seasonality) is cut by the chosen percentage, and the seasonal pattern is kept. A 30% reduction keeps 70% of the projected trend. The intervention only slows a rising trend: if business as usual already declines (as for MRSA), both lines coincide. It is computed directly from the business-as-usual forecast (no refit, no randomness), so it reproduces exactly. The reduction percentage is an assumption you set, not a measured effect of any specific programme. With 'Show 95% bands' on, the intervention band is the business-as-usual 95% interval shifted with the intervention mean (same forecast uncertainty). Starting later shows how much of the gain is lost by waiting.",
        "ACF/PACF PLOTS: The Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF) plots are diagnostic tools for evaluating time series structure. Each vertical bar shows the correlation between the series and a lagged version of itself (e.g., lag 12 = correlation with the value from 12 months ago). Bars extending beyond the horizontal blue dashed lines are statistically significant. In the ACF, a significant spike at lag 12 confirms annual seasonality. In the PACF, significant spikes indicate the number of direct autoregressive terms needed. For a well-fitted model, the residual ACF/PACF should show no significant spikes (all bars within the blue bands), indicating the model has captured all systematic patterns.",
        "AIC AND BIC: The Akaike Information Criterion (AIC) and Bayesian Information Criterion (BIC) are model selection metrics displayed in the diagnostics panel. Both balance goodness-of-fit against model complexity -- lower values indicate a better model. AIC tends to favor more complex models, while BIC penalizes complexity more heavily. These values are most useful for comparing alternative model specifications (e.g., different p, d, q orders) on the same dataset. An AIC/BIC difference of less than 2 between models suggests they perform similarly; differences greater than 10 indicate strong evidence for the lower-scoring model.",
        "RESIDUAL DIAGNOSTICS: The residuals chart shows the difference between the model's fitted values and the actual historical data at each time point. Good residuals should appear randomly scattered around zero with no visible trends, cycles, or patterns. Systematic patterns in residuals (e.g., consistently positive then negative, or seasonal waves) indicate the model is missing important structure in the data. The residual standard deviation, displayed above the chart, quantifies typical forecast error magnitude.",
        "IMPORTANT LIMITATIONS: The monthly resistance data underlying these models is synthetic -- generated to match the scale, trend, and seasonal characteristics of published AMR surveillance data, but not drawn from actual laboratory results. The SARIMA approach assumes that future patterns will resemble past patterns (stationarity after differencing), which may not hold if there are major disruptions (new antibiotics introduced, pandemic-related changes in prescribing, novel resistance mechanisms emerging). These forecasts should be interpreted as illustrative of the methodology rather than as operational predictions.",
        "EXTENDING THIS ANALYSIS: Researchers can adapt this approach with their own surveillance data by: (1) replacing the synthetic monthly series with real resistance rates from their institution or national surveillance system, (2) using the ACF/PACF diagnostics to select appropriate model orders for their data, (3) comparing multiple SARIMA specifications using AIC/BIC to find the best fit, and (4) incorporating exogenous variables (antibiotic consumption data, infection control policy changes) using the SARIMAX framework's exogenous regressor capability.",
    ]),

    # Controls row
    html.Div([
        html.Div([
            html.H3("SARIMA Time Series Forecasting", className="card-title"),
            html.P(
                "Fit seasonal ARIMA models to monthly resistance data and "
                "generate forecasts with confidence intervals.",
                className="card-subtitle",
            ),
        ]),
        html.Div([
            html.Div([
                html.Label("Pathogen", style={"fontWeight": "600", "marginBottom": "0.4rem", "display": "block"}),
                dmc.SegmentedControl(
                    id="ts-pathogen-dropdown",
                    data=[{"label": p, "value": p} for p in PATHOGEN_CHOICES],
                    value="MRSA",
                    color="cyan",
                    radius="md",
                    fullWidth=True,
                ),
            ], style={"flex": "1 1 340px"}),
            html.Div([
                html.Label("Forecast horizon (months)", style={"fontWeight": "600", "marginBottom": "0.4rem", "display": "block"}),
                dmc.SegmentedControl(
                    id="ts-horizon-slider",
                    data=[
                        {"label": "6 m", "value": "6"},
                        {"label": "12 m", "value": "12"},
                        {"label": "24 m", "value": "24"},
                        {"label": "36 m", "value": "36"},
                    ],
                    value="12",
                    color="cyan",
                    radius="md",
                ),
            ], style={"flex": "0 0 auto"}),
        ], style={"display": "flex", "alignItems": "flex-end", "flexWrap": "wrap", "gap": "1.25rem"}),
    ], className="card"),

    # Main forecast chart
    html.Div([
        chart_title_with_info(
            "Historical Data + SARIMA Forecast",
            "Historical monthly resistance rates with SARIMAX(1,1,1)(1,1,0,12) forecast. The shaded band shows the 95% confidence interval \u2014 wider bands indicate greater uncertainty in predictions.",
        ),
        html.P(id="ts-model-label", className="card-subtitle"),
        dcc.Loading(dcc.Graph(id="ts-main-chart", config=SVG_CONFIG), type="default", color="#4fc3f7"),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            "Synthetic data generated from published AMR trends. Model: SARIMAX(1,1,1)(1,1,0,12). Based on methodology from: ",
            html.A("Kim et al. 2023 (SARIMA for AMR)", href="https://pubmed.ncbi.nlm.nih.gov/37250043/", target="_blank"),
            " · ",
            html.A("Arepyeva et al. 2017", href="https://pubmed.ncbi.nlm.nih.gov/28167308/", target="_blank"),
        ], className="chart-sources"),
    ], className="card"),

    # Scenario comparison (adjustable intervention)
    html.Div([
        chart_title_with_info(
            "Scenario Comparison",
            "Business as usual (red) is the SARIMA forecast above. The intervention (green) "
            "cuts the forecast's monthly trend by the chosen percentage from the start month on, "
            "keeping the seasonal pattern. "
            "The reduction is your assumption, not a measured effect.",
            "Business as usual vs. an adjustable intervention",
        ),
        html.Div([
            html.Div([
                html.Label("Trend reduction", style={"fontWeight": "600", "display": "block", "marginBottom": "0.5rem"}),
                dmc.Slider(
                    id="ts-int-reduction", min=0, max=100, step=5, value=30, color="green",
                    marks=[{"value": v, "label": f"{v}%"} for v in (0, 25, 50, 75, 100)],
                ),
            ], style={"flex": "1 1 280px", "minWidth": "240px", "paddingBottom": "1.2rem"}),
            html.Div([
                html.Label("Intervention starts", style={"fontWeight": "600", "display": "block", "marginBottom": "0.4rem"}),
                dmc.SegmentedControl(
                    id="ts-int-delay",
                    data=[
                        {"label": "Now", "value": "0"},
                        {"label": "+6 m", "value": "6"},
                        {"label": "+12 m", "value": "12"},
                        {"label": "+24 m", "value": "24"},
                    ],
                    value="0", color="green", radius="md",
                ),
            ], style={"flex": "0 0 auto"}),
            html.Div([
                dmc.Switch(id="ts-int-band", label="Show 95% bands", checked=False, color="green"),
            ], style={"flex": "0 0 auto", "paddingBottom": "0.4rem"}),
        ], style={"display": "flex", "alignItems": "flex-end", "flexWrap": "wrap", "gap": "1.5rem",
                  "margin": "0.8rem 0 1rem"}),
        html.Div(id="ts-scenario-stats", className="stats-row"),
        dcc.Loading(dcc.Graph(id="ts-scenario-chart", config=SVG_CONFIG), type="default", color="#4fc3f7"),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            "Forecast: SARIMAX(1,1,1)(1,1,0,12) on the synthetic monthly series above. "
            "Intervention: user-defined assumption (no published source).",
        ], className="chart-sources"),
    ], className="card"),

    # Diagnostics row
    html.Div([
        html.Div([
            chart_title_with_info(
                "Model Diagnostics",
                "Model residuals (observed - predicted). A good model should show residuals randomly distributed around zero with no patterns. Systematic patterns suggest model misspecification.",
            ),
            html.Div(id="ts-diag-stats", style={"marginBottom": "0.5rem"}),
            dcc.Graph(id="ts-residuals-chart", config=SVG_CONFIG),
        ], className="card"),
        html.Div([
            chart_title_with_info(
                "Correlogram (ACF / PACF)",
                "Autocorrelation (ACF) and Partial Autocorrelation (PACF) functions. Bars outside the blue confidence band indicate significant correlations at that lag. Useful for diagnosing seasonal patterns and model adequacy.",
                "Autocorrelation and partial autocorrelation of the raw series",
            ),
            dcc.Graph(id="ts-acf-chart", config=SVG_CONFIG),
            dcc.Graph(id="ts-pacf-chart", config=SVG_CONFIG),
        ], className="card"),
    ], className="chart-grid-2"),
])


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

# Deterministic model (fixed seed) -> the SARIMA fits are identical every time,
# so cache per (pathogen, horizon): compute once, then serve instantly. This is
# what makes the page slow on first load (statsmodels MLE fit); everything else
# on the site is precomputed.
_TS_CACHE = {}


@callback(
    Output("ts-main-chart", "figure"),
    Output("ts-model-label", "children"),
    Output("ts-residuals-chart", "figure"),
    Output("ts-diag-stats", "children"),
    Output("ts-acf-chart", "figure"),
    Output("ts-pacf-chart", "figure"),
    Input("ts-pathogen-dropdown", "value"),
    Input("ts-horizon-slider", "value"),
)
def update_timeseries(pathogen, horizon):
    horizon = int(horizon)  # SegmentedControl returns the value as a string
    key = (pathogen, horizon)
    cached = _TS_CACHE.get(key)
    if cached is not None:
        return cached
    result = _compute_timeseries(pathogen, horizon)
    _TS_CACHE[key] = result
    return result


_FIT_CACHE = {}


def _get_fit(pathogen, horizon):
    """Series + SARIMA fit for (pathogen, horizon), fitted once and cached."""
    key = (pathogen, horizon)
    if key not in _FIT_CACHE:
        df = MONTHLY_DATA[pathogen].copy()
        series = df.set_index("date")["resistance_rate"]
        series.index = pd.DatetimeIndex(series.index, freq="MS")
        _FIT_CACHE[key] = (series, fit_sarima(series, horizon))
    return _FIT_CACHE[key]


def _compute_timeseries(pathogen, horizon):
    series, result = _get_fit(pathogen, horizon)
    color = PATHOGEN_COLORS.get(pathogen, "#4fc3f7")

    # Forecast dates
    last_date = series.index[-1]
    forecast_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1),
        periods=horizon,
        freq="MS",
    )

    # --- Compute x-axis zoom range based on horizon ---
    # Show enough history to give context but keep forecast visually prominent
    history_months_map = {6: 24, 12: 36, 24: 48, 36: 60}
    history_months = history_months_map.get(horizon, horizon * 2)
    x_range_start = last_date - pd.DateOffset(months=history_months)
    x_range_end = forecast_dates[-1] + pd.DateOffset(months=1)

    # --- Main chart ---
    fig_main = go.Figure()

    # Confidence band (more opaque fill)
    fig_main.add_trace(go.Scatter(
        x=list(forecast_dates) + list(forecast_dates[::-1]),
        y=list(result["upper"]) + list(result["lower"][::-1]),
        fill="toself",
        fillcolor=f"rgba({_hex_to_rgb(color)}, 0.35)",
        line=dict(width=0),
        name="95% CI",
        hoverinfo="skip",
    ))

    # Historical (thinner line so forecast stands out)
    fig_main.add_trace(go.Scatter(
        x=series.index,
        y=series.values,
        mode="lines",
        line=dict(color=color, width=1.5),
        name="Historical",
        hovertemplate="%{x|%b %Y}<br>%{y:.1f}%<extra>Historical</extra>",
    ))

    # Forecast mean (thicker line for emphasis)
    fig_main.add_trace(go.Scatter(
        x=forecast_dates,
        y=result["mean"],
        mode="lines",
        line=dict(color=color, width=3, dash="dash"),
        name="Forecast",
        hovertemplate="%{x|%b %Y}<br>%{y:.1f}%<extra>Forecast</extra>",
    ))

    # Vertical line at forecast start (use add_shape + add_annotation to avoid Plotly sum() bug)
    last_date_str = last_date.isoformat() if hasattr(last_date, "isoformat") else str(last_date)
    fig_main.add_shape(
        type="line", x0=last_date_str, x1=last_date_str, y0=0, y1=1,
        yref="paper", line=dict(dash="dot", color="#9aa0a6", width=1.5),
    )
    fig_main.add_annotation(
        x=last_date_str, y=1, yref="paper",
        text="Forecast start", showarrow=False,
        font=dict(size=11, color="#9aa0a6"), xanchor="left", yanchor="bottom",
    )

    fig_main.update_layout(
        **CHART_LAYOUT,
        title=dict(text=f"{pathogen} — Resistance Rate Forecast", font=dict(size=15)),
        xaxis_title="Date",
        yaxis_title="% Resistant Isolates",
        xaxis_range=[x_range_start, x_range_end],
        height=420,
        margin=dict(l=60, r=30, t=55, b=50),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )

    model_label = f"Model: {result['method']}"

    # --- Residuals chart ---
    fig_resid = go.Figure()
    resid = result["residuals"]
    resid_dates = series.index[:len(resid)]

    fig_resid.add_trace(go.Bar(
        x=resid_dates,
        y=resid,
        marker_color=[
            "#ef5350" if v < 0 else "#66bb6a" for v in resid
        ],
        hovertemplate="%{x|%b %Y}<br>Residual: %{y:.2f}<extra></extra>",
    ))

    fig_resid.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Model Residuals", font=dict(size=13)),
        xaxis_title="Date",
        yaxis_title="Residual",
        height=300,
        margin=dict(l=55, r=20, t=40, b=40),
        showlegend=False,
    )

    # --- Diagnostic stats ---
    aic_str = f"{result['aic']:.1f}" if not np.isnan(result['aic']) else "N/A"
    bic_str = f"{result['bic']:.1f}" if not np.isnan(result['bic']) else "N/A"
    diag_stats = html.Div([
        html.Span(f"AIC: {aic_str}", className="source-tag", style={"marginRight": "1rem"}),
        html.Span(f"BIC: {bic_str}", className="source-tag", style={"marginRight": "1rem"}),
        html.Span(
            f"Residual std: {np.std(resid):.2f}",
            className="source-tag",
        ),
    ])

    # --- ACF / PACF ---
    nlags = min(36, len(series) // 3)
    acf_vals, pacf_vals = compute_acf_pacf(series.values, nlags=nlags)
    conf_bound = 1.96 / np.sqrt(len(series))

    fig_acf = go.Figure()
    lags = list(range(len(acf_vals)))

    fig_acf.add_trace(go.Bar(
        x=lags,
        y=acf_vals,
        marker_color="#4fc3f7",
        width=0.4,
        hovertemplate="Lag %{x}<br>ACF: %{y:.3f}<extra></extra>",
    ))
    fig_acf.add_hline(y=conf_bound, line_dash="dot", line_color="#9aa0a6", line_width=1)
    fig_acf.add_hline(y=-conf_bound, line_dash="dot", line_color="#9aa0a6", line_width=1)

    fig_acf.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Autocorrelation (ACF)", font=dict(size=13)),
        xaxis_title="Lag",
        yaxis_title="ACF",
        height=260,
        margin=dict(l=55, r=20, t=40, b=40),
        showlegend=False,
    )

    fig_pacf = go.Figure()
    pacf_lags = list(range(len(pacf_vals)))

    fig_pacf.add_trace(go.Bar(
        x=pacf_lags,
        y=pacf_vals,
        marker_color="#ffb74d",
        width=0.4,
        hovertemplate="Lag %{x}<br>PACF: %{y:.3f}<extra></extra>",
    ))
    fig_pacf.add_hline(y=conf_bound, line_dash="dot", line_color="#9aa0a6", line_width=1)
    fig_pacf.add_hline(y=-conf_bound, line_dash="dot", line_color="#9aa0a6", line_width=1)

    fig_pacf.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Partial Autocorrelation (PACF)", font=dict(size=13)),
        xaxis_title="Lag",
        yaxis_title="PACF",
        height=260,
        margin=dict(l=55, r=20, t=40, b=40),
        showlegend=False,
    )

    return fig_main, model_label, fig_resid, diag_stats, fig_acf, fig_pacf


def _hex_to_rgb(hex_color):
    """Convert hex color to 'r, g, b' string for rgba()."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{r}, {g}, {b}"


# ---------------------------------------------------------------------------
# Scenario comparison: adjustable intervention (own callback, reuses the fit)
# ---------------------------------------------------------------------------

def _scenario_stat(value, label, cls):
    return html.Div([
        html.Div(value, className=f"stat-value {cls}", style={"fontSize": "1.6rem"}),
        html.Div(label, className="stat-label"),
    ], className="stat-card")


@callback(
    Output("ts-scenario-chart", "figure"),
    Output("ts-scenario-stats", "children"),
    Input("ts-pathogen-dropdown", "value"),
    Input("ts-horizon-slider", "value"),
    Input("ts-int-reduction", "value"),
    Input("ts-int-delay", "value"),
    Input("ts-int-band", "checked"),
)
def update_scenario(pathogen, horizon, reduction, delay, show_band):
    horizon, delay = int(horizon), int(delay)  # SegmentedControl values are strings
    series, result = _get_fit(pathogen, horizon)
    red = reduction / 100.0
    last_date = series.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.DateOffset(months=1),
                                   periods=horizon, freq="MS")
    bau = np.asarray(result["mean"], dtype=float)
    slope = forecast_trend(series.values, bau)
    # An intervention slows a rising trend; it never slows an existing decline
    interv = apply_intervention(bau, max(slope, 0.0), red, delay)
    shift = interv - bau  # intervention band = BAU 95% CI shifted with the mean

    history_months = {6: 24, 12: 36, 24: 48, 36: 60}.get(horizon, horizon * 2)
    x_range_start = last_date - pd.DateOffset(months=history_months)
    x_range_end = forecast_dates[-1] + pd.DateOffset(months=1)

    fig = go.Figure()
    if show_band:
        for lo, hi, col, nm in (
            (result["lower"], result["upper"], "239, 83, 80", "BAU 95% CI"),
            (np.asarray(result["lower"]) + shift, np.asarray(result["upper"]) + shift,
             "102, 187, 106", "Intervention 95% CI"),
        ):
            fig.add_trace(go.Scatter(
                x=list(forecast_dates) + list(forecast_dates[::-1]),
                y=list(hi) + list(lo[::-1]),
                fill="toself", fillcolor=f"rgba({col}, 0.15)", line=dict(width=0),
                name=nm, hoverinfo="skip",
            ))
    fig.add_trace(go.Scatter(
        x=series.index, y=series.values, mode="lines",
        line=dict(color="#9aa0a6", width=1.5), name="Historical",
        hovertemplate="%{x|%b %Y}<br>%{y:.1f}%<extra>Historical</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=bau, mode="lines",
        line=dict(color="#ef5350", width=2.5, dash="dash"), name="Business as usual",
        hovertemplate="%{x|%b %Y}<br>%{y:.1f}%<extra>BAU</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=interv, mode="lines",
        line=dict(color="#66bb6a", width=2.5, dash="dot"),
        name=f"Intervention (-{reduction}% trend)",
        hovertemplate="%{x|%b %Y}<br>%{y:.1f}%<extra>Intervention</extra>",
    ))

    last_date_str = last_date.isoformat()
    fig.add_shape(type="line", x0=last_date_str, x1=last_date_str, y0=0, y1=1,
                  yref="paper", line=dict(dash="dot", color="#9aa0a6", width=1.5))
    fig.add_annotation(x=last_date_str, y=1, yref="paper", text="Forecast start",
                       showarrow=False, font=dict(size=11, color="#9aa0a6"),
                       xanchor="left", yanchor="bottom")
    if 0 < delay < horizon:
        start_str = forecast_dates[delay].isoformat()
        fig.add_shape(type="line", x0=start_str, x1=start_str, y0=0, y1=1,
                      yref="paper", line=dict(dash="dash", color="#66bb6a", width=1.2))
        fig.add_annotation(x=start_str, y=0, yref="paper", text="Intervention starts",
                           showarrow=False, font=dict(size=11, color="#66bb6a"),
                           xanchor="left", yanchor="bottom", xshift=4)

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=f"{pathogen}: business as usual vs intervention", font=dict(size=15)),
        xaxis_title="Date", yaxis_title="% Resistant Isolates",
        xaxis_range=[x_range_start, x_range_end],
        height=420, margin=dict(l=60, r=30, t=55, b=50),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )

    end_label = forecast_dates[-1].strftime("%b %Y")
    if delay >= horizon:
        stats = [html.P(
            f"The intervention starts after the {horizon}-month horizon, so it has no "
            "effect in this window. Choose a longer horizon or an earlier start.",
            style={"fontSize": "0.82rem", "color": "var(--warning)", "margin": "0"},
        )]
    elif slope <= 0:
        stats = [html.P(
            f"Business as usual already projects a declining trend for {pathogen} "
            f"({slope:+.2f} percentage points per month), so a trend reduction has "
            "nothing to slow: both lines coincide.",
            style={"fontSize": "0.82rem", "color": "var(--warning)", "margin": "0"},
        )]
    else:
        diff = bau[-1] - interv[-1]
        stats = [
            _scenario_stat(f"{bau[-1]:.1f}%", f"Business as usual, {end_label}", "danger"),
            _scenario_stat(f"{interv[-1]:.1f}%", f"Intervention, {end_label}", "success"),
            _scenario_stat(f"-{diff:.1f} pp" if diff >= 0 else f"+{-diff:.1f} pp",
                           "Difference at horizon (percentage points)", "accent"),
        ]
    return fig, stats


# Warm the default view (MRSA, 12-month horizon) in the background at import, so
# the first visit to /timeseries is instant instead of ~10s. Daemon thread ->
# does not block gunicorn startup or the DO health check; the cache fills a few
# seconds after boot.
import threading as _threading


def _warm_default_ts_cache():
    try:
        _TS_CACHE[("MRSA", 12)] = _compute_timeseries("MRSA", 12)  # also fills _FIT_CACHE
    except Exception:
        pass


_threading.Thread(target=_warm_default_ts_cache, daemon=True).start()
