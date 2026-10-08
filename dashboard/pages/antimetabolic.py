"""
Metabolic page: the paper's "possible metabolic escape route", reduced to what
the published paper says (Br J Med Health Res. 2026;13(8):43-56, section
"Antimetabolites in the treatment of infections", references 39-55).

Editorial discipline: every statement on this page is the paper's own text,
quoted and attributed to its references. No charts, scenarios or placeholders
are added: the paper presents this route as a working hypothesis and does not
model it quantitatively.
"""

import dash
from dash import html

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.references_data import REFERENCES
from components import help_section

from i18n import translate, translated, current_lang

dash.register_page(__name__, path="/metabolic", name="Metabolic")

PAPER_URL = "https://doi.org/10.5281/zenodo.21898960"
_REF_BY_N = {r["n"]: r for r in REFERENCES}


def _refs(*numbers):
    """Inline reference markers, each linking to the cited work."""
    parts = [" ("]
    for i, n in enumerate(numbers):
        if i:
            parts.append(", ")
        parts.append(html.A(str(n), href=_REF_BY_N[n]["url"], target="_blank",
                            title=_REF_BY_N[n]["citation"], className="ref-link"))
    parts.append(")")
    return parts


def _point(title, quote_parts):
    return html.Div([
        html.Div(title, className="meta-point-title"),
        html.P(quote_parts, className="meta-quote"),
    ], className="meta-point")


def hypothesis_banner():
    return html.Div([
        html.Span("WORKING HYPOTHESIS", className="meta-badge"),
        html.Span(
            "The paper presents the metabolic route as a working hypothesis to be tested "
            "clinically, not as an available treatment. It does not model this route "
            "quantitatively: the forecasts on the other pages refer to classical antibiotics.",
            className="meta-banner-text",
        ),
    ], className="card meta-banner")


def abstract_card():
    return html.Div([
        html.H3("From the abstract", className="card-title"),
        html.P('"Unless new categories of germicidal substances are developed, a reverse '
               'epidemiological transition seems inevitable. This paper describes our forecast '
               'based on a mathematical model from hard data on the declining effect of '
               'antimicrobial medication. Additionally, it suggests an already proven, scalable '
               'line of treatment that could overcome microbial resistance."',
               className="meta-quote meta-quote-lead"),
        html.P(["Prieto Gratacós E, Botto J. ",
                html.A("Br J Med Health Res. 2026;13(8):43-56", href=PAPER_URL, target="_blank"),
                ", Abstract."], className="meta-attrib"),
    ], className="card")


def section_card():
    return html.Div([
        html.H3("What the paper proposes", className="card-title"),
        html.P("Quoted from the section 'Antimetabolites in the treatment of infections' of the "
               "published paper. Numbers in brackets link to the cited works.",
               className="card-subtitle"),
        _point("The proposal", [
            '"As a working hypothesis, we propose now that a readily accessible, non-toxic '
            'approach to overcoming antibiotic resistance could be the enzymatic disruption of '
            'bacterial metabolic pathways with structural analogs of glucose"', *_refs(39, 40, 41, 42),
            '. "This kind of antimetabolic interventions has been known for decades, since it is '
            'based on the principle of competitive inhibition"', *_refs(43), ".",
        ]),
        _point("Why it can be selective", [
            '"In vivo, enzymatic inhibition with structural analogs (EISA) is only possible due to '
            'the pronounced functional asymmetry between normal eukaryotic cells and bacteria. Many '
            'ESKAPE pathogens behave as facultative anaerobes, relying heavily on transporters and '
            'fermentation pathways functionally equivalent to the GLUT family, and to hexokinase-2 '
            'and LDH-A, respectively, all of which are demonstrably susceptible to competitive '
            'inhibition"', *_refs(44, 45, 46),
            '. "Although their glucose-uptake and metabolism are mechanistically distinct from their '
            'mammalian counterparts, they share enough biochemical architecture to be susceptible to '
            'the same class of structural-analog inhibitors that have long been characterized in '
            'oncology."',
        ]),
        _point("Candidate agents", [
            '"Antimetabolites such as 2-deoxy-D-glucose (2DG) -an undegradable pseudo-sugar with '
            'antiproliferative effects- and sodium ascorbate (a six-carbon glucose analog) have '
            'proven both safe and effective for the treatment of cancer and opportunistic '
            'infections in humans"', *_refs(47, 48),
            '. "Ascorbate is widely recognized for its strong antimicrobial and antineoplastic '
            'properties, when applied in pharmacological doses through the intravenous route"',
            *_refs(49, 50),
            '. "Said effects are enhanced by means of the synchronous use of autophagy inhibitors '
            'such as hydroxychloroquine"', *_refs(51, 52, 53), ".",
        ]),
        _point("Why it may last", [
            '"Antimetabolic interventions that constrict bacterial access to biosynthetic material '
            'and energy sources have retained their efficacy over the decades. A probable '
            'explanation of this phenomenon seems to be that rapidly growing bacteria cannot '
            'overcome deep, extended starvation"', *_refs(54), ".",
        ]),
        _point("The paper's conclusion", [
            '"Based on this general principle, non-toxic antimetabolites should be tested '
            'clinically, as a means to neutralize bacterial infections."',
        ]),
    ], className="card")


def references_card():
    items = [
        html.Li([
            html.Span(f"[{r['n']}] ", className="meta-ref-n"),
            html.A(r["citation"], href=r["url"], target="_blank", className="meta-ref"),
        ])
        for r in REFERENCES if r["section"] == "Antimetabolites"
    ]
    return html.Div([
        html.H3("References of this section (39-55)", className="card-title"),
        html.P("Numbered as in the published paper. The full bibliography is on the References page.",
               className="card-subtitle"),
        html.Ul(items, className="meta-ref-list"),
    ], className="card")


_layout = html.Div([
    html.Div([
        help_section("Metabolic route", [
            "PAGE PURPOSE: This page presents the 'possible metabolic escape route' in the paper's title exactly as the published paper states it, in the section 'Antimetabolites in the treatment of infections', with links to its references 39-55.",
            "WHAT THIS PAGE IS NOT: It does not add data, charts, forecasts or interpretations of its own. The paper presents the route as a working hypothesis to be tested clinically and does not model it quantitatively.",
            "QUOTES: Texts in quotation marks are the paper's own words. In the Spanish version they are translations of the English original.",
        ]),
        hypothesis_banner(),
        abstract_card(),
        section_card(),
        references_card(),
    ], className="meta-page"),
])


def layout(lang=None, **_query):
    """Page layout in the visitor's language (?lang=, cookie or browser)."""
    return translate(_layout, current_lang(lang))
