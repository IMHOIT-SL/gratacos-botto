"""
Antimetabolic Solution page — preview / scaffold for the paper's
"metabolic solution" thesis (UPDATE v.A-29 subtitle, párrs. 5 & 24).

Editorial discipline: this page does not invent therapeutic claims. It
presents the paper's exact framing, contrasts the classical-antibiotic
selective-pressure paradigm with the proposed antimetabolic angle at a
conceptual level, and leaves explicit open-question placeholders for the
authors to populate.
"""

import dash
from dash import html, dcc
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.amr_data import compute_super_exponential_curve
from components import help_section, chart_title_with_info

dash.register_page(__name__, path="/metabolic", name="Metabolic")


CHART_LAYOUT = dict(
    paper_bgcolor="#21232d",
    plot_bgcolor="#21232d",
    font=dict(color="#e8eaed", family="Inter, sans-serif", size=12),
    xaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
    yaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
    margin=dict(l=60, r=30, t=50, b=50),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
)

SVG_CONFIG = {
    "toImageButtonOptions": {"format": "svg", "scale": 3},
    "displayModeBar": True,
}


def build_paradigm_chart():
    """
    Conceptual chart contrasting two trajectories:
      * Classical-antibiotic effectiveness — anchored to the super-exponential
        resistance model (deterministic, real data).
      * Antimetabolic hypothesis envelope — schematic shaded region indicating
        the paper's claim that an alternative therapeutic angle could sustain
        effectiveness; SHOWN AS QUALITATIVE BAND, NOT FORECAST DATA.
    """
    curve = compute_super_exponential_curve(1990, 2060)
    classical_effectiveness = 100.0 - curve["resistance_index"]

    fig = go.Figure()

    # Classical antibiotic effectiveness — the only series with empirical anchoring
    fig.add_trace(go.Scatter(
        x=curve["year"], y=classical_effectiveness,
        mode="lines",
        line=dict(color="#ef5350", width=3),
        name="Classical antibiotic effectiveness (data-driven)",
        hovertemplate="<b>%{x}</b><br>Effectiveness: %{y:.1f}<extra></extra>",
    ))

    # Antimetabolic hypothesis envelope — qualitative band, explicitly labelled
    years = curve["year"].values
    upper = [None if y < 2025 else 75 for y in years]
    lower = [None if y < 2025 else 55 for y in years]
    fig.add_trace(go.Scatter(
        x=years, y=upper,
        mode="lines", line=dict(width=0),
        showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=years, y=lower,
        mode="lines", line=dict(width=0),
        fill="tonexty", fillcolor="rgba(79, 195, 247, 0.18)",
        name="Antimetabolic hypothesis (qualitative — not a forecast)",
        hoverinfo="skip",
    ))

    # Vertical separator at "now"
    fig.add_vline(
        x=2026, line_dash="dot", line_color="#9aa0a6", line_width=1,
        annotation_text="2026 (paper context)",
        annotation_position="top",
        annotation_font=dict(color="#9aa0a6", size=10),
    )

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(
            text="Paradigm comparison — classical vs antimetabolic (conceptual)",
            font=dict(size=14),
        ),
        xaxis_title="Year",
        yaxis_title="Therapeutic effectiveness (100 = full)",
        height=400,
        hovermode="x unified",
        annotations=[
            dict(
                xref="paper", yref="paper", x=0.5, y=-0.27,
                showarrow=False,
                text=("⚠ The blue band is a qualitative working-hypothesis envelope, "
                      "not a quantitative forecast. The red curve is anchored to "
                      "the super-exponential resistance model."),
                font=dict(color="#ffb74d", size=11),
                xanchor="center",
            ),
        ],
    )
    fig.update_yaxes(range=[0, 100])

    return fig


def hypothesis_banner():
    return html.Div(
        [
            html.Div([
                html.Span("⚠ WORKING HYPOTHESIS — PREVIEW",
                          style={
                              "background": "#ffb74d",
                              "color": "#21232d",
                              "padding": "0.25rem 0.7rem",
                              "borderRadius": "4px",
                              "fontSize": "0.7rem",
                              "fontFamily": "var(--font-mono)",
                              "fontWeight": "700",
                              "letterSpacing": "0.05em",
                              "marginRight": "0.7rem",
                          }),
                html.Span(
                    "This page previews the paper's proposed antimetabolic line "
                    "of treatment. The paper section is in active drafting "
                    "(UPDATE v.A-29 párr. 24). Content here is structural — no "
                    "therapeutic claims are made beyond what the paper states.",
                    style={"color": "#e8eaed", "fontSize": "0.82rem"},
                ),
            ], style={"display": "flex", "alignItems": "center", "flexWrap": "wrap",
                      "gap": "0.5rem"}),
        ],
        className="card",
        style={"borderLeft": "4px solid #ffb74d"},
    )


def paper_quote_card():
    return html.Div([
        html.H3("From the paper", className="card-title"),
        html.P('"Unless new categories of germicidal substances are developed, '
               'a reverse epidemiological transition seems inevitable. This paper '
               'describes our forecast based on a mathematical model from hard '
               'data on the declining effect of antimicrobial medication. '
               'Additionally, it suggests a line of treatment that could overcome '
               'microbial resistance."',
               style={
                   "fontStyle": "italic",
                   "color": "#e8eaed",
                   "borderLeft": "3px solid var(--accent)",
                   "paddingLeft": "1rem",
                   "marginBottom": "0.7rem",
                   "fontSize": "0.88rem",
                   "lineHeight": "1.7",
               }),
        html.P("— Gratacós & Botto, paper UPDATE v.A-29 párr. 5 (Summary)",
               style={"fontSize": "0.75rem", "color": "#9aa0a6"}),
    ], className="card")


def comparison_table_card():
    rows = [
        ("Therapeutic mechanism",
         "Direct microbicidal/microbistatic action on bacterial structures or biosynthetic pathways",
         "Disruption of metabolic substrates / cofactors that resistant phenotypes still depend on (paper UPDATE v.A-29 párr. 24)"),
        ("Selective pressure target",
         "Bacteria — drug presence selects for resistant survivors (Darwinian adaptation)",
         "To be specified in paper — distinct selective topology proposed"),
        ("Resistance trajectory",
         "Exponential / super-exponential (this dashboard's primary forecast)",
         "Hypothesised to be more durable; quantitative model not yet specified"),
        ("R&D pipeline status",
         "Saturating: no fundamentally new antibiotic class approved in decades (paper Summary)",
         "Open territory — premise of the paper's solution proposal"),
        ("Combinatorial use",
         "Combination therapy can accelerate adaptation due to compounded selective pressure (párr. 5)",
         "Combination logic differs — to be detailed by authors"),
        ("Empirical anchoring (in this dashboard)",
         "Anchored to 10+ peer-reviewed sources; super-exp model in Overview",
         "No quantitative anchor yet; this page is structural scaffold only"),
    ]

    return html.Div([
        html.H3("Paradigm comparison (qualitative)", className="card-title"),
        html.P(
            "Side-by-side framing of the classical antibiotic paradigm vs the "
            "antimetabolic angle. Right-column cells marked 'to be specified' are "
            "explicit placeholders for the authors — this dashboard does not invent "
            "therapeutic claims.",
            className="card-subtitle",
        ),
        html.Table([
            html.Thead(html.Tr([
                html.Th("Dimension"),
                html.Th("Classical antibiotic"),
                html.Th("Antimetabolic (proposed)"),
            ])),
            html.Tbody([
                html.Tr([html.Td(d), html.Td(c), html.Td(a)])
                for d, c, a in rows
            ]),
        ], className="data-table"),
    ], className="card")


def open_questions_card():
    questions = [
        "What metabolic substrate or cofactor is the proposed therapeutic lever, and through which pathway is its disruption selectively pathogen-toxic?",
        "How is host-pathogen metabolic discrimination achieved (specificity to avoid mitochondrial / human enzyme overlap)?",
        "What is the kinetic resistance-emergence model under the proposed mechanism, and how does it compare to the super-exponential trajectory of classical antibiotics?",
        "In which ESKAPEE / PDR phenotypes is the antimetabolic angle expected to be most effective? Where might intrinsic biology limit it (e.g., S. maltophilia metabolic versatility)?",
        "What is the minimum viable preclinical evidence package required to test the hypothesis?",
        "Are there existing compounds (repurposed) whose mechanism overlaps with the proposed metabolic disruption, that could provide proof-of-concept data?",
        "How does the proposal interact with combinatorial-use concerns (párr. 13: 'cycling strategies... force a Darwinian adaptation')?",
    ]

    return html.Div([
        html.H3("Open research questions",
                className="card-title"),
        html.P(
            "Placeholder list. Authors: replace each item with the corresponding "
            "answer or sub-thesis. This card is intentionally scaffold-only.",
            className="card-subtitle",
        ),
        html.Ol(
            [html.Li(q, style={"marginBottom": "0.6rem", "lineHeight": "1.6"})
             for q in questions],
            style={"fontSize": "0.85rem", "color": "#e8eaed", "paddingLeft": "1.5rem"},
        ),
    ], className="card")


def model_categories_card():
    """Mathematical model categories from the paper's Math section that may
    underpin a quantitative antimetabolic-resistance trajectory."""
    rows = [
        ("Multiscale (mutation + selection + horizontal gene transfer)",
         "Proc. R. Soc. B 2019",
         "Whole-organism dynamics with inter-cell genetic exchange — natural fit for population-scale resistance kinetics."),
        ("Mechanistic cycling/mixing",
         "Pimenta et al., Microb. Drug Resist. 2020",
         "Compares antibiotic cycling vs mixing strategies — relevant when reasoning about combination therapy with antimetabolic agents."),
        ("Population-level AMR modelling",
         "Niewiadomska et al., Infect. Dis. Model. 2019",
         "Foundational framework for hospital/community AMR — adaptable to alternate selective topologies."),
        ("Pharmacodynamic models under sub-therapeutic dosing",
         "J. Theor. Biol. 2019",
         "Drug-concentration thresholds that drive (or avoid) resistance emergence."),
        ("Biofilm models",
         "Bull. Math. Biol. 2020",
         "Biofilm-bound bacteria respond differently to therapy — relevant for nosocomial Gram-negative settings (P. aeruginosa, K. pneumoniae)."),
        ("Network / hospital-spread models",
         "Sci. Rep. 2020",
         "Healthcare-system contact networks — bound the population-scale impact of any new therapeutic strategy."),
        ("Within-host metabolic models (gap)",
         "—",
         "No paper UPDATE v.A-29 reference yet. This is the natural quantitative complement to the antimetabolic proposal."),
    ]

    return html.Div([
        html.H3("Mathematical model categories (from paper's Math section)",
                className="card-title"),
        html.P(
            "Existing model families that could underpin a quantitative "
            "antimetabolic-resistance trajectory once the mechanism is specified. "
            "The last row marks a gap — no within-host metabolic model is cited "
            "in the paper, suggesting a possible methodology contribution.",
            className="card-subtitle",
        ),
        html.Table([
            html.Thead(html.Tr([
                html.Th("Model family"),
                html.Th("Reference"),
                html.Th("Relevance to antimetabolic angle"),
            ])),
            html.Tbody([
                html.Tr([html.Td(f), html.Td(r), html.Td(rel)])
                for f, r, rel in rows
            ]),
        ], className="data-table"),
    ], className="card")


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
layout = html.Div([
    help_section("Antimetabolic Solution", [
        "PAGE PURPOSE: This page previews the antimetabolic line of treatment proposed by the paper UPDATE v.A-29. The corresponding section in the paper is currently a scaffold (párr. 24, with the substantive content in active drafting). This dashboard page mirrors that status — it is structural and citational, not therapeutic. Where the paper does not yet make a specific claim, this page leaves an explicit placeholder rather than inventing one.",
        "WHY A PARADIGM SHIFT IS PROPOSED: The Summary (párr. 5) and Discussion (párrs. 22, 25) establish that classical antibiotics are caught in a structural feedback loop. Selective pressure on bacterial targets selects for resistant survivors; combination therapy can intensify rather than relieve the pressure (párr. 5: 'combinatorial treatments... may even accelerate the rate of microbial adaptation'); cycling strategies have been studied but do not break the underlying Darwinian adaptation (párr. 13). The paper's quantitative model — visualised on the Overview page — projects a critical-ineffectiveness point in 2040–2047 under this paradigm. The paper concludes that 'unless new categories of germicidal substances are developed, a reverse epidemiological transition seems inevitable' (párr. 5).",
        "WHAT THE PAPER PROPOSES (literal): The subtitle of the paper UPDATE v.A-29 reads 'A predictive mathematical model of declining antimicrobial effectiveness, and its possible metabolic solution.' Section 'Antimetabolic interventions' (párr. 24) introduces the alternative angle. The paper does not yet specify the molecular target, the substrate of disruption, or the kinetics of resistance emergence under the proposed mechanism — those are open at the time of this dashboard build. This page therefore presents a paradigm-comparison framework rather than a quantitative model.",
        "PARADIGM-COMPARISON CHART: The chart on this page contrasts two trajectories. The red curve is the classical antibiotic effectiveness trajectory derived deterministically from the super-exponential resistance model (i.e. 100 minus the resistance index). The blue band is a qualitative envelope intended only to visualise the paper's claim that an alternative line could sustain therapeutic effectiveness — it is NOT a quantitative forecast. The band is annotated as such directly in the figure to prevent any misreading. This is the only page in the dashboard where a series is shown without empirical anchoring; the convention is enforced everywhere else.",
        "COMPARISON TABLE: The qualitative comparison table contrasts six dimensions (mechanism, selective-pressure target, resistance trajectory, R&D pipeline, combinatorial use, empirical anchoring) between the classical and antimetabolic paradigms. Right-column cells marked 'to be specified' are explicit author-fillable placeholders — they signal where additional content from the authors will replace the scaffold.",
        "OPEN RESEARCH QUESTIONS: The numbered list captures questions the antimetabolic proposal raises but does not yet answer. They cover specificity (how host metabolism is preserved while pathogen metabolism is disrupted), kinetics (what the resistance-emergence curve looks like under the new mechanism), pathogen scope (which ESKAPEE / PDR phenotypes are best candidates), and methodological prerequisites. Authors can replace each item with the corresponding answer or sub-thesis.",
        "MATHEMATICAL MODEL CATEGORIES: The final card lists the model families cited in the paper's Math section (multiscale, mechanistic cycling, population-level, pharmacodynamic, biofilm, network) and notes a gap — no within-host metabolic model is cited, suggesting a possible methodology contribution from the authors.",
        "EDITORIAL DISCIPLINE: Throughout this page the constraint is the same as the rest of the dashboard — no fabricated data, no speculative therapeutic claims, all references traceable to the paper or to peer-reviewed literature. The qualitative band on the chart is the single exception, clearly marked as qualitative. Once the authors specify the molecular mechanism and supply quantitative inputs, this page can be upgraded to mirror the empirical rigour of the Overview and Pathogens pages.",
    ]),

    hypothesis_banner(),

    paper_quote_card(),

    # Paradigm chart
    html.Div([
        chart_title_with_info(
            "Classical vs antimetabolic — paradigm comparison",
            "Red: deterministic effectiveness trajectory derived from the super-exponential resistance model (Overview page). Blue band: qualitative working-hypothesis envelope, explicitly NOT a forecast. Authors will replace the band with a quantitative trajectory once the mechanism is specified.",
            "One empirical curve, one qualitative envelope — no fabricated forecasts",
        ),
        dcc.Graph(id="paradigm-chart", figure=build_paradigm_chart(), config=SVG_CONFIG),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            html.A("Paper UPDATE v.A-29 párrs. 5, 22, 24", href="#", target="_blank"),
            " · ",
            html.A("Super-exponential resistance model (Overview)", href="/", target="_blank"),
        ], className="chart-sources"),
    ], className="card"),

    comparison_table_card(),

    open_questions_card(),

    model_categories_card(),

    # Closing card with cross-links
    html.Div([
        html.H3("Cross-references", className="card-title"),
        html.Div([
            html.P([
                "• Resistance trajectory modelled on the ",
                html.A("Overview", href="/", style={"color": "var(--accent)"}),
                " page (super-exponential thesis).",
            ], style={"marginBottom": "0.4rem"}),
            html.P([
                "• Pathogens for which PDR is documented are flagged on the ",
                html.A("Pathogens", href="/pathogens", style={"color": "var(--accent)"}),
                " page (Magiorakos badges).",
            ], style={"marginBottom": "0.4rem"}),
            html.P([
                "• Industry-side context — funding grows while efficacy declines — on the ",
                html.A("Industry", href="/industry", style={"color": "var(--accent)"}),
                " page.",
            ], style={"marginBottom": "0.4rem"}),
            html.P([
                "• Time-series evidence per phenotype on the ",
                html.A("Time Series", href="/timeseries", style={"color": "var(--accent)"}),
                " page (SARIMA forecasts).",
            ]),
        ], style={"fontSize": "0.85rem", "color": "#9aa0a6"}),
    ], className="card"),
])
