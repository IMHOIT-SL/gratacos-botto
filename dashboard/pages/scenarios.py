"""
Scenario Lab page: what-if interventions on the paper's super-exponential
model. Exploratory sensitivity analysis, not part of the paper's forecast.

Two levers act on the model's own parameters from a chosen start year:
  * stewardship   reduces the base rate r          (r -> r·(1 - s))
  * new drugs     reduces the acceleration b       (b -> b·(1 - p))
Everything is closed-form (see data/amr_data.py, compute_scenario_curve).
"""

import math
import sys
import os

import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.amr_data import (
    SUPER_EXP_PARAMS,
    OBSERVED_DATA,
    CRITICAL_THRESHOLD,
    compute_scenario_curve,
    scenario_crossing_year,
)
from components import help_section, chart_title_with_info, graph_config

from i18n import translate, translated, current_lang
from model_cards import model_card, live_equation

dash.register_page(__name__, path="/scenarios", name="Scenario Lab")

PAPER_URL = "https://doi.org/10.5281/zenodo.21898960"

CHART_LAYOUT = dict(
    paper_bgcolor="#21232d",
    plot_bgcolor="#21232d",
    font=dict(color="#e8eaed", family="Inter, sans-serif", size=12),
    xaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
    yaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
)

SVG_CONFIG = graph_config()

BASE_COLOR = "#4fc3f7"
SCEN_COLOR = "#66bb6a"
THRESH_COLOR = "#ef5350"

# Illustrative presets. The percentages are hypothetical lever settings,
# not values taken from the paper or from any intervention study.
PRESETS = {
    "baseline":  {"s": 0,  "p": 0,  "start": 2027},
    "moderate":  {"s": 15, "p": 30, "start": 2027},
    "ambitious": {"s": 30, "p": 60, "start": 2027},
    "late":      {"s": 30, "p": 60, "start": 2035},
}

END_YEAR = 2100


def _threshold_year(year):
    """First calendar year with index >= threshold (matches the Overview's 2047)."""
    return None if year is None or year > END_YEAR else math.ceil(year - 1e-9)


def _label(slider_title, slider_id, value, help_text, **kw):
    return html.Div([
        html.Label(slider_title, style={"fontWeight": "600", "display": "block"}),
        html.P(help_text, style={"fontSize": "0.75rem", "color": "var(--text-secondary)",
                                 "margin": "0.15rem 0 0.6rem"}),
        dmc.Slider(id=slider_id, value=value, color="cyan", **kw),
    ], style={"flex": "1 1 260px", "minWidth": "240px", "paddingBottom": "1.2rem"})


controls = html.Div([
    html.Div([
        html.Label("Preset", style={"fontWeight": "600", "marginBottom": "0.4rem", "display": "block"}),
        dmc.SegmentedControl(
            id="scn-preset",
            data=[
                {"label": "No intervention", "value": "baseline"},
                {"label": "Moderate", "value": "moderate"},
                {"label": "Ambitious", "value": "ambitious"},
                {"label": "Ambitious, late (2035)", "value": "late"},
            ],
            value="moderate",
            color="cyan",
            radius="md",
        ),
    ], style={"marginBottom": "1.2rem"}),
    html.Div([
        _label("Stewardship (slows the base rate r)", "scn-stewardship", 15,
               "Prudent prescribing, diagnostics, infection control. "
               "Reduces the model's base rate of resistance growth by this percentage.",
               min=0, max=100, step=1,
               marks=[{"value": v, "label": f"{v}%"} for v in (0, 25, 50, 75, 100)]),
        _label("New antibiotics (slows the acceleration b)", "scn-pipeline", 30,
               "New drug classes and pipeline investment. Reduces the super-exponential "
               "acceleration (how fast the rate itself grows) by this percentage.",
               min=0, max=100, step=1,
               marks=[{"value": v, "label": f"{v}%"} for v in (0, 25, 50, 75, 100)]),
        _label("Intervention starts in", "scn-start", 2027,
               "Before this year the curve follows the paper's model exactly.",
               min=2026, max=2045, step=1,
               marks=[{"value": v, "label": str(v)} for v in (2026, 2030, 2035, 2040, 2045)]),
    ], style={"display": "flex", "gap": "2rem", "flexWrap": "wrap"}),
], className="card")


_layout = html.Div([
    help_section("Scenario Lab", [
        "PURPOSE: This page answers one question: how many years before the critical inefficacy threshold (~95) do we gain if we act, and how much does it matter when we start? It applies hypothetical interventions to the paper's super-exponential model and redraws the curve instantly.",
        "WHAT THIS IS NOT: The paper does not quantify the effect of any intervention. The lever percentages are assumptions you choose, not measured effects, and the presets are illustrative. Read the results as the sensitivity of the paper's model to those assumptions, not as a prediction.",
        "THE MODEL: The paper's curve is y(τ) = K / (1 + A·exp(-r·τ - b·τ²)), τ = year - 1990, with K = 100, A = 88/12, r = 0.0705, b = 3.05·10⁻⁴. Its effective rate r + 2bτ grows every year: that is the paper's thesis that 'the rate of increasing resistance is itself growing'.",
        "THE LEVERS: From the start year on, Stewardship multiplies the base rate r by (1 - s) and New antibiotics multiplies the acceleration b by (1 - p). Before the start year the curve is identical to the paper's. The curve bends at the start year without jumping (the exponent is continuous).",
        "THRESHOLD YEAR: The crossing of the ~95 threshold is solved exactly with the quadratic formula, then reported as the first calendar year with index ≥ 95 (2047 with no intervention, the same year shown on the Overview page).",
        "DETERMINISM: Closed-form only. No fitting, no random sampling: the same settings always give the same curve and the same years, on any machine.",
        "WHY STARTING LATE COSTS SO MUCH: Under a super-exponential model the rate keeps growing while we wait, so the same intervention buys fewer years the later it starts. Compare 'Ambitious' with 'Ambitious, late (2035)'.",
    ]),

    html.Div([
        html.Strong("Exploratory what-if, not part of the paper's forecast. "),
        "The interventions are hypothetical assumptions applied to the paper's model ",
        html.A("(Prieto Gratacós & Botto, Br J Med Health Res 2026)", href=PAPER_URL, target="_blank"),
        ". They show how sensitive the threshold year is to acting, and to acting early.",
    ], className="scn-disclaimer"),

    controls,

    html.Div(id="scn-stats", className="stats-row"),

    html.Div([
        chart_title_with_info(
            "Resistance pressure index: no intervention vs your scenario",
            "Blue: the paper's super-exponential model. Green: the same model with your "
            "interventions from the start year on. Red dotted line: critical inefficacy "
            "threshold (~95). Markers show the first year at or above the threshold.",
            subtitle="Closed-form model (computed to 2100). Observed anchor points 1990-2025 shown as circles.",
        ),
        dcc.Graph(id="scn-curve", config=SVG_CONFIG),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            html.A("Super-exponential model: Prieto Gratacós & Botto, Br J Med Health Res 2026",
                   href=PAPER_URL, target="_blank"),
            " · Interventions: user-defined assumptions (no published source)",
        ], className="chart-sources"),
        model_card("scenario", open=True),
    ], className="card"),

    html.Div([
        chart_title_with_info(
            "Effective rate of resistance growth",
            "The yearly growth rate of the model's exponent, r + 2bτ. In the paper's model "
            "it rises every year (the rate is itself growing). Your interventions lower its "
            "level (stewardship) and its slope (new antibiotics).",
            subtitle="Why acting early matters: the blue line never stops climbing.",
        ),
        dcc.Graph(id="scn-rate", config=SVG_CONFIG),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            html.A("Prieto Gratacós & Botto, Br J Med Health Res 2026 (Discussion)",
                   href=PAPER_URL, target="_blank"),
        ], className="chart-sources"),
        model_card("rate", open=True),
    ], className="card"),
])


@callback(
    Output("scn-stewardship", "value"),
    Output("scn-pipeline", "value"),
    Output("scn-start", "value"),
    Input("scn-preset", "value"),
    prevent_initial_call=True,
)
def apply_preset(preset):
    p = PRESETS[preset]
    return p["s"], p["p"], p["start"]


def _stat(value, label, cls):
    return html.Div([
        html.Div(value, className=f"stat-value {cls}"),
        html.Div(label, className="stat-label"),
    ], className="stat-card")


@callback(
    Output("scn-curve", "figure"),
    Output("scn-rate", "figure"),
    Output("scn-stats", "children"),
    Output({"type": "mc-live", "card": "scenario"}, "children"),
    Output({"type": "mc-live", "card": "rate"}, "children"),
    Input("scn-stewardship", "value"),
    Input("scn-pipeline", "value"),
    Input("scn-start", "value"),
)
@translated
def update_scenario(stewardship, pipeline, start_year):
    s, p, start_year = stewardship / 100.0, pipeline / 100.0, int(start_year)
    df = compute_scenario_curve(s, p, start_year, end=END_YEAR)
    base_year = _threshold_year(scenario_crossing_year(0.0, 0.0, start_year))
    scen_year = _threshold_year(scenario_crossing_year(s, p, start_year))

    # --- stats ---
    if scen_year is None:
        gained, scen_txt = f"> {END_YEAR - base_year}", f"after {END_YEAR}"
    else:
        gained, scen_txt = f"+{scen_year - base_year}", str(scen_year)
    row_2040 = df[df["year"] == 2040].iloc[0]
    stats = [
        _stat(str(base_year), "Threshold year, no intervention", "danger"),
        _stat(scen_txt, "Threshold year, your scenario", "success"),
        _stat(gained, "Years gained", "accent"),
        _stat(f"{row_2040['baseline']:.0f} → {row_2040['scenario']:.0f}",
              "Index in 2040 (no intervention → scenario)", "warning"),
    ]

    # Show 1990-2080 unless the scenario crosses later
    x_end = 2080 if scen_year is not None and scen_year <= 2075 else END_YEAR

    # --- main curve ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["year"], y=df["baseline"], name="No intervention (paper's model)",
        line=dict(color=BASE_COLOR, width=3),
        hovertemplate="%{y:.1f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["year"], y=df["scenario"], name="Your scenario",
        line=dict(color=SCEN_COLOR, width=3),
        hovertemplate="%{y:.1f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=OBSERVED_DATA["year"], y=OBSERVED_DATA["resistance_index"],
        name="Observed anchors (1990-2025)", mode="markers",
        marker=dict(color=BASE_COLOR, size=7, line=dict(color="#e8eaed", width=1)),
        hovertemplate="%{y} (%{text})<extra></extra>", text=OBSERVED_DATA["source"],
    ))
    for yr, col, nm in ((base_year, BASE_COLOR, "No intervention"), (scen_year, SCEN_COLOR, "Scenario")):
        if yr is not None:
            fig.add_trace(go.Scatter(
                x=[yr], y=[CRITICAL_THRESHOLD], mode="markers+text", showlegend=False,
                marker=dict(color=col, size=13, symbol="diamond", line=dict(color="#e8eaed", width=1)),
                text=[str(yr)], textposition="bottom center", textfont=dict(color=col, size=12),
                hovertemplate=f"{nm} reaches the threshold in %{{x}}<extra></extra>",
            ))
    fig.add_shape(type="line", x0=1990, x1=x_end, y0=CRITICAL_THRESHOLD, y1=CRITICAL_THRESHOLD,
                  line=dict(color=THRESH_COLOR, width=1, dash="dot"))
    fig.add_annotation(x=1992, y=CRITICAL_THRESHOLD, text="Critical inefficacy threshold (~95)",
                       showarrow=False, yshift=10, xanchor="left",
                       font=dict(color=THRESH_COLOR, size=11))
    fig.add_shape(type="line", x0=start_year, x1=start_year, y0=0, y1=100,
                  line=dict(color=SCEN_COLOR, width=1, dash="dash"))
    fig.add_annotation(x=start_year, y=8, text=f"Intervention starts ({start_year})",
                       showarrow=False, xanchor="left", xshift=4,
                       font=dict(color=SCEN_COLOR, size=11))
    fig.update_layout(
        **CHART_LAYOUT, height=480, margin=dict(l=50, r=20, t=20, b=40),
        yaxis_title="Resistance pressure index (0-100)", yaxis_range=[0, 102],
        xaxis_title="Year", xaxis_range=[1990, x_end],
        legend=dict(orientation="h", y=-0.15, x=0),
        hovermode="x unified",
    )

    # --- effective rate ---
    rate = go.Figure()
    rate.add_trace(go.Scatter(
        x=df["year"], y=df["rate_baseline"], name="No intervention",
        line=dict(color=BASE_COLOR, width=3),
        hovertemplate="%{y:.4f}<extra></extra>",
    ))
    rate.add_trace(go.Scatter(
        x=df["year"], y=df["rate_scenario"], name="Your scenario",
        line=dict(color=SCEN_COLOR, width=3),
        hovertemplate="%{y:.4f}<extra></extra>",
    ))
    rate.add_shape(type="line", x0=start_year, x1=start_year, y0=0, y1=1, yref="paper",
                   line=dict(color=SCEN_COLOR, width=1, dash="dash"))
    rate.update_layout(
        **CHART_LAYOUT, height=340, margin=dict(l=50, r=20, t=20, b=40),
        yaxis_title="Effective rate r + 2bτ (per year)", yaxis_rangemode="tozero",
        xaxis_title="Year", xaxis_range=[1990, END_YEAR],
        legend=dict(orientation="h", y=-0.22, x=0),
        hovermode="x unified",
    )
    # Live equations for the model cards (numbers of the current scenario)
    lang = current_lang()
    P = SUPER_EXP_PARAMS
    r2, b2 = P["r"] * (1 - s), P["b"] * (1 - p)
    tau_s = start_year - P["t0"]
    year_tex = str(scen_year) if scen_year is not None else r"> " + str(END_YEAR)
    live_scn = live_equation(
        rf"$$r'=r\,(1-s)={P['r']:.4f}\,(1-{s:.2f})={r2:.4f}\qquad "
        rf"b'=b\,(1-p)={P['b']:.6f}\,(1-{p:.2f})={b2:.6f}$$"
        rf"$$\tau_s={tau_s}\;({start_year})\qquad \tau_{{95}}\;\Rightarrow\;{year_tex}$$", lang)
    tau40 = 2040 - P["t0"]
    reff0 = P["r"] + 2 * P["b"] * tau40
    reff1 = (r2 + 2 * b2 * tau40) if 2040 >= start_year else reff0
    live_rate = live_equation(
        rf"$$r_{{\mathrm{{ef}}}}(2040)=r+2b\,\tau={P['r']:.4f}+2\cdot{P['b']:.6f}\cdot{tau40}={reff0:.4f}$$"
        rf"$$r'_{{\mathrm{{ef}}}}(2040)={r2:.4f}+2\cdot{b2:.6f}\cdot{tau40}={reff1:.4f}$$", lang)
    return fig, rate, stats, live_scn, live_rate


def layout(lang=None, **_query):
    """Page layout in the visitor's language (?lang=, cookie or browser)."""
    return translate(_layout, current_lang(lang))
