"""
Data Sources page — AMR data source catalog, coverage timeline, and summary.
"""

import dash
from dash import html, dcc
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from components import help_section, chart_title_with_info

dash.register_page(__name__, path="/datasources", name="Data Sources")

CHART_LAYOUT = dict(
    paper_bgcolor="#21232d",
    plot_bgcolor="#21232d",
    font=dict(color="#e8eaed", family="Inter, sans-serif", size=12),
)

# --- Data source definitions ---

DATA_SOURCES = [
    {
        "name": "WHO GLASS",
        "description": "Global Antimicrobial Resistance and Use Surveillance System — the primary international surveillance platform collecting national AMR data from enrolled countries.",
        "data_type": "Laboratory-based surveillance (clinical isolates)",
        "coverage": "127 enrolled countries, 2015-present",
        "url": "https://www.who.int/initiatives/glass",
        "status": "connected",
        "years": (2015, 2025),
    },
    {
        "name": "ECDC EARS-Net",
        "description": "European Antimicrobial Resistance Surveillance Network — systematic collection of resistance data from 30 EU/EEA countries on invasive isolates.",
        "data_type": "Invasive isolate surveillance (blood/CSF)",
        "coverage": "30 EU/EEA countries, 1998-present",
        "url": "https://www.ecdc.europa.eu/en/antimicrobial-resistance/surveillance-and-disease-data/data-ecdc",
        "status": "connected",
        "years": (1998, 2025),
    },
    {
        "name": "CDC AR Threats Report",
        "description": "US Centers for Disease Control threat assessment ranking pathogens by danger level, with national resistance estimates and trend data.",
        "data_type": "Threat assessment & national estimates",
        "coverage": "United States, 2013/2019/2022 editions",
        "url": "https://www.cdc.gov/antimicrobial-resistance/data-research/threats/index.html",
        "status": "available",
        "years": (2013, 2022),
    },
    {
        "name": "ResistanceMap (CDDEP)",
        "description": "Interactive platform from the Center for Disease Dynamics, Economics & Policy providing antibiotic resistance and consumption data across countries.",
        "data_type": "Resistance rates & antibiotic consumption",
        "coverage": "40+ countries, 2000-present",
        "url": "https://resistancemap.onehealthtrust.org/",
        "status": "available",
        "years": (2000, 2025),
    },
    {
        "name": "GRAM Project",
        "description": "Global Research on Antimicrobial Resistance — IHME-led initiative producing comprehensive estimates of AMR burden by pathogen-drug combination.",
        "data_type": "Statistical burden estimates (deaths, DALYs)",
        "coverage": "204 countries/territories, 1990-2021",
        "url": "https://www.healthdata.org/research-analysis/health-risks-issues/antimicrobial-resistance-amr",
        "status": "connected",
        "years": (1990, 2021),
    },
    {
        "name": "Lancet GBD-AMR (Murray et al.)",
        "description": "Landmark 2022 Lancet study estimating 4.95 million deaths associated with bacterial AMR in 2019 across 204 countries using Bayesian hierarchical models.",
        "data_type": "Modeled burden estimates (cross-sectional)",
        "coverage": "204 countries, reference year 2019",
        "url": "https://doi.org/10.1016/S0140-6736(21)02724-0",
        "status": "connected",
        "years": (2019, 2019),
    },
]

STATUS_STYLES = {
    "connected": {"color": "#66bb6a", "label": "Connected"},
    "available": {"color": "#ffb74d", "label": "Available"},
    "planned": {"color": "#9aa0a6", "label": "Planned"},
}


def build_status_badge(status):
    style_info = STATUS_STYLES.get(status, STATUS_STYLES["planned"])
    return html.Span(
        style_info["label"],
        style={
            "display": "inline-block",
            "background": f"{style_info['color']}22",
            "color": style_info["color"],
            "padding": "0.15rem 0.6rem",
            "borderRadius": "4px",
            "fontSize": "0.7rem",
            "fontWeight": "600",
            "letterSpacing": "0.04em",
            "textTransform": "uppercase",
        },
    )


def build_source_table():
    """Build data source listing as an HTML table."""
    rows = []
    for src in DATA_SOURCES:
        rows.append(
            html.Tr([
                html.Td([
                    html.Div(src["name"], style={"fontWeight": "600", "marginBottom": "0.2rem"}),
                    html.Div(src["description"], style={"fontSize": "0.75rem", "color": "#9aa0a6", "lineHeight": "1.4"}),
                ]),
                html.Td(src["data_type"], style={"fontSize": "0.78rem"}),
                html.Td(src["coverage"], style={"fontSize": "0.78rem"}),
                html.Td(
                    html.A(
                        "Link",
                        href=src["url"],
                        target="_blank",
                        style={"color": "#4fc3f7", "textDecoration": "none", "fontSize": "0.78rem"},
                    )
                ),
                html.Td(build_status_badge(src["status"])),
            ])
        )

    return html.Table(
        [
            html.Thead(
                html.Tr([
                    html.Th("Source"),
                    html.Th("Data Type"),
                    html.Th("Coverage"),
                    html.Th("URL"),
                    html.Th("Status"),
                ])
            ),
            html.Tbody(rows),
        ],
        className="data-table",
    )


def build_coverage_timeline():
    """Gantt-like horizontal bar chart showing data coverage by source."""
    fig = go.Figure()

    colors = ["#4fc3f7", "#ef5350", "#ffb74d", "#ce93d8", "#66bb6a", "#ff7043"]

    for i, src in enumerate(reversed(DATA_SOURCES)):
        start, end = src["years"]
        # For single-year sources, give a visible width
        duration = max(end - start, 1)
        fig.add_trace(go.Bar(
            y=[src["name"]],
            x=[duration],
            base=[start],
            orientation="h",
            marker_color=colors[len(DATA_SOURCES) - 1 - i],
            marker_line=dict(width=0),
            hovertemplate=(
                f"<b>{src['name']}</b><br>"
                f"{start}–{end}<br>"
                f"Duration: {duration} years<extra></extra>"
            ),
            showlegend=False,
        ))

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Data Coverage Timeline by Source", font=dict(size=14)),
        xaxis=dict(
            title="Year",
            range=[1988, 2027],
            gridcolor="#2d2f3a",
            dtick=5,
        ),
        yaxis=dict(
            gridcolor="#2d2f3a",
            tickfont=dict(size=11),
        ),
        height=350,
        margin=dict(l=200, r=40, t=50, b=50),
        bargap=0.3,
    )

    return fig


def build_summary_cards():
    """Summary statistics about data sources."""
    total_sources = len(DATA_SOURCES)
    connected = sum(1 for s in DATA_SOURCES if s["status"] == "connected")
    min_year = min(s["years"][0] for s in DATA_SOURCES)
    max_year = max(s["years"][1] for s in DATA_SOURCES)

    cards = [
        html.Div([
            html.Div(str(total_sources), className="stat-value accent"),
            html.Div("Data Sources", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div(str(connected), className="stat-value success"),
            html.Div("Connected", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div(str(total_sources - connected), className="stat-value warning"),
            html.Div("Available", className="stat-label"),
        ], className="stat-card"),
        html.Div([
            html.Div(f"{min_year}–{max_year}", className="stat-value accent"),
            html.Div("Year Range", className="stat-label"),
        ], className="stat-card"),
    ]

    return html.Div(cards, className="stats-row")


SVG_CONFIG = {
    "toImageButtonOptions": {"format": "svg", "scale": 3},
    "displayModeBar": True,
}

layout = html.Div([
    # Help section
    help_section("Data Sources", [
        "WHY DATA PROVENANCE MATTERS: Antimicrobial resistance research is only as reliable as the underlying surveillance data. Different data sources use different sampling methods (clinical isolates vs population-based sampling), different breakpoint standards (EUCAST vs CLSI), and different geographic coverage. Understanding where the data comes from, how it was collected, and what populations it represents is essential for interpreting resistance estimates correctly and for assessing whether findings from one setting can be generalized to another. This page provides a transparent audit trail linking every dashboard visualization back to its primary data source.",
        "WHO GLASS: The Global Antimicrobial Resistance and Use Surveillance System is the WHO's flagship international AMR surveillance platform. It collects standardized national data from enrolled countries on resistance rates in clinical isolates from blood, urine, stool, and genital specimens. Strengths: broadest geographic scope (127+ enrolled countries), standardized reporting framework, includes antibiotic consumption data. Limitations: voluntary enrollment means coverage is uneven (many low-income countries have limited laboratory capacity), data quality varies by country, and reporting focuses on clinical isolates from healthcare settings rather than community infections.",
        "ECDC EARS-NET: The European Antimicrobial Resistance Surveillance Network is widely regarded as the gold standard for regional AMR surveillance. It systematically collects resistance data on invasive isolates (blood and cerebrospinal fluid cultures) from 30 EU/EEA countries. Strengths: highly standardized methodology, long time series (since 1998), consistent population denominators enabling reliable trend analysis. Limitations: restricted to Europe, focuses only on invasive infections (may underestimate resistance in urinary or respiratory isolates), and bloodstream infection isolates may not represent the full spectrum of AMR in a country.",
        "GRAM PROJECT AND LANCET GBD-AMR: The Global Research on Antimicrobial Resistance project at IHME produced the landmark Murray et al. 2022 Lancet study estimating 4.95 million deaths associated with AMR in 2019 across 204 countries. This study used Bayesian hierarchical models to synthesize heterogeneous data sources into comprehensive burden estimates by pathogen-drug combination and by region. Strengths: most comprehensive global burden estimates available, covers all regions including those without formal surveillance. Limitations: heavy reliance on statistical modeling for data-sparse regions, estimates carry wide uncertainty intervals in low-income settings, and the cross-sectional design (reference year 2019) does not directly capture trends.",
        "STATUS DEFINITIONS: 'Connected' (green) means the data source is actively integrated into the dashboard visualizations -- the charts you see are constructed from or calibrated against this data. 'Available' (amber) means the data source is publicly accessible and contains relevant AMR data, but has not yet been programmatically integrated into the dashboard pipeline. Available sources can be manually consulted for validation or supplementary analysis. 'Planned' (grey) indicates sources identified for future integration pending data access agreements, format standardization, or development resources.",
        "REQUESTING ADDITIONAL DATA SOURCES: If you are aware of AMR surveillance data sources not listed here -- particularly national or institutional datasets, veterinary/agricultural surveillance (One Health perspective), or environmental resistance monitoring -- these can potentially be integrated into the dashboard framework. Priority is given to sources that: cover underrepresented geographic regions, provide longitudinal time series data, use standardized susceptibility testing methods (EUCAST or CLSI), and are publicly accessible or available through data sharing agreements.",
        "DATA QUALITY CONSIDERATIONS: All AMR surveillance data is subject to several systematic biases. Surveillance bias: resistance rates from clinical isolates (sick patients who sought care and had cultures taken) tend to overestimate true population-level resistance. Geographic coverage gaps: most surveillance data comes from high-income countries; resistance estimates for Sub-Saharan Africa, Central Asia, and parts of South America rely heavily on statistical extrapolation. Reporting standards: different laboratories use different susceptibility breakpoints (EUCAST vs CLSI), which can cause the same isolate to be classified differently. Temporal gaps: many national systems report annually, making it difficult to detect short-term outbreaks or seasonal patterns. These limitations should be acknowledged when interpreting any resistance estimate presented in this dashboard.",
    ]),

    # Summary stats
    build_summary_cards(),

    # Source catalog table
    html.Div([
        chart_title_with_info(
            "AMR Data Source Catalog",
            "Comprehensive listing of global AMR surveillance databases and published studies used to construct the dashboard visualizations.",
            "Major global antimicrobial resistance data sources used in this research project.",
        ),
        build_source_table(),
    ], className="card"),

    # Coverage timeline chart
    html.Div([
        chart_title_with_info(
            "Coverage Timeline",
            "Gantt-style chart showing the temporal span of each data source. Longer bars indicate broader historical coverage, useful for understanding which sources support long-term trend analysis.",
            "Temporal coverage of each data source \u2014 year range over which data is available.",
        ),
        dcc.Graph(
            id="coverage-timeline",
            figure=build_coverage_timeline(),
            config=SVG_CONFIG,
        ),
    ], className="card"),
])
