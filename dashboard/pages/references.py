"""
References page — full bibliography of the paper UPDATE v.A-29, grouped by
section, with clickable links (DOI when known, journal/PubMed otherwise).
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

dash.register_page(__name__, path="/references", name="References")


SECTION_COLOR = {
    "Foundational epidemiology": "#4fc3f7",
    "ESKAPEE pathogens":          "#ef5350",
    "Surveillance & cycling":     "#ce93d8",
    "Superbugs (MDR/XDR/PDR)":    "#ff7043",
    "Industry / market":          "#ffb74d",
    "Mathematical models":        "#66bb6a",
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

layout = html.Div([
    help_section("References", [
        "PURPOSE: This page reproduces the full bibliography of the paper UPDATE v.A-29 (Gratacós & Botto), grouped by paper section. Every entry is a clickable link — DOI when the paper provides one, journal homepage or PubMed search otherwise.",
        "GROUPING: References are organised by the section of the paper they support: Foundational epidemiology and global burden (párrs. 6–9), ESKAPEE pathogens and dynamic susceptibility (párrs. 10–13), Surveillance and antibiotic cycling, Superbugs and Magiorakos MDR/XDR/PDR definitions (párrs. 51–65), Industry / market context (párr. 25), and the Mathematical Models catalogue from the paper's Math section.",
        "REFERENCE NUMBERS: Where the paper assigns a numeric reference (refs 1–20), the number is shown in monospace before the citation. Many of the post-numbered entries in the paper are subsequent listings in the Math, Trends, and Superbugs subsections — they are linked here without their narrative number for clarity.",
        "URL POLICY: All links are best-effort. The paper provides DOIs for ~5 of the 50+ references; for the rest this page links to the journal landing page or to a PubMed search. When a DOI is provided in the paper text it is preserved verbatim. None of these URLs is fabricated — every target is either explicitly cited in the paper or a canonical resolver for the journal in question.",
        "USE IN DRAFTING: Use this page as a single source-of-truth bibliography while drafting the paper. The Magiorakos 2012 link, in particular, is the canonical source for the MDR / XDR / PDR isolate-level definitions used elsewhere in this dashboard (Pathogens page badges).",
    ]),

    # How to cite the companion (mirrors the paper's "Citation of the companion"
    # section + Force11 Software Citation Principles / FAIR4RS).
    html.Div([
        html.H3("Cite this open computational companion", className="card-title"),
        html.P(
            "Prieto Gratacós, E. & Botto, J. A. (2026). The Twilight of Antibiotics "
            "— open computational companion [Software]. Zenodo. "
            "DOI: [to be assigned at publication]. Available at "
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
            "is released under an open-source license and will be deposited in Zenodo "
            "with a citable DOI at the time of publication.",
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
