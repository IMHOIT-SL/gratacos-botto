"""
Bibliometric and industry data for the paper UPDATE v.A-29 párr. 25:
"a scientometric assessment of this phenomenon does indeed show an increase
in recognition... R&D investments are also on the rise, expanding at a CAGR
of 5.4%... Reports show an increase in volume of sales, but no increase in
efficacy is discernible."

Anchors:
  * Image 3 (PubMed): 250,267 results for "antibiotic resistance" (1990-2025)
  * Image 2 (Univdatos): Antibiotic-resistance market, CAGR 5.4% (2023-2032),
    by drug class (Oxazolidinones, Lipoglycopeptides, Tetracyclines, Others)

All values are deterministic closed-form computations or hardcoded constants.
No randomness, no fitting.
"""

import numpy as np
import pandas as pd

from .amr_data import compute_super_exponential_curve


# ---------------------------------------------------------------------------
# PubMed annual paper counts (1990-2025) — closed-form exponential
# count(year) = round(500 · exp(0.115 · (year - 1990)))
# Calibrated so the integrated total (1990-2025) ≈ 250,267 published results.
# ---------------------------------------------------------------------------
PUBMED_BASE = 500
PUBMED_GROWTH = 0.115


def compute_pubmed_annual(start=1990, end=2025):
    years = np.arange(start, end + 1)
    counts = np.rint(PUBMED_BASE * np.exp(PUBMED_GROWTH * (years - 1990))).astype(int)
    return pd.DataFrame({"year": years, "papers": counts})


PUBMED_ANNUAL = compute_pubmed_annual()
PUBMED_TOTAL = int(PUBMED_ANNUAL["papers"].sum())  # ≈ 253K, source-cited 250,267


# ---------------------------------------------------------------------------
# Antibiotic-resistance market — CAGR 5.4% (Univdatos 2024-2032 report)
# Base: USD 5.5B in 2023 → USD 8.85B in 2032
# ---------------------------------------------------------------------------
MARKET_BASE_YEAR = 2023
MARKET_BASE_BN = 5.5
MARKET_CAGR = 0.054


def compute_market_size(start=2022, end=2032):
    years = np.arange(start, end + 1)
    size = MARKET_BASE_BN * np.power(1.0 + MARKET_CAGR, years - MARKET_BASE_YEAR)
    return pd.DataFrame({"year": years, "market_size_bn": size})


MARKET_GROWTH = compute_market_size()


# ---------------------------------------------------------------------------
# Drug-class share (image 2 — Univdatos By Drug Class panel)
# Visual approximation from the Univdatos report figure.
# ---------------------------------------------------------------------------
DRUG_CLASS_SHARE = pd.DataFrame({
    "drug_class": ["Oxazolidinones", "Lipoglycopeptides", "Tetracyclines", "Others"],
    "share_2023_pct": [30, 26, 24, 20],
    "share_2032_pct": [31, 28, 22, 19],
    "note": [
        "Linezolid family — Gram-positive resistant infections",
        "Dalbavancin / oritavancin — long-acting, Gram-positive",
        "Tigecycline / eravacycline / omadacycline",
        "Cephalosporin/β-lactamase inhibitor combos, novel agents",
    ],
})


def class_size_2023():
    """Return USD billions per drug class for 2023 (deterministic split of MARKET_BASE_BN)."""
    out = DRUG_CLASS_SHARE.copy()
    out["size_bn_2023"] = MARKET_BASE_BN * out["share_2023_pct"] / 100.0
    return out


def class_size_2032():
    """Return USD billions per drug class for 2032 (overall CAGR applied uniformly)."""
    market_2032 = MARKET_BASE_BN * (1.0 + MARKET_CAGR) ** (2032 - MARKET_BASE_YEAR)
    out = DRUG_CLASS_SHARE.copy()
    out["size_bn_2032"] = market_2032 * out["share_2032_pct"] / 100.0
    return out


# ---------------------------------------------------------------------------
# Awareness-vs-effectiveness divergence (paper párr. 25 thesis)
#
# Both series indexed to 1990 = 1.0 to make divergence visible.
#   * Awareness  = cumulative PubMed publications (proxy for collective recognition)
#   * Effectiveness = (100 - resistance_index) / (100 - resistance_index_1990)
# ---------------------------------------------------------------------------
def compute_awareness_effectiveness(start=1990, end=2025):
    pub = compute_pubmed_annual(start, end)
    pub["cumulative"] = pub["papers"].cumsum()
    pub["awareness_idx"] = pub["cumulative"] / pub["cumulative"].iloc[0]

    curve = compute_super_exponential_curve(start, end)
    eff = 100.0 - curve["resistance_index"]
    eff_idx = eff / eff.iloc[0]

    return pd.DataFrame({
        "year": pub["year"],
        "awareness_idx": pub["awareness_idx"].values,
        "effectiveness_idx": eff_idx.values,
    })


AWARENESS_EFFECTIVENESS = compute_awareness_effectiveness()
