"""
THE TWILIGHT OF ANTIBIOTICS — Research Dashboard
AMR Resistance Modeling & Forecasting Platform
"""

import os

import dash
from dash import Dash, html, dcc, callback, Input, Output, State

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="AMR Research Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        # Header
        html.Header(
            [
                dcc.Link(
                    html.Div(
                        [
                            html.H1(
                                "THE TWILIGHT OF ANTIBIOTICS",
                                className="header-title",
                            ),
                            html.P(
                                "Antimicrobial Resistance — Research Dashboard",
                                className="header-subtitle",
                            ),
                        ],
                        className="header-text",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                html.Nav(
                    id="nav-bar",
                    className="nav-bar",
                ),
            ],
            className="header",
        ),
        # Page content
        html.Main(
            dash.page_container,
            className="main-content",
        ),
        # Footer
        html.Footer(
            html.P([
                html.Span("Paper v.A-29 · ",
                          style={"color": "var(--accent)", "fontWeight": "600",
                                 "fontFamily": "var(--font-mono)"}),
                "E. Prieto Gratacós, J.A. Botto · ",
                "Data sources: Lancet GBD, O'Neill Review, GRAM/CIDRAP, "
                "Tai 2025 IJAA, Magiorakos 2012, WHO GLASS",
            ]),
            className="footer",
        ),
    ],
    className="app-container",
)

NAV_ITEMS = [
    ("Overview", "/"),
    ("Pathogens", "/pathogens"),
    ("Time Series", "/timeseries"),
    ("Industry", "/industry"),
    ("Metabolic", "/metabolic"),
    ("Data Sources", "/datasources"),
    ("References", "/references"),
    ("Export", "/export"),
    ("Docs", "/docs"),
    ("Tutorial", "/tutorial"),
]


@callback(Output("nav-bar", "children"), Input("url", "pathname"))
def update_nav(pathname):
    """Highlight the active page in the navigation bar."""
    links = []
    for label, href in NAV_ITEMS:
        is_active = (pathname == href) or (pathname and href != "/" and pathname.startswith(href))
        cls = "nav-link active" if is_active else "nav-link"
        links.append(dcc.Link(label, href=href, className=cls))
    return links


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DEBUG", "true").lower() == "true",
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "8082")),
    )
