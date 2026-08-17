"""
Methods page — Materials & Methods of the paper: the open computational
companion (programming tools, implementation, components, access & licensing,
reproducibility, citation). Mirrors the manuscript's Materials and Methods
section so the methodology is inspectable from within the app itself.
"""

import dash
from dash import html

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from components import help_section

dash.register_page(__name__, path="/methods", name="Methods")


def _card(title, *children):
    return html.Div([html.H3(title, className="card-title"), *children], className="card")


layout = html.Div([
    help_section("Methods", [
        "This page reproduces the Materials & Methods of the paper: how the open "
        "computational companion is built, what it contains, how it is licensed, and "
        "why it is fully reproducible. Every quantitative claim in the paper can be "
        "traced and re-derived through this application.",
    ]),

    _card(
        "Programming tools & computational companion",
        html.P(
            "The quantitative claims rest on a multi-source synthesis: more than ten "
            "peer-reviewed sources for the resistance trajectory, three independent "
            "mortality streams (GRAM/O'Neill, Murray 2022, Tai 2025), a per-pathogen "
            "surveillance matrix spanning four global agencies (WHO GLASS, ECDC "
            "EARS-Net, CDC AR Threats, Murray 2022), and a complementary SARIMA "
            "exercise. The literature was harvested from PubMed, EMBASE and the "
            "Cochrane Library."
        ),
        html.P([
            "Rather than static figures, we developed an open computational companion "
            "that exposes every model surface, anchor table and calibration coefficient "
            "to direct inspection, following the ",
            html.A("FAIR Principles for Research Software", href="https://doi.org/10.1038/s41597-022-01710-x", target="_blank"),
            " and the ",
            html.A("Force11 Software Citation Principles", href="https://doi.org/10.7717/peerj-cs.86", target="_blank"),
            ".",
        ]),
    ),

    _card(
        "Implementation",
        html.P(
            "A multi-page interactive application implemented in Python 3.12. NumPy and "
            "pandas drive the closed-form models; statsmodels performs the SARIMA fits; "
            "and the rendering layer is built on Plotly and Dash. The application runs "
            "as a single self-contained process and requires no external API at "
            "run-time — every coefficient and anchor point is embedded in the source — "
            "so it can be served as a public web instance or executed offline from a "
            "local clone with identical results."
        ),
    ),

    _card(
        "Components",
        html.P("The application is organized in ten pages that mirror the structure of the paper:"),
        html.Ul([
            html.Li([html.B("Overview"), " — the super-exponential resistance trajectory against the constant-rate reference logistic, with published anchor points and the 2040–2047 critical-point window."]),
            html.Li([html.B("Pathogens"), " — the ESKAPEE × antibiotic-class surveillance matrix with WHO priority labels and Magiorakos (2012) MDR/XDR/PDR badges, plus regional and temporal-trend panels."]),
            html.Li([html.B("Time Series"), " — SARIMAX(1,1,1)(1,1,0,12) fits with ACF/PACF correlograms, residual diagnostics, AIC/BIC and a counterfactual intervention scenario."]),
            html.Li([html.B("Industry"), " — bibliometric growth (PubMed 1990–2025), the antibiotic-resistance market (CAGR 5.4% through 2032), and the awareness-vs-effectiveness divergence."]),
            html.Li([html.B("Metabolic"), " — scaffolds the antimetabolic line of treatment at a conceptual level (presented as a working hypothesis)."]),
            html.Li([html.B("Data Sources, References, Export Studio, Documentation, Tutorial"), " — a fully cited source list with direct links, a publication-grade figure-export workspace, and onboarding material for first-time users."]),
        ], style={"paddingLeft": "1.2rem", "lineHeight": "1.7"}),
    ),

    _card(
        "Access & licensing",
        html.P([
            "The source code is released under an open-source license and will be "
            "deposited in a long-term archive (",
            html.A("Zenodo", href="https://zenodo.org/", target="_blank"),
            ") with a citable DOI at the time of publication. Following the Force11 "
            "Software Citation Principles, we ask that any reuse of the model "
            "coefficients, anchor tables or visualizations cite the deposited release "
            "rather than the paper alone. The application is publicly available at ",
            html.A("resistome.imhoit.com", href="https://resistome.imhoit.com", target="_blank"),
            ".",
        ]),
    ),

    _card(
        "Reproducibility",
        html.P(
            "The central super-exponential forecast is a closed-form analytic "
            "expression with hand-calibrated coefficients — no parameter fitting, no "
            "random sampling and no Monte Carlo. Mortality and pathogen-surveillance "
            "values are loaded from named published sources and presented as such, not "
            "derived from the resistance-pressure model. The SARIMA series are "
            "generated deterministically with a fixed seed, so the diagnostic plots "
            "reproduce identically across machines. Every figure can therefore be "
            "re-derived bit-for-bit from the open source — the minimum bar the FAIR4RS "
            "framework sets for research software supporting a publication."
        ),
    ),

    _card(
        "Cite this companion",
        html.P(
            "Prieto Gratacós, E. & Botto, J. A. (2026). The Twilight of Antibiotics "
            "— open computational companion [Software]. Zenodo. "
            "DOI: [to be assigned at publication]. Available at resistome.imhoit.com",
            style={
                "fontFamily": "var(--font-mono)",
                "fontSize": "0.83rem",
                "background": "var(--bg-secondary)",
                "border": "1px solid var(--border)",
                "borderRadius": "6px",
                "padding": "0.7rem 0.9rem",
                "lineHeight": "1.55",
            },
        ),
    ),
])
