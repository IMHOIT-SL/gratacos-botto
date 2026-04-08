"""
Pathogens page — Heatmap, regional comparison, and temporal trends.
"""

import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.pathogen_data import (
    PATHOGENS, ANTIBIOTIC_CLASSES, RESISTANCE_MATRIX,
    WHO_PRIORITY, REGIONAL_DATA, TEMPORAL_TRENDS,
)
from components import help_section, chart_title_with_info

dash.register_page(__name__, path="/pathogens", name="Pathogens")

CHART_LAYOUT = dict(
    paper_bgcolor="#21232d",
    plot_bgcolor="#21232d",
    font=dict(color="#e8eaed", family="Inter, sans-serif", size=12),
)

PRIORITY_COLORS = {
    "Critical": "#ef5350",
    "High": "#ffb74d",
    "Medium": "#4fc3f7",
    "Special": "#ce93d8",
}


def build_heatmap():
    """Pathogen vs antibiotic resistance heatmap."""
    # Custom text for hover showing NaN as "N/A (intrinsic)"
    hover_text = []
    display_text = []
    for i, pathogen in enumerate(PATHOGENS):
        hover_row = []
        display_row = []
        for j, abx in enumerate(ANTIBIOTIC_CLASSES):
            val = RESISTANCE_MATRIX[i, j]
            abx_clean = abx.replace("\n", " ")
            if np.isnan(val):
                hover_row.append(f"{pathogen}<br>{abx_clean}<br>N/A (intrinsic R or not tested)")
                display_row.append("—")
            else:
                hover_row.append(f"{pathogen}<br>{abx_clean}<br><b>{val:.0f}%</b> resistant")
                display_row.append(f"{val:.0f}")
        hover_text.append(hover_row)
        display_text.append(display_row)

    # Priority labels for y-axis
    y_labels = [f"{p}  [{WHO_PRIORITY[p]}]" for p in PATHOGENS]

    fig = go.Figure(data=go.Heatmap(
        z=RESISTANCE_MATRIX,
        x=ANTIBIOTIC_CLASSES,
        y=y_labels,
        text=display_text,
        texttemplate="%{text}",
        textfont=dict(size=11, color="white"),
        hovertext=hover_text,
        hovertemplate="%{hovertext}<extra></extra>",
        colorscale=[
            [0, "#1a3a4a"],      # 0% — dark teal
            [0.3, "#4fc3f7"],    # 30% — blue
            [0.5, "#ffb74d"],    # 50% — amber
            [0.7, "#ff7043"],    # 70% — orange
            [1.0, "#ef5350"],    # 100% — red
        ],
        zmin=0,
        zmax=100,
        colorbar=dict(
            title=dict(text="% Resistant", font=dict(size=11)),
            ticksuffix="%",
            len=0.9,
        ),
        xgap=2,
        ygap=2,
    ))

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Resistance Profile: Pathogen × Antibiotic Class", font=dict(size=15)),
        xaxis=dict(side="bottom", tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
        height=550,
        margin=dict(l=220, r=80, t=60, b=100),
    )

    return fig


def build_regional_chart():
    """Regional resistance comparison (grouped bar)."""
    fig = go.Figure()

    pathogens_in_data = REGIONAL_DATA["pathogen"].unique()
    colors = {"K. pneumoniae": "#ef5350", "E. coli": "#4fc3f7",
              "S. aureus (MRSA)": "#ffb74d", "A. baumannii": "#ce93d8"}

    for pathogen in pathogens_in_data:
        subset = REGIONAL_DATA[REGIONAL_DATA["pathogen"] == pathogen]
        fig.add_trace(go.Bar(
            x=subset["region"],
            y=subset["resistance_index"],
            name=pathogen,
            marker_color=colors.get(pathogen, "#66bb6a"),
            hovertemplate=f"<b>{pathogen}</b><br>%{{x}}<br>Resistance: %{{y}}%<extra></extra>",
        ))

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Regional Resistance (key pathogens, 3GC/Carbapenem)", font=dict(size=14)),
        barmode="group",
        xaxis_title="WHO Region",
        yaxis_title="% Resistant Isolates",
        yaxis=dict(range=[0, 100], gridcolor="#2d2f3a"),
        xaxis=dict(gridcolor="#2d2f3a"),
        height=400,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    )

    return fig


def build_trends_chart():
    """Temporal trends of key resistance phenotypes."""
    fig = go.Figure()

    colors = {"MRSA": "#ffb74d", "3GC-R E. coli": "#4fc3f7", "CRE K. pneumoniae": "#ef5350"}

    for phenotype in TEMPORAL_TRENDS["phenotype"].unique():
        subset = TEMPORAL_TRENDS[TEMPORAL_TRENDS["phenotype"] == phenotype]
        fig.add_trace(go.Scatter(
            x=subset["year"],
            y=subset["prevalence"],
            mode="lines+markers",
            name=phenotype,
            line=dict(color=colors.get(phenotype, "#66bb6a"), width=2.5),
            marker=dict(size=4),
            hovertemplate=f"<b>{phenotype}</b><br>%{{x}}<br>Prevalence: %{{y}}%<extra></extra>",
        ))

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Resistance Trends (2000–2025): Key Phenotypes", font=dict(size=14)),
        xaxis_title="Year",
        yaxis_title="% Resistant",
        yaxis=dict(range=[0, 60], gridcolor="#2d2f3a"),
        xaxis=dict(gridcolor="#2d2f3a"),
        height=400,
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    )

    return fig


def build_priority_summary():
    """WHO priority classification summary cards."""
    counts = {}
    for p, priority in WHO_PRIORITY.items():
        counts.setdefault(priority, []).append(p)

    cards = []
    for priority in ["Critical", "High", "Medium", "Special"]:
        if priority not in counts:
            continue
        pathogen_list = counts[priority]
        cards.append(
            html.Div([
                html.Div(
                    f"{len(pathogen_list)}",
                    className="stat-value",
                    style={"color": PRIORITY_COLORS[priority]},
                ),
                html.Div(f"WHO {priority}", className="stat-label"),
                html.Div(
                    ", ".join(p.split(" (")[0] for p in pathogen_list),
                    style={"fontSize": "0.72rem", "color": "#9aa0a6", "marginTop": "0.3rem"},
                ),
            ], className="stat-card")
        )

    return html.Div(cards, className="stats-row")


SVG_CONFIG = {
    "toImageButtonOptions": {"format": "svg", "scale": 3},
    "displayModeBar": True,
}

layout = html.Div([
    # Help section
    help_section("Pathogens", [
        "ESKAPE PATHOGENS: The ESKAPE group -- Enterococcus faecium, Staphylococcus aureus, Klebsiella pneumoniae, Acinetobacter baumannii, Pseudomonas aeruginosa, and Enterobacter species -- are the leading causes of nosocomial (hospital-acquired) infections worldwide. They are named 'ESKAPE' because they effectively 'escape' the effects of most available antibiotics through multiple resistance mechanisms. Together, these organisms account for the majority of multidrug-resistant infections in intensive care units and are responsible for a disproportionate share of AMR-attributable mortality globally.",
        "READING THE HEATMAP: Each row represents a pathogen and each column represents an antibiotic class (e.g., carbapenems, fluoroquinolones, aminoglycosides). The cell value shows the approximate percentage of clinical isolates that are resistant to that drug class, based on global surveillance medians from WHO GLASS, ECDC EARS-Net, and CDC reports. Colors encode severity: dark teal/blue indicates low resistance (0-30%), amber indicates moderate resistance (30-50%), orange indicates high resistance (50-70%), and red indicates very high resistance (70-100%). Higher-resistance cells represent pathogen-drug combinations where empiric therapy is increasingly unreliable.",
        "WHO PRIORITY CLASSIFICATION: The World Health Organization classifies resistant bacteria into three priority tiers to guide research and development investment. 'Critical' priority (red) includes carbapenem-resistant Acinetobacter, Pseudomonas, and Enterobacterales -- these represent the most urgent public health threat due to extremely limited remaining treatment options. 'High' priority (amber) includes vancomycin-resistant Enterococcus, MRSA, and others where resistance is widespread but some treatment alternatives exist. 'Medium' priority (blue) includes organisms like penicillin-non-susceptible Streptococcus pneumoniae where resistance is concerning but manageable. These classifications directly inform which pathogens receive priority funding for new antibiotic and diagnostic development.",
        "INTRINSIC RESISTANCE (GREY CELLS): Cells displayed as a dash ('--') on a grey background indicate 'intrinsic resistance' -- the organism is naturally resistant to that antibiotic class due to its fundamental biology, not through acquired resistance mechanisms. For example, Gram-negative bacteria are intrinsically resistant to vancomycin because the drug cannot penetrate their outer membrane. These cells are excluded from the color scale because the resistance is not clinically meaningful in the same way as acquired resistance; clinicians would never prescribe these combinations. Some grey cells may also indicate insufficient surveillance data for that pathogen-drug pair.",
        "REGIONAL VARIATION: The grouped bar chart shows resistance rates across six WHO regions (Africa, Americas, Eastern Mediterranean, Europe, South-East Asia, Western Pacific) for four key pathogens. Geographic differences are driven by several factors: antibiotic access patterns (over-the-counter availability without prescription in many low- and middle-income countries), antimicrobial stewardship program maturity (strongest in Northern Europe, weakest in regions with limited healthcare infrastructure), infection prevention and control practices (hand hygiene, sanitation, hospital water systems), and surveillance capacity (regions with less surveillance may underreport resistance). Higher resistance rates in Africa, South-East Asia, and the Eastern Mediterranean reflect both genuine higher burden and differential access to healthcare resources.",
        "TEMPORAL TRENDS: The trend chart tracks three key resistance phenotypes over 25 years (2000-2025). MRSA (methicillin-resistant S. aureus) shows a declining trend in many regions, representing one of AMR's success stories -- this decline is attributed to targeted screening programs, improved hand hygiene, and decolonization protocols implemented particularly in European and North American hospitals. In contrast, third-generation cephalosporin-resistant (3GC-R) E. coli and carbapenem-resistant Enterobacterales (CRE) K. pneumoniae show concerning upward trends, driven by the spread of extended-spectrum beta-lactamases (ESBLs) and carbapenemase-producing genes (KPC, NDM, OXA-48) through plasmid-mediated horizontal gene transfer. The divergent trajectories demonstrate that targeted interventions can work (MRSA) but must be sustained and adapted for each pathogen.",
        "CLINICAL IMPLICATIONS: When resistance exceeds 10-20% for a pathogen-drug combination, clinical guidelines typically recommend against using that drug for empiric therapy. Cells showing 50%+ resistance indicate that the antibiotic class is unreliable for more than half of infections caused by that organism -- clinicians must rely on culture results before selecting therapy, which can take 48-72 hours during which patients receive suboptimal treatment. For critical-priority pathogens with high resistance across multiple drug classes (e.g., carbapenem-resistant A. baumannii), therapeutic options narrow to last-resort agents such as colistin, which carry significant toxicity risks.",
    ]),

    # WHO Priority summary
    build_priority_summary(),

    # Main heatmap
    html.Div([
        chart_title_with_info(
            "Resistance Heatmap",
            "Resistance percentage for each pathogen-antibiotic pair. Values are approximate global medians from WHO GLASS, ECDC EARS-Net, and CDC surveillance reports. Pathogens are labeled with their WHO priority classification.",
            "Global median % resistant isolates \u2014 ESKAPE pathogens + WHO priority list. Grey cells = intrinsic resistance or insufficient data.",
        ),
        dcc.Graph(id="pathogen-heatmap", figure=build_heatmap(), config=SVG_CONFIG),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            html.A("WHO GLASS Report 2022", href="https://www.who.int/publications/i/item/9789240062702", target="_blank"),
            " · ",
            html.A("ECDC EARS-Net", href="https://www.ecdc.europa.eu/en/antimicrobial-resistance/surveillance-and-disease-data/data-ecdc", target="_blank"),
            " · ",
            html.A("CDC AR Threats Report 2019", href="https://www.cdc.gov/antimicrobial-resistance/data-research/threats/index.html", target="_blank"),
            " · ",
            html.A("Murray et al., Lancet 2022", href="https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext", target="_blank"),
        ], className="chart-sources"),
    ], className="card"),

    # Regional + Trends side by side
    html.Div([
        html.Div([
            chart_title_with_info(
                "Regional Variation",
                "Comparison of resistance rates across 6 WHO regions for 4 key pathogens. Shows geographic disparities in AMR burden \u2014 higher rates in Africa, SE Asia, and E. Mediterranean regions.",
                "Resistance rates by WHO region (GLASS 2022)",
            ),
            dcc.Graph(id="regional-chart", figure=build_regional_chart(), config=SVG_CONFIG),
            html.Div([
                html.Span("Sources: ", className="source-label"),
                html.A("WHO GLASS Report 2022", href="https://www.who.int/publications/i/item/9789240062702", target="_blank"),
            ], className="chart-sources"),
        ], className="card"),
        html.Div([
            chart_title_with_info(
                "Temporal Trends",
                "25-year resistance trajectories: MRSA shows declining trend (successful interventions), while 3rd-gen cephalosporin-resistant E. coli and carbapenem-resistant K. pneumoniae show concerning upward trends.",
                "25-year trajectory of key resistance phenotypes",
            ),
            dcc.Graph(id="trends-chart", figure=build_trends_chart(), config=SVG_CONFIG),
            html.Div([
                html.Span("Sources: ", className="source-label"),
                html.A("ECDC EARS-Net", href="https://www.ecdc.europa.eu/en/antimicrobial-resistance/surveillance-and-disease-data/data-ecdc", target="_blank"),
                " · ",
                html.A("WHO GLASS Report 2022", href="https://www.who.int/publications/i/item/9789240062702", target="_blank"),
                " · ",
                html.A("CDC NARMS", href="https://www.cdc.gov/narms/index.html", target="_blank"),
            ], className="chart-sources"),
        ], className="card"),
    ], className="chart-grid-2"),

    # Data sources note
    html.Div([
        html.H3("Data Sources", className="card-title"),
        html.Div([
            html.P([
                html.Span("WHO GLASS", className="source-tag"), " Global Antimicrobial Resistance Surveillance System (2022/2023 reports) ",
            ], style={"marginBottom": "0.4rem"}),
            html.P([
                html.Span("EARS-Net", className="source-tag"), " European Antimicrobial Resistance Surveillance Network ",
            ], style={"marginBottom": "0.4rem"}),
            html.P([
                html.Span("Murray et al.", className="source-tag"), " Lancet 2022 — Global burden of bacterial AMR in 2019 ",
            ], style={"marginBottom": "0.4rem"}),
            html.P([
                html.Span("CDC", className="source-tag"), " Antibiotic Resistance Threats in the United States (2019/2022) ",
            ]),
        ], style={"fontSize": "0.82rem", "color": "#9aa0a6"}),
    ], className="card"),
])
