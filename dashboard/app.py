"""
THE TWILIGHT OF ANTIBIOTICS — Research Dashboard
AMR Resistance Modeling & Forecasting Platform
"""

import dash
from dash import Dash, html, dcc

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="AMR Research Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.layout = html.Div(
    [
        # Header
        html.Header(
            [
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
                html.Nav(
                    [
                        dcc.Link("Overview", href="/", className="nav-link"),
                        dcc.Link("Pathogens", href="/pathogens", className="nav-link"),
                        dcc.Link("Time Series", href="/timeseries", className="nav-link"),
                        dcc.Link("Data Sources", href="/datasources", className="nav-link"),
                        dcc.Link("Export", href="/export", className="nav-link"),
                        dcc.Link("Docs", href="/docs", className="nav-link"),
                        dcc.Link("Tutorial", href="/tutorial", className="nav-link"),
                    ],
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
            html.P("Gratacos-Botto Research Lab — Data sources: Lancet GBD, O'Neill Review, GRAM, CIDRAP, WHO GLASS"),
            className="footer",
        ),
    ],
    className="app-container",
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
