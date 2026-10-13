"""
Impact page: the paper's model translated into units anyone can read.

Two pieces:
  * Impact figures: time left to the critical window, remaining margin of the
    index, doubling time of the resistance odds and the observed speed-up of
    the published anchors. Every figure is closed-form arithmetic on the
    paper's coefficients or on published anchors, with its derivation in the
    model card below it.
  * Resistance network: each "neuron" is one pathogen x antibiotic-class cell
    of the surveillance matrix, lit by its published % resistant (2025).
    Layers follow the WHO AWaRe classification (Access, Watch, Reserve). Other
    years are illustrative: every cell is shifted on the odds scale by the same
    factor as the paper's index (the paper does not project pathogens one by
    one). Drawn client-side by assets/impact_network.js.
"""

import datetime as _dt
import json
import math
import os
import sys

import dash
from dash import html

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.amr_data import SUPER_EXP_PARAMS, OBSERVED_DATA, scenario_crossing_year
from data.pathogen_data import PATHOGENS, RESISTANCE_MATRIX
from components import help_section, chart_title_with_info
from model_cards import model_card, MURRAY, GLASS, EARS, CDC, AWARE

from i18n import translate, current_lang

dash.register_page(__name__, path="/impact", name="Impact")

PAPER_URL = "https://doi.org/10.5281/zenodo.21898960"
P = SUPER_EXP_PARAMS
WINDOW_START = _dt.date(2040, 1, 1)

# WHO AWaRe 2023 layers, as column indices of RESISTANCE_MATRIX
# (Penicillins, Ceph3, Carbapenems, FQ, Aminoglycosides, Vancomycin,
#  Polymyxins, Macrolides, Tetracyclines, SMX/TMP)
AWARE_LAYERS = [[0, 8, 9, 4], [7, 1, 3, 5, 2], [6]]

# Same illustrative presets as the Scenario Lab
PRESETS = [
    ("Nothing changes", 0, 0, 2027),
    ("Stewardship 15 % and new antibiotics 30 %, from 2027", 15, 30, 2027),
    ("Stewardship 30 % and new antibiotics 60 %, from 2027", 30, 60, 2027),
    ("The same, but starting in 2035", 30, 60, 2035),
]


def _y(tau):
    return P["K"] / (1 + P["A"] * math.exp(-(P["r"] * tau + P["b"] * tau * tau)))


def _doubling(tau):
    return math.log(2) / (P["r"] + 2 * P["b"] * tau)


def _anchor(year):
    return float(OBSERVED_DATA.loc[OBSERVED_DATA.year == year, "resistance_index"].iloc[0])


def _fmt(x, lang, nd=1):
    s = f"{x:.{nd}f}"
    return s.replace(".", ",") if lang == "es" else s


def _countdown(today):
    y, m, d = WINDOW_START.year - today.year, WINDOW_START.month - today.month, WINDOW_START.day - today.day
    if d < 0:
        m -= 1
        prev = (WINDOW_START.replace(day=1) - _dt.timedelta(days=1))
        d += prev.day
    if m < 0:
        y -= 1
        m += 12
    return y, m, d


def _stat(value, label, cls):
    return html.Div([html.Div(value, className=f"stat-value {cls}"),
                     html.Div(label, className="stat-label")], className="stat-card")


def _figures(lang):
    today = _dt.date.today()
    tau_now = today.year + (today.timetuple().tm_yday - 1) / 365.25 - 1990
    yrs, mos, days = _countdown(today)
    margin_now = P["K"] - _y(tau_now)
    v_old = (_anchor(2000) - _anchor(1990)) / 10
    v_new = (_anchor(2025) - _anchor(2015)) / 10
    return html.Div([
        _stat([str(yrs), html.Small("years"), str(mos), html.Small("months"), str(days), html.Small("days")],
              "Until the critical window (2040)", "danger"),
        _stat([_fmt(margin_now, lang, 0), html.Small("of 100")],
              "Margin of the index left today (88 in 1990)", "warning"),
        _stat([_fmt(_doubling(tau_now), lang), html.Small("years")],
              "Years the resistance odds take to double (9.8 in 1990)", "accent"),
        _stat(["× ", _fmt(v_new / v_old, lang)],
              "Observed speed-up of the published anchors, 1990-2000 vs 2015-2025", "warning"),
    ], className="stats-row")


def _scenario_rows():
    base = math.ceil(scenario_crossing_year(0, 0, 2027) - 1e-9)
    rows = []
    for label, s, p, start in PRESETS:
        yr = math.ceil(scenario_crossing_year(s / 100, p / 100, start) - 1e-9)
        rows.append(html.Tr([html.Td(label), html.Td(str(yr), className="mc-num"),
                             html.Td(f"+{yr - base}" if yr > base else "0", className="mc-num")]))
    return rows


def _network():
    data = {
        "pathogens": PATHOGENS,
        "matrix": [[None if (isinstance(v, float) and math.isnan(v)) else float(v) for v in row]
                   for row in RESISTANCE_MATRIX.tolist()],
        "layers": AWARE_LAYERS,
        "params": {k: P[k] for k in ("K", "A", "r", "b")},
    }
    return html.Div(id="impact-net", className="impact-net", **{"data-model": json.dumps(data)})


def _layout(lang):
    return html.Div([
        help_section("Impact", [
            "PURPOSE: This page translates the paper's model into figures anyone can read, and shows how resistance pressure reaches deeper into the antibiotic arsenal.",
            "THE FIGURES: Each one is arithmetic on the paper's coefficients or on its published anchor points. The card under them shows how each number is obtained.",
            "THE NETWORK: Each point is one pathogen and one antibiotic class of the surveillance matrix. Brightness is the published % of resistant isolates. Layers follow the WHO AWaRe classification: Access (first choice), Watch and Reserve (last resort).",
            "WHAT IS ILLUSTRATIVE: The 2025 network is published data. The paper does not project pathogens one by one, so for other years every cell is shifted on the odds scale by the same factor as the paper's index. Read it as an illustration of the model, not as a per-pathogen forecast.",
            "DETERMINISM: Closed-form only. The countdown and today's margin depend on today's date; everything else is fixed.",
        ]),
        html.Div([
            html.Strong("The paper's model, in plain units. "),
            "Figures from ",
            html.A("Prieto Gratacós & Botto, Br J Med Health Res 2026", href=PAPER_URL, target="_blank"),
            " and its published anchors. The human cost, as a single fact: 1.27 million deaths attributable to AMR in 2019 (",
            html.A("Murray et al., Lancet 2022", href=MURRAY, target="_blank"),
            ").",
        ], className="scn-disclaimer"),

        _figures(lang),
        html.Div([model_card("impact", open=True)], className="card"),

        html.Div([
            chart_title_with_info(
                "Resistance network: from first-choice to last-resort antibiotics",
                "Each point is a pathogen × antibiotic class. The brighter, the higher the % of "
                "resistant isolates. Press the button to raise the pressure from 1990 to 2060 and "
                "watch the light reach the last-resort layer.",
                subtitle="2025: published data. Other years: illustrative shift with the paper's index.",
            ),
            _network(),
            html.Div([
                html.Span("Sources: ", className="source-label"),
                html.A("WHO GLASS Report 2022", href=GLASS, target="_blank"), " · ",
                html.A("ECDC EARS-Net", href=EARS, target="_blank"), " · ",
                html.A("CDC AR Threats Report", href=CDC, target="_blank"), " · ",
                html.A("Murray et al., Lancet 2022", href=MURRAY, target="_blank"), " · ",
                html.A("Layers: WHO AWaRe classification 2023", href=AWARE, target="_blank"), " · ",
                html.A("Index: Prieto Gratacós & Botto 2026", href=PAPER_URL, target="_blank"),
            ], className="chart-sources"),
            model_card("network", open=True),
        ], className="card"),

        html.Div([
            chart_title_with_info(
                "Scenarios in plain words",
                "The Scenario Lab presets, read as sentences. The percentages are illustrative "
                "assumptions: the paper does not quantify the effect of any intervention.",
                subtitle="No scenario avoids the threshold; each one only postpones it.",
            ),
            html.Div(html.Table([
                html.Thead(html.Tr([html.Th("If…"), html.Th("The threshold arrives in"), html.Th("Years gained")])),
                html.Tbody(_scenario_rows()),
            ], className="mc-table"), className="mc-table-box"),
            html.Div([
                html.Span("Sources: ", className="source-label"),
                html.A("Super-exponential model: Prieto Gratacós & Botto, Br J Med Health Res 2026",
                       href=PAPER_URL, target="_blank"),
                " · Interventions: user-defined assumptions (no published source)",
            ], className="chart-sources"),
        ], className="card"),
    ])


def layout(lang=None, **_query):
    """Page layout in the visitor's language (?lang=, cookie or browser)."""
    lang = current_lang(lang)
    return translate(_layout(lang), lang)
