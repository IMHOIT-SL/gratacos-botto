"""
Standalone matplotlib visualisation — Gratacós-Botto super-exponential resistance
curve from paper UPDATE v.A-29.

Produces a single figure showing:
  * The super-exponential curve (primary model, paper párr. 22)
  * The constant-r reference logistic (faint dotted)
  * ±3-year temporal envelope
  * Critical threshold (95) and critical-point band (2040–2047)

This script is fully deterministic — no random sampling, no fitting.
Coefficients are hardcoded and identical to dashboard/data/amr_data.py.

Run:
    python docs/antibiotics.py

Requires: numpy, matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Closed-form super-exponential model parameters
#   y(τ) = K / (1 + A · exp(-r·τ - b·τ²))     with τ = year - 1990
# ---------------------------------------------------------------------------
K = 100.0
A = 88.0 / 12.0           # ≈ 7.3333; sets y(1990) = 12
R_SUPER = 0.0705          # base rate
B_SUPER = 3.05e-4         # super-exponential acceleration
T0 = 1990

# Reference logistic (b = 0): same K, A; r' calibrated so y(2025) = 70 with b=0
R_REF = 0.0811


def curve(years, r, b):
    tau = np.asarray(years, dtype=float) - T0
    return K / (1.0 + A * np.exp(-r * tau - b * tau * tau))


years = np.arange(1990, 2061)
super_exp = curve(years, R_SUPER, B_SUPER)
reference = curve(years, R_REF, 0.0)

# ±3-year envelope (lateral shift)
upper = curve(years + 3, R_SUPER, B_SUPER)
lower = curve(years - 3, R_SUPER, B_SUPER)

# Published anchor markers (Murray, GRAM, O'Neill, Oxford VG, GBD)
anchor_years = np.array([1990, 2000, 2010, 2019, 2021, 2025])
anchor_vals = np.array([12, 23, 35, 58, 63, 70])

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.5))

# ±3 year band
ax.fill_between(years, lower, upper, color="#4fc3f7", alpha=0.15,
                label="Uncertainty band (±3 yrs)")

# Reference logistic (faint)
ax.plot(years, reference, color="#888", linewidth=1.2, linestyle=":",
        label="Reference logistic (constant r)")

# Super-exponential curve — observed segment
mask_obs = years <= 2025
ax.plot(years[mask_obs], super_exp[mask_obs], color="#4fc3f7", linewidth=2.8,
        label="Observed (1990–2025)")

# Super-exponential curve — forecast segment
mask_fc = years >= 2025
ax.plot(years[mask_fc], super_exp[mask_fc], color="#ef5350", linewidth=2.8,
        linestyle="--", label="Super-exponential forecast (Gratacós-Botto)")

# Published anchor markers
ax.scatter(anchor_years, anchor_vals, s=60, color="#4fc3f7",
           edgecolor="white", linewidth=1.5, zorder=5,
           label="Published anchor points")

# Critical threshold + critical-point band
ax.axhline(95, color="#ef5350", linestyle=":", linewidth=1,
           label="Critical threshold (~95)")
ax.axvspan(2040, 2047, color="#ef5350", alpha=0.10,
           label="Critical Point (2040–2047)")

ax.set_xlabel("Year")
ax.set_ylabel("Resistance Pressure Index (0–100)")
ax.set_title("AMR Resistance Pressure — Super-exponential model (Gratacós-Botto v.A-29)")
ax.set_ylim(0, 105)
ax.set_xlim(1990, 2060)
ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=9, framealpha=0.9)

# Where each model crosses the critical threshold (95)
super_cross = int(years[super_exp >= 95][0]) if (super_exp >= 95).any() else None
ref_cross = int(years[reference >= 95][0]) if (reference >= 95).any() else None
if super_cross and ref_cross:
    ax.text(2042, 50,
            f"Crosses 95:\n  super-exp: {super_cross}\n  reference: {ref_cross}\n  Δ = {ref_cross - super_cross} yrs",
            fontsize=9, color="#444",
            bbox=dict(facecolor="white", edgecolor="#ccc", boxstyle="round,pad=0.4"))

plt.tight_layout()
plt.show()
