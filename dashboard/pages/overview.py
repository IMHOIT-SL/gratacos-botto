"""
Overview page — Main AMR resistance curve with interactive confidence bands.
"""

import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.amr_data import (
    compute_sigmoid_curve,
    OBSERVED_DATA,
    FORECAST_DATA,
    MORTALITY_DATA,
)
from components import help_section, chart_title_with_info

dash.register_page(__name__, path="/", name="Overview")

# Plotly dark template matching our CSS
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
    """Build the primary AMR resistance sigmoid curve with confidence bands."""
    curve = compute_sigmoid_curve()

    fig = go.Figure()

    # Confidence band (upper)
    fig.add_trace(go.Scatter(
        x=curve["year"], y=curve["upper_bound"],
        mode="lines", line=dict(width=0),
        showlegend=False, hoverinfo="skip",
    ))

    # Confidence band (lower) — fills to upper
    fig.add_trace(go.Scatter(
        x=curve["year"], y=curve["lower_bound"],
        mode="lines", line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(79, 195, 247, 0.15)",
        name="Uncertainty band",
        hoverinfo="skip",
    ))

    # Observed segment (1990-2025)
    obs = curve[curve["year"] <= 2025]
    fig.add_trace(go.Scatter(
        x=obs["year"], y=obs["resistance_index"],
        mode="lines",
        line=dict(color="#4fc3f7", width=3),
        name="Observed (1990–2025)",
        hovertemplate="<b>%{x}</b><br>Resistance Index: %{y:.1f}<extra></extra>",
    ))

    # Forecast segment (2025-2060)
    fcast = curve[curve["year"] >= 2025]
    fig.add_trace(go.Scatter(
        x=fcast["year"], y=fcast["resistance_index"],
        mode="lines",
        line=dict(color="#ef5350", width=3, dash="dash"),
        name="Forecast (2025–2060)",
        hovertemplate="<b>%{x}</b><br>Resistance Index: %{y:.1f} (projected)<extra></extra>",
    ))

    # Data point markers (observed)
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
        annotation_text="Critical threshold (~95)",
        annotation_position="top left",
        annotation_font=dict(color="#ef5350", size=11),
    )

    # Critical point zone
    fig.add_vrect(
        x0=2040, x1=2045,
        fillcolor="rgba(239, 83, 80, 0.1)",
        line_width=0,
        annotation_text="Critical Point",
        annotation_position="top",
        annotation_font=dict(color="#ef5350", size=11),
    )

    template = CHART_TEMPLATE["layout"].copy()
    template_yaxis = template.pop("yaxis", {})
    template.pop("xaxis", None)

    fig.update_layout(
        **template,
        title=dict(text="AMR Resistance Pressure Index (1990–2060)", font=dict(size=16)),
        xaxis_title="Year",
        xaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
        yaxis_title="Resistance Pressure Index (0–100)",
        yaxis=dict(range=[0, 105], **template_yaxis),
        height=500,
        hovermode="x unified",
    )

    return fig


def build_mortality_chart():
    """Build AMR mortality projection chart."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=MORTALITY_DATA["year"],
        y=MORTALITY_DATA["attributable_deaths_k"],
        name="Directly attributable",
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

    fig.update_layout(
        **CHART_TEMPLATE["layout"],
        title=dict(text="Projected AMR Mortality (thousands/year)", font=dict(size=14)),
        barmode="stack",
        xaxis_title="Year",
        yaxis_title="Deaths (thousands)",
        height=380,
    )

    return fig


def build_data_table():
    """Build the reference data table."""
    rows = []
    for _, r in OBSERVED_DATA.iterrows():
        rows.append(
            html.Tr([
                html.Td(int(r["year"])),
                html.Td(f'{r["resistance_index"]:.0f}'),
                html.Td(f'{r["lower_bound"]:.0f}–{r["upper_bound"]:.0f}'),
                html.Td(html.Span(r["source"], className="source-tag")),
                html.Td("Observed"),
            ])
        )
    for _, r in FORECAST_DATA.iterrows():
        if r["year"] == 2025:
            continue  # already in observed
        rows.append(
            html.Tr([
                html.Td(int(r["year"])),
                html.Td(f'{r["resistance_index"]:.0f}'),
                html.Td(f'{r["lower_bound"]:.0f}–{r["upper_bound"]:.0f}'),
                html.Td(html.Span(r["source"], className="source-tag")),
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
    # Help section
    help_section("Overview", [
        "RESISTANCE PRESSURE INDEX: The y-axis on the main chart represents a normalized 'Resistance Pressure Index' scored from 0 to 100. This is a composite conceptual metric, not a raw epidemiological measurement. It synthesizes multiple indicators -- percentage of resistant isolates across priority pathogens, loss of effective drug classes, and clinical treatment failure rates -- into a single normalized score. A value of 0 represents a pre-antibiotic baseline; 100 represents near-total resistance across all first-line agents for hospital-acquired Gram-negative infections.",
        "SIGMOID CURVE SHAPE: The resistance trajectory follows a logistic (sigmoid) curve, which is characteristic of biological systems subject to saturation dynamics. Early growth is slow (1940s-1990s: resistance genes emerging but contained), followed by an acceleration phase (2000-2035: resistance spreading exponentially through horizontal gene transfer, selective pressure from antibiotic overuse, and global travel), and finally a plateau as resistance approaches theoretical maximum levels. This S-shaped pattern is well-documented in evolutionary biology and matches observed resistance trends across multiple pathogen-drug combinations.",
        "UNCERTAINTY BANDS: The shaded region around the main curve represents the range of estimates across published sources rather than a formal statistical confidence interval. The width reflects disagreement among models and data sources -- narrower bands in the historical period (where surveillance data exists) and wider bands in the forecast period (where models diverge). Interpret the band as: 'published estimates fall within this range,' not as a probability distribution.",
        "CRITICAL THRESHOLD (~95): The horizontal dashed line at index value 95 represents the threshold at which first-line antibiotics become largely ineffective for treating hospital-acquired Gram-negative infections (Enterobacterales, Acinetobacter, Pseudomonas). This threshold was determined by mapping clinical breakpoints: when resistance rates exceed ~90-95% for a given drug class, empiric therapy with that class is no longer viable and clinicians must rely on last-resort agents (colistin, novel beta-lactam/inhibitor combinations) or combination regimens. Crossing this threshold does not mean all antibiotics fail, but that routine empiric treatment protocols require fundamental restructuring.",
        "OBSERVED VS FORECAST SEGMENTS: The solid blue line (1990-2025) represents the 'observed' segment, anchored to published data points from surveillance systems (WHO GLASS, EARS-Net, CDC) and landmark studies (Murray et al. Lancet 2022, O'Neill Review 2016). These values carry higher confidence because they are grounded in actual resistance measurements. The dashed red line (2025-2060) represents the 'forecast' segment, generated by fitting the logistic model to observed data and extrapolating. Forecast reliability decreases with distance from the last observed point -- projections beyond 2040 should be treated as scenario illustrations rather than precise predictions.",
        "MORTALITY CHART: The stacked bar chart below the main curve shows two distinct mortality categories. 'Directly attributable' deaths (red) are those where resistant infection was the primary cause of death -- the patient would likely have survived with an effective antibiotic. 'Associated' deaths (amber, stacked above) are cases where AMR was a contributing factor but not the sole cause. The 2019 baseline (1.27M attributable, 4.95M associated) comes from Murray et al. Lancet 2022. Future projections extrapolate using GRAM Project and O'Neill Review methodology. The gap between attributable and associated deaths highlights the broader systemic impact of resistance beyond direct treatment failure.",
        "USING CHARTS IN PUBLICATIONS: To export any chart, click the camera icon in the Plotly toolbar (top-right of the chart). The default export is SVG at 3x resolution, suitable for most journal submissions. For the highest quality, use the Export Studio page where you can select Publication Light or Print B&W color themes with white backgrounds. When citing these visualizations, reference the underlying data sources listed below each chart (Murray et al. 2022, GRAM/CIDRAP, O'Neill Review 2016) and note that the resistance pressure index is a composite normalized metric constructed for this research project.",
        "DATA TABLE: The reference data table at the bottom of this page lists every published anchor point used to construct the sigmoid curve, including the year, index value, uncertainty range, original source, and whether the point is observed or forecast. Use this table to trace any point on the curve back to its primary literature source.",
    ]),

    # Stats row
    html.Div([
        html.Div([
            html.Div("~70", className="stat-value accent"),
            html.Div("Current Index (2025)", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div("1.27M", className="stat-value danger"),
            html.Div("AMR Deaths 2019", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div("2040–45", className="stat-value warning"),
            html.Div("Projected Critical Point", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div("10M", className="stat-value danger"),
            html.Div("Deaths/yr by 2050 (O'Neill)", className="stat-label"),
        ], className="stat-card"),
    ], className="stats-row"),

    # Main curve
    html.Div([
        chart_title_with_info(
            "Resistance Pressure Trajectory",
            "Normalized resistance pressure index (0-100) showing observed data (1990-2025, solid blue) and forecast (2025-2060, dashed red). The shaded band represents uncertainty. The red zone marks the projected critical point where most first-line antibiotics lose effectiveness.",
            "Sigmoid curve anchored to 10+ published sources with uncertainty bands",
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
            html.A("Oxford Vaccine Group AMR timeline", href="https://www.ovg.ox.ac.uk/news/antibiotic-resistance", target="_blank"),
            " · ",
            html.A("IHME GBD AMR", href="https://www.healthdata.org/research-analysis/diseases-injuries-risks/factsheets/2021-amr-factsheet", target="_blank"),
        ], className="chart-sources"),
    ], className="card"),

    # Second row: mortality + data table
    html.Div([
        html.Div([
            chart_title_with_info(
                "Mortality Projections",
                "Stacked bar chart showing AMR-attributable deaths (directly caused by resistant infections) and AMR-associated deaths (where resistance was a contributing factor). Based on Murray et al. Lancet 2022 and O'Neill projections.",
                "Attributable vs associated AMR deaths",
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
            ], className="chart-sources"),
        ], className="card"),
        html.Div([
            chart_title_with_info(
                "Reference Data Points",
                "Published data points used to anchor the sigmoid resistance curve, with their uncertainty ranges and original sources.",
                "Published anchors used to construct the resistance curve",
            ),
            build_data_table(),
        ], className="card"),
    ], className="chart-grid-2"),
])
