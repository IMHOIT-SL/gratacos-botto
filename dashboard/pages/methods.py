"""
Methods page — Materials & Methods of the paper.

Sober restyle (Option C): scannable one-point-per-row layout, but the multicolour
emoji are replaced by thin single-tone line icons (accent for section headers,
muted for points) and the four section colours collapse to a single accent.
Acronyms are expanded in parentheses. Content mirrors the manuscript's
Materials and Methods section.
"""

import base64

import dash
from dash import html

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

dash.register_page(__name__, path="/methods", name="Methods")

ACCENT = "#4fc3f7"   # single accent (cyan) — section-header icons + hero rule
MUTED = "#9298a1"    # point icons

# --- Line-icon set (Feather-style inner SVG markup, stroke only) -------------
ICONS = {
    "file": "<path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/><path d='M14 2v6h6'/><path d='M16 13H8'/><path d='M16 17H8'/><path d='M10 9H8'/>",
    "activity": "<path d='M22 12h-4l-3 9L9 3l-3 9H2'/>",
    "globe": "<circle cx='12' cy='12' r='10'/><path d='M2 12h20'/><path d='M12 2a15 15 0 0 1 0 20'/><path d='M12 2a15 15 0 0 0 0 20'/>",
    "search": "<circle cx='11' cy='11' r='8'/><path d='M21 21l-4.35-4.35'/>",
    "check": "<path d='M22 11.08V12a10 10 0 1 1-5.93-9.14'/><path d='M22 4 12 14.01l-3-3'/>",
    "code": "<path d='M16 18l6-6-6-6'/><path d='M8 6l-6 6 6 6'/>",
    "database": "<path d='M12 2c4.42 0 8 1.34 8 3s-3.58 3-8 3-8-1.34-8-3 3.58-3 8-3z'/><path d='M4 5v6c0 1.66 3.58 3 8 3s8-1.34 8-3V5'/><path d='M4 11v6c0 1.66 3.58 3 8 3s8-1.34 8-3v-6'/>",
    "bar": "<path d='M12 20V10'/><path d='M18 20V4'/><path d='M6 20v-4'/>",
    "layers": "<path d='M12 2 2 7l10 5 10-5-10-5z'/><path d='M2 17l10 5 10-5'/><path d='M2 12l10 5 10-5'/>",
    "zap": "<path d='M13 2 3 14h9l-1 8 10-12h-9l1-8z'/>",
    "trending": "<path d='M23 6l-9.5 9.5-5-5L1 18'/><path d='M17 6h6v6'/>",
    "clock": "<circle cx='12' cy='12' r='10'/><path d='M12 6v6l4 2'/>",
    "briefcase": "<rect x='2' y='7' width='20' height='14' rx='2'/><path d='M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16'/>",
    "flask": "<path d='M9 3h6'/><path d='M10 3v6l-5.5 9A2 2 0 0 0 6 21h12a2 2 0 0 0 1.5-3L14 9V3'/>",
    "folder": "<path d='M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z'/>",
    "unlock": "<rect x='3' y='11' width='18' height='11' rx='2'/><path d='M7 11V7a5 5 0 0 1 9.9-1'/>",
    "landmark": "<path d='M3 21h18'/><path d='M5 21v-8'/><path d='M9 21v-8'/><path d='M15 21v-8'/><path d='M19 21v-8'/><path d='M12 3 3 8v2h18V8z'/>",
    "link": "<path d='M10 13a5 5 0 0 0 7.07 0l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71'/><path d='M14 11a5 5 0 0 0-7.07 0l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71'/>",
    "refresh": "<path d='M23 4v6h-6'/><path d='M1 20v-6h6'/><path d='M3.51 9a9 9 0 0 1 14.85-3.36L23 10'/><path d='M1 14l4.64 4.36A9 9 0 0 0 20.49 15'/>",
    "hash": "<path d='M4 9h16'/><path d='M4 15h16'/><path d='M10 3 8 21'/><path d='M16 3l-2 18'/>",
    "shuffle": "<path d='M16 3h5v5'/><path d='M4 20 21 3'/><path d='M21 16v5h-5'/><path d='M15 15l6 6'/><path d='M4 4l5 5'/>",
    "pin": "<path d='M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z'/><circle cx='12' cy='10' r='3'/>",
    "commit": "<circle cx='12' cy='12' r='3'/><path d='M3 12h6'/><path d='M15 12h6'/>",
    "book": "<path d='M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z'/><path d='M22 3h-6a4 4 0 0 1-4 4v14a3 3 0 0 0 3-3h7z'/>",
    "edit": "<path d='M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7'/><path d='M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4z'/>",
}


def _svg(name, color, size, top="0px"):
    """Render a line icon as a self-contained data-URI image (single tone)."""
    inner = ICONS[name]
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' "
        f"stroke='{color}' stroke-width='1.7' stroke-linecap='round' stroke-linejoin='round'>"
        f"{inner}</svg>"
    )
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return html.Img(
        src=f"data:image/svg+xml;base64,{b64}",
        style={"width": f"{size}px", "height": f"{size}px", "flex": "0 0 auto",
               "display": "block", "marginTop": top},
    )


def _point(icon, lead, body=None):
    """A single point: muted line icon + bold lead + optional body."""
    content = [html.B(lead, style={"color": "#e9ebee"})]
    if body is not None:
        content.append(html.Span(" — ", style={"color": "var(--text-secondary)"}))
        content.extend(body if isinstance(body, list) else [body])
    return html.Div(
        [
            _svg(icon, MUTED, 16, top="2px"),
            html.Div(content, style={"flex": "1", "lineHeight": "1.5", "fontSize": "0.92rem"}),
        ],
        style={
            "display": "flex", "gap": "0.6rem", "alignItems": "flex-start",
            "padding": "0.6rem 0.15rem", "borderTop": "1px solid var(--border)",
        },
    )


def _section(icon, title, points):
    return html.Div(
        [
            html.Div(
                [
                    _svg(icon, ACCENT, 18),
                    html.H3(title, style={"margin": 0, "color": "#e9ebee",
                                          "fontSize": "1.02rem", "fontWeight": "650"}),
                ],
                style={"display": "flex", "alignItems": "center", "gap": "0.55rem",
                       "marginBottom": "0.35rem"},
            ),
            *points,
        ],
        className="card",
    )


_CITE_LABEL = {
    "fontSize": "0.72rem", "fontWeight": "700", "letterSpacing": "0.08em",
    "textTransform": "uppercase", "color": "var(--text-secondary)", "margin": "0.5rem 0 0.35rem",
}

_CITE_BOX = {
    "fontFamily": "var(--font-mono)", "fontSize": "0.82rem",
    "background": "var(--bg-secondary)", "border": "1px solid var(--border)",
    "borderRadius": "8px", "padding": "0.75rem 0.9rem", "lineHeight": "1.55", "margin": "0",
}


def _badge(text):
    return html.Span(
        text,
        style={
            "display": "inline-block", "padding": "0.28rem 0.7rem", "margin": "0.2rem 0.35rem 0.2rem 0",
            "background": "var(--bg-secondary)", "border": "1px solid var(--border)",
            "color": "var(--text-secondary)", "borderRadius": "6px", "fontSize": "0.78rem",
            "fontWeight": "600", "fontFamily": "var(--font-mono)",
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
                _badge("Open-source"), _badge("Zenodo DOI"),
                _badge("No fitting"), _badge("No randomness"), _badge("Bit-for-bit"),
            ]),
        ],
        className="card",
        style={"borderLeft": f"3px solid {ACCENT}"},
    ),

    # 1 — Evidence
    _section("file", "Built on the evidence", [
        _point("file", "10+ peer-reviewed sources", "for the resistance trajectory."),
        _point("activity", "3 independent mortality streams", "GRAM (Global Research on Antimicrobial Resistance) / O'Neill, Murray 2022, and Tai 2025."),
        _point("globe", "4 global surveillance agencies", "WHO GLASS (Global Antimicrobial Resistance & Use Surveillance System), ECDC EARS-Net (European Antimicrobial Resistance Surveillance Network), CDC AR Threats (Antibiotic Resistance Threats report), and Murray 2022."),
        _point("search", "Literature harvested from", "PubMed, EMBASE and the Cochrane Library."),
        _point("check", "Built to open-science standards", [
            "the ", html.A("FAIR", href="https://doi.org/10.1038/s41597-022-01710-x", target="_blank"),
            " (Findable, Accessible, Interoperable, Reusable) Principles for Research Software and the ",
            html.A("Force11", href="https://doi.org/10.7717/peerj-cs.86", target="_blank"),
            " software-citation principles.",
        ]),
    ]),

    # 2 — How it's built
    _section("code", "How it's built", [
        _point("code", "Python 3.12", "the whole application."),
        _point("database", "NumPy + pandas", "run the closed-form (analytic) models."),
        _point("bar", "statsmodels", "runs the SARIMA (Seasonal AutoRegressive Integrated Moving Average) fits."),
        _point("trending", "Plotly + Dash", "the interactive charts you're looking at."),
        _point("zap", "No external API", "(Application Programming Interface) at run-time — every coefficient is embedded in the source."),
        _point("globe", "Runs online or fully offline", "with identical results."),
    ]),

    # 3 — What's inside
    _section("layers", "What's inside — 10 pages", [
        _point("trending", "Overview", "the super-exponential curve vs. the constant-rate reference, with the 2040–2047 critical-point window."),
        _point("activity", "Pathogens", "the ESKAPEE (the 7 priority superbugs) × antibiotic map, with WHO priority and Magiorakos MDR/XDR/PDR (Multidrug- / Extensively drug- / Pandrug-Resistant) badges."),
        _point("clock", "Time Series", "SARIMA forecasts with ACF/PACF (Auto- / Partial Autocorrelation) diagnostics and AIC/BIC (Akaike / Bayesian Information Criterion)."),
        _point("briefcase", "Industry", "publications (PubMed 1990–2025), the market (CAGR — Compound Annual Growth Rate — 5.4%), and awareness-vs-effectiveness."),
        _point("flask", "Metabolic", "the antimetabolic line of treatment — presented as a working hypothesis."),
        _point("folder", "Data Sources · References · Export Studio · Docs · Tutorial", "cited sources, publication-grade figure export, and onboarding."),
    ]),

    # 4 — Open & citable
    _section("book", "Open & citable", [
        _point("unlock", "Open-source license", "the full source is public."),
        _point("landmark", "Archived in Zenodo", [
            "with a citable DOI (Digital Object Identifier): ",
            html.A("10.5281/zenodo.22117640", href="https://doi.org/10.5281/zenodo.22117640", target="_blank"),
            ".",
        ]),
        _point("link", "Cite the deposited release", "if you reuse the coefficients, tables or visualizations (Force11)."),
        _point("globe", "Live at", [html.A("resistome.imhoit.com", href="https://resistome.imhoit.com", target="_blank")]),
    ]),

    # 5 — Reproducible
    _section("refresh", "100% reproducible", [
        _point("hash", "Closed-form model", "an exact formula — no parameter fitting."),
        _point("shuffle", "No random sampling", "and no Monte Carlo simulation."),
        _point("pin", "Data loaded from named sources", "mortality & surveillance values are cited, not model-derived."),
        _point("commit", "Fixed random seed", "so the SARIMA diagnostics come out identical on any machine."),
        _point("refresh", "Every figure re-derivable bit-for-bit", "from the open source — the minimum bar of FAIR4RS (FAIR for Research Software)."),
    ]),

    # 6 — Cite
    _section("edit", "Cite this companion", [
        html.Div("Cite the paper (Vancouver)", style=_CITE_LABEL),
        html.P(
            [
                "Prieto Gratacós E, Botto J. The Twilight of Antibiotics: a predictive "
                "mathematical model of declining antimicrobial effectiveness, and a possible "
                "metabolic escape route. Br J Med Health Res. 2026;13(8):43-56. doi:",
                html.A("10.5281/zenodo.21898960",
                       href="https://doi.org/10.5281/zenodo.21898960", target="_blank"),
            ],
            style=_CITE_BOX,
        ),
        html.Div("Cite the software (archived release)", style={**_CITE_LABEL, "marginTop": "0.9rem"}),
        html.P(
            [
                "Prieto Gratacós, E. & Botto, J. A. (2026). The Twilight of Antibiotics "
                "— open computational companion [Software]. Zenodo. DOI: ",
                html.A("10.5281/zenodo.22117640",
                       href="https://doi.org/10.5281/zenodo.22117640", target="_blank"),
                " (concept DOI — always latest). Available at resistome.imhoit.com",
            ],
            style=_CITE_BOX,
        ),
    ]),
])
