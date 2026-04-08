"""
Reusable UI components for the AMR dashboard pages.
"""

from dash import html


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
