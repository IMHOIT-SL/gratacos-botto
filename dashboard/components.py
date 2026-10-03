"""
Reusable UI components for the AMR dashboard pages.
"""

from dash import html


# Curated chart toolbar, shared by every dcc.Graph in the app.
# Plotly's own selection tools (box/lasso), autoscale, camera and logo are
# removed; assets/graph_toolbar.js adds SVG, PNG 3x, CSV-data and full-screen
# buttons to every chart. What remains: zoom, pan, zoom in/out, reset axes.
_TOOLBAR_REMOVE = ["lasso2d", "select2d", "autoScale2d", "toImage"]


def graph_config(filename=None, **extra):
    """dcc.Graph config with the curated toolbar. `filename` names the
    downloaded SVG/PNG/CSV files (defaults to the graph id)."""
    cfg = {
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": list(_TOOLBAR_REMOVE),
        "toImageButtonOptions": {"format": "svg", "scale": 3},
    }
    if filename:
        cfg["toImageButtonOptions"]["filename"] = filename
    cfg.update(extra)
    return cfg


def help_section(page_title, content_paragraphs):
    """Collapsible help section for top of page."""
    return html.Details([
        html.Summary(f"? Help \u2014 {page_title}", className="help-toggle"),
        html.Div(
            [html.P(p) for p in content_paragraphs],
            className="help-content",
        ),
    ], className="help-section")


def chart_title_with_info(title, tooltip_text, subtitle=None):
    """Chart title with ? icon tooltip."""
    elements = [
        html.Div([
            html.H3(title, className="card-title", style={"margin": "0"}),
            html.Div([
                "?",
                html.Div(tooltip_text, className="chart-tooltip"),
            ], className="chart-info-btn"),
        ], className="chart-header"),
    ]
    if subtitle:
        elements.append(html.P(subtitle, className="card-subtitle"))
    return html.Div(elements)
