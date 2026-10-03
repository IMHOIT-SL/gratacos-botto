"""
Press & materials page: every published output of the project in one place
(paper, software, congress poster, blog and social posts) with links,
downloads and how to cite.

Items whose public URL is not known yet are listed as "coming soon" instead of
linking anywhere (sources are cited, never invented).
"""

import dash
from dash import html

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from components import help_section

from i18n import translate, translated, current_lang

dash.register_page(__name__, path="/press", name="Press")

PAPER_DOI_URL = "https://doi.org/10.5281/zenodo.21898960"
PAPER_PDF_URL = "https://zenodo.org/records/21898960"
JOURNAL_URL = "https://www.bjmhr.com"
SOFTWARE_DOI_URL = "https://doi.org/10.5281/zenodo.22117640"
GITHUB_URL = "https://github.com/IMHOIT-SL/gratacos-botto"
APP_URL = "https://resistome.imhoit.com"
POSTER_PDF = "/assets/press/poster-biominds-2026.pdf"
POSTER_PREVIEW = "/assets/press/poster-biominds-2026-preview.jpg"

# Fill in each URL when the piece is published; None shows "Coming soon".
OUTREACH = [
    {"kind": "Blog", "title": "The Twilight of Antibiotics, on the IMHOIT blog",
     "detail": "Long-form article presenting the model, the forecast and the metabolic route as a line of research.",
     "url": None},
    {"kind": "LinkedIn", "title": "Carousel: the forecast in 9 slides",
     "detail": "Visual summary of the model and its key dates.",
     "url": None},
    {"kind": "LinkedIn", "title": "Post by E. Prieto Gratacós",
     "detail": "The scientific and clinical perspective.",
     "url": None},
    {"kind": "LinkedIn", "title": "Post by J. Botto",
     "detail": "The mathematical model and the open platform.",
     "url": None},
]


def _button(label, href, primary=False, download=False):
    props = {"href": href, "target": "_blank", "className": "press-btn primary" if primary else "press-btn"}
    if download:
        props["download"] = ""
    return html.A(label, **props)


def _cite(label, text_parts):
    return html.Div([
        html.Div(label, className="press-cite-label"),
        html.P(text_parts, className="press-cite"),
    ])


def paper_card():
    return html.Div([
        html.Div("PAPER", className="press-kind"),
        html.H3("The Twilight of Antibiotics: A predictive mathematical model of declining "
                "antimicrobial effectiveness, and a possible metabolic escape route",
                className="press-title"),
        html.P("Prieto Gratacós E, Botto J. British Journal of Medical and Health Research. "
               "2026;13(8):43-56. Open access.", className="press-meta"),
        html.Div([
            _button("Read the paper", PAPER_DOI_URL, primary=True),
            _button("PDF on Zenodo", PAPER_PDF_URL),
            _button("Journal website", JOURNAL_URL),
        ], className="press-actions"),
    ], className="card press-card")


def poster_card():
    return html.Div([
        html.A(
            html.Img(src=POSTER_PREVIEW, alt="Poster: El ocaso de los antibióticos (BIOMINDS 2026)",
                     className="press-poster-img"),
            href=POSTER_PDF, target="_blank", className="press-poster-link",
        ),
        html.Div([
            html.Div("CONGRESS POSTER", className="press-kind"),
            html.H3("El ocaso de los antibióticos", className="press-title"),
            html.P("Scientific poster (in Spanish) presented at BIOMINDS 2026, the II International "
                   "Congress of Biological, Functional and Regenerative Medicine and Biological "
                   "Dentistry.", className="press-meta"),
            html.Ul([
                html.Li("8-10 October 2026"),
                html.Li("Hotel Marriott Downtown, Buenos Aires, Argentina"),
                html.Li("Format: 90 x 120 cm, vector PDF"),
                html.Li("Every figure is generated from this app's data and models"),
            ], className="press-list"),
            html.Div([
                _button("Download poster (PDF)", POSTER_PDF, primary=True, download=True),
                _button("Open full size", POSTER_PDF),
            ], className="press-actions"),
        ], className="press-poster-body"),
    ], className="card press-card press-poster")


def software_card():
    return html.Div([
        html.Div("OPEN SOFTWARE", className="press-kind"),
        html.H3("Open computational companion", className="press-title"),
        html.P("This interactive app: every model, anchor point and coefficient of the paper, "
               "open and reproducible. MIT license, archived on Zenodo.", className="press-meta"),
        html.Div([
            _button("Zenodo (citable DOI)", SOFTWARE_DOI_URL, primary=True),
            _button("Source code on GitHub", GITHUB_URL),
        ], className="press-actions"),
    ], className="card press-card")


def outreach_card():
    rows = []
    for item in OUTREACH:
        status = (html.A("Open", href=item["url"], target="_blank", className="press-btn")
                  if item["url"] else html.Span("Coming soon", className="press-soon"))
        rows.append(html.Div([
            html.Span(item["kind"], className="press-chip"),
            html.Div([
                html.Div(item["title"], className="press-row-title"),
                html.Div(item["detail"], className="press-row-detail"),
            ], className="press-row-text"),
            status,
        ], className="press-row"))
    return html.Div([
        html.Div("BLOG AND SOCIAL MEDIA", className="press-kind"),
        html.H3("Articles and posts", className="press-title"),
        html.Div(rows, className="press-rows"),
    ], className="card press-card")


def cite_card():
    return html.Div([
        html.Div("HOW TO CITE", className="press-kind"),
        _cite("Paper (Vancouver)", [
            "Prieto Gratacós E, Botto J. The Twilight of Antibiotics: a predictive mathematical "
            "model of declining antimicrobial effectiveness, and a possible metabolic escape route. "
            "Br J Med Health Res. 2026;13(8):43-56. doi:",
            html.A("10.5281/zenodo.21898960", href=PAPER_DOI_URL, target="_blank"),
        ]),
        _cite("Software", [
            "Prieto Gratacós E, Botto JA. The Twilight of Antibiotics: open computational "
            "companion [Software]. Zenodo; 2026. doi:",
            html.A("10.5281/zenodo.22117640", href=SOFTWARE_DOI_URL, target="_blank"),
            ". Available at ",
            html.A("resistome.imhoit.com", href=APP_URL, target="_blank"),
        ]),
    ], className="card press-card")


_layout = html.Div([
    help_section("Press", [
        "PURPOSE: This page gathers everything published about The Twilight of Antibiotics: the peer-reviewed paper, this open software, the congress poster, and the blog and social media posts, with links and downloads.",
        "FOR JOURNALISTS AND EDITORS: Figures from this app may be reproduced citing the paper and the software (see How to cite). Every chart can be downloaded from its toolbar as SVG, PNG or CSV data.",
        "COMING SOON: Items marked 'Coming soon' are prepared but not yet published; their links will appear here as soon as they are online.",
    ]),
    html.Div([
        html.H2("Press and materials", className="press-h1"),
        html.P("The paper, the open software and every piece published about it, in one place.",
               className="press-lede"),
    ], className="press-head"),
    html.Div([paper_card(), software_card()], className="press-grid"),
    poster_card(),
    html.Div([outreach_card(), cite_card()], className="press-grid"),
])


def layout(lang=None, **_query):
    """Page layout in the visitor's language (?lang=, cookie or browser)."""
    return translate(_layout, current_lang(lang))
