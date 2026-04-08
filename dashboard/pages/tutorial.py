"""
Tutorial page — Interactive guide to Plotly chart controls.
"""

import dash
from dash import html, dcc
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from components import help_section, chart_title_with_info

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
    """Build an interactive demo chart with sample AMR data for practicing controls."""
    years = list(range(1990, 2061))
    # Sigmoid curve for resistance index
    resistance = [100 / (1 + 80 * (0.92 ** (y - 1990))) for y in years]

    fig = go.Figure()

    # Observed segment
    obs_years = [y for y in years if y <= 2025]
    obs_vals = resistance[:len(obs_years)]
    fig.add_trace(go.Scatter(
        x=obs_years, y=obs_vals,
        mode="lines+markers",
        line=dict(color="#4fc3f7", width=3),
        marker=dict(size=5, color="#4fc3f7"),
        name="Observed (1990-2025)",
        hovertemplate="<b>%{x}</b><br>Resistance Index: %{y:.1f}<extra></extra>",
    ))

    # Forecast segment
    fcast_years = [y for y in years if y >= 2025]
    fcast_vals = resistance[years.index(2025):]
    fig.add_trace(go.Scatter(
        x=fcast_years, y=fcast_vals,
        mode="lines+markers",
        line=dict(color="#ef5350", width=3, dash="dash"),
        marker=dict(size=5, color="#ef5350"),
        name="Forecast (2025-2060)",
        hovertemplate="<b>%{x}</b><br>Resistance Index: %{y:.1f} (projected)<extra></extra>",
    ))

    # Key data points with labels
    key_years = [1990, 2000, 2010, 2019, 2025, 2035, 2045, 2060]
    key_vals = [100 / (1 + 80 * (0.92 ** (y - 1990))) for y in key_years]
    key_labels = [
        "Baseline era",
        "MRSA/ESBL era",
        "GBD benchmark",
        "1.27M deaths/yr",
        "Current (2025)",
        "Accelerating",
        "Critical point",
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
        annotation_text="Critical threshold (~95)",
        annotation_position="top left",
        annotation_font=dict(color="#ef5350", size=11),
    )

    # Critical point zone
    fig.add_vrect(
        x0=2040, x1=2045,
        fillcolor="rgba(239, 83, 80, 0.1)",
        line_width=0,
        annotation_text="Critical Zone",
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
    ]),

    # Demo chart
    html.Div([
        chart_title_with_info(
            "Practice Chart -- Try the Controls",
            "This is a demo chart for practicing Plotly interactive controls. It uses a subset of the AMR sigmoid curve data with key milestones marked. Hover over the top-right corner to reveal the toolbar, then try each control described below.",
            "Use this chart to practice all 10 toolbar controls described below",
        ),
        dcc.Graph(
            id="tutorial-demo-chart",
            figure=build_demo_chart(),
            config={
                "toImageButtonOptions": {"format": "svg", "filename": "amr_tutorial_demo", "scale": 3},
                "displayModeBar": True,
                "modeBarButtonsToAdd": ["toggleSpikelines"],
            },
        ),
        html.P(
            "Hover over the top-right corner of the chart above to reveal the modebar toolbar. Then follow the guides below to learn each control.",
            style={"color": "#b0b3b8", "fontStyle": "italic", "marginTop": "0.5rem"},
        ),
    ], className="card"),

    # Tutorial section header
    html.H2("Chart Controls Reference", style={
        "color": "#e8eaed", "marginTop": "2rem", "marginBottom": "1rem",
        "borderBottom": "1px solid #2d2f3a", "paddingBottom": "0.5rem",
    }),
    html.P(
        "Each chart in the dashboard includes a toolbar (modebar) that appears when you hover over the top-right corner. Below is a detailed guide for each control, from left to right.",
        style={"color": "#b0b3b8", "marginBottom": "1.5rem"},
    ),

    # 1. Download Plot
    control_card(
        icon="\U0001f4f7",
        name="Download Plot (Camera Icon)",
        description="Downloads the current chart view as an image file. In this dashboard, all charts are configured to export as SVG at 3x scale for publication-quality output.",
        steps=[
            "Hover over the chart to reveal the toolbar in the top-right corner.",
            "Click the camera icon (first button on the left).",
            "The chart will be downloaded automatically as an SVG file.",
            "Open the SVG in any browser, vector editor (Inkscape, Illustrator), or import into your manuscript.",
        ],
        example="Download the resistance curve as a high-resolution SVG for inclusion in your paper. SVG files are vector graphics, so they scale perfectly for print at any size.",
        tips=[
            "SVG format preserves text as selectable/searchable text, unlike PNG.",
            "Right-click the chart for additional browser-level save options (e.g., copy image).",
            "SVG files can be converted to PDF, EPS, or PNG using Inkscape or online tools.",
            "The 3x scale ensures sharp output even when downscaled for publication columns.",
        ],
    ),

    # 2. Zoom
    control_card(
        icon="\U0001f50d",
        name="Zoom (Magnifying Glass)",
        description="Enables rectangular zoom mode. Click and drag on the chart to draw a box around the area you want to zoom into. The axes will rescale to show only the selected region.",
        steps=[
            "Click the magnifying glass icon in the toolbar (active by default).",
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

    # 3. Pan
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

    # 4. Box Select
    control_card(
        icon="\u25a1",
        name="Box Select (Dotted Rectangle)",
        description="Draws a rectangular selection box to highlight and select data points within that region. Selected points are visually emphasized while others are dimmed.",
        steps=[
            "Click the dotted-rectangle icon in the toolbar.",
            "Click and drag on the chart to draw a rectangular selection area.",
            "Data points inside the rectangle will be highlighted/selected.",
            "Points outside the selection are dimmed for contrast.",
        ],
        example="Select the cluster of key milestones between 2010-2030 to identify which published data points fall within the steepest acceleration phase of the resistance curve.",
        tips=[
            "Hold Shift and drag to add more points to your existing selection.",
            "Click on empty space (without dragging) to clear the selection.",
            "Useful for identifying outlier data points that deviate from the trend.",
        ],
    ),

    # 5. Lasso Select
    control_card(
        icon="\u27b0",
        name="Lasso Select (Lasso Icon)",
        description="Enables free-form selection by drawing an arbitrary shape. More flexible than box select for irregularly distributed data points.",
        steps=[
            "Click the lasso icon in the toolbar.",
            "Click and hold on the chart, then draw a freehand shape around the points of interest.",
            "Release the mouse -- the shape closes automatically and points inside are selected.",
            "Selected points are highlighted; others are dimmed.",
        ],
        example="Draw a lasso around the key milestone markers that sit above the main curve line to isolate data points with higher-than-expected resistance readings.",
        tips=[
            "Hold Shift while drawing to add to an existing selection.",
            "Lasso select is especially useful with scatter plots that have clusters.",
            "Click on empty space to deselect all points.",
        ],
    ),

    # 6. Zoom In
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

    # 7. Zoom Out
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
            "If you zoom out beyond the data range, use Autoscale to snap back to the data bounds.",
            "Zoom Out can reveal data points that were clipped by previous zoom operations.",
        ],
    ),

    # 8. Autoscale
    control_card(
        icon="\u2922",
        name="Autoscale (Expanding Arrows)",
        description="Automatically adjusts both axes to fit all visible data with optimal padding. Useful for quickly framing the data after manual zoom/pan operations.",
        steps=[
            "Click the expanding-arrows icon in the toolbar.",
            "Both axes rescale automatically to encompass all visible data series.",
            "Padding is added to prevent data from touching the edges.",
        ],
        example="After toggling off the forecast series in the legend and zooming around, click Autoscale to automatically frame just the observed 1990-2025 data with proper margins.",
        tips=[
            "Autoscale respects which series are currently visible (shown in legend).",
            "This differs from Reset Axes, which returns to the original hardcoded view.",
        ],
    ),

    # 9. Reset Axes
    control_card(
        icon="\u2302",
        name="Reset Axes (Home Icon)",
        description="Returns the chart to its original view, undoing all zoom, pan, and autoscale operations. Restores the exact axis ranges the chart was created with.",
        steps=[
            "Click the home icon in the toolbar.",
            "All axes return to their original ranges.",
            "All zoom and pan history is cleared.",
        ],
        example="After exploring different periods of the resistance curve, click Reset Axes to return to the full 1990-2060 view with the y-axis range of 0-105.",
        tips=[
            "Keyboard shortcut: double-click anywhere on the chart background to reset.",
            "Reset Axes restores the original programmed ranges, while Autoscale computes new optimal ranges.",
        ],
    ),

    # 10. Toggle Spike Lines
    control_card(
        icon="\u253c",
        name="Toggle Spike Lines (Crosshair Icon)",
        description="Shows or hides vertical and horizontal guide lines that extend from the cursor position to each axis. These help you read exact values by projecting the cursor position onto the axis labels.",
        steps=[
            "Click the crosshair icon in the toolbar to enable spike lines.",
            "Move your cursor over the chart -- dashed lines will extend from the cursor to both axes.",
            "Read the axis values where the spike lines intersect the axis labels.",
            "Click the crosshair icon again to disable spike lines.",
        ],
        example="Enable spike lines, then hover over the year 2040 to see exactly where the resistance index stands relative to the critical threshold of 95. The horizontal spike line makes it easy to compare values across different years.",
        tips=[
            "Essential for comparing data points at different positions along the timeline.",
            "Spike lines work with all other modes (zoom, pan, select) simultaneously.",
            "Combined with the unified hover mode, spike lines provide the most precise data reading experience.",
        ],
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
                    "The toolbar (modebar) appears in the top-right corner of each chart when you hover over it. It auto-hides when the cursor moves away.",
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
])
