"""
Synthetic monthly AMR resistance data (2000-2025) for SARIMA modeling.
Three pathogens with trend, seasonality, and noise.
"""

import numpy as np
import pandas as pd


def generate_monthly_amr_data():
    """
    Generate deterministic synthetic monthly resistance data for 3 pathogens.
    Returns a dict mapping pathogen name -> pandas DataFrame with
    columns: date, resistance_rate.
    """
    rng = np.random.default_rng(seed=42)
    months = pd.date_range("2000-01-01", "2025-12-01", freq="MS")
    n = len(months)
    t = np.arange(n)

    data = {}

    # --- MRSA ---
    # Peaked around 2005-2008 then declined due to interventions
    # Logistic-style rise then slow decline
    trend_mrsa = 40 + 15 * (1 / (1 + np.exp(-0.04 * (t - 60)))) - 0.03 * np.maximum(t - 100, 0)
    seasonal_mrsa = 2.0 * np.sin(2 * np.pi * t / 12) + 1.0 * np.sin(4 * np.pi * t / 12)
    noise_mrsa = rng.normal(0, 1.2, n)
    mrsa = trend_mrsa + seasonal_mrsa + noise_mrsa
    mrsa = np.clip(mrsa, 5, 65)

    data["MRSA"] = pd.DataFrame({"date": months, "resistance_rate": mrsa})

    # --- 3GC-R E. coli ---
    # Steady upward trend
    trend_ecoli = 8 + 0.08 * t + 0.00005 * t ** 2
    seasonal_ecoli = 1.5 * np.sin(2 * np.pi * t / 12) + 0.8 * np.cos(4 * np.pi * t / 12)
    noise_ecoli = rng.normal(0, 1.0, n)
    ecoli = trend_ecoli + seasonal_ecoli + noise_ecoli
    ecoli = np.clip(ecoli, 2, 50)

    data["3GC-R E. coli"] = pd.DataFrame({"date": months, "resistance_rate": ecoli})

    # --- CRE K. pneumoniae ---
    # Low baseline, accelerating increase (exponential-ish)
    trend_cre = 2 + 0.01 * t + 0.0003 * t ** 2
    seasonal_cre = 1.2 * np.sin(2 * np.pi * t / 12) + 0.6 * np.sin(4 * np.pi * t / 12 + 0.5)
    noise_cre = rng.normal(0, 0.8, n)
    cre = trend_cre + seasonal_cre + noise_cre
    cre = np.clip(cre, 0.5, 55)

    data["CRE K. pneumoniae"] = pd.DataFrame({"date": months, "resistance_rate": cre})

    return data


PATHOGEN_CHOICES = ["MRSA", "3GC-R E. coli", "CRE K. pneumoniae"]
MONTHLY_DATA = generate_monthly_amr_data()
