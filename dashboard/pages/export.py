"""
Export Studio page — Preview and export every chart in the dashboard with
publication-ready themes (dark / light / bw).

All chart builders are deterministic and themed via the `theme` parameter.
"""

import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import numpy as np

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from components import help_section, chart_title_with_info
from data.amr_data import (
    compute_super_exponential_curve,
    compute_reference_logistic_curve,
    OBSERVED_DATA,
    MORTALITY_DATA,
    CARBAPENEM_PROJECTION,
)
from data.pathogen_data import (
    PATHOGENS,
    ANTIBIOTIC_CLASSES,
    RESISTANCE_MATRIX,
    WHO_PRIORITY,
    MDR_XDR_PDR,
    REGIONAL_DATA,
    TEMPORAL_TRENDS,
)
from data.bibliometrics_data import (
    PUBMED_ANNUAL,
    PUBMED_TOTAL,
    MARKET_GROWTH,
    MARKET_CAGR,
    MARKET_BASE_BN,
    MARKET_BASE_YEAR,
    DRUG_CLASS_SHARE,
    class_size_2023,
    class_size_2032,
    AWARENESS_EFFECTIVENESS,
)

dash.register_page(__name__, path="/export", name="Export")

# ---------------------------------------------------------------------------
# Selectable charts (grouped by source page)
# ---------------------------------------------------------------------------
CHART_OPTIONS = [
    {"label": "── Overview ──", "value": "_sep_ov", "disabled": True},
    {"label": "Resistance Pressure Trajectory (super-exp)", "value": "main_curve"},
    {"label": "Mortality Projections (Murray + Tai 2025)",  "value": "mortality"},
    {"label": "Carbapenem 2035 Spotlight (Tai 2025)",       "value": "carbapenem"},
    {"label": "── Pathogens ──", "value": "_sep_pa", "disabled": True},
    {"label": "ESKAPEE Resistance Heatmap",                 "value": "heatmap"},
    {"label": "Regional Variation",                         "value": "regional"},
    {"label": "Temporal Trends",                            "value": "trends"},
    {"label": "── Industry ──", "value": "_sep_in", "disabled": True},
    {"label": "PubMed Scientometric Trend",                 "value": "pubmed"},
    {"label": "Market Growth (CAGR 5.4%)",                  "value": "market"},
    {"label": "Drug Class Breakdown",                       "value": "drug_class"},
    {"label": "Awareness vs Effectiveness (divergence)",    "value": "divergence"},
    {"label": "── Metabolic ──", "value": "_sep_me", "disabled": True},
    {"label": "Paradigm Comparison (classical vs antimet.)","value": "paradigm"},
]

FORMAT_OPTIONS = [
    {"label": "SVG (vectorial — recommended for publications)", "value": "svg"},
    {"label": "PNG (raster — presentations & web)", "value": "png"},
]

SCALE_OPTIONS = [
    {"label": "1x (screen)", "value": 1},
    {"label": "2x (presentation)", "value": 2},
    {"label": "3x (publication 300 dpi)", "value": 3},
]

COLOR_SCHEME_OPTIONS = [
    {"label": "Dashboard Dark", "value": "dark"},
    {"label": "Publication Light", "value": "light"},
    {"label": "Print B&W", "value": "bw"},
]

# ---------------------------------------------------------------------------
# Color theme definitions
# ---------------------------------------------------------------------------
THEMES = {
    "dark": {
        "paper_bgcolor": "#21232d",
        "plot_bgcolor": "#21232d",
        "font_color": "#e8eaed",
        "gridcolor": "#2d2f3a",
        "accent1": "#4fc3f7",
        "accent2": "#ef5350",
        "accent3": "#ffb74d",
        "accent4": "#ce93d8",
        "accent5": "#66bb6a",
        "accent6": "#ff7043",
        "muted":   "#9aa0a6",
        "fill_alpha": 0.15,
        "bar_colors": {
            "attributable": "#ef5350",
            "associated": "#ffb74d",
        },
        "heatmap_colorscale": [
            [0, "#1a3a4a"], [0.3, "#4fc3f7"], [0.5, "#ffb74d"],
            [0.7, "#ff7043"], [1.0, "#ef5350"],
        ],
        "heatmap_text_color": "white",
        "annotation_color": "#ef5350",
    },
    "light": {
        "paper_bgcolor": "white",
        "plot_bgcolor": "white",
        "font_color": "black",
        "gridcolor": "#cccccc",
        "accent1": "#1565c0",
        "accent2": "#c62828",
        "accent3": "#e65100",
        "accent4": "#6a1b9a",
        "accent5": "#2e7d32",
        "accent6": "#bf360c",
        "muted":   "#666666",
        "fill_alpha": 0.12,
        "bar_colors": {
            "attributable": "#c62828",
            "associated": "#e65100",
        },
        "heatmap_colorscale": [
            [0, "#e3f2fd"], [0.3, "#42a5f5"], [0.5, "#ffa726"],
            [0.7, "#ef6c00"], [1.0, "#c62828"],
        ],
        "heatmap_text_color": "black",
        "annotation_color": "#c62828",
    },
    "bw": {
        "paper_bgcolor": "white",
        "plot_bgcolor": "white",
        "font_color": "black",
        "gridcolor": "#bbbbbb",
        "accent1": "#222222",
        "accent2": "#555555",
        "accent3": "#888888",
        "accent4": "#aaaaaa",
        "accent5": "#444444",
        "accent6": "#666666",
        "muted":   "#999999",
        "fill_alpha": 0.08,
        "bar_colors": {
            "attributable": "#333333",
            "associated": "#999999",
        },
        "heatmap_colorscale": [
            [0, "#f5f5f5"], [0.5, "#888888"], [1.0, "#111111"],
        ],
        "heatmap_text_color": "black",
        "annotation_color": "#333333",
    },
}


def _hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return ", ".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def _base_layout(theme):
    return dict(
        paper_bgcolor=theme["paper_bgcolor"],
        plot_bgcolor=theme["plot_bgcolor"],
        font=dict(color=theme["font_color"], family="Inter, sans-serif", size=12),
    )


# ---------------------------------------------------------------------------
# Chart builders
# ---------------------------------------------------------------------------

def build_main_curve(theme):
    """AMR resistance super-exponential curve + reference logistic + ±3y band."""
    curve = compute_super_exponential_curve()
    ref = compute_reference_logistic_curve()
    fig = go.Figure()

    # ±3 year envelope
    fig.add_trace(go.Scatter(
        x=curve["year"], y=curve["upper_bound"],
        mode="lines", line=dict(width=0),
        showlegend=False, hoverinfo="skip",
    ))
    fill_rgba = f"rgba({_hex_to_rgb(theme['accent1'])}, {theme['fill_alpha']})"
    fig.add_trace(go.Scatter(
        x=curve["year"], y=curve["lower_bound"],
        mode="lines", line=dict(width=0),
        fill="tonexty", fillcolor=fill_rgba,
        name="Uncertainty band (±3 yrs)", hoverinfo="skip",
    ))

    # Reference logistic
    fig.add_trace(go.Scatter(
        x=ref["year"], y=ref["resistance_index"],
        mode="lines",
        line=dict(color=theme["muted"], width=1.5, dash="dot"),
        name="Constant-rate logistic (limit of V=S·(1+r)ᵀ)",
        opacity=0.7,
    ))

    # Observed segment
    obs = curve[curve["year"] <= 2025]
    fig.add_trace(go.Scatter(
        x=obs["year"], y=obs["resistance_index"],
        mode="lines",
        line=dict(color=theme["accent1"], width=3),
        name="Observed (1990–2025)",
    ))

    # Forecast segment
    fcast = curve[curve["year"] >= 2025]
    fig.add_trace(go.Scatter(
        x=fcast["year"], y=fcast["resistance_index"],
        mode="lines",
        line=dict(color=theme["accent2"], width=3, dash="dash"),
        name="Super-exponential forecast (Gratacós-Botto)",
    ))

    # Anchor markers
    fig.add_trace(go.Scatter(
        x=OBSERVED_DATA["year"], y=OBSERVED_DATA["resistance_index"],
        mode="markers",
        marker=dict(color=theme["accent1"], size=8, symbol="circle",
                    line=dict(color=theme["paper_bgcolor"], width=1.5)),
        name="Published data points",
    ))

    fig.add_hline(
        y=95, line_dash="dot", line_color=theme["annotation_color"], line_width=1,
        annotation_text="Critical inefficacy threshold (~95)",
        annotation_position="top left",
        annotation_font=dict(color=theme["annotation_color"], size=11),
    )
    fig.add_vrect(
        x0=2040, x1=2047,
        fillcolor=f"rgba({_hex_to_rgb(theme['accent2'])}, 0.10)",
        line_width=0,
        annotation_text="Critical Point (2040–2047)",
        annotation_position="top",
        annotation_font=dict(color=theme["annotation_color"], size=11),
    )

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="AMR Resistance Pressure Index (1990–2060) — Super-exponential model",
                   font=dict(size=15)),
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"], zerolinecolor=theme["gridcolor"]),
        yaxis_title="Resistance Pressure Index (0–100)",
        yaxis=dict(range=[0, 105], gridcolor=theme["gridcolor"], zerolinecolor=theme["gridcolor"]),
        height=520,
        margin=dict(l=60, r=30, t=50, b=50),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    return fig


def build_mortality(theme):
    """Murray/GRAM/O'Neill stacked + Tai 2025 overlay."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=MORTALITY_DATA["year"],
        y=MORTALITY_DATA["attributable_deaths_k"],
        name="Attributable (GRAM/O'Neill)",
        marker_color=theme["bar_colors"]["attributable"],
    ))
    fig.add_trace(go.Bar(
        x=MORTALITY_DATA["year"],
        y=MORTALITY_DATA["associated_deaths_k"] - MORTALITY_DATA["attributable_deaths_k"],
        name="Associated (additional)",
        marker_color=theme["bar_colors"]["associated"],
    ))
    fig.add_trace(go.Scatter(
        x=MORTALITY_DATA["year"],
        y=MORTALITY_DATA["tai_2025_deaths_k"],
        mode="lines+markers",
        line=dict(color=theme["accent1"], width=2.5, dash="dash"),
        marker=dict(size=7, symbol="diamond"),
        name="Tai 2025 (GBD-hierarchical)",
    ))

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Projected AMR Mortality (thousands/year)", font=dict(size=14)),
        barmode="stack",
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"], zerolinecolor=theme["gridcolor"]),
        yaxis_title="Deaths (thousands)",
        yaxis=dict(gridcolor=theme["gridcolor"], zerolinecolor=theme["gridcolor"]),
        height=400,
        margin=dict(l=60, r=30, t=50, b=50),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    return fig


def build_carbapenem(theme):
    """Carbapenem-resistant mortality stacked area through 2035 (Tai 2025)."""
    df = CARBAPENEM_PROJECTION
    fig = go.Figure()

    series_palette = [
        ("CRE",  "CRE (Enterobacterales)",   theme["accent2"]),
        ("CRAB", "CRAB (A. baumannii)",      theme["accent6"]),
        ("CRPA", "CRPA (P. aeruginosa)",     theme["accent3"]),
    ]
    for col, label, color in series_palette:
        fill_rgba = f"rgba({_hex_to_rgb(color)}, 0.45)"
        fig.add_trace(go.Scatter(
            x=df["year"], y=df[col],
            mode="lines+markers",
            name=label,
            stackgroup="carba",
            line=dict(color=color, width=0.5),
            marker=dict(size=6, color=color,
                        line=dict(color=theme["paper_bgcolor"], width=1)),
            fillcolor=fill_rgba,
        ))

    fig.add_vline(
        x=2025, line_dash="dot", line_color=theme["muted"], line_width=1,
        annotation_text="Forecast →",
        annotation_position="top",
        annotation_font=dict(color=theme["muted"], size=10),
    )
    fig.add_vline(
        x=2035, line_dash="dot", line_color=theme["annotation_color"], line_width=1,
        annotation_text="Tai 2025 horizon",
        annotation_position="top",
        annotation_font=dict(color=theme["annotation_color"], size=10),
    )

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Carbapenem-Resistance Mortality (CRE + CRAB + CRPA) — through 2035",
                   font=dict(size=14)),
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"], zerolinecolor=theme["gridcolor"]),
        yaxis_title="Deaths/yr (thousands, stacked)",
        yaxis=dict(gridcolor=theme["gridcolor"], zerolinecolor=theme["gridcolor"]),
        height=400,
        margin=dict(l=60, r=30, t=50, b=50),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    return fig


def build_heatmap(theme):
    """ESKAPEE pathogen × antibiotic resistance heatmap."""
    hover_text, display_text = [], []
    for i, pathogen in enumerate(PATHOGENS):
        hover_row, display_row = [], []
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

    y_labels = [f"{p}  [{WHO_PRIORITY[p]} · {MDR_XDR_PDR.get(p, '')}]" for p in PATHOGENS]

    fig = go.Figure(data=go.Heatmap(
        z=RESISTANCE_MATRIX,
        x=ANTIBIOTIC_CLASSES,
        y=y_labels,
        text=display_text,
        texttemplate="%{text}",
        textfont=dict(size=11, color=theme["heatmap_text_color"]),
        hovertext=hover_text,
        hovertemplate="%{hovertext}<extra></extra>",
        colorscale=theme["heatmap_colorscale"],
        zmin=0, zmax=100,
        colorbar=dict(title=dict(text="% Resistant", font=dict(size=11)),
                      ticksuffix="%", len=0.9),
        xgap=2, ygap=2,
    ))

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="ESKAPEE Resistance Profile: Pathogen × Antibiotic Class",
                   font=dict(size=15)),
        xaxis=dict(side="bottom", tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
        height=580,
        margin=dict(l=260, r=80, t=60, b=100),
    )
    return fig


def build_regional(theme):
    fig = go.Figure()
    pathogens_in_data = REGIONAL_DATA["pathogen"].unique()
    color_map = {
        "K. pneumoniae": theme["accent2"],
        "E. coli": theme["accent1"],
        "S. aureus (MRSA)": theme["accent3"],
        "A. baumannii": theme["accent4"],
    }

    for pathogen in pathogens_in_data:
        subset = REGIONAL_DATA[REGIONAL_DATA["pathogen"] == pathogen]
        fig.add_trace(go.Bar(
            x=subset["region"], y=subset["resistance_index"],
            name=pathogen,
            marker_color=color_map.get(pathogen, theme["accent5"]),
        ))

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Regional Resistance (key pathogens)", font=dict(size=14)),
        barmode="group",
        xaxis_title="WHO Region",
        xaxis=dict(gridcolor=theme["gridcolor"]),
        yaxis_title="% Resistant Isolates",
        yaxis=dict(range=[0, 100], gridcolor=theme["gridcolor"]),
        height=400,
        margin=dict(l=60, r=30, t=50, b=60),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    )
    return fig


def build_trends(theme):
    fig = go.Figure()
    color_map = {
        "MRSA": theme["accent3"],
        "3GC-R E. coli": theme["accent1"],
        "CRE K. pneumoniae": theme["accent2"],
    }
    for phenotype in TEMPORAL_TRENDS["phenotype"].unique():
        subset = TEMPORAL_TRENDS[TEMPORAL_TRENDS["phenotype"] == phenotype]
        fig.add_trace(go.Scatter(
            x=subset["year"], y=subset["prevalence"],
            mode="lines+markers",
            name=phenotype,
            line=dict(color=color_map.get(phenotype, theme["accent5"]), width=2.5),
            marker=dict(size=4),
        ))

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Resistance Trends (2000–2025): Key Phenotypes", font=dict(size=14)),
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"]),
        yaxis_title="% Resistant",
        yaxis=dict(range=[0, 60], gridcolor=theme["gridcolor"]),
        height=400,
        margin=dict(l=60, r=30, t=50, b=50),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    )
    return fig


def build_pubmed(theme):
    """Annual PubMed publications for 'antibiotic resistance' 1990-2025."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=PUBMED_ANNUAL["year"], y=PUBMED_ANNUAL["papers"],
        marker_color=theme["accent1"],
        marker_line=dict(color=theme["paper_bgcolor"], width=0.5),
        name="Annual papers",
    ))
    fig.update_layout(
        **_base_layout(theme),
        title=dict(text=f'PubMed: "antibiotic resistance" — {PUBMED_TOTAL:,} cumulative results',
                   font=dict(size=14)),
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"]),
        yaxis_title="Annual publications",
        yaxis=dict(gridcolor=theme["gridcolor"]),
        height=400,
        margin=dict(l=60, r=30, t=50, b=50),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    return fig


def build_market(theme):
    fig = go.Figure()
    fill_rgba = f"rgba({_hex_to_rgb(theme['accent3'])}, 0.10)"
    fig.add_trace(go.Scatter(
        x=MARKET_GROWTH["year"], y=MARKET_GROWTH["market_size_bn"],
        mode="lines+markers",
        line=dict(color=theme["accent3"], width=3, shape="spline"),
        marker=dict(size=7, color=theme["accent3"],
                    line=dict(color=theme["paper_bgcolor"], width=1.5)),
        fill="tozeroy", fillcolor=fill_rgba,
        name=f"Market size (CAGR {MARKET_CAGR*100:.1f}%)",
    ))

    fig.add_annotation(
        x=MARKET_BASE_YEAR, y=MARKET_BASE_BN,
        text=f"Base ${MARKET_BASE_BN:.1f}B",
        showarrow=True, arrowhead=2, arrowcolor=theme["accent3"],
        bgcolor=theme["paper_bgcolor"], bordercolor=theme["gridcolor"], borderwidth=1,
        font=dict(color=theme["accent3"], size=11),
        ax=-30, ay=-40,
    )
    end = MARKET_GROWTH.iloc[-1]
    fig.add_annotation(
        x=int(end["year"]), y=float(end["market_size_bn"]),
        text=f"${end['market_size_bn']:.2f}B by {int(end['year'])}",
        showarrow=True, arrowhead=2, arrowcolor=theme["accent3"],
        bgcolor=theme["paper_bgcolor"], bordercolor=theme["gridcolor"], borderwidth=1,
        font=dict(color=theme["accent3"], size=11),
        ax=-50, ay=-30,
    )

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text=f"Global Antibiotic-Resistance Market — CAGR {MARKET_CAGR*100:.1f}%",
                   font=dict(size=14)),
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"]),
        yaxis_title="Market size (USD billions)",
        yaxis=dict(gridcolor=theme["gridcolor"]),
        height=400,
        margin=dict(l=60, r=30, t=50, b=50),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    return fig


def build_drug_class(theme):
    df_23 = class_size_2023()
    df_32 = class_size_2032()
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_23["drug_class"], y=df_23["size_bn_2023"],
        name="2023",
        marker_color=theme["accent1"],
        text=[f"${v:.2f}B" for v in df_23["size_bn_2023"]],
        textposition="outside",
        textfont=dict(color=theme["font_color"], size=11),
    ))
    fig.add_trace(go.Bar(
        x=df_32["drug_class"], y=df_32["size_bn_2032"],
        name="2032",
        marker_color=theme["accent2"],
        text=[f"${v:.2f}B" for v in df_32["size_bn_2032"]],
        textposition="outside",
        textfont=dict(color=theme["font_color"], size=11),
    ))

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Market by Drug Class — 2023 vs 2032 (USD bn)", font=dict(size=14)),
        barmode="group",
        xaxis_title="",
        xaxis=dict(gridcolor=theme["gridcolor"]),
        yaxis_title="USD billions",
        yaxis=dict(gridcolor=theme["gridcolor"]),
        height=400,
        margin=dict(l=60, r=30, t=50, b=50),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    fig.update_yaxes(range=[0, 3.2])
    return fig


def build_divergence(theme):
    df = AWARENESS_EFFECTIVENESS
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["year"], y=df["awareness_idx"],
        mode="lines",
        line=dict(color=theme["accent1"], width=3),
        name="Scientometric awareness (cumulative PubMed)",
    ))
    fig.add_trace(go.Scatter(
        x=df["year"], y=df["effectiveness_idx"],
        mode="lines",
        line=dict(color=theme["accent2"], width=3, dash="dash"),
        name="Therapeutic effectiveness (100 − resistance index)",
    ))
    fig.add_hline(
        y=1.0, line_dash="dot", line_color=theme["muted"], line_width=1,
        annotation_text="1990 baseline",
        annotation_position="bottom right",
        annotation_font=dict(color=theme["muted"], size=10),
    )

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Awareness vs Effectiveness — divergence (1990 = 1.0)",
                   font=dict(size=14)),
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"]),
        yaxis_title="Index (log scale, 1990 = 1.0)",
        yaxis=dict(gridcolor=theme["gridcolor"]),
        height=420,
        margin=dict(l=60, r=30, t=50, b=50),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    fig.update_yaxes(type="log")
    return fig


def build_paradigm(theme):
    """Paradigm comparison — classical curve + qualitative antimetabolic band."""
    curve = compute_super_exponential_curve(1990, 2060)
    classical_eff = 100.0 - curve["resistance_index"]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=curve["year"], y=classical_eff,
        mode="lines",
        line=dict(color=theme["accent2"], width=3),
        name="Classical antibiotic effectiveness (data-driven)",
    ))

    years = curve["year"].values
    upper = [None if y < 2025 else 75 for y in years]
    lower = [None if y < 2025 else 55 for y in years]
    fig.add_trace(go.Scatter(
        x=years, y=upper, mode="lines", line=dict(width=0),
        showlegend=False, hoverinfo="skip",
    ))
    band_rgba = f"rgba({_hex_to_rgb(theme['accent1'])}, 0.18)"
    fig.add_trace(go.Scatter(
        x=years, y=lower, mode="lines", line=dict(width=0),
        fill="tonexty", fillcolor=band_rgba,
        name="Antimetabolic hypothesis (qualitative — not a forecast)",
        hoverinfo="skip",
    ))

    fig.add_vline(
        x=2026, line_dash="dot", line_color=theme["muted"], line_width=1,
        annotation_text="2026 (paper context)",
        annotation_position="top",
        annotation_font=dict(color=theme["muted"], size=10),
    )

    fig.update_layout(
        **_base_layout(theme),
        title=dict(text="Paradigm comparison — classical vs antimetabolic (conceptual)",
                   font=dict(size=14)),
        xaxis_title="Year",
        xaxis=dict(gridcolor=theme["gridcolor"]),
        yaxis_title="Therapeutic effectiveness (100 = full)",
        yaxis=dict(gridcolor=theme["gridcolor"]),
        height=420,
        margin=dict(l=60, r=30, t=50, b=80),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        annotations=[
            dict(
                xref="paper", yref="paper", x=0.5, y=-0.27,
                showarrow=False,
                text=("⚠ The shaded band is a qualitative working-hypothesis envelope, "
                      "not a quantitative forecast."),
                font=dict(color=theme["accent3"], size=11),
                xanchor="center",
            ),
        ],
    )
    fig.update_yaxes(range=[0, 100])
    return fig


CHART_BUILDERS = {
    "main_curve": build_main_curve,
    "mortality":  build_mortality,
    "carbapenem": build_carbapenem,
    "heatmap":    build_heatmap,
    "regional":   build_regional,
    "trends":     build_trends,
    "pubmed":     build_pubmed,
    "market":     build_market,
    "drug_class": build_drug_class,
    "divergence": build_divergence,
    "paradigm":   build_paradigm,
}

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

layout = html.Div([
    help_section("Export Studio", [
        "FORMAT SELECTION -- SVG VS PNG VS PDF: SVG (Scalable Vector Graphics) is recommended for journal submissions and any context where the figure may be resized. SVG files are resolution-independent, produce crisp text and lines at any zoom level, and are accepted by most major publishers (Nature, Lancet, PLOS, BMJ, JAMA). PNG is best for presentations and web; use 2x or 3x scale for clarity. For PDF, export as SVG and convert with Inkscape (free) or Adobe Illustrator.",
        "RESOLUTION GUIDE: 1x is screen-only. 2x (~150 dpi) is appropriate for slide presentations, posters, and internal reports. 3x (~300 dpi) meets the minimum for print publication in peer-reviewed journals. When in doubt, export at 3x.",
        "COLOR THEME GUIDE: 'Dashboard Dark' is for on-screen analysis only — not for publication. 'Publication Light' uses a white background with high-contrast publication colors — recommended for journal submission, reports, and supplementary files. 'Print B&W' uses a white background with grayscale-only encoding for journals that print B&W or charge extra for color.",
        "AVAILABLE CHARTS — 11 total, grouped by source page: Overview (Resistance Trajectory super-exp, Mortality with Tai 2025 overlay, Carbapenem 2035 Spotlight); Pathogens (ESKAPEE Heatmap, Regional Variation, Temporal Trends); Industry (PubMed Scientometric, Market Growth CAGR 5.4%, Drug Class Breakdown, Awareness vs Effectiveness divergence); Metabolic (Paradigm Comparison classical-vs-antimetabolic). Each chart respects the selected color theme.",
        "POST-PROCESSING SVG EXPORTS: Open in Adobe Illustrator, Inkscape, or Affinity Designer to fine-tune. Common tasks: adjust font sizes, reposition legends, add annotations, combine panels into a composite figure, convert text to outlines.",
        "CITING THE DASHBOARD: Suggested citation: 'Figure generated using the AMR Research Dashboard (Gratacós-Botto, paper UPDATE v.A-29), based on data from [list relevant primary sources for the chart].' Each Overview/Pathogens/Industry chart lists its specific data sources below the visualization on the source page.",
    ]),

    # Controls
    html.Div([
        chart_title_with_info(
            "Export Studio",
            "Configure chart appearance and export settings. 11 charts available, 3 themes (dark/light/bw), 2 formats (SVG/PNG), 3 resolutions (1x/2x/3x).",
            "Preview charts with publication-ready color schemes, then export via the Plotly modebar.",
        ),
        html.Div([
            html.Div([
                html.Label("Chart", style={"fontWeight": "600", "marginBottom": "0.3rem", "display": "block"}),
                dcc.Dropdown(
                    id="export-chart-select",
                    options=CHART_OPTIONS,
                    value="main_curve",
                    clearable=False,
                    style={"backgroundColor": "#2d2f3a", "color": "#e8eaed", "minWidth": "260px"},
                ),
            ], style={"flex": "2", "minWidth": "280px"}),
            html.Div([
                html.Label("Color Scheme", style={"fontWeight": "600", "marginBottom": "0.3rem", "display": "block"}),
                dcc.Dropdown(
                    id="export-color-scheme",
                    options=COLOR_SCHEME_OPTIONS,
                    value="dark",
                    clearable=False,
                    style={"backgroundColor": "#2d2f3a", "color": "#e8eaed", "minWidth": "180px"},
                ),
            ], style={"flex": "1", "minWidth": "180px"}),
            html.Div([
                html.Label("Format", style={"fontWeight": "600", "marginBottom": "0.3rem", "display": "block"}),
                dcc.RadioItems(
                    id="export-format",
                    options=FORMAT_OPTIONS,
                    value="svg",
                    inline=True,
                    inputStyle={"marginRight": "4px"},
                    labelStyle={"marginRight": "14px", "cursor": "pointer", "color": "#e8eaed"},
                ),
            ], style={"flex": "0 0 auto"}),
            html.Div([
                html.Label("Resolution", style={"fontWeight": "600", "marginBottom": "0.3rem", "display": "block"}),
                dcc.RadioItems(
                    id="export-scale",
                    options=SCALE_OPTIONS,
                    value=2,
                    inline=True,
                    inputStyle={"marginRight": "4px"},
                    labelStyle={"marginRight": "14px", "cursor": "pointer", "color": "#e8eaed"},
                ),
            ], style={"flex": "0 0 auto"}),
        ], style={
            "display": "flex",
            "flexWrap": "wrap",
            "gap": "1.2rem",
            "alignItems": "flex-end",
            "marginTop": "1rem",
        }),
    ], className="card"),

    # Preview
    html.Div([
        chart_title_with_info(
            "Preview",
            "Live preview of the selected chart with your chosen color scheme. Click Download Chart below to export.",
            "The chart below reflects your selected color scheme. Use the Download Chart button to save in your chosen format and resolution.",
        ),
        dcc.Graph(
            id="export-preview",
            config={
                "displayModeBar": True,
                "toImageButtonOptions": {"format": "svg", "scale": 2},
            },
        ),
        html.Div([
            html.Button(
                "Download Chart",
                id="btn-download-chart",
                style={
                    "background": "linear-gradient(135deg, #4fc3f7, #0288d1)",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "8px",
                    "padding": "0.75rem 2rem",
                    "fontSize": "1rem",
                    "fontWeight": "700",
                    "cursor": "pointer",
                    "letterSpacing": "0.03em",
                    "boxShadow": "0 2px 8px rgba(79, 195, 247, 0.3)",
                    "transition": "all 0.2s ease",
                },
            ),
            html.Span(
                id="download-status",
                style={"marginLeft": "1rem", "fontSize": "0.88rem", "color": "#9aa0a6"},
            ),
        ], style={"marginTop": "1rem", "display": "flex", "alignItems": "center"}),
    ], className="card"),

    # Instructions
    html.Div([
        html.H3("Export Instructions", className="card-title"),
        html.Div([
            html.Ol([
                html.Li("Select the chart, color scheme, format, and resolution above."),
                html.Li([
                    "Click ", html.Strong("Download Chart"),
                    " to save. You can also use the camera icon in the chart toolbar.",
                ]),
                html.Li([
                    html.Strong("SVG (recommended for publications): "),
                    "Vectorial, infinite resolution, editable in Illustrator/Inkscape. Accepted by all major journals.",
                ]),
                html.Li([
                    html.Strong("PNG: "),
                    "Raster image. Use 3x scale for print-quality 300 dpi. Good for presentations and web.",
                ]),
                html.Li([
                    html.Strong("Need PDF? "),
                    "Export as SVG, then convert: open in Inkscape → File → Save as PDF. Or use ",
                    html.Code("cairosvg input.svg -o output.pdf"),
                    " from the command line.",
                ]),
                html.Li([
                    "For publication, choose ", html.Strong("Publication Light"),
                    " or ", html.Strong("Print B&W"),
                    " theme with ", html.Strong("3x resolution"), ".",
                ]),
            ], style={"color": "#9aa0a6", "fontSize": "0.88rem", "lineHeight": "1.7"}),
        ]),
    ], className="card"),
])


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@callback(
    Output("export-preview", "figure"),
    Input("export-chart-select", "value"),
    Input("export-color-scheme", "value"),
)
def update_preview(chart_name, color_scheme):
    theme = THEMES.get(color_scheme, THEMES["dark"])
    builder = CHART_BUILDERS.get(chart_name, build_main_curve)
    fig = builder(theme)
    return fig
