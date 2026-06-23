"""
Industry & Bibliometrics page — paper UPDATE v.A-29 párr. 25:
"market grows but efficacy doesn't".

Four charts:
  1. PubMed scientometric trend (annual paper counts 1990-2025)
  2. Antibiotic-resistance market size 2022-2032 (CAGR 5.4%)
  3. Drug-class share 2023 vs 2032
  4. Awareness vs effectiveness — divergence visualization
"""

import dash
from dash import html, dcc
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.bibliometrics_data import (
    PUBMED_ANNUAL, PUBMED_TOTAL,
    MARKET_GROWTH, MARKET_CAGR, MARKET_BASE_BN, MARKET_BASE_YEAR,
    DRUG_CLASS_SHARE, class_size_2023, class_size_2032,
    AWARENESS_EFFECTIVENESS,
)
from components import help_section, chart_title_with_info

dash.register_page(__name__, path="/industry", name="Industry")


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


def build_pubmed_chart():
    """Annual PubMed paper count for 'antibiotic resistance', 1990-2025."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=PUBMED_ANNUAL["year"],
        y=PUBMED_ANNUAL["papers"],
        marker_color="#4fc3f7",
        marker_line=dict(color="#21232d", width=0.5),
        name="Annual papers",
        hovertemplate="<b>%{x}</b><br>%{y:,} publications<extra></extra>",
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(
            text=f'PubMed: "antibiotic resistance" — {PUBMED_TOTAL:,} cumulative results',
            font=dict(size=14),
        ),
        xaxis_title="Year",
        yaxis_title="Annual publications",
        height=360,
    )

    return fig


def build_market_chart():
    """Antibiotic-resistance market size with CAGR 5.4% growth."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=MARKET_GROWTH["year"],
        y=MARKET_GROWTH["market_size_bn"],
        mode="lines+markers",
        line=dict(color="#ffb74d", width=3, shape="spline"),
        marker=dict(size=7, color="#ffb74d",
                    line=dict(color="#21232d", width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(255, 183, 77, 0.10)",
        name=f"Market size (CAGR {MARKET_CAGR*100:.1f}%)",
        hovertemplate="<b>%{x}</b><br>$%{y:.2f}B<extra></extra>",
    ))

    fig.add_annotation(
        x=MARKET_BASE_YEAR, y=MARKET_BASE_BN,
        text=f"Base ${MARKET_BASE_BN:.1f}B",
        showarrow=True, arrowhead=2, arrowcolor="#ffb74d",
        bgcolor="#1a1c25", bordercolor="#2d2f3a", borderwidth=1,
        font=dict(color="#ffb74d", size=11),
        ax=-30, ay=-40,
    )
    end = MARKET_GROWTH.iloc[-1]
    fig.add_annotation(
        x=int(end["year"]), y=float(end["market_size_bn"]),
        text=f"${end['market_size_bn']:.2f}B by {int(end['year'])}",
        showarrow=True, arrowhead=2, arrowcolor="#ffb74d",
        bgcolor="#1a1c25", bordercolor="#2d2f3a", borderwidth=1,
        font=dict(color="#ffb74d", size=11),
        ax=-50, ay=-30,
    )

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(
            text=f"Global Antibiotic-Resistance Market — CAGR {MARKET_CAGR*100:.1f}%",
            font=dict(size=14),
        ),
        xaxis_title="Year",
        yaxis_title="Market size (USD billions)",
        height=360,
    )

    return fig


def build_drug_class_chart():
    """Drug-class share, 2023 vs 2032, in USD billions."""
    df_23 = class_size_2023()
    df_32 = class_size_2032()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_23["drug_class"], y=df_23["size_bn_2023"],
        name="2023",
        marker_color="#4fc3f7",
        text=[f"${v:.2f}B" for v in df_23["size_bn_2023"]],
        textposition="outside",
        textfont=dict(color="#e8eaed", size=11),
        hovertemplate="<b>%{x}</b><br>2023: $%{y:.2f}B<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=df_32["drug_class"], y=df_32["size_bn_2032"],
        name="2032",
        marker_color="#ef5350",
        text=[f"${v:.2f}B" for v in df_32["size_bn_2032"]],
        textposition="outside",
        textfont=dict(color="#e8eaed", size=11),
        hovertemplate="<b>%{x}</b><br>2032: $%{y:.2f}B<extra></extra>",
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Market by Drug Class — 2023 vs 2032 (USD bn)", font=dict(size=14)),
        barmode="group",
        xaxis_title="",
        yaxis_title="USD billions",
        height=360,
    )
    fig.update_yaxes(range=[0, 3.2])

    return fig


def build_divergence_chart():
    """
    Awareness vs effectiveness divergence — paper párr. 25 thesis:
    'market grows but efficacy doesn't'.
    Both indexed to 1990 = 1.0; logarithmic Y to fit the 500x growth + 0.34x decline.
    """
    df = AWARENESS_EFFECTIVENESS

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["year"], y=df["awareness_idx"],
        mode="lines",
        line=dict(color="#4fc3f7", width=3),
        name="Scientometric awareness (cumulative PubMed)",
        hovertemplate="<b>%{x}</b><br>Awareness index: %{y:,.1f}× (1990 baseline)<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=df["year"], y=df["effectiveness_idx"],
        mode="lines",
        line=dict(color="#ef5350", width=3, dash="dash"),
        name="Therapeutic effectiveness (100 − resistance index)",
        hovertemplate="<b>%{x}</b><br>Effectiveness index: %{y:.3f}× (1990 baseline)<extra></extra>",
    ))

    fig.add_hline(
        y=1.0, line_dash="dot", line_color="#9aa0a6", line_width=1,
        annotation_text="1990 baseline",
        annotation_position="bottom right",
        annotation_font=dict(color="#9aa0a6", size=10),
    )

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(
            text="Awareness vs Effectiveness — divergence (1990 = 1.0)",
            font=dict(size=14),
        ),
        xaxis_title="Year",
        yaxis_title="Index (log scale, 1990 = 1.0)",
        height=400,
        hovermode="x unified",
    )
    fig.update_yaxes(type="log")

    return fig


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
last_year = int(PUBMED_ANNUAL["year"].iloc[-1])
last_papers = int(PUBMED_ANNUAL["papers"].iloc[-1])
market_2032 = float(MARKET_GROWTH[MARKET_GROWTH["year"] == 2032]["market_size_bn"].iloc[0])

layout = html.Div([
    help_section("Industry & Bibliometrics", [
        "PAPER CONTEXT (UPDATE v.A-29 párr. 25): The paper observes that 'a scientometric assessment of this phenomenon does indeed show an increase in recognition within the community... R&D investments are also on the rise, expanding at a compound annual growth rate (CAGR) of 5.4%. Through the lens of our own forecast, however, both awareness and actions seem insufficient. Although the antibiotic resistance market has been evolving on par with the declining effect of standard pharmaceuticals. Reports show an increase in volume of sales, but no increase in efficacy is discernible.' This page operationalises that thesis with four charts.",
        "PUBMED SCIENTOMETRIC TREND: The bar chart shows annual publication counts for the search term 'antibiotic resistance' on PubMed, 1990–2025. The cumulative total in the figure (~253K) closely matches the 250,267 results visible in the PubMed query screenshot embedded in the paper (image 3). The annual count is computed deterministically by the closed-form expression count(y) = round(500 · exp(0.115 · (y - 1990))) — calibrated to reproduce the visual envelope of the PubMed bar chart. The exponential growth in publications confirms rising awareness; the next chart shows the awareness has not translated into improved effectiveness.",
        "MARKET GROWTH (CAGR 5.4%): The Univdatos 'Antibiotic Resistance Market 2024–2032' report projects a 5.4% compound annual growth rate. Anchored at a base of USD 5.5B in 2023, the market reaches approximately USD 8.83B by 2032 under uniform CAGR. The line chart represents this deterministic projection. While market size growth signals attention and capital, the paper's central observation is that growth in revenue has not translated into a measurable increase in clinical effectiveness — the next chart visualises that gap.",
        "DRUG-CLASS BREAKDOWN: The grouped bar chart compares 2023 and 2032 estimated revenue for the four drug-class buckets reported by Univdatos: Oxazolidinones (linezolid family — Gram-positive infections), Lipoglycopeptides (dalbavancin/oritavancin — long-acting Gram-positive), Tetracyclines (tigecycline/eravacycline/omadacycline — broad-spectrum salvage), and Others (β-lactam/inhibitor combinations and novel agents). Per-class shares are visual approximations of the Univdatos figure embedded in the paper (image 2). Note: this is revenue allocation, not therapeutic effectiveness — the antibiotics are still the same molecules, with the same resistance pressures eroding their utility.",
        "AWARENESS-vs-EFFECTIVENESS DIVERGENCE: The fourth chart is the most important. Both series are indexed to 1990 = 1.0 to make the divergence visible. Awareness (blue solid) tracks cumulative PubMed publications: by 2025 it reaches ~500× the 1990 baseline. Effectiveness (red dashed) tracks (100 − resistance pressure index), the proportion of antibiotic activity remaining: by 2025 it has declined to ~0.34× of the 1990 baseline. The two curves move in opposite directions on a log scale — exactly the pattern the paper describes as 'increase in volume of sales, but no increase in efficacy'. This is a structural, not cyclical, divergence; awareness alone has not solved the problem.",
        "WHY THIS MATTERS FOR THE PAPER'S THESIS: The Industry section supports the paper's call (párr. 5) for 'new categories of germicidal substances'. Funding and publications are growing exponentially, but the underlying biology of selective pressure means that more of the same kind of drug development cannot, by itself, reverse the resistance trajectory. The Antimetabolic Escape Route page elaborates the alternative therapeutic angle the paper proposes.",
        "DATA PROVENANCE: PubMed annual counts are deterministic approximations to the visual envelope of the search-results-by-year chart at the time the paper was prepared (image 3, 250,267 cumulative results). Market and drug-class data are deterministic projections anchored to the Univdatos 'Antibiotic Resistance Market 2024–2032' report (image 2). The awareness-vs-effectiveness chart combines these with the super-exponential resistance model from the Overview page. All values reproduce identically on every reload — no random sampling, no fitting.",
    ]),

    # Stats row — 4 cards
    html.Div([
        html.Div([
            html.Div(f"{PUBMED_TOTAL:,}", className="stat-value accent"),
            html.Div("PubMed Results 1990–2025", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div(f"{MARKET_CAGR*100:.1f}%", className="stat-value warning"),
            html.Div("Market CAGR 2024–2032", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div(f"${market_2032:.1f}B", className="stat-value warning"),
            html.Div("Market Size 2032", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div("0.34×", className="stat-value danger"),
            html.Div("Effectiveness 2025 vs 1990", className="stat-label"),
        ], className="stat-card"),
    ], className="stats-row"),

    # PubMed
    html.Div([
        chart_title_with_info(
            "Scientometric Awareness (PubMed)",
            "Annual publications matching 'antibiotic resistance' on PubMed, 1990-2025. Cumulative ~253K results, closely matching the 250,267 figure visible in the PubMed query screenshot embedded in the paper (image 3).",
            "Annual publication counts — closed-form exponential calibrated to PubMed total",
        ),
        dcc.Graph(id="pubmed-chart", figure=build_pubmed_chart(), config=SVG_CONFIG),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            html.A("PubMed search 'antibiotic resistance'",
                   href="https://pubmed.ncbi.nlm.nih.gov/?term=antibiotic+resistance",
                   target="_blank"),
            " · ",
            html.A("Paper UPDATE v.A-29 párr. 25",
                   href="#", target="_blank"),
        ], className="chart-sources"),
    ], className="card"),

    # Market + Drug class side by side
    html.Div([
        html.Div([
            chart_title_with_info(
                "Antibiotic Resistance Market (2022–2032)",
                "Univdatos report projects 5.4% CAGR. Base of USD 5.5B in 2023 grows to approximately USD 8.83B by 2032 under uniform CAGR. Revenue growth without efficacy growth is the paper's central industry observation.",
                f"Deterministic CAGR {MARKET_CAGR*100:.1f}% projection",
            ),
            dcc.Graph(id="market-chart", figure=build_market_chart(), config=SVG_CONFIG),
            html.Div([
                html.Span("Sources: ", className="source-label"),
                html.A("Univdatos — Antibiotic Resistance Market 2024-2032",
                       href="https://univdatos.com/reports/antibiotic-resistance-market",
                       target="_blank"),
            ], className="chart-sources"),
        ], className="card"),
        html.Div([
            chart_title_with_info(
                "Market by Drug Class",
                "Per-class revenue allocation 2023 vs 2032. Oxazolidinones (linezolid family), Lipoglycopeptides (dalbavancin/oritavancin), Tetracyclines (tigecycline/eravacycline/omadacycline), and Others (β-lactam/inhibitor combinations and novel agents).",
                "Visual approximations from Univdatos drug-class figure",
            ),
            dcc.Graph(id="drug-class-chart", figure=build_drug_class_chart(), config=SVG_CONFIG),
            html.Div([
                html.Span("Sources: ", className="source-label"),
                html.A("Univdatos — Antibiotic Resistance Market 2024-2032",
                       href="https://univdatos.com/reports/antibiotic-resistance-market",
                       target="_blank"),
            ], className="chart-sources"),
        ], className="card"),
    ], className="chart-grid-2"),

    # Divergence chart — central thesis
    html.Div([
        chart_title_with_info(
            "Awareness vs Effectiveness — divergence",
            "Paper UPDATE v.A-29 párr. 25 thesis. Both series indexed to 1990 = 1.0 on a log scale. Awareness (blue) reflects cumulative PubMed publications; effectiveness (red) reflects (100 − resistance index). By 2025: awareness at ~500× baseline, effectiveness at ~0.34× — a structural divergence.",
            "The paper's central industry argument visualised",
        ),
        dcc.Graph(id="divergence-chart", figure=build_divergence_chart(), config=SVG_CONFIG),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            html.A("PubMed search 'antibiotic resistance'",
                   href="https://pubmed.ncbi.nlm.nih.gov/?term=antibiotic+resistance",
                   target="_blank"),
            " · ",
            html.A("Murray et al., Lancet 2022",
                   href="https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext",
                   target="_blank"),
            " · ",
            html.A("Tai et al., IJAA 2025",
                   href="https://doi.org/10.1016/j.ijantimicag.2025.107636",
                   target="_blank"),
        ], className="chart-sources"),
    ], className="card"),

    # Summary card
    html.Div([
        html.H3("Bottom line", className="card-title"),
        html.Div([
            html.P(
                "Funding and publications grow exponentially. Effectiveness declines on a logistic super-exponential. "
                "Within the same therapeutic paradigm — selective pressure on existing drug classes — the trends move "
                "in opposite directions. The paper argues that closing the gap requires a categorical shift in the "
                "therapeutic approach, not more of the same. See the Metabolic page for the alternative line of "
                "treatment proposed by Gratacós-Botto.",
                style={"fontSize": "0.85rem", "color": "#9aa0a6", "lineHeight": "1.7"}
            ),
        ]),
    ], className="card"),
])
