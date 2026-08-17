"""
Methods page — Materials & Methods of the paper, redesigned to be scannable:
every point is a highlighted row, acronyms are expanded in parentheses, and the
"reproducible / open" story reads at a glance. Content mirrors the manuscript's
Materials and Methods section.
"""

import dash
from dash import html

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

dash.register_page(__name__, path="/methods", name="Methods")

CY = "#4fc3f7"   # cyan
PU = "#ce93d8"   # purple
AM = "#ffb74d"   # amber
GR = "#66bb6a"   # green


def _point(emoji, lead, body=None, color=CY):
    """A single highlighted point: emoji + bold lead + optional body."""
    content = [html.B(lead, style={"color": color})]
    if body is not None:
        content.append(html.Span(" — ", style={"color": "var(--text-secondary)"}))
        content.extend(body if isinstance(body, list) else [body])
    return html.Div(
        [
            html.Span(emoji, style={"flex": "0 0 auto", "fontSize": "1.05rem", "width": "1.5rem", "textAlign": "center"}),
            html.Div(content, style={"flex": "1", "lineHeight": "1.5", "fontSize": "0.92rem"}),
        ],
        style={
            "display": "flex", "gap": "0.55rem", "alignItems": "baseline",
            "padding": "0.6rem 0.85rem", "marginBottom": "0.5rem",
            "background": "var(--bg-secondary)", "border": "1px solid var(--border)",
            "borderLeft": f"3px solid {color}", "borderRadius": "9px",
        },
    )


def _section(emoji, title, color, points):
    return html.Div(
        [
            html.Div(
                [
                    html.Span(emoji, style={"fontSize": "1.25rem"}),
                    html.H3(title, style={"margin": 0, "color": color, "fontSize": "1.05rem"}),
                ],
                style={"display": "flex", "alignItems": "center", "gap": "0.55rem", "marginBottom": "0.85rem"},
            ),
            *points,
        ],
        className="card",
    )


def _badge(text, color=CY):
    return html.Span(
        text,
        style={
            "display": "inline-block", "padding": "0.28rem 0.7rem", "margin": "0.2rem 0.35rem 0.2rem 0",
            "background": "var(--bg-secondary)", "border": f"1px solid {color}",
            "color": color, "borderRadius": "999px", "fontSize": "0.78rem", "fontWeight": "600",
            "fontFamily": "var(--font-mono)",
        },
    )


layout = html.Div([

    # Hero
    html.Div(
        [
            html.H2("How it's built — and why every figure can be reproduced, bit for bit.",
                    style={"margin": "0 0 0.6rem", "fontSize": "1.35rem", "lineHeight": "1.3"}),
            html.P("The methods behind the model, and the open companion that lets you verify every number yourself.",
                   style={"color": "var(--text-secondary)", "margin": "0 0 0.9rem", "fontSize": "0.95rem"}),
            html.Div([
                _badge("Python 3.12"), _badge("Plotly + Dash"), _badge("statsmodels"),
                _badge("Open-source", GR), _badge("Zenodo DOI", GR),
                _badge("No fitting", AM), _badge("No randomness", AM), _badge("Bit-for-bit", GR),
            ]),
        ],
        className="card",
        style={"borderLeft": f"3px solid {CY}"},
    ),

    # 1 — Evidence
    _section("📚", "Built on the evidence", CY, [
        _point("📄", "10+ peer-reviewed sources", "for the resistance trajectory.", CY),
        _point("💀", "3 independent mortality streams", "GRAM (Global Research on Antimicrobial Resistance) / O'Neill, Murray 2022, and Tai 2025.", CY),
        _point("🌍", "4 global surveillance agencies", "WHO GLASS (Global Antimicrobial Resistance & Use Surveillance System), ECDC EARS-Net (European Antimicrobial Resistance Surveillance Network), CDC AR Threats (Antibiotic Resistance Threats report), and Murray 2022.", CY),
        _point("🔎", "Literature harvested from", "PubMed, EMBASE and the Cochrane Library.", CY),
        _point("✅", "Built to open-science standards", [
            "the ", html.A("FAIR", href="https://doi.org/10.1038/s41597-022-01710-x", target="_blank"),
            " (Findable, Accessible, Interoperable, Reusable) Principles for Research Software and the ",
            html.A("Force11", href="https://doi.org/10.7717/peerj-cs.86", target="_blank"),
            " software-citation principles.",
        ], CY),
    ]),

    # 2 — How it's built
    _section("🛠️", "How it's built", PU, [
        _point("🐍", "Python 3.12", "the whole application.", PU),
        _point("📊", "NumPy + pandas", "run the closed-form (analytic) models.", PU),
        _point("📈", "statsmodels", "runs the SARIMA (Seasonal AutoRegressive Integrated Moving Average) fits.", PU),
        _point("🎨", "Plotly + Dash", "the interactive charts you're looking at.", PU),
        _point("🔌", "No external API", "(Application Programming Interface) at run-time — every coefficient is embedded in the source.", PU),
        _point("🌐", "Runs online or fully offline", "with identical results.", PU),
    ]),

    # 3 — What's inside
    _section("🧩", "What's inside — 10 pages", AM, [
        _point("📉", "Overview", "the super-exponential curve vs. the constant-rate reference, with the 2040–2047 critical-point window.", AM),
        _point("🦠", "Pathogens", "the ESKAPEE (the 7 priority superbugs) × antibiotic map, with WHO priority and Magiorakos MDR/XDR/PDR (Multidrug- / Extensively drug- / Pandrug-Resistant) badges.", AM),
        _point("⏱️", "Time Series", "SARIMA forecasts with ACF/PACF (Auto- / Partial Autocorrelation) diagnostics and AIC/BIC (Akaike / Bayesian Information Criterion).", AM),
        _point("🏭", "Industry", "publications (PubMed 1990–2025), the market (CAGR — Compound Annual Growth Rate — 5.4%), and awareness-vs-effectiveness.", AM),
        _point("🧪", "Metabolic", "the antimetabolic line of treatment — presented as a working hypothesis.", AM),
        _point("🗂️", "Data Sources · References · Export Studio · Docs · Tutorial", "cited sources, publication-grade figure export, and onboarding.", AM),
    ]),

    # 4 — Open & citable
    _section("📖", "Open & citable", GR, [
        _point("🔓", "Open-source license", "the full source is public.", GR),
        _point("🏛️", "Archived in Zenodo", "with a citable DOI (Digital Object Identifier) at the time of publication.", GR),
        _point("🔗", "Cite the deposited release", "if you reuse the coefficients, tables or visualizations (Force11).", GR),
        _point("🌍", "Live at", [html.A("resistome.imhoit.com", href="https://resistome.imhoit.com", target="_blank")], GR),
    ]),

    # 5 — Reproducible (the WoW)
    _section("🔁", "100% reproducible", GR, [
        _point("🧮", "Closed-form model", "an exact formula — no parameter fitting.", GR),
        _point("🎲", "No random sampling", "and no Monte Carlo simulation.", GR),
        _point("📌", "Data loaded from named sources", "mortality & surveillance values are cited, not model-derived.", GR),
        _point("🌱", "Fixed random seed", "so the SARIMA diagnostics come out identical on any machine.", GR),
        _point("💎", "Every figure re-derivable bit-for-bit", "from the open source — the minimum bar of FAIR4RS (FAIR for Research Software).", GR),
    ]),

    # 6 — Cite
    _section("✍️", "Cite this companion", CY, [
        html.P(
            "Prieto Gratacós, E. & Botto, J. A. (2026). The Twilight of Antibiotics "
            "— open computational companion [Software]. Zenodo. "
            "DOI: [to be assigned at publication]. Available at resistome.imhoit.com",
            style={
                "fontFamily": "var(--font-mono)", "fontSize": "0.82rem",
                "background": "var(--bg-secondary)", "border": "1px solid var(--border)",
                "borderRadius": "8px", "padding": "0.75rem 0.9rem", "lineHeight": "1.55", "margin": 0,
            },
        ),
    ]),
])
