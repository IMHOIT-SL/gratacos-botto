"""
AMR data sources and computations.
Anchored to 10+ published sources (Lancet GBD, O'Neill, GRAM, CIDRAP, Tai 2025).

Two deterministic models are exposed:
  * compute_sigmoid_curve()           — interpolated piecewise (legacy reference)
  * compute_super_exponential_curve() — closed-form analytic curve, primary
                                        model of the Gratacós-Botto thesis
                                        (paper UPDATE v.A-29 párr. 22):
                                        "the rate of increasing resistance is
                                        itself growing".

The super-exponential form has a time-quadratic term in the exponent
(-r·τ - b·τ²) so the effective rate r_eff(τ) = r + 2·b·τ grows linearly
with τ, advancing the critical-ineffectiveness point relative to a
constant-rate logistic.

All coefficients are hardcoded (no fitting, no random sampling). 100% reproducible.
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Published anchor points (observed segment, 1990-2025)
# ---------------------------------------------------------------------------
OBSERVED_DATA = pd.DataFrame({
    "year": [1990, 1995, 2000, 2005, 2010, 2015, 2019, 2021, 2025],
    "resistance_index": [12, 18, 23, 28, 35, 45, 58, 63, 70],
    "lower_bound": [8, 13, 18, 22, 28, 38, 52, 56, 63],
    "upper_bound": [16, 23, 28, 34, 42, 52, 64, 70, 77],
    "source": [
        "Oxford VG baseline",
        "Oxford VG baseline",
        "Oxford VG (MRSA/ESBL era)",
        "Oxford VG",
        "Lancet GBD",
        "Lancet GBD (CRE/XDR-TB rise)",
        "Murray et al. 2022 (1.27M deaths)",
        "Lancet GBD update",
        "CIDRAP/GRAM projection",
    ],
})


# ---------------------------------------------------------------------------
# Forecast anchor points (recalibrated to paper UPDATE v.A-29 párr. 19)
#   2025–2032: 70 → 80
#   2033–2040: → 90
#   2040–2047: → 95–98 (CRITICAL POINT, 14 ± 3 yrs from 2026)
#   2045–2060: → ~100
# ---------------------------------------------------------------------------
FORECAST_DATA = pd.DataFrame({
    "year": [2025, 2032, 2040, 2047, 2050, 2055, 2060],
    "resistance_index": [70, 80, 90, 96, 97.5, 98.5, 99],
    "lower_bound": [63, 73, 84, 91, 93, 94, 95],
    "upper_bound": [77, 87, 95, 99, 99.5, 99.8, 99.9],
    "source": [
        "CIDRAP/GRAM",
        "Gratacós-Botto v.A-29 (párr. 19)",
        "Gratacós-Botto v.A-29 (párr. 19)",
        "Gratacós-Botto v.A-29 (critical point)",
        "O'Neill 10M deaths/yr",
        "Extrapolation",
        "Asymptotic",
    ],
})


# ---------------------------------------------------------------------------
# Mortality projections (deaths per year, thousands)
#   * Murray 2022 (Lancet GBD)        — historical 2019 baseline
#   * GRAM/O'Neill                    — high-end trajectory
#   * Tai et al. 2025 (Int J Antimicrob Ag) — conservative GBD-hierarchical
#     (paper párr. 9: "~1.91M annual deaths by 2040")
# ---------------------------------------------------------------------------
MORTALITY_DATA = pd.DataFrame({
    "year": [2019, 2025, 2030, 2035, 2040, 2045, 2050],
    "attributable_deaths_k": [1270, 1500, 2100, 3200, 5000, 7200, 10000],
    "associated_deaths_k": [4950, 5800, 7500, 9500, 12000, 14500, 17000],
    "tai_2025_deaths_k": [1270, 1380, 1520, 1700, 1910, 2150, 2400],
    "source": [
        "Murray et al. Lancet 2022",
        "GRAM projection",
        "GRAM projection",
        "GRAM/O'Neill interpolation",
        "GRAM/O'Neill + Tai 2025",
        "O'Neill trajectory",
        "O'Neill Review (10M target)",
    ],
})


# ---------------------------------------------------------------------------
# Super-exponential model (deterministic closed form)
# ---------------------------------------------------------------------------
# y(τ) = K / (1 + A · exp(-r·τ - b·τ²))   with τ = year - 1990
#
# Coefficients hand-calibrated to the paper's milestones:
#   τ=0  (1990) → 12     τ=35 (2025) → 70
#   τ=42 (2032) → 80     τ=50 (2040) → 90
#   τ=57 (2047) → 96     τ=70 (2060) → 99
SUPER_EXP_PARAMS = dict(
    K=100.0,
    A=88.0 / 12.0,       # ≈ 7.3333  (sets y(1990)=12)
    r=0.0705,            # base rate
    b=3.05e-4,           # super-exponential acceleration: r_eff grows ~2bτ/yr
    t0=1990,
)

# Reference (constant-r) logistic — same K, A; b=0 — for visual comparison.
# Calibrated so y(1990)=12 and y(2025)=70 with b=0 only.
#   r' = ln((K-y0)/y0 / ((K-y(τ))/y(τ))) / τ
#      = ln((88/12) / (30/70)) / 35 = ln(17.111) / 35 ≈ 0.0811
REFERENCE_LOGISTIC_PARAMS = dict(
    K=100.0,
    A=88.0 / 12.0,
    r=0.0811,
    b=0.0,
    t0=1990,
)


def _generalized_logistic(years, K, A, r, b, t0):
    """Closed-form deterministic logistic with optional super-exp acceleration."""
    tau = np.asarray(years, dtype=float) - t0
    expo = -r * tau - b * tau * tau
    return K / (1.0 + A * np.exp(expo))


def compute_super_exponential_curve(start=1990, end=2060):
    """
    Primary model — Gratacós-Botto super-exponential thesis.
    100% deterministic (no fitting, no randomness).
    """
    years = np.arange(start, end + 1)
    y = _generalized_logistic(years, **SUPER_EXP_PARAMS)

    # Uncertainty envelope: ±3 years of trajectory shift (paper: 14 ± 3 yrs)
    upper = _generalized_logistic(years + 3, **SUPER_EXP_PARAMS)
    lower = _generalized_logistic(years - 3, **SUPER_EXP_PARAMS)

    return pd.DataFrame({
        "year": years,
        "resistance_index": y,
        "lower_bound": lower,
        "upper_bound": upper,
    })


def compute_reference_logistic_curve(start=1990, end=2060):
    """Reference (constant-r) logistic — for visual comparison only."""
    years = np.arange(start, end + 1)
    y = _generalized_logistic(years, **REFERENCE_LOGISTIC_PARAMS)
    return pd.DataFrame({"year": years, "resistance_index": y})


# ---------------------------------------------------------------------------
# Carbapenem-resistance trajectory through 2035
# Anchored to:
#   * Murray et al. Lancet 2022 — ~140K carbapenem-resistant deaths in 2019
#   * Tai et al. IJAA 2025 (paper ref 10, párr. 9) —
#     "carbapenem-resistant deaths are projected to escalate sharply by 2035
#      even as overall age-standardized mortality declines"
#   * Pathogen split (CRE / CRAB / CRPA) approximated from GBD AMR breakdown
#
# Numbers below are deterministic anchor points (deaths per year, thousands).
# Hardcoded — no random sampling, no fitting.
# ---------------------------------------------------------------------------
CARBAPENEM_PROJECTION = pd.DataFrame({
    "year":   [2010, 2015, 2019, 2021, 2025, 2030, 2035],
    "CRE":    [25,   45,   70,   80,   105,  150,  200],   # Enterobacterales
    "CRAB":   [20,   30,   45,   50,    65,   90,  115],   # A. baumannii
    "CRPA":   [15,   22,   30,   35,    45,   62,   80],   # P. aeruginosa
})


def compute_sigmoid_curve(start=1990, end=2060):
    """Legacy piecewise interpolation — kept for backward compatibility."""
    years = np.arange(start, end + 1)
    n = len(years)

    resistance = np.zeros(n)
    lower = np.zeros(n)
    upper = np.zeros(n)

    for i, y in enumerate(years):
        if y <= 2025:
            resistance[i] = np.interp(y, OBSERVED_DATA["year"], OBSERVED_DATA["resistance_index"])
            lower[i] = np.interp(y, OBSERVED_DATA["year"], OBSERVED_DATA["lower_bound"])
            upper[i] = np.interp(y, OBSERVED_DATA["year"], OBSERVED_DATA["upper_bound"])
        else:
            resistance[i] = np.interp(y, FORECAST_DATA["year"], FORECAST_DATA["resistance_index"])
            lower[i] = np.interp(y, FORECAST_DATA["year"], FORECAST_DATA["lower_bound"])
            upper[i] = np.interp(y, FORECAST_DATA["year"], FORECAST_DATA["upper_bound"])

    return pd.DataFrame({
        "year": years,
        "resistance_index": resistance,
        "lower_bound": lower,
        "upper_bound": upper,
    })
