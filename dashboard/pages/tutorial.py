"""
Tutorial page — Interactive guide to Plotly chart controls + chart map.
"""

import dash
from dash import html, dcc
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from components import help_section, chart_title_with_info, graph_config
from data.amr_data import compute_super_exponential_curve

dash.register_page(__name__, path="/tutorial", name="Tutorial")

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


def build_demo_chart():
    """Demo chart using the same super-exponential model as the Overview page."""
    curve = compute_super_exponential_curve(1990, 2060)

    fig = go.Figure()

    # Observed segment
    obs = curve[curve["year"] <= 2025]
    fig.add_trace(go.Scatter(
        x=obs["year"], y=obs["resistance_index"],
        mode="lines+markers",
        line=dict(color="#4fc3f7", width=3),
        marker=dict(size=5, color="#4fc3f7"),
        name="Observed (1990-2025)",
        hovertemplate="<b>%{x}</b><br>Resistance Index: %{y:.1f}<extra></extra>",
    ))

    # Forecast segment
    fcast = curve[curve["year"] >= 2025]
    fig.add_trace(go.Scatter(
        x=fcast["year"], y=fcast["resistance_index"],
        mode="lines+markers",
        line=dict(color="#ef5350", width=3, dash="dash"),
        marker=dict(size=5, color="#ef5350"),
        name="Forecast (2025-2060)",
        hovertemplate="<b>%{x}</b><br>Resistance Index: %{y:.1f} (projected)<extra></extra>",
    ))

    # Key milestones aligned with the published paper, forecast segment
    key_years = [1990, 2000, 2010, 2019, 2025, 2032, 2040, 2047, 2060]
    key_vals = [
        float(curve.loc[curve["year"] == y, "resistance_index"].iloc[0])
        for y in key_years
    ]
    key_labels = [
        "Baseline era",
        "MRSA/ESBL era",
        "GBD benchmark",
        "1.27M deaths/yr (Murray)",
        "Current (2025) ~70",
        "~80 (paper milestone)",
        "~90 (paper milestone)",
        "Critical Point ~96",
        "Near-total resistance",
    ]
    fig.add_trace(go.Scatter(
        x=key_years, y=key_vals,
        mode="markers",
        marker=dict(color="#ffb74d", size=12, symbol="diamond",
                    line=dict(color="#21232d", width=2)),
        name="Key milestones",
        customdata=key_labels,
        hovertemplate="<b>%{x}</b><br>Index: %{y:.1f}<br>%{customdata}<extra></extra>",
    ))

    # Critical threshold line
    fig.add_hline(
        y=95, line_dash="dot", line_color="#ef5350", line_width=1,
        annotation_text="Critical inefficacy threshold (~95)",
        annotation_position="top left",
        annotation_font=dict(color="#ef5350", size=11),
    )

    # Critical point zone (published paper, forecast segment: 2040–2047)
    fig.add_vrect(
        x0=2040, x1=2047,
        fillcolor="rgba(239, 83, 80, 0.1)",
        line_width=0,
        annotation_text="Critical Zone (2040–2047)",
        annotation_position="top",
        annotation_font=dict(color="#ef5350", size=11),
    )

    template = CHART_TEMPLATE["layout"].copy()
    template_yaxis = template.pop("yaxis", {})
    template.pop("xaxis", None)

    fig.update_layout(
        **template,
        title=dict(text="Demo: AMR Resistance Pressure Index (1990-2060)", font=dict(size=16)),
        xaxis_title="Year",
        xaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
        yaxis_title="Resistance Pressure Index (0-100)",
        yaxis=dict(range=[0, 105], **template_yaxis),
        height=500,
        hovermode="x unified",
    )

    return fig


def control_card(icon, name, description, steps, example, tips=None):
    """Build a tutorial card for a single chart control."""
    elements = [
        html.Div([
            html.Span(icon, className="stat-value", style={
                "fontSize": "1.5rem", "marginRight": "0.75rem", "minWidth": "2rem",
                "textAlign": "center", "display": "inline-block",
            }),
            html.H3(name, className="card-title", style={"margin": "0", "display": "inline"}),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "0.75rem"}),
        html.P(description, style={"color": "#b0b3b8", "marginBottom": "0.75rem"}),
        html.H4("How to use:", style={"color": "#e8eaed", "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        html.Ol(
            [html.Li(step, style={"color": "#b0b3b8", "marginBottom": "0.25rem"}) for step in steps],
            style={"paddingLeft": "1.25rem", "marginBottom": "0.75rem"},
        ),
        html.Div([
            html.Strong("AMR Example: ", style={"color": "#4fc3f7"}),
            html.Span(example, style={"color": "#b0b3b8"}),
        ], style={"marginBottom": "0.75rem", "padding": "0.5rem", "backgroundColor": "rgba(79,195,247,0.08)", "borderRadius": "4px"}),
    ]

    if tips:
        elements.append(html.Div([
            html.Strong("Tips: ", style={"color": "#ffb74d"}),
            html.Ul(
                [html.Li(tip, style={"color": "#b0b3b8", "marginBottom": "0.15rem"}) for tip in tips],
                style={"paddingLeft": "1.25rem", "marginTop": "0.25rem", "marginBottom": "0"},
            ),
        ], style={"padding": "0.5rem", "backgroundColor": "rgba(255,183,77,0.08)", "borderRadius": "4px"}))

    return html.Div(elements, className="card", style={"marginBottom": "1rem"})


layout = html.Div([
    # Help section
    help_section("Tutorial", [
        "This page teaches you how to use the interactive chart controls available on every chart in the dashboard.",
        "DASHBOARD MAP: The current build has 11 pages with 11 distinct charts in total (plus auxiliary panels). The Plotly toolbar described below works identically on every chart — once you learn the controls here, they apply everywhere. The 'Where to find each chart' section at the bottom of this page lists which page hosts which chart.",
        "PUBLICATION-QUALITY EXPORT: Every chart can be exported from its own toolbar as SVG (vector), PNG at 3x resolution, or CSV with its data. For more control (light/B&W themes, drug-class panel, etc.), use the dedicated Export Studio page (`/export`) — it surfaces all 11 charts with theme switching.",
    ]),

    # Demo chart
    html.Div([
        chart_title_with_info(
            "Practice Chart -- Try the Controls",
            "This is a demo chart for practicing Plotly interactive controls. It uses a subset of the AMR sigmoid curve data with key milestones marked. The toolbar sits at the top right of the chart; try each control described below.",
            "Use this chart to practice the 9 toolbar controls described below",
        ),
        dcc.Graph(
            id="tutorial-demo-chart",
            figure=build_demo_chart(),
            config=graph_config("amr_tutorial_demo"),
        ),
        html.P(
            "The toolbar is at the top right of the chart above. Follow the guides below to learn each control.",
            style={"color": "#b0b3b8", "fontStyle": "italic", "marginTop": "0.5rem"},
        ),
    ], className="card"),

    # Tutorial section header
    html.H2("Chart Controls Reference", style={
        "color": "#e8eaed", "marginTop": "2rem", "marginBottom": "1rem",
        "borderBottom": "1px solid #2d2f3a", "paddingBottom": "0.5rem",
    }),
    html.P(
        "Every chart in the dashboard has the same toolbar at its top right: navigation tools on the left (zoom, pan, zoom in, zoom out, reset) and output tools on the right (SVG, PNG, data, full screen). Below is a guide for each control, from left to right.",
        style={"color": "#b0b3b8", "marginBottom": "1.5rem"},
    ),

    # Toolbar layout: navigation tools on the left, downloads + full screen on the right.
    # 1. Zoom
    control_card(
        icon="\U0001f50d",
        name="Zoom (Magnifying Glass)",
        description="Enables rectangular zoom mode. Click and drag on the chart to draw a box around the area you want to zoom into. The axes will rescale to show only the selected region.",
        steps=[
            "Click the magnifying glass (first button on the left; active by default).",
            "Click and hold on the chart at one corner of the area you want to inspect.",
            "Drag to the opposite corner to draw a selection rectangle.",
            "Release the mouse button -- the chart zooms to show only the selected area.",
            "Double-click anywhere on the chart to reset back to the full view.",
        ],
        example="Select the region from 2019 to 2025 to inspect the recent acceleration in resistance during and after the COVID-19 pandemic, when antibiotic misuse surged.",
        tips=[
            "Double-click the chart to reset zoom at any time.",
            "You can zoom multiple times to progressively magnify a region.",
            "Hold Shift while in zoom mode to temporarily switch to pan mode.",
        ],
    ),

    # 2. Pan
    control_card(
        icon="\u271c",
        name="Pan (Cross Arrows)",
        description="Switches to pan mode. Click and drag to move the visible area without changing the zoom level. This is useful after zooming in to navigate to different parts of the data.",
        steps=[
            "Click the cross-arrows icon in the toolbar to activate pan mode.",
            "Click and hold anywhere on the chart.",
            "Drag in any direction to shift the visible window.",
            "Release the mouse button when the desired region is in view.",
        ],
        example="After zooming into the 2030-2040 forecast period, pan left to compare it side-by-side with the 2010-2020 observed acceleration without losing your zoom level.",
        tips=[
            "Hold Shift while in zoom mode to temporarily pan without switching tools.",
            "Pan works on both axes simultaneously by default.",
            "Double-click to reset the view if you get lost.",
        ],
    ),

    # 3. Zoom In
    control_card(
        icon="\u2295",
        name="Zoom In (+)",
        description="Incrementally zooms into the center of the current view. Each click magnifies the view by approximately 50%, keeping the current center point fixed.",
        steps=[
            "Click the + button in the toolbar.",
            "The chart zooms in 50% toward the center of the current view.",
            "Click again to zoom in further.",
            "Use pan mode to reposition if the area of interest is off-center.",
        ],
        example="Click Zoom In three times to magnify the critical zone (2040-2045) and examine exactly where the curve crosses the 95 threshold line.",
        tips=[
            "Combine with pan to navigate precisely after zooming in.",
            "For precise area selection, the rectangular zoom tool is often faster.",
        ],
    ),

    # 4. Zoom Out
    control_card(
        icon="\u2296",
        name="Zoom Out (-)",
        description="Incrementally zooms out from the center of the current view. Each click widens the view by approximately 50%, showing more of the data range.",
        steps=[
            "Click the - button in the toolbar.",
            "The chart zooms out 50% from the center of the current view.",
            "Click again to zoom out further.",
        ],
        example="After closely inspecting the 2019 data point (Murray et al., 1.27M deaths), zoom out to see how it fits within the broader 70-year trajectory.",
        tips=[
            "If you zoom out beyond the data range, use Reset Axes (home icon) to return to the original view.",
            "Zoom Out can reveal data points that were clipped by previous zoom operations.",
        ],
    ),

    # 5. Reset Axes
    control_card(
        icon="\u2302",
        name="Reset Axes (Home Icon)",
        description="Returns the chart to its original view, undoing all zoom and pan operations. Restores the exact axis ranges the chart was created with.",
        steps=[
            "Click the home icon in the toolbar.",
            "All axes return to their original ranges.",
            "All zoom and pan history is cleared.",
        ],
        example="After exploring different periods of the resistance curve, click Reset Axes to return to the full 1990-2060 view.",
        tips=[
            "Keyboard shortcut: double-click anywhere on the chart background to reset.",
        ],
    ),

    # 6. Download SVG
    control_card(
        icon="\u2b07",
        name="Download SVG (Arrow Icon)",
        description="Downloads the chart as an SVG vector file, the best format for the paper: text stays selectable and the figure scales to any size without losing sharpness.",
        steps=[
            "Click the downward-arrow icon (first button of the right-hand group).",
            "The SVG file is saved with the chart's name.",
            "Open it in a browser or a vector editor (Inkscape, Illustrator), or insert it in the manuscript.",
        ],
        example="Download the resistance curve from the Overview page as SVG and place it as Image #1 of the manuscript.",
        tips=[
            "The download reflects the current view: reset the axes first if you want the full figure.",
            "For light or black-and-white versions, use the Export Studio page.",
        ],
    ),

    # 7. Download PNG
    control_card(
        icon="\U0001f5bc",
        name="Download PNG 3x (Picture Icon)",
        description="Downloads the chart as a high-resolution PNG image (three times the on-screen size). Use it for slides, posters, social media or anywhere SVG is not accepted.",
        steps=[
            "Click the picture icon.",
            "The PNG file is saved at 3x resolution.",
        ],
        example="Download the Scenario Lab curve as PNG to show the 'years gained' comparison in a talk.",
        tips=[
            "PNG is a raster image: prefer SVG for print and journal submissions.",
        ],
    ),

    # 8. Download data (CSV)
    control_card(
        icon="\u25a6",
        name="Download Data (Grid Icon)",
        description="Downloads the numbers behind the chart as a CSV file that opens in Excel, LibreOffice, R or Python. Each row has the series name, the x and y values and, for heatmaps, the cell value.",
        steps=[
            "Click the grid icon.",
            "A CSV file with every series of the chart is saved.",
            "Open it in a spreadsheet or analysis tool.",
        ],
        example="Download the data of the resistance heatmap to check the exact value of each pathogen-antibiotic pair, including any what-if changes you made in the Sensitivity Analysis panel.",
        tips=[
            "The CSV contains what the chart shows, including scenario changes made on the page.",
            "Empty cells mean intrinsic resistance or no value (grey cells in the heatmap).",
        ],
    ),

    # 9. Full screen
    control_card(
        icon="\u26f6",
        name="Full Screen (Corners Icon)",
        description="Expands the chart to fill the whole screen, useful for presentations and for reading dense charts such as the heatmap.",
        steps=[
            "Click the four-corners icon (last button on the right).",
            "The chart fills the screen; all tools keep working.",
            "Press Esc (or click the icon again) to return to the page.",
        ],
        example="Open the resistance heatmap in full screen during a meeting so every value is readable from across the room.",
    ),

    # General Tips section
    html.H2("General Tips", style={
        "color": "#e8eaed", "marginTop": "2rem", "marginBottom": "1rem",
        "borderBottom": "1px solid #2d2f3a", "paddingBottom": "0.5rem",
    }),

    html.Div([
        html.Div([
            html.H3("Hover and Legends", className="card-title"),
            html.Ul([
                html.Li([
                    html.Strong("Hover for details: "),
                    "Move your cursor over any data point to see a tooltip with precise values, years, and source information.",
                ]),
                html.Li([
                    html.Strong("Click legend items to toggle: "),
                    "Single-click any series name in the legend to show or hide that series. The icon will dim when hidden.",
                ]),
                html.Li([
                    html.Strong("Double-click to isolate: "),
                    "Double-click a legend item to hide all other series and show only that one. Double-click again to restore all.",
                ]),
                html.Li([
                    html.Strong("Mouse wheel zoom: "),
                    "Scroll the mouse wheel while hovering over the chart to zoom in and out centered on the cursor position.",
                ]),
                html.Li([
                    html.Strong("Modebar location: "),
                    "The toolbar sits in the top-right corner of every chart and is always visible: navigation tools on the left, downloads and full screen on the right.",
                ]),
            ], style={"color": "#b0b3b8", "lineHeight": "1.8"}),
        ], className="card"),

        html.Div([
            html.H3("Keyboard and Mouse Shortcuts", className="card-title"),
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Action", style={"textAlign": "left", "padding": "0.5rem"}),
                    html.Th("Shortcut", style={"textAlign": "left", "padding": "0.5rem"}),
                ])),
                html.Tbody([
                    html.Tr([html.Td("Reset view"), html.Td("Double-click chart background")]),
                    html.Tr([html.Td("Temporary pan (in zoom mode)"), html.Td("Hold Shift + drag")]),
                    html.Tr([html.Td("Add to selection"), html.Td("Shift + drag")]),
                    html.Tr([html.Td("Zoom in/out"), html.Td("Mouse wheel scroll")]),
                    html.Tr([html.Td("Clear selection"), html.Td("Click empty area")]),
                    html.Tr([html.Td("Isolate series"), html.Td("Double-click legend item")]),
                    html.Tr([html.Td("Toggle series"), html.Td("Single-click legend item")]),
                ]),
            ], className="data-table", style={"width": "100%"}),
        ], className="card"),
    ], className="chart-grid-2"),

    # Chart map — where to find each chart
    html.H2("Where to find each chart", style={
        "color": "#e8eaed", "marginTop": "2rem", "marginBottom": "1rem",
        "borderBottom": "1px solid #2d2f3a", "paddingBottom": "0.5rem",
    }),
    html.Div([
        html.Table([
            html.Thead(html.Tr([
                html.Th("Chart"),
                html.Th("Page"),
                html.Th("What it shows"),
            ])),
            html.Tbody([
                html.Tr([html.Td("Resistance Pressure Trajectory"),
                         html.Td(dcc.Link("Overview", href="/", style={"color": "var(--accent)"})),
                         html.Td("Super-exponential curve + reference logistic + ±3 yr band + critical 2040-2047 zone")]),
                html.Tr([html.Td("Mortality Projections"),
                         html.Td(dcc.Link("Overview", href="/", style={"color": "var(--accent)"})),
                         html.Td("Murray/GRAM/O'Neill stack + Tai 2025 (~1.91M @ 2040) overlay")]),
                html.Tr([html.Td("Carbapenem 2035 Spotlight"),
                         html.Td(dcc.Link("Overview", href="/", style={"color": "var(--accent)"})),
                         html.Td("Stacked CRE + CRAB + CRPA mortality through 2035 (Tai 2025; paper Introduction)")]),
                html.Tr([html.Td("ESKAPEE Resistance Heatmap"),
                         html.Td(dcc.Link("Pathogens", href="/pathogens", style={"color": "var(--accent)"})),
                         html.Td("11×10 matrix with WHO priority + Magiorakos MDR/XDR/PDR badges")]),
                html.Tr([html.Td("Sensitivity Analysis (companion)"),
                         html.Td(dcc.Link("Pathogens", href="/pathogens", style={"color": "var(--accent)"})),
                         html.Td("What-if: single cells, whole rows/columns, presets, difference view (transient, reset on reload)")]),
                html.Tr([html.Td("Regional Variation"),
                         html.Td(dcc.Link("Pathogens", href="/pathogens", style={"color": "var(--accent)"})),
                         html.Td("Resistance rates across 6 WHO regions for 4 key pathogens")]),
                html.Tr([html.Td("Temporal Trends"),
                         html.Td(dcc.Link("Pathogens", href="/pathogens", style={"color": "var(--accent)"})),
                         html.Td("MRSA / 3GC-R E. coli / CRE K. pneumoniae 25-year trajectory")]),
                html.Tr([html.Td("SARIMA Forecast"),
                         html.Td(dcc.Link("Time Series", href="/timeseries", style={"color": "var(--accent)"})),
                         html.Td("Monthly resistance forecast with 95% CI + scenario comparison + diagnostics")]),
                html.Tr([html.Td("PubMed Scientometric"),
                         html.Td(dcc.Link("Industry", href="/industry", style={"color": "var(--accent)"})),
                         html.Td("~253K cumulative publications 1990-2025")]),
                html.Tr([html.Td("Market Growth (CAGR 5.4%)"),
                         html.Td(dcc.Link("Industry", href="/industry", style={"color": "var(--accent)"})),
                         html.Td("Univdatos 2024-2032 projection ($5.5B → $8.83B)")]),
                html.Tr([html.Td("Drug Class Breakdown"),
                         html.Td(dcc.Link("Industry", href="/industry", style={"color": "var(--accent)"})),
                         html.Td("Oxazolidinones / Lipoglycopeptides / Tetracyclines / Others — 2023 vs 2032")]),
                html.Tr([html.Td("Awareness vs Effectiveness divergence"),
                         html.Td(dcc.Link("Industry", href="/industry", style={"color": "var(--accent)"})),
                         html.Td("Log-scale 1990=1 — awareness 500× vs effectiveness 0.34× (paper bibliometrics & industry note)")]),
                html.Tr([html.Td("Paradigm Comparison"),
                         html.Td(dcc.Link("Metabolic", href="/metabolic", style={"color": "var(--accent)"})),
                         html.Td("Classical (data-driven) + qualitative antimetabolic envelope (working hypothesis)")]),
                html.Tr([html.Td("Data Coverage Timeline"),
                         html.Td(dcc.Link("Data Sources", href="/datasources", style={"color": "var(--accent)"})),
                         html.Td("Gantt-style temporal coverage of every data source")]),
            ]),
        ], className="data-table", style={"width": "100%"}),
        html.P([
            "All 11 charts are also available in the ",
            dcc.Link("Export Studio", href="/export", style={"color": "var(--accent)"}),
            " with three publication-ready themes (Dashboard Dark, Publication Light, Print B&W). For the full bibliography of every source cited in any chart, see the ",
            dcc.Link("References", href="/references", style={"color": "var(--accent)"}),
            " page.",
        ], style={"color": "#9aa0a6", "marginTop": "1rem", "fontSize": "0.85rem"}),
    ], className="card"),
])
