"""
Overview page — Main AMR resistance curve (super-exponential thesis,
Gratacós-Botto v.A-29) + mortality projections + reference data table.
"""

import dash
from dash import html, dcc
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.amr_data import (
    compute_super_exponential_curve,
    compute_reference_logistic_curve,
    OBSERVED_DATA,
    FORECAST_DATA,
    MORTALITY_DATA,
    CARBAPENEM_PROJECTION,
)
from components import help_section, chart_title_with_info

dash.register_page(__name__, path="/", name="Overview")

SOURCE_URLS = {
    "Oxford VG baseline": "https://www.ovg.ox.ac.uk/news/antibiotic-resistance",
    "Oxford VG (MRSA/ESBL era)": "https://www.ovg.ox.ac.uk/news/antibiotic-resistance",
    "Oxford VG": "https://www.ovg.ox.ac.uk/news/antibiotic-resistance",
    "Lancet GBD": "https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext",
    "Lancet GBD (CRE/XDR-TB rise)": "https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext",
    "Murray et al. 2022 (1.27M deaths)": "https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext",
    "Lancet GBD update": "https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(24)01867-1/fulltext",
    "CIDRAP/GRAM projection": "https://www.cidrap.umn.edu/antimicrobial-stewardship/study-forecasts-more-39-million-deaths-antimicrobial-resistance-2050",
    "CIDRAP/GRAM": "https://www.cidrap.umn.edu/antimicrobial-stewardship/study-forecasts-more-39-million-deaths-antimicrobial-resistance-2050",
    "GRAM forecast": "https://www.cidrap.umn.edu/antimicrobial-stewardship/study-forecasts-more-39-million-deaths-antimicrobial-resistance-2050",
    "Gratacós-Botto v.A-29 (párr. 19)": "#",
    "Gratacós-Botto v.A-29 (critical point)": "#",
    "O'Neill trajectory": "https://amr-review.org/sites/default/files/160518_Final%20paper_with%20cover.pdf",
    "Critical threshold": "https://www.nature.com/articles/s41564-024-01891-8",
    "O'Neill 10M deaths/yr": "https://amr-review.org/sites/default/files/160518_Final%20paper_with%20cover.pdf",
    "Extrapolation": "https://www.cidrap.umn.edu/antimicrobial-stewardship/study-forecasts-more-39-million-deaths-antimicrobial-resistance-2050",
    "Asymptotic": "https://www.cidrap.umn.edu/antimicrobial-stewardship/study-forecasts-more-39-million-deaths-antimicrobial-resistance-2050",
    "GRAM/O'Neill interpolation": "https://amr-review.org/sites/default/files/160518_Final%20paper_with%20cover.pdf",
    "GRAM projection": "https://www.cidrap.umn.edu/antimicrobial-stewardship/study-forecasts-more-39-million-deaths-antimicrobial-resistance-2050",
    "Murray et al. Lancet 2022": "https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext",
    "O'Neill Review (10M target)": "https://amr-review.org/sites/default/files/160518_Final%20paper_with%20cover.pdf",
    "GRAM/O'Neill + Tai 2025": "https://doi.org/10.1016/j.ijantimicag.2025.107636",
    "Tai et al. 2025 (IJAA)": "https://doi.org/10.1016/j.ijantimicag.2025.107636",
}

CHART_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="#21232d",
        plot_bgcolor="#21232d",
        font=dict(color="#e8eaed", family="Inter, sans-serif", size=12),
        xaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
        yaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
        margin=dict(l=60, r=30, t=50, b=50),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
    )
)


def build_main_curve():
    """
    Primary AMR resistance curve — Gratacós-Botto super-exponential thesis.
    Faint reference line shows constant-r logistic for comparison.
    """
    curve = compute_super_exponential_curve()
    ref = compute_reference_logistic_curve()

    fig = go.Figure()

    # ±3-year shifted envelope (paper: 14 ± 3 yrs uncertainty)
    fig.add_trace(go.Scatter(
        x=curve["year"], y=curve["upper_bound"],
        mode="lines", line=dict(width=0),
        showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=curve["year"], y=curve["lower_bound"],
        mode="lines", line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(79, 195, 247, 0.15)",
        name="Uncertainty band (±3 yrs)",
        hoverinfo="skip",
    ))

    # Reference logistic (constant r) — faint, for visual comparison
    fig.add_trace(go.Scatter(
        x=ref["year"], y=ref["resistance_index"],
        mode="lines",
        line=dict(color="#9aa0a6", width=1.5, dash="dot"),
        name="Constant-rate logistic (limit of V=S·(1+r)ᵀ)",
        hovertemplate="<b>%{x}</b><br>Reference: %{y:.1f}<extra></extra>",
        opacity=0.55,
    ))

    # Observed segment of super-exp curve (1990–2025)
    obs = curve[curve["year"] <= 2025]
    fig.add_trace(go.Scatter(
        x=obs["year"], y=obs["resistance_index"],
        mode="lines",
        line=dict(color="#4fc3f7", width=3),
        name="Observed (1990–2025)",
        hovertemplate="<b>%{x}</b><br>Resistance Index: %{y:.1f}<extra></extra>",
    ))

    # Forecast segment (super-exp)
    fcast = curve[curve["year"] >= 2025]
    fig.add_trace(go.Scatter(
        x=fcast["year"], y=fcast["resistance_index"],
        mode="lines",
        line=dict(color="#ef5350", width=3, dash="dash"),
        name="Super-exponential forecast (Gratacós-Botto)",
        hovertemplate="<b>%{x}</b><br>Resistance Index: %{y:.1f} (projected)<extra></extra>",
    ))

    # Published anchor markers
    fig.add_trace(go.Scatter(
        x=OBSERVED_DATA["year"], y=OBSERVED_DATA["resistance_index"],
        mode="markers",
        marker=dict(color="#4fc3f7", size=8, symbol="circle",
                    line=dict(color="#21232d", width=1.5)),
        name="Published data points",
        customdata=OBSERVED_DATA["source"],
        hovertemplate="<b>%{x}</b><br>Index: %{y}<br>Source: %{customdata}<extra></extra>",
    ))

    # Critical threshold line
    fig.add_hline(
        y=95, line_dash="dot", line_color="#ef5350", line_width=1,
        annotation_text="Critical inefficacy threshold (~95)",
        annotation_position="top left",
        annotation_font=dict(color="#ef5350", size=11),
    )

    # Critical-point band: approach-to-threshold window — index ~90 (2040) up to
    # the y=95 crossing under the super-exponential model (2047). Matches paper
    # párr. 19 ("~90 by 2040 ... ~95–98 in the 2040–2047 period").
    fig.add_vrect(
        x0=2040, x1=2047,
        fillcolor="rgba(239, 83, 80, 0.10)",
        line_width=0,
        annotation_text="Critical Point (2040–2047)",
        annotation_position="top",
        annotation_font=dict(color="#ef5350", size=11),
    )

    template = CHART_TEMPLATE["layout"].copy()
    template_yaxis = template.pop("yaxis", {})
    template.pop("xaxis", None)

    fig.update_layout(
        **template,
        title=dict(
            text="AMR Resistance Pressure Index (1990–2060) — Super-exponential model",
            font=dict(size=16),
        ),
        xaxis_title="Year",
        xaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
        yaxis_title="Resistance Pressure Index (0–100)",
        yaxis=dict(range=[0, 105], **template_yaxis),
        height=520,
        hovermode="x unified",
    )

    return fig


def build_mortality_chart():
    """AMR mortality projection — Murray/GRAM/O'Neill (high) + Tai 2025 (low)."""
    fig = go.Figure()

    # GRAM/O'Neill stacked bars (existing methodology)
    fig.add_trace(go.Bar(
        x=MORTALITY_DATA["year"],
        y=MORTALITY_DATA["attributable_deaths_k"],
        name="Attributable (GRAM/O'Neill)",
        marker_color="#ef5350",
        hovertemplate="<b>%{x}</b><br>%{y:,}K deaths<extra>Attributable</extra>",
    ))
    fig.add_trace(go.Bar(
        x=MORTALITY_DATA["year"],
        y=MORTALITY_DATA["associated_deaths_k"] - MORTALITY_DATA["attributable_deaths_k"],
        name="Associated (additional)",
        marker_color="#ffb74d",
        hovertemplate="<b>%{x}</b><br>%{y:,}K additional<extra>Associated</extra>",
    ))

    # Tai et al. 2025 conservative GBD-hierarchical line
    fig.add_trace(go.Scatter(
        x=MORTALITY_DATA["year"],
        y=MORTALITY_DATA["tai_2025_deaths_k"],
        mode="lines+markers",
        line=dict(color="#4fc3f7", width=2.5, dash="dash"),
        marker=dict(size=7, symbol="diamond"),
        name="Tai 2025 (GBD-hierarchical)",
        hovertemplate="<b>%{x}</b><br>%{y:,}K deaths<extra>Tai 2025</extra>",
    ))

    fig.update_layout(
        **CHART_TEMPLATE["layout"],
        title=dict(text="Projected AMR Mortality (thousands/year)", font=dict(size=14)),
        barmode="stack",
        xaxis_title="Year",
        yaxis_title="Deaths (thousands)",
        height=380,
    )

    return fig


def build_carbapenem_chart():
    """
    Carbapenem-resistance mortality trajectory through 2035 — Tai 2025
    (paper ref 10, párr. 9). Three series stacked: CRE, CRAB, CRPA.
    """
    df = CARBAPENEM_PROJECTION
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["year"], y=df["CRE"],
        mode="lines+markers",
        name="CRE (Enterobacterales)",
        stackgroup="carba",
        line=dict(color="#ef5350", width=0.5),
        marker=dict(size=6, color="#ef5350",
                    line=dict(color="#21232d", width=1)),
        fillcolor="rgba(239, 83, 80, 0.45)",
        hovertemplate="<b>%{x}</b><br>CRE: %{y}K deaths/yr<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["year"], y=df["CRAB"],
        mode="lines+markers",
        name="CRAB (A. baumannii)",
        stackgroup="carba",
        line=dict(color="#ff7043", width=0.5),
        marker=dict(size=6, color="#ff7043",
                    line=dict(color="#21232d", width=1)),
        fillcolor="rgba(255, 112, 67, 0.45)",
        hovertemplate="<b>%{x}</b><br>CRAB: %{y}K deaths/yr<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["year"], y=df["CRPA"],
        mode="lines+markers",
        name="CRPA (P. aeruginosa)",
        stackgroup="carba",
        line=dict(color="#ffb74d", width=0.5),
        marker=dict(size=6, color="#ffb74d",
                    line=dict(color="#21232d", width=1)),
        fillcolor="rgba(255, 183, 77, 0.45)",
        hovertemplate="<b>%{x}</b><br>CRPA: %{y}K deaths/yr<extra></extra>",
    ))

    # 2025 separator (observed → forecast)
    fig.add_vline(
        x=2025, line_dash="dot", line_color="#9aa0a6", line_width=1,
        annotation_text="Forecast →",
        annotation_position="top",
        annotation_font=dict(color="#9aa0a6", size=10),
    )

    # Critical 2035 marker
    fig.add_vline(
        x=2035, line_dash="dot", line_color="#ef5350", line_width=1,
        annotation_text="Tai 2025 horizon",
        annotation_position="top",
        annotation_font=dict(color="#ef5350", size=10),
    )

    template = CHART_TEMPLATE["layout"].copy()
    template.pop("yaxis", None)
    template.pop("xaxis", None)

    fig.update_layout(
        **template,
        title=dict(
            text="Carbapenem-Resistance Mortality (CRE + CRAB + CRPA) — through 2035",
            font=dict(size=14),
        ),
        xaxis_title="Year",
        xaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
        yaxis_title="Deaths/yr (thousands, stacked)",
        yaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
        height=380,
        hovermode="x unified",
    )

    return fig


def build_data_table():
    rows = []
    for _, r in OBSERVED_DATA.iterrows():
        rows.append(
            html.Tr([
                html.Td(int(r["year"])),
                html.Td(f'{r["resistance_index"]:.0f}'),
                html.Td(f'{r["lower_bound"]:.0f}–{r["upper_bound"]:.0f}'),
                html.Td(html.A(r["source"], href=SOURCE_URLS.get(r["source"], "#"), className="source-tag", target="_blank")),
                html.Td("Observed"),
            ])
        )
    for _, r in FORECAST_DATA.iterrows():
        if r["year"] == 2025:
            continue
        rows.append(
            html.Tr([
                html.Td(int(r["year"])),
                html.Td(f'{r["resistance_index"]:.0f}'),
                html.Td(f'{r["lower_bound"]:.0f}–{r["upper_bound"]:.0f}'),
                html.Td(html.A(r["source"], href=SOURCE_URLS.get(r["source"], "#"), className="source-tag", target="_blank")),
                html.Td("Forecast"),
            ])
        )

    return html.Table(
        [
            html.Thead(html.Tr([
                html.Th("Year"), html.Th("Index"), html.Th("Range"),
                html.Th("Source"), html.Th("Type"),
            ])),
            html.Tbody(rows),
        ],
        className="data-table",
    )


# Layout
layout = html.Div([
    help_section("Overview", [
        "RESISTANCE PRESSURE INDEX: The y-axis on the main chart represents a normalized 'Resistance Pressure Index' scored from 0 to 100. This is a composite conceptual metric, not a raw epidemiological measurement. It synthesizes multiple indicators -- percentage of resistant isolates across priority pathogens, loss of effective drug classes, and clinical treatment failure rates -- into a single normalized score. A value of 0 represents a pre-antibiotic baseline; 100 represents near-total resistance across all first-line agents for hospital-acquired Gram-negative infections.",
        "SUPER-EXPONENTIAL MODEL (Gratacós-Botto thesis, paper UPDATE v.A-29 párr. 22): The primary curve plotted on this chart is NOT a standard logistic. The Gratacós-Botto model proposes that the rate of increasing resistance is itself growing — i.e., resistance accelerates faster than a constant-rate process would predict. Mathematically the curve is y(τ) = K / (1 + A · exp(-r·τ - b·τ²)), where the time-quadratic term -b·τ² makes the effective rate r_eff(τ) = r + 2·b·τ grow linearly with elapsed years. Coefficients (K=100, A=7.333, r=0.0705, b=3.05·10⁻⁴) are hardcoded and calibrated to published anchor points; the model is fully deterministic and reproducible.",
        "REFERENCE CURVE (faint dotted grey): For visual contrast, the chart also plots the constant-rate logistic — the continuous limit of the discrete geometric law V = S·(1+r)ᵀ, with the same ceiling K — calibrated to the same observed segment (1990 → 2025). This reference reaches the critical inefficacy threshold (~95) in 2051. The Gratacós-Botto super-exponential reaches the same threshold in 2047 — a 4-year advance of the critical inefficacy threshold, which is the central forecasting claim of the paper.",
        "UNCERTAINTY BANDS (±3 YEARS): The shaded blue envelope around the primary curve is generated by laterally shifting the trajectory by ±3 years, matching the paper's stated uncertainty (párr. 5: 'fourteen years (±3)'). It is not a statistical confidence interval. Interpret it as: the critical inefficacy threshold could realistically fall up to 3 years earlier or later than the central forecast. The band tightens at the asymptote because all trajectories converge to the same K=100.",
        "CRITICAL THRESHOLD (~95): The horizontal dashed line at index value 95 represents the threshold at which first-line antibiotics become largely ineffective for treating hospital-acquired Gram-negative infections (Enterobacterales, Acinetobacter, Pseudomonas). This threshold was determined by mapping clinical breakpoints: when resistance rates exceed ~90-95% for a given drug class, empiric therapy with that class is no longer viable and clinicians must rely on last-resort agents (colistin, novel beta-lactam/inhibitor combinations) or combination regimens. Crossing this threshold does not mean all antibiotics fail, but that routine empiric treatment protocols require fundamental restructuring.",
        "CRITICAL POINT BAND (2040–2047): The red-shaded vertical region marks the projected window during which the resistance pressure index crosses the critical inefficacy threshold under the super-exponential model. The paper anchors this to specific milestones in párr. 19: pressure ~80 by 2032, ~90 by 2040, and ~95–98 in the 2040–2047 period. Once inside this band, panresistant 'superbugs' transition from exceptional to common in nosocomial Gram-negative infections.",
        "PUBLISHED ANCHOR MARKERS: The blue circular markers represent published anchor points from the literature (Murray Lancet 2022, GRAM/CIDRAP, O'Neill 2016, Oxford VG, Tai IJAA 2025). The model curve does not pass exactly through every marker — the closed-form analytic function smooths slight inter-source variation. Hover over any marker to read its source citation.",
        "MORTALITY CHART — THREE METHODOLOGIES: The mortality chart now overlays three projection methodologies. (a) Stacked bars (red+amber): GRAM/O'Neill methodology — directly attributable + associated deaths, peaking at ~10M associated deaths/year by 2050. (b) Dashed blue diamond line: Tai et al. 2025 (Int J Antimicrob Agents) — a more conservative GBD-hierarchical methodology projecting ~1.91M annual attributable deaths by 2040. The two curves represent legitimate methodological alternatives; the gap between them is itself a measure of model uncertainty in long-horizon AMR mortality forecasting.",
        "USING CHARTS IN PUBLICATIONS: To export any chart, click the camera icon in the Plotly toolbar (top-right of the chart). The default export is SVG at 3x resolution, suitable for most journal submissions. For the highest quality, use the Export Studio page where you can select Publication Light or Print B&W color themes with white backgrounds. When citing these visualizations, reference the underlying data sources listed below each chart and note that the resistance pressure index is a composite normalized metric constructed for this research project.",
        "DATA TABLE: The reference data table at the bottom of this page lists every published anchor point used to construct the curve, including the year, index value, uncertainty range, original source, and whether the point is observed or forecast. Use this table to trace any point on the curve back to its primary literature source.",
    ]),

    # Stats row — 5 cards
    html.Div([
        html.Div([
            html.Div("~70", className="stat-value accent"),
            html.Div("Current Index (2025)", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div("1.27M", className="stat-value danger"),
            html.Div("AMR Deaths 2019 (Murray)", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div("14 ± 3", className="stat-value warning"),
            html.Div("Years to Critical Point", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div("1.91M", className="stat-value danger"),
            html.Div("Deaths/yr 2040 (Tai 2025)", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div("10M", className="stat-value danger"),
            html.Div("Deaths/yr 2050 (O'Neill)", className="stat-label"),
        ], className="stat-card"),
    ], className="stats-row"),

    # Main curve
    html.Div([
        chart_title_with_info(
            "Resistance Pressure Trajectory",
            "Primary curve: super-exponential model from the Gratacós-Botto paper (UPDATE v.A-29) with rate growing linearly in time. Faint dotted grey: constant-rate logistic (continuous limit of V=S·(1+r)ᵀ) for comparison. Red-shaded zone: projected critical-point window (2040–2047).",
            "Super-exponential model anchored to 10+ published sources, with reference logistic and ±3-year uncertainty band",
        ),
        dcc.Graph(id="main-curve", figure=build_main_curve(), config={
            "toImageButtonOptions": {"format": "svg", "filename": "amr_resistance_curve", "scale": 3},
            "displayModeBar": True,
        }),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            html.A("Murray et al., Lancet 2022", href="https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext", target="_blank"),
            " · ",
            html.A("O'Neill Review on AMR (2016)", href="https://amr-review.org/sites/default/files/160518_Final%20paper_with%20cover.pdf", target="_blank"),
            " · ",
            html.A("GRAM Project — CIDRAP", href="https://www.cidrap.umn.edu/antimicrobial-stewardship/study-forecasts-more-39-million-deaths-antimicrobial-resistance-2050", target="_blank"),
            " · ",
            html.A("Tai et al., IJAA 2025", href="https://doi.org/10.1016/j.ijantimicag.2025.107636", target="_blank"),
            " · ",
            html.A("Oxford Vaccine Group AMR timeline", href="https://www.ovg.ox.ac.uk/news/antibiotic-resistance", target="_blank"),
            " · ",
            html.A("IHME GBD AMR", href="https://www.healthdata.org/research-analysis/diseases-injuries-risks/factsheets/2021-amr-factsheet", target="_blank"),
        ], className="chart-sources"),
    ], className="card"),

    # Second row
    html.Div([
        html.Div([
            chart_title_with_info(
                "Mortality Projections",
                "Stacked bars: GRAM/O'Neill methodology (attributable + associated). Dashed blue line: Tai et al. 2025 (conservative GBD-hierarchical, ~1.91M attributable deaths by 2040). Both methodologies are legitimate; the gap reflects model uncertainty.",
                "Three methodologies: Murray/GRAM/O'Neill stacked + Tai 2025 overlay",
            ),
            dcc.Graph(id="mortality-chart", figure=build_mortality_chart(), config={
                "toImageButtonOptions": {"format": "svg", "filename": "amr_mortality", "scale": 3},
            }),
            html.Div([
                html.Span("Sources: ", className="source-label"),
                html.A("Murray et al., Lancet 2022", href="https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext", target="_blank"),
                " · ",
                html.A("GRAM Project — CIDRAP", href="https://www.cidrap.umn.edu/antimicrobial-stewardship/study-forecasts-more-39-million-deaths-antimicrobial-resistance-2050", target="_blank"),
                " · ",
                html.A("O'Neill Review on AMR (2016)", href="https://amr-review.org/sites/default/files/160518_Final%20paper_with%20cover.pdf", target="_blank"),
                " · ",
                html.A("Tai et al., IJAA 2025", href="https://doi.org/10.1016/j.ijantimicag.2025.107636", target="_blank"),
            ], className="chart-sources"),
        ], className="card"),
        html.Div([
            chart_title_with_info(
                "Reference Data Points",
                "Published data points used to anchor the resistance curve, with their uncertainty ranges and original sources.",
                "Published anchors used to construct the resistance curve",
            ),
            build_data_table(),
        ], className="card"),
    ], className="chart-grid-2"),

    # Carbapenem spotlight (Tai 2025, paper ref 10, párr. 9)
    html.Div([
        chart_title_with_info(
            "Carbapenem Resistance Spotlight (Tai 2025 — to 2035)",
            "Carbapenem-resistant Enterobacterales (CRE), A. baumannii (CRAB) and P. aeruginosa (CRPA) mortality through 2035, anchored to Murray et al. Lancet 2022 (2019 baseline) and Tai et al. IJAA 2025 (paper ref 10, párr. 9): 'carbapenem-resistant deaths are projected to escalate sharply by 2035 even as overall age-standardized mortality declines'. Stacked area shows the three pathogen contributions; vertical dotted line at 2025 marks observed → forecast.",
            "Spotlight on the paper's párr. 9 claim — sharp carbapenem-resistant escalation through 2035 (Tai 2025)",
        ),
        dcc.Graph(id="carbapenem-chart", figure=build_carbapenem_chart(), config={
            "toImageButtonOptions": {"format": "svg", "filename": "carbapenem_2035", "scale": 3},
            "displayModeBar": True,
        }),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            html.A("Tai et al., IJAA 2025 (paper ref 10)",
                   href="https://doi.org/10.1016/j.ijantimicag.2025.107636",
                   target="_blank"),
            " · ",
            html.A("Murray et al., Lancet 2022 (GBD AMR baseline)",
                   href="https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext",
                   target="_blank"),
            " · ",
            html.A("Paper UPDATE v.A-29 párr. 9", href="#", target="_blank"),
        ], className="chart-sources"),
    ], className="card"),
])
