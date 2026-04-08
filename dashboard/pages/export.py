"""
Export Studio page — Preview and export charts with different color themes.
"""

import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import numpy as np

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from components import help_section, chart_title_with_info
from data.amr_data import (
    compute_sigmoid_curve,
    OBSERVED_DATA,
    FORECAST_DATA,
    MORTALITY_DATA,
)
from data.pathogen_data import (
    PATHOGENS,
    ANTIBIOTIC_CLASSES,
    RESISTANCE_MATRIX,
    WHO_PRIORITY,
    REGIONAL_DATA,
    TEMPORAL_TRENDS,
)

dash.register_page(__name__, path="/export", name="Export")

# ---------------------------------------------------------------------------
# Chart names matching overview and pathogens pages
# ---------------------------------------------------------------------------
CHART_OPTIONS = [
    {"label": "AMR Resistance Curve (Overview)", "value": "main_curve"},
    {"label": "Mortality Projections (Overview)", "value": "mortality"},
    {"label": "Resistance Heatmap (Pathogens)", "value": "heatmap"},
    {"label": "Regional Variation (Pathogens)", "value": "regional"},
    {"label": "Temporal Trends (Pathogens)", "value": "trends"},
]

FORMAT_OPTIONS = [
    {"label": "SVG", "value": "svg"},
    {"label": "PNG", "value": "png"},
    {"label": "PDF", "value": "pdf"},
]

SCALE_OPTIONS = [
    {"label": "1x (screen)", "value": 1},
    {"label": "2x (presentation)", "value": 2},
    {"label": "3x (publication 300 dpi)", "value": 3},
]

COLOR_SCHEME_OPTIONS = [
    {"label": "Dashboard Dark", "value": "dark"},
    {"label": "Publication Light", "value": "light"},
    {"label": "Print B&W", "value": "bw"},
]

# ---------------------------------------------------------------------------
# Color theme definitions
# ---------------------------------------------------------------------------
THEMES = {
    "dark": {
        "paper_bgcolor": "#21232d",
        "plot_bgcolor": "#21232d",
        "font_color": "#e8eaed",
        "gridcolor": "#2d2f3a",
        "accent1": "#4fc3f7",
        "accent2": "#ef5350",
        "accent3": "#ffb74d",
        "accent4": "#ce93d8",
        "accent5": "#66bb6a",
        "fill_alpha": 0.15,
        "bar_colors": {
            "attributable": "#ef5350",
            "associated": "#ffb74d",
        },
        "heatmap_colorscale": [
            [0, "#1a3a4a"],
            [0.3, "#4fc3f7"],
            [0.5, "#ffb74d"],
            [0.7, "#ff7043"],
            [1.0, "#ef5350"],
        ],
        "heatmap_text_color": "white",
        "annotation_color": "#ef5350",
    },
    "light": {
        "paper_bgcolor": "white",
        "plot_bgcolor": "white",
        "font_color": "black",
        "gridcolor": "#cccccc",
        "accent1": "#1565c0",
        "accent2": "#c62828",
        "accent3": "#e65100",
        "accent4": "#6a1b9a",
        "accent5": "#2e7d32",
        "fill_alpha": 0.12,
        "bar_colors": {
            "attributable": "#c62828",
            "associated": "#e65100",
        },
        "heatmap_colorscale": [
            [0, "#e3f2fd"],
            [0.3, "#42a5f5"],
            [0.5, "#ffa726"],
            [0.7, "#ef6c00"],
            [1.0, "#c62828"],
        ],
        "heatmap_text_color": "black",
        "annotation_color": "#c62828",
    },
    "bw": {
        "paper_bgcolor": "white",
        "plot_bgcolor": "white",
        "font_color": "black",
        "gridcolor": "#bbbbbb",
        "accent1": "#222222",
        "accent2": "#555555",
        "accent3": "#888888",
        "accent4": "#aaaaaa",
        "accent5": "#444444",
        "fill_alpha": 0.08,
        "bar_colors": {
            "attributable": "#333333",
            "associated": "#999999",
        },
        "heatmap_colorscale": [
            [0, "#f5f5f5"],
            [0.5, "#888888"],
            [1.0, "#111111"],
        ],
        "heatmap_text_color": "black",
        "annotation_color": "#333333",
    },
}


def _base_layout(theme):
    """Return shared layout properties (without margin)."""
    return dict(
        paper_bgcolor=theme["paper_bgcolor"],
        plot_bgcolor=theme["plot_bgcolor"],
        font=dict(color=theme["font_color"], family="Inter, sans-serif", size=12),
    )


# ---------------------------------------------------------------------------
# Chart builders — each sets its own margin
# ---------------------------------------------------------------------------

def build_main_curve(theme):
    """AMR resistance sigmoid curve with confidence bands."""
    curve = compute_sigmoid_curve()
    fig = go.Figure()

    # Confidence band upper
    fig.add_trace(go.Scatter(
        x=curve["year"], y=curve["upper_bound"],
        mode="lines", line=dict(width=0),
        showlegend=False, hoverinfo="skip",
    ))
    # Confidence band lower
    fill_rgba = f"rgba({_hex_to_rgb(theme['accent1'])}, {theme['fill_alpha']})"
    fig.add_trace(go.Scatter(
        x=curve["year"], y=curve["lower_bound"],
        mode="lines", line=dict(width=0),
        fill="tonexty", fillcolor=fill_rgba,
        name="Uncertainty band", hoverinfo="skip",
    ))

    # Observed segment
    obs = curve[curve["year"] <= 2025]
    fig.add_trace(go.Scatter(
        x=obs["year"], y=obs["resistance_index"],
        mode="lines", line=dict(color=theme["accent1"], width=3),
        name="Observed (1990-2025)",
        hovertemplate="<b>%{x}</b><br>Resistance Index: %{y:.1f}<extra></extra>",
    ))

    # Forecast segment
    fcast = curve[curve["year"] >= 2025]
    fig.add_trace(go.Scatter(
        x=fcast["year"], y=fcast["resistance_index"],
        mode="lines", line=dict(color=theme["accent2"], width=3, dash="dash"),
        name="Forecast (2025-2060)",
        hovertemplate="<b>%{x}</b><br>Resistance Index: %{y:.1f} (projected)<extra></extra>",
    ))

    # Published data point markers
    fig.add_trace(go.Scatter(
        x=OBSERVED_DATA["year"], y=OBSERVED_DATA["resistance_index"],
        mode="markers",
        marker=dict(color=theme["accent1"], size=8, symbol="circle",
                    line=dict(color=theme["paper_bgcolor"], width=1.5)),
        name="Published data points",
        customdata=OBSERVED_DATA["source"],
        hovertemplate="<b>%{x}</b><br>Index: %{y}<br>Source: %{customdata}<extra></extra>",
    ))

    # Critical threshold
    fig.add_hline(
        y=95, line_dash="dot", line_color=theme["annotation_color"], line_width=1,
        annotation_text="Critical threshold (~95)",
        annotation_position="top left",
        annotation_font=dict(color=theme["annotation_color"], size=11),
    )

    # Critical point zone
    fig.add_vrect(
        x0=2040, x1=2045,
        fillcolor=f"rgba({_hex_to_rgb(theme['accent2'])}, 0.1)",
        line_width=0,
        annotation_text="Critical Point",
        annotation_position="top",
        annotation_font=dict(color=theme["annotation_color"], size=11),
    )

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="AMR Resistance Pressure Index (1990-2060)", font=dict(size=16)),
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"], zerolinecolor=theme["gridcolor"]),
        yaxis_title="Resistance Pressure Index (0-100)",
        yaxis=dict(range=[0, 105], gridcolor=theme["gridcolor"], zerolinecolor=theme["gridcolor"]),
        height=500,
        margin=dict(l=60, r=30, t=50, b=50),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    return fig


def build_mortality(theme):
    """AMR mortality projection chart."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=MORTALITY_DATA["year"],
        y=MORTALITY_DATA["attributable_deaths_k"],
        name="Directly attributable",
        marker_color=theme["bar_colors"]["attributable"],
        hovertemplate="<b>%{x}</b><br>%{y:,}K deaths<extra>Attributable</extra>",
    ))

    fig.add_trace(go.Bar(
        x=MORTALITY_DATA["year"],
        y=MORTALITY_DATA["associated_deaths_k"] - MORTALITY_DATA["attributable_deaths_k"],
        name="Associated (additional)",
        marker_color=theme["bar_colors"]["associated"],
        hovertemplate="<b>%{x}</b><br>%{y:,}K additional<extra>Associated</extra>",
    ))

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Projected AMR Mortality (thousands/year)", font=dict(size=14)),
        barmode="stack",
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"], zerolinecolor=theme["gridcolor"]),
        yaxis_title="Deaths (thousands)",
        yaxis=dict(gridcolor=theme["gridcolor"], zerolinecolor=theme["gridcolor"]),
        height=380,
        margin=dict(l=60, r=30, t=50, b=50),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    return fig


def build_heatmap(theme):
    """Pathogen vs antibiotic resistance heatmap."""
    hover_text = []
    display_text = []
    for i, pathogen in enumerate(PATHOGENS):
        hover_row = []
        display_row = []
        for j, abx in enumerate(ANTIBIOTIC_CLASSES):
            val = RESISTANCE_MATRIX[i, j]
            abx_clean = abx.replace("\n", " ")
            if np.isnan(val):
                hover_row.append(f"{pathogen}<br>{abx_clean}<br>N/A (intrinsic R or not tested)")
                display_row.append("\u2014")
            else:
                hover_row.append(f"{pathogen}<br>{abx_clean}<br><b>{val:.0f}%</b> resistant")
                display_row.append(f"{val:.0f}")
        hover_text.append(hover_row)
        display_text.append(display_row)

    y_labels = [f"{p}  [{WHO_PRIORITY[p]}]" for p in PATHOGENS]

    fig = go.Figure(data=go.Heatmap(
        z=RESISTANCE_MATRIX,
        x=ANTIBIOTIC_CLASSES,
        y=y_labels,
        text=display_text,
        texttemplate="%{text}",
        textfont=dict(size=11, color=theme["heatmap_text_color"]),
        hovertext=hover_text,
        hovertemplate="%{hovertext}<extra></extra>",
        colorscale=theme["heatmap_colorscale"],
        zmin=0, zmax=100,
        colorbar=dict(
            title=dict(text="% Resistant", font=dict(size=11)),
            ticksuffix="%", len=0.9,
        ),
        xgap=2, ygap=2,
    ))

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Resistance Profile: Pathogen x Antibiotic Class", font=dict(size=15)),
        xaxis=dict(side="bottom", tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
        height=550,
        margin=dict(l=180, r=80, t=60, b=100),
    )
    return fig


def build_regional(theme):
    """Regional resistance comparison (grouped bar)."""
    fig = go.Figure()

    pathogens_in_data = REGIONAL_DATA["pathogen"].unique()
    color_map = {
        "K. pneumoniae": theme["accent2"],
        "E. coli": theme["accent1"],
        "S. aureus (MRSA)": theme["accent3"],
        "A. baumannii": theme["accent4"],
    }

    for pathogen in pathogens_in_data:
        subset = REGIONAL_DATA[REGIONAL_DATA["pathogen"] == pathogen]
        fig.add_trace(go.Bar(
            x=subset["region"],
            y=subset["resistance_index"],
            name=pathogen,
            marker_color=color_map.get(pathogen, theme["accent5"]),
            hovertemplate=f"<b>{pathogen}</b><br>%{{x}}<br>Resistance: %{{y}}%<extra></extra>",
        ))

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Regional Resistance (key pathogens, 3GC/Carbapenem)", font=dict(size=14)),
        barmode="group",
        xaxis_title="WHO Region",
        xaxis=dict(gridcolor=theme["gridcolor"]),
        yaxis_title="% Resistant Isolates",
        yaxis=dict(range=[0, 100], gridcolor=theme["gridcolor"]),
        height=400,
        margin=dict(l=60, r=30, t=50, b=60),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    )
    return fig


def build_trends(theme):
    """Temporal trends of key resistance phenotypes."""
    fig = go.Figure()

    color_map = {
        "MRSA": theme["accent3"],
        "3GC-R E. coli": theme["accent1"],
        "CRE K. pneumoniae": theme["accent2"],
    }

    for phenotype in TEMPORAL_TRENDS["phenotype"].unique():
        subset = TEMPORAL_TRENDS[TEMPORAL_TRENDS["phenotype"] == phenotype]
        fig.add_trace(go.Scatter(
            x=subset["year"],
            y=subset["prevalence"],
            mode="lines+markers",
            name=phenotype,
            line=dict(color=color_map.get(phenotype, theme["accent5"]), width=2.5),
            marker=dict(size=4),
            hovertemplate=f"<b>{phenotype}</b><br>%{{x}}<br>Prevalence: %{{y}}%<extra></extra>",
        ))

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Resistance Trends (2000-2025): Key Phenotypes", font=dict(size=14)),
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"]),
        yaxis_title="% Resistant",
        yaxis=dict(range=[0, 60], gridcolor=theme["gridcolor"]),
        height=400,
        margin=dict(l=60, r=30, t=50, b=50),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    )
    return fig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_color):
    """Convert hex color like '#4fc3f7' to 'r, g, b' string."""
    h = hex_color.lstrip("#")
    return ", ".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


CHART_BUILDERS = {
    "main_curve": build_main_curve,
    "mortality": build_mortality,
    "heatmap": build_heatmap,
    "regional": build_regional,
    "trends": build_trends,
}

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

layout = html.Div([
    # Help section
    help_section("Export Studio", [
        "FORMAT SELECTION -- SVG VS PNG VS PDF: SVG (Scalable Vector Graphics) is recommended for journal submissions and any context where the figure may be resized. SVG files are resolution-independent, produce crisp text and lines at any zoom level, and are accepted by most major publishers (Nature, Lancet, PLOS, BMJ, JAMA). PNG (Portable Network Graphics) is a raster format best suited for presentations (PowerPoint, Google Slides) and web use where you need a simple image file. PNG quality depends on resolution -- always use 2x or 3x scale for clarity. PDF is ideal for standalone figure files in grant applications, reports, and supplementary materials. Note: Plotly exports SVG and PNG natively; for PDF output, export as SVG first and convert using a tool such as Inkscape (free) or Adobe Illustrator.",
        "RESOLUTION GUIDE: The scale multiplier controls the output resolution relative to screen display. 1x (72 dpi equivalent) is suitable only for screen previews and informal sharing. 2x (~150 dpi) is appropriate for slide presentations, posters viewed at a distance, and internal reports. 3x (~300 dpi) meets the minimum resolution requirement for print publication in peer-reviewed journals. Most publishers specify a minimum of 300 dpi for raster images at final print size. When in doubt, export at 3x -- larger files can always be downsampled, but low-resolution exports cannot be improved after the fact.",
        "COLOR THEME GUIDE: 'Dashboard Dark' uses the default dark background optimized for on-screen viewing during analysis and presentations in dimly lit rooms. This theme is not suitable for print publication. 'Publication Light' switches to a white background with high-contrast colors optimized for readability on paper and in PDF viewers. This is the recommended theme for any figure destined for journal submission, reports, or supplementary files. 'Print B&W' uses a white background with grayscale-only encoding, designed for journals that print in black and white or charge extra for color figures. B&W mode uses line patterns and brightness differences to distinguish data series rather than color, ensuring the figure remains interpretable without color.",
        "POST-PROCESSING EXPORTED CHARTS: SVG files exported from this dashboard can be opened directly in vector graphics editors such as Adobe Illustrator, Inkscape (free, open-source), or Affinity Designer for fine-tuning. Common post-processing tasks include: adjusting font sizes to match journal style requirements, repositioning legends, adding annotations or callout boxes, combining multiple panels into a composite figure, and converting text to outlines to avoid font embedding issues. When editing SVGs, be careful to preserve the data-encoding elements (paths, shapes) while adjusting only presentational attributes.",
        "JOURNAL-SPECIFIC TIPS: Most biomedical journals accept SVG or high-resolution PNG (300+ dpi). The Lancet and Nature family journals prefer vector formats (SVG, EPS, or PDF). PLOS journals require TIFF or EPS at 300 dpi minimum for print figures. For maximum compatibility, export as SVG at 3x scale and convert to the journal's preferred format during submission. Always check your target journal's 'Guide for Authors' or 'Figure Requirements' page before final export. Common requirements include: minimum 300 dpi, maximum file size (often 10-20 MB per figure), specific color space (RGB for online, CMYK for print), and minimum text size (typically 6-8 pt at final print size).",
        "CITING THE DASHBOARD: When using figures from this dashboard in publications, presentations, or reports, please cite both the dashboard and the underlying primary data sources. A suggested citation format: 'Figure generated using the AMR Research Dashboard (Gratacos-Botto project, 2025), based on data from [list relevant primary sources: Murray et al. Lancet 2022, WHO GLASS 2022, ECDC EARS-Net, O'Neill Review 2016, GRAM/CIDRAP] as applicable.' Each chart on the Overview and Pathogens pages lists its specific data sources below the visualization -- include the relevant subset in your citation. For the resistance pressure index specifically, note that it is a composite normalized metric constructed for this research project, not a standard epidemiological measure.",
    ]),

    # Controls row
    html.Div([
        chart_title_with_info(
            "Export Studio",
            "Configure chart appearance and export settings. Choose from dark, light, or black-and-white themes with adjustable resolution for screen, presentation, or print.",
            "Preview charts with publication-ready color schemes, then export via the Plotly modebar.",
        ),

        html.Div([
            # Chart selector
            html.Div([
                html.Label("Chart", style={"fontWeight": "600", "marginBottom": "0.3rem", "display": "block"}),
                dcc.Dropdown(
                    id="export-chart-select",
                    options=CHART_OPTIONS,
                    value="main_curve",
                    clearable=False,
                    style={"backgroundColor": "#2d2f3a", "color": "#e8eaed"},
                ),
            ], style={"flex": "1", "minWidth": "220px"}),

            # Color scheme
            html.Div([
                html.Label("Color Scheme", style={"fontWeight": "600", "marginBottom": "0.3rem", "display": "block"}),
                dcc.Dropdown(
                    id="export-color-scheme",
                    options=COLOR_SCHEME_OPTIONS,
                    value="dark",
                    clearable=False,
                    style={"backgroundColor": "#2d2f3a", "color": "#e8eaed"},
                ),
            ], style={"flex": "1", "minWidth": "180px"}),

            # Format
            html.Div([
                html.Label("Format", style={"fontWeight": "600", "marginBottom": "0.3rem", "display": "block"}),
                dcc.RadioItems(
                    id="export-format",
                    options=FORMAT_OPTIONS,
                    value="svg",
                    inline=True,
                    inputStyle={"marginRight": "4px"},
                    labelStyle={"marginRight": "14px", "cursor": "pointer"},
                ),
            ], style={"flex": "0 0 auto"}),

            # Scale
            html.Div([
                html.Label("Resolution", style={"fontWeight": "600", "marginBottom": "0.3rem", "display": "block"}),
                dcc.RadioItems(
                    id="export-scale",
                    options=SCALE_OPTIONS,
                    value=2,
                    inline=True,
                    inputStyle={"marginRight": "4px"},
                    labelStyle={"marginRight": "14px", "cursor": "pointer"},
                ),
            ], style={"flex": "0 0 auto"}),
        ], style={
            "display": "flex",
            "flexWrap": "wrap",
            "gap": "1.2rem",
            "alignItems": "flex-end",
            "marginTop": "1rem",
        }),
    ], className="card"),

    # Preview area
    html.Div([
        chart_title_with_info(
            "Preview",
            "Live preview of the selected chart with your chosen color scheme and settings. The Plotly modebar (top-right) provides the download button.",
            "The chart below reflects your selected color scheme. Use the camera icon in the Plotly modebar (top-right of chart) to download.",
        ),
        dcc.Graph(
            id="export-preview",
            config={
                "toImageButtonOptions": {"format": "svg", "scale": 2},
                "displayModeBar": True,
            },
        ),
    ], className="card"),

    # Export instructions card
    html.Div([
        html.H3("Export Instructions", className="card-title"),
        html.Div([
            html.Ol([
                html.Li("Select the chart, color scheme, format, and resolution above."),
                html.Li([
                    "In the chart preview, click the ",
                    html.Strong("camera icon"),
                    " in the modebar (top-right corner of the chart).",
                ]),
                html.Li("The chart will be downloaded in the selected format and resolution."),
                html.Li([
                    "For PDF output, export as SVG first, then convert with a tool such as ",
                    html.Code("inkscape"), " or ", html.Code("cairosvg"),
                    ". Browser-native PDF export from Plotly is not supported in all environments.",
                ]),
                html.Li([
                    "For publication use, choose ",
                    html.Strong("Publication Light"),
                    " or ",
                    html.Strong("Print B&W"),
                    " with 3x resolution for 300 dpi quality.",
                ]),
            ], style={"color": "#9aa0a6", "fontSize": "0.88rem", "lineHeight": "1.7"}),
        ]),
    ], className="card"),
])


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@callback(
    Output("export-preview", "figure"),
    Output("export-preview", "config"),
    Input("export-chart-select", "value"),
    Input("export-color-scheme", "value"),
    Input("export-format", "value"),
    Input("export-scale", "value"),
)
def update_preview(chart_name, color_scheme, fmt, scale):
    theme = THEMES.get(color_scheme, THEMES["dark"])
    builder = CHART_BUILDERS.get(chart_name, build_main_curve)
    fig = builder(theme)

    config = {
        "toImageButtonOptions": {
            "format": fmt,
            "scale": scale,
            "filename": f"amr_{chart_name}_{color_scheme}",
        },
        "displayModeBar": True,
    }

    return fig, config
