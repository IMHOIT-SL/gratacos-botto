"""
References page — full bibliography of the published paper (Br J Med Health
Res. 2026;13(8):43-56), grouped by section, with clickable links (DOI when
the paper gives one, journal/PubMed otherwise).
"""

import dash
from dash import html, dcc

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.references_data import (
    REFERENCES,
    SECTION_ORDER,
    references_by_section,
    total_count,
    section_counts,
)
from components import help_section

from i18n import translate, translated, current_lang

dash.register_page(__name__, path="/references", name="References")


SECTION_COLOR = {
    "Foundational epidemiology":        "#4fc3f7",
    "ESKAPEE & dynamic susceptibility": "#ef5350",
    "Superbugs (MDR/XDR/PDR)":          "#ff7043",
    "Bibliometrics & industry":         "#ffb74d",
    "Antimetabolites":                  "#66bb6a",
}


def render_reference(ref):
    """Single reference list item with optional [n] tag."""
    n_tag = (
        html.Span(
            f"[{ref['n']}]",
            style={
                "fontFamily": "var(--font-mono)",
                "color": "var(--accent)",
                "fontSize": "0.75rem",
                "marginRight": "0.5rem",
                "fontWeight": "600",
            },
        )
        if ref.get("n") is not None else None
    )

    children = []
    if n_tag:
        children.append(n_tag)
    children.append(
        html.A(
            ref["citation"],
            href=ref["url"],
            target="_blank",
            style={
                "color": "var(--text-primary)",
                "textDecoration": "none",
            },
        )
    )

    return html.Li(
        children,
        style={
            "marginBottom": "0.6rem",
            "lineHeight": "1.55",
            "fontSize": "0.83rem",
        },
    )


def section_card(section_name, refs):
    color = SECTION_COLOR.get(section_name, "var(--accent)")
    return html.Div([
        html.Div([
            html.Span(
                f"§ {section_name}",
                style={
                    "fontSize": "0.95rem",
                    "fontWeight": "600",
                    "color": color,
                },
            ),
            html.Span(
                f"  {len(refs)} ref{'s' if len(refs) != 1 else ''}",
                style={
                    "color": "var(--text-secondary)",
                    "fontSize": "0.75rem",
                    "fontFamily": "var(--font-mono)",
                    "marginLeft": "0.5rem",
                },
            ),
        ], style={
            "marginBottom": "0.75rem",
            "paddingBottom": "0.5rem",
            "borderBottom": "1px solid var(--border)",
        }),
        html.Ul(
            [render_reference(r) for r in refs],
            style={"paddingLeft": "1.2rem", "color": "var(--text-secondary)"},
        ),
    ], className="card", style={"borderLeft": f"3px solid {color}"})


def stats_row():
    counts = section_counts()
    cards = []
    cards.append(html.Div([
        html.Div(f"{total_count()}", className="stat-value accent"),
        html.Div("Total References", className="stat-label"),
    ], className="stat-card"))
    for sec in SECTION_ORDER:
        cards.append(html.Div([
            html.Div(
                f"{counts.get(sec, 0)}",
                className="stat-value",
                style={"color": SECTION_COLOR.get(sec, "var(--accent)")},
            ),
            html.Div(sec, className="stat-label"),
        ], className="stat-card"))
    return html.Div(cards, className="stats-row")


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
grouped = references_by_section()

_layout = html.Div([
    help_section("References", [
        "PURPOSE: This page reproduces the full bibliography of the published paper (Prieto Gratacós E, Botto J. Br J Med Health Res. 2026;13(8):43-56), grouped by paper section. Every entry is a clickable link.",
        "GROUPING: References are organised by the section of the published paper they support: Introduction, Foundational epidemiology and global burden (refs 1-10); Introduction, Exponentially evolving pan resistant strains (ESKAPEE, dynamic susceptibility and antibiotic cycling, refs 11-22; superbugs and Magiorakos MDR/XDR/PDR definitions, refs 23-36); Materials and Method, bibliometric dynamics and industry trends (refs 37-38); and Antimetabolites in the treatment of infections (refs 39-55).",
        "REFERENCE NUMBERS: The number shown in monospace before each citation is the reference number in the published paper, so [10] here is reference 10 in the journal version.",
        "URL POLICY: When the published paper gives a DOI, the link goes to that DOI. Otherwise the link goes to the article or journal page, or to a PubMed search on the article title. None of these URLs is fabricated: every target is either cited in the paper or a canonical resolver.",
        "MAGIORAKOS 2012 (ref 23) is the canonical source for the MDR / XDR / PDR isolate-level definitions used elsewhere in this dashboard (Pathogens page badges).",
    ]),

    # How to cite the companion (mirrors the paper's "Citation of the companion"
    # section + Force11 Software Citation Principles / FAIR4RS).
    html.Div([
        html.H3("Cite this open computational companion", className="card-title"),
        html.P(
            "Prieto Gratacós, E. & Botto, J. A. (2026). The Twilight of Antibiotics "
            "— open computational companion [Software]. Zenodo. "
            "DOI: 10.5281/zenodo.22117640. Available at "
            "https://resistome.imhoit.com",
            style={
                "fontFamily": "var(--font-mono)",
                "fontSize": "0.8rem",
                "color": "var(--text-primary)",
                "background": "var(--bg-secondary)",
                "border": "1px solid var(--border)",
                "borderRadius": "6px",
                "padding": "0.7rem 0.9rem",
                "lineHeight": "1.55",
            },
        ),
        html.P([
            "Following the ",
            html.A("Force11 Software Citation Principles", href="https://doi.org/10.7717/peerj-cs.86", target="_blank"),
            " and the ",
            html.A("FAIR Principles for Research Software (FAIR4RS)", href="https://doi.org/10.1038/s41597-022-01710-x", target="_blank"),
            ", any reuse of the model coefficients, anchor tables or visualizations "
            "should cite the deposited release rather than the paper alone. The source "
            "is released under the MIT license and archived in Zenodo (",
            html.A("10.5281/zenodo.22117640", href="https://doi.org/10.5281/zenodo.22117640", target="_blank"),
            "). The paper itself: ",
            html.A("Br J Med Health Res. 2026;13(8):43-56", href="https://doi.org/10.5281/zenodo.21898960", target="_blank"),
            " (",
            html.A("journal home page", href="https://www.bjmhr.com", target="_blank"),
            ").",
        ], style={"fontSize": "0.82rem", "color": "var(--text-secondary)", "marginTop": "0.6rem"}),
    ], className="card", style={"borderLeft": "3px solid var(--accent)"}),

    stats_row(),

    # One card per section, full-width
    *[section_card(sec, grouped[sec]) for sec in SECTION_ORDER if grouped[sec]],

    # Closing note
    html.Div([
        html.H3("Citation maintenance", className="card-title"),
        html.P(
            "When the paper adds new references, update dashboard/data/references_data.py "
            "and they will appear here automatically. Section grouping is driven by the "
            "'section' field on each entry; SECTION_ORDER governs the display order.",
            style={"fontSize": "0.82rem", "color": "var(--text-secondary)"},
        ),
    ], className="card"),
])


def layout(lang=None, **_query):
    """Page layout in the visitor's language (?lang=, cookie or browser)."""
    return translate(_layout, current_lang(lang))
