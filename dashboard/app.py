"""
THE TWILIGHT OF ANTIBIOTICS — Research Dashboard
AMR Resistance Modeling & Forecasting Platform
"""

import os

import dash
from dash import Dash, html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="AMR Research Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# WSGI entry point for gunicorn (production): reference as `app:server`.
# (gunicorn 23+ rejects the dotted `app:app.server` spec.)
server = app.server

# Published paper (open access, archived on Zenodo)
PAPER_URL = "https://doi.org/10.5281/zenodo.21898960"
JOURNAL_URL = "https://www.bjmhr.com"
PAPER_CITATION = ("Prieto Gratacós E, Botto J. The Twilight of Antibiotics. "
                  "Br J Med Health Res. 2026;13(8):43-56")

_app_body = html.Div(
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
                # Direct access to the published paper (open-access PDF on Zenodo)
                html.A(
                    "📄 Read the paper",
                    href=PAPER_URL,
                    target="_blank",
                    title=PAPER_CITATION,
                    className="paper-pill",
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
                html.A("Br J Med Health Res. 2026;13(8):43-56",
                       href=PAPER_URL, target="_blank",
                       style={"color": "var(--accent)", "fontWeight": "600",
                              "fontFamily": "var(--font-mono)"}),
                " (",
                html.A("British Journal of Medical and Health Research",
                       href=JOURNAL_URL, target="_blank"),
                ") · E. Prieto Gratacós, J.A. Botto · ",
                "Data sources: Lancet GBD, O'Neill Review, GRAM/CIDRAP, "
                "Tai 2025 IJAA, Magiorakos 2012, WHO GLASS",
            ]),
            className="footer",
        ),
    ],
    className="app-container",
)

# Mantine (dmc) provides the modern, accessible controls (SegmentedControl,
# Select, Slider, Button) used on the interactive pages. The provider must wrap
# the whole layout so those components work on any page. Theme is aligned to the
# app's dark palette (cyan accent); fonts are inherited from style.css.
app.layout = dmc.MantineProvider(
    forceColorScheme="dark",
    theme={
        "primaryColor": "cyan",
        "primaryShade": 4,
        "fontFamily": "inherit",
        "fontFamilyMonospace": "var(--font-mono, monospace)",
        "defaultRadius": "md",
    },
    children=_app_body,
)

NAV_ITEMS = [
    ("Overview", "/"),
    ("Scenario Lab", "/scenarios"),
    ("Pathogens", "/pathogens"),
    ("Time Series", "/timeseries"),
    ("Industry", "/industry"),
    ("Metabolic", "/metabolic"),
    ("Methods", "/methods"),
    ("Data Sources", "/datasources"),
    ("References", "/references"),
    ("Export Studio", "/export"),
    ("Documentation", "/docs"),
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
