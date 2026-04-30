"""
Pathogens page — ESKAPEE heatmap, regional comparison, temporal trends,
MDR/XDR/PDR phenotype badges, and a transient Sensitivity Analysis panel.
"""

import dash
from dash import html, dcc, callback, Input, Output, State, ALL, ctx
import plotly.graph_objects as go
import numpy as np

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.pathogen_data import (
    PATHOGENS, ANTIBIOTIC_CLASSES, RESISTANCE_MATRIX,
    WHO_PRIORITY, MDR_XDR_PDR, REGIONAL_DATA, TEMPORAL_TRENDS,
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

# MDR/XDR/PDR badge colors — distinct from WHO Priority palette so the two
# classifications coexist visually without clashing.
PHENOTYPE_COLORS = {
    "MDR": "#ffb74d",
    "XDR": "#ff7043",
    "PDR": "#ef5350",
}


def _apply_overrides(matrix, overrides):
    """Return a copy of matrix with sensitivity overrides applied. Deterministic."""
    out = matrix.copy()
    if not overrides:
        return out
    for key, val in overrides.items():
        # key format: "p_idx,a_idx"
        try:
            p, a = (int(x) for x in key.split(","))
        except (ValueError, AttributeError):
            continue
        if 0 <= p < out.shape[0] and 0 <= a < out.shape[1]:
            out[p, a] = float(val)
    return out


def build_heatmap(overrides=None):
    """Pathogen × antibiotic resistance heatmap. overrides: dict {'p,a': value}."""
    matrix = _apply_overrides(RESISTANCE_MATRIX, overrides or {})

    hover_text = []
    display_text = []
    for i, pathogen in enumerate(PATHOGENS):
        hover_row = []
        display_row = []
        for j, abx in enumerate(ANTIBIOTIC_CLASSES):
            val = matrix[i, j]
            abx_clean = abx.replace("\n", " ")
            modified = (overrides or {}).get(f"{i},{j}") is not None
            tag = "  ⚙ modified" if modified else ""
            if np.isnan(val):
                hover_row.append(f"{pathogen}<br>{abx_clean}<br>N/A (intrinsic R or not tested)")
                display_row.append("—")
            else:
                hover_row.append(
                    f"{pathogen}<br>{abx_clean}<br><b>{val:.0f}%</b> resistant{tag}"
                )
                display_row.append(f"{val:.0f}")
        hover_text.append(hover_row)
        display_text.append(display_row)

    # Y labels: WHO priority + Magiorakos phenotype badge
    y_labels = []
    for p in PATHOGENS:
        prio = WHO_PRIORITY[p]
        pheno = MDR_XDR_PDR.get(p, "")
        y_labels.append(f"{p}  [{prio} · {pheno}]")

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=ANTIBIOTIC_CLASSES,
        y=y_labels,
        text=display_text,
        texttemplate="%{text}",
        textfont=dict(size=11, color="white"),
        hovertext=hover_text,
        hovertemplate="%{hovertext}<extra></extra>",
        colorscale=[
            [0, "#1a3a4a"],
            [0.3, "#4fc3f7"],
            [0.5, "#ffb74d"],
            [0.7, "#ff7043"],
            [1.0, "#ef5350"],
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
        title=dict(text="ESKAPEE Resistance Profile: Pathogen × Antibiotic Class", font=dict(size=15)),
        xaxis=dict(side="bottom", tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
        height=580,
        margin=dict(l=260, r=80, t=60, b=100),
    )

    return fig


def build_regional_chart():
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


def build_phenotype_legend():
    """Inline legend explaining MDR/XDR/PDR badges (Magiorakos 2012)."""
    badges = []
    for code, color in PHENOTYPE_COLORS.items():
        badges.append(html.Span(
            code,
            style={
                "background": color,
                "color": "#21232d",
                "padding": "0.15rem 0.55rem",
                "borderRadius": "4px",
                "fontSize": "0.7rem",
                "fontFamily": "JetBrains Mono, monospace",
                "fontWeight": "700",
                "marginRight": "0.4rem",
            },
        ))
    return html.Div(
        [
            html.Span("Phenotype legend (Magiorakos 2012, isolate-level): ",
                      className="source-label"),
            *badges,
            html.Span(
                "MDR = ≥1 agent in ≥3 classes · XDR = susceptible to ≤2 classes · "
                "PDR = resistant to all tested agents",
                style={"color": "#9aa0a6"},
            ),
        ],
        className="chart-sources",
    )


SVG_CONFIG = {
    "toImageButtonOptions": {"format": "svg", "scale": 3},
    "displayModeBar": True,
}


# ---------------------------------------------------------------------------
# Sensitivity Analysis panel — transient overrides (per-session, not persisted)
# ---------------------------------------------------------------------------
def build_sensitivity_panel():
    pathogen_options = [{"label": p, "value": i} for i, p in enumerate(PATHOGENS)]
    abx_options = [{"label": a.replace("\n", " "), "value": j}
                   for j, a in enumerate(ANTIBIOTIC_CLASSES)]

    return html.Div([
        chart_title_with_info(
            "Sensitivity Analysis (what-if mode)",
            "Override individual pathogen × antibiotic resistance values for sensitivity analysis. Defaults are anchored to peer-reviewed surveillance data; overrides are transient (reset on page reload) to preserve reproducibility.",
            "Transient cell-level overrides — peer-reviewed defaults preserved on reload",
        ),

        html.Div([
            html.Div([
                html.Label("Pathogen", style={"fontSize": "0.78rem", "color": "#9aa0a6", "display": "block", "marginBottom": "0.25rem"}),
                dcc.Dropdown(
                    id="sens-pathogen",
                    options=pathogen_options,
                    value=0,
                    clearable=False,
                    style={"width": "240px"},
                ),
            ], style={"flex": "0 0 auto"}),

            html.Div([
                html.Label("Antibiotic class", style={"fontSize": "0.78rem", "color": "#9aa0a6", "display": "block", "marginBottom": "0.25rem"}),
                dcc.Dropdown(
                    id="sens-antibiotic",
                    options=abx_options,
                    value=2,  # carbapenems by default
                    clearable=False,
                    style={"width": "240px"},
                ),
            ], style={"flex": "0 0 auto"}),

            html.Div([
                html.Label("% Resistant override (0–100)",
                           style={"fontSize": "0.78rem", "color": "#9aa0a6", "display": "block", "marginBottom": "0.25rem"}),
                dcc.Slider(
                    id="sens-value",
                    min=0, max=100, step=1, value=50,
                    marks={0: "0", 25: "25", 50: "50", 75: "75", 100: "100"},
                    tooltip={"placement": "top", "always_visible": False},
                ),
            ], style={"flex": "1 1 320px", "minWidth": "260px"}),

            html.Div([
                html.Button("Apply override", id="sens-apply", n_clicks=0,
                            style={
                                "background": "var(--accent-dim)",
                                "color": "var(--accent)",
                                "border": "1px solid var(--border)",
                                "padding": "0.5rem 1rem",
                                "borderRadius": "6px",
                                "fontSize": "0.82rem",
                                "fontWeight": "600",
                                "cursor": "pointer",
                                "marginRight": "0.5rem",
                            }),
                html.Button("Reset all", id="sens-reset", n_clicks=0,
                            style={
                                "background": "transparent",
                                "color": "var(--text-secondary)",
                                "border": "1px solid var(--border)",
                                "padding": "0.5rem 1rem",
                                "borderRadius": "6px",
                                "fontSize": "0.82rem",
                                "fontWeight": "600",
                                "cursor": "pointer",
                            }),
            ], style={"flex": "0 0 auto", "alignSelf": "flex-end"}),

        ], style={
            "display": "flex",
            "flexWrap": "wrap",
            "gap": "1rem",
            "alignItems": "flex-end",
            "marginTop": "0.5rem",
            "marginBottom": "0.75rem",
        }),

        html.Div(id="sens-status",
                 style={"fontSize": "0.78rem", "color": "#9aa0a6", "marginTop": "0.25rem"}),

        # Transient store (memory) — wiped on page reload by design
        dcc.Store(id="sens-overrides", storage_type="memory", data={}),

    ], className="card")


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------
@callback(
    Output("sens-overrides", "data"),
    Input("sens-apply", "n_clicks"),
    Input("sens-reset", "n_clicks"),
    State("sens-pathogen", "value"),
    State("sens-antibiotic", "value"),
    State("sens-value", "value"),
    State("sens-overrides", "data"),
    prevent_initial_call=True,
)
def update_overrides(_apply, _reset, p_idx, a_idx, val, overrides):
    overrides = dict(overrides or {})
    triggered = ctx.triggered_id
    if triggered == "sens-reset":
        return {}
    if triggered == "sens-apply" and p_idx is not None and a_idx is not None:
        # Refuse to override intrinsic-R cells (NaN) — preserves biological correctness
        if np.isnan(RESISTANCE_MATRIX[p_idx, a_idx]):
            return overrides
        overrides[f"{p_idx},{a_idx}"] = float(val)
    return overrides


@callback(
    Output("pathogen-heatmap", "figure"),
    Output("sens-status", "children"),
    Input("sens-overrides", "data"),
)
def render_heatmap(overrides):
    overrides = overrides or {}
    fig = build_heatmap(overrides)
    if not overrides:
        status = "Defaults active — 0 cells modified."
    else:
        status = (
            f"⚙ {len(overrides)} cell(s) modified vs literature defaults. "
            "Overrides reset on page reload (preserves reproducibility)."
        )
    return fig, status


layout = html.Div([
    help_section("Pathogens", [
        "ESKAPEE PATHOGENS: The ESKAPEE group — Enterococcus faecium, Staphylococcus aureus, Klebsiella pneumoniae, Acinetobacter baumannii, Pseudomonas aeruginosa, Enterobacter species, and Escherichia coli — are the leading causes of nosocomial (hospital-acquired) infections worldwide. The acronym was originally ESKAPE (paper UPDATE v.A-29 párr. 11 makes E. coli explicit, hence ESKAPEE). They 'escape' the effects of most available antibiotics through multiple resistance mechanisms. Together, these organisms account for the majority of multidrug-resistant infections in intensive care units and a disproportionate share of AMR-attributable mortality globally.",
        "STENOTROPHOMONAS MALTOPHILIA: Added to the heatmap per paper párr. 65 (PDR-Sm bloodstream infections, J Hosp Infect 2020). S. maltophilia is intrinsically resistant to most β-lactams (penicillins, 3rd-gen cephalosporins, carbapenems) due to its L1 metallo-β-lactamase and L2 cephalosporinase, and to aminoglycosides, vancomycin, and macrolides. It is therefore shown with many grey ('—') cells: those reflect biology, not missing data. The few treatable classes — TMP/SMX (~15% R), fluoroquinolones (~35% R), tetracyclines (~25% R) — are themselves losing efficacy in resistant isolates.",
        "WHO PRIORITY CLASSIFICATION: 'Critical' priority (red) includes carbapenem-resistant Acinetobacter, Pseudomonas, and Enterobacterales. 'High' priority (amber) includes vancomycin-resistant Enterococcus, MRSA, and others where resistance is widespread but some treatment alternatives exist. 'Medium' priority (blue) includes organisms like penicillin-non-susceptible Streptococcus pneumoniae. 'Special' priority (lavender) covers M. tuberculosis and S. maltophilia, which require their own surveillance frameworks.",
        "MDR / XDR / PDR PHENOTYPE BADGES (Magiorakos 2012): Each row is also labelled with the strongest documented isolate-level phenotype reported in peer-reviewed literature. MDR = non-susceptible to ≥1 agent in ≥3 antibiotic classes. XDR = susceptible to agents in ≤2 classes. PDR = resistant to all tested agents. CRITICAL: these classifications are isolate-level, not species-level — saying 'A. baumannii is PDR' is shorthand for 'PDR strains of A. baumannii are documented in the literature'. Most clinical isolates of any species are still susceptible to at least some drugs.",
        "INTRINSIC RESISTANCE (GREY CELLS): Cells displayed as a dash ('—') indicate intrinsic resistance — the organism is naturally resistant due to fundamental biology, not acquired mechanisms. Gram-negative bacteria are intrinsically resistant to vancomycin (drug cannot penetrate the outer membrane). S. maltophilia carries metallo-β-lactamases that hydrolyze every carbapenem. These cells are excluded from the colour scale because the resistance is not clinically meaningful in the same way as acquired resistance.",
        "SENSITIVITY ANALYSIS PANEL (research-mode what-if): Below the heatmap, a transient panel lets you override individual cell values to explore 'what if resistance for this pathogen-drug pair were X% instead?'. Defaults are anchored to peer-reviewed surveillance medians and are restored on every page reload — overrides are not persisted, by design, to preserve reproducibility for publication. The panel refuses to override intrinsic-R (NaN) cells: those reflect biology, not surveillance data, and forcing a number on them would be misleading.",
        "REGIONAL VARIATION: The grouped bar chart shows resistance rates across six WHO regions for four key pathogens. Geographic differences are driven by antibiotic access patterns (over-the-counter availability without prescription in many low- and middle-income countries), antimicrobial stewardship maturity, infection prevention practices, and surveillance capacity. Higher rates in Africa, South-East Asia, and the Eastern Mediterranean reflect both genuine higher burden and differential access to healthcare.",
        "TEMPORAL TRENDS: MRSA shows a declining trend in many regions (targeted screening, hand hygiene, decolonization protocols). 3GC-R E. coli and CRE K. pneumoniae show concerning upward trends, driven by ESBL and carbapenemase-producing genes (KPC, NDM, OXA-48) spreading via plasmid-mediated horizontal transfer. The divergent trajectories demonstrate that targeted interventions can work but must be sustained and adapted per pathogen.",
        "CLINICAL IMPLICATIONS: When resistance exceeds 10–20% for a pathogen-drug combination, guidelines typically recommend against using that drug for empiric therapy. Cells at 50%+ indicate the antibiotic class is unreliable for more than half of infections — clinicians must wait 48–72 h for culture results, during which patients receive suboptimal treatment. For Critical-priority pathogens with documented PDR phenotypes (A. baumannii, P. aeruginosa, K. pneumoniae, S. maltophilia), therapeutic options narrow to last-resort agents such as colistin (significant nephrotoxicity) or salvage combinations.",
    ]),

    # WHO Priority summary
    build_priority_summary(),

    # Heatmap (now reactive to overrides)
    html.Div([
        chart_title_with_info(
            "Resistance Heatmap",
            "Resistance percentage for each pathogen × antibiotic pair. Values are approximate global medians from WHO GLASS, ECDC EARS-Net, and CDC. Y-labels include WHO priority and Magiorakos isolate-level phenotype badge.",
            "Global median % resistant isolates — ESKAPEE + S. maltophilia + reference pathogens. Grey cells = intrinsic R or insufficient data.",
        ),
        dcc.Graph(id="pathogen-heatmap", figure=build_heatmap(), config=SVG_CONFIG),
        build_phenotype_legend(),
        html.Div([
            html.Span("Sources: ", className="source-label"),
            html.A("WHO GLASS Report 2022", href="https://www.who.int/publications/i/item/9789240062702", target="_blank"),
            " · ",
            html.A("ECDC EARS-Net", href="https://www.ecdc.europa.eu/en/antimicrobial-resistance/surveillance-and-disease-data/data-ecdc", target="_blank"),
            " · ",
            html.A("CDC AR Threats Report 2019", href="https://www.cdc.gov/antimicrobial-resistance/data-research/threats/index.html", target="_blank"),
            " · ",
            html.A("Murray et al., Lancet 2022", href="https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext", target="_blank"),
            " · ",
            html.A("Magiorakos et al., Clin Microbiol Infect 2012", href="https://www.clinicalmicrobiologyandinfection.com/article/S1198-743X(14)61632-3/fulltext", target="_blank"),
        ], className="chart-sources"),
    ], className="card"),

    # Sensitivity panel
    build_sensitivity_panel(),

    # Regional + Trends side by side
    html.Div([
        html.Div([
            chart_title_with_info(
                "Regional Variation",
                "Comparison of resistance rates across 6 WHO regions for 4 key pathogens. Higher rates in Africa, SE Asia, and E. Mediterranean.",
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
                "25-year resistance trajectories: MRSA shows decline (successful interventions); 3GC-R E. coli and CRE K. pneumoniae show concerning upward trends.",
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
                html.A("WHO GLASS", href="https://www.who.int/publications/i/item/9789240062702", className="source-tag", target="_blank"), " Global Antimicrobial Resistance Surveillance System (2022/2023 reports)",
            ], style={"marginBottom": "0.4rem"}),
            html.P([
                html.A("EARS-Net", href="https://www.ecdc.europa.eu/en/antimicrobial-resistance/surveillance-and-disease-data/data-ecdc", className="source-tag", target="_blank"), " European Antimicrobial Resistance Surveillance Network",
            ], style={"marginBottom": "0.4rem"}),
            html.P([
                html.A("Murray et al.", href="https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext", className="source-tag", target="_blank"), " Lancet 2022 — Global burden of bacterial AMR in 2019",
            ], style={"marginBottom": "0.4rem"}),
            html.P([
                html.A("Magiorakos 2012", href="https://www.clinicalmicrobiologyandinfection.com/article/S1198-743X(14)61632-3/fulltext", className="source-tag", target="_blank"), " MDR/XDR/PDR isolate-level definitions",
            ], style={"marginBottom": "0.4rem"}),
            html.P([
                html.A("CDC", href="https://www.cdc.gov/antimicrobial-resistance/data-research/threats/index.html", className="source-tag", target="_blank"), " Antibiotic Resistance Threats in the United States (2019/2022)",
            ]),
        ], style={"fontSize": "0.82rem", "color": "#9aa0a6"}),
    ], className="card"),
])
