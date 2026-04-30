"""
Pathogen resistance data — ESKAPEE pathogens + WHO priority + Stenotrophomonas.
Resistance rates (%) based on published surveillance data:
- WHO GLASS 2022/2023 reports
- ECDC/EARS-Net surveillance
- Murray et al. Lancet 2022 (GBD-AMR)
- CDC AR Threats Report 2019/2022
- Gratacós-Botto paper UPDATE v.A-29 (ESKAPEE designation, párr. 11;
  Stenotrophomonas + PDR documentation, párr. 65)
- Magiorakos et al. Clin Microbiol Infect 2012 (MDR/XDR/PDR isolate-level
  definitions)
"""

import pandas as pd
import numpy as np

# ESKAPEE + key pathogens vs antibiotic classes.
# ESKAPEE = E. faecium, S. aureus, K. pneumoniae, A. baumannii,
#           P. aeruginosa, Enterobacter spp., E. coli (added in párr. 11).
# S. maltophilia added per párr. 65 (PDR-Sm bloodstream infections).
PATHOGENS = [
    "S. aureus (MRSA)",
    "E. faecium (VRE)",
    "K. pneumoniae",
    "A. baumannii",
    "P. aeruginosa",
    "Enterobacter spp.",
    "E. coli",
    "S. maltophilia",
    "N. gonorrhoeae",
    "S. pneumoniae",
    "M. tuberculosis",
]

ANTIBIOTIC_CLASSES = [
    "Penicillins",
    "Cephalosporins\n(3rd gen)",
    "Carbapenems",
    "Fluoroquinolones",
    "Aminoglycosides",
    "Vancomycin",
    "Polymyxins\n(Colistin)",
    "Macrolides",
    "Tetracyclines",
    "Sulfonamides/\nTrimethoprim",
]

# Resistance matrix (% resistant, approximate global medians).
# NaN = intrinsically resistant or not applicable.
# S. maltophilia row: intrinsic R to penicillins, 3GC, carbapenems (L1+L2 β-
# lactamases), aminoglycosides, vancomycin (Gram-neg), macrolides; treatable
# with TMP/SMX (~15% R), fluoroquinolones (~35% R), tetracyclines (~25% R).
# Polymyxins variable / often used.
RESISTANCE_MATRIX = np.array([
    # Penic  Ceph3  Carba  FQuino Amino  Vanco  Polym  Macro  Tetra  Sulfa
    [95,     35,    2,     30,    5,     1,     np.nan,55,    15,    25   ],  # S. aureus MRSA
    [99,     99,    5,     80,    50,    30,    np.nan,90,    25,    70   ],  # E. faecium VRE
    [90,     55,    25,    45,    35,    np.nan,5,     np.nan,40,    60   ],  # K. pneumoniae
    [99,     85,    60,    70,    50,    np.nan,10,    np.nan,45,    75   ],  # A. baumannii
    [np.nan, 20,    15,    25,    10,    np.nan,3,     np.nan,np.nan,np.nan],  # P. aeruginosa
    [85,     40,    8,     25,    15,    np.nan,2,     np.nan,30,    45   ],  # Enterobacter
    [65,     20,    2,     35,    20,    np.nan,1,     np.nan,35,    45   ],  # E. coli
    [np.nan, np.nan,np.nan,35,    np.nan,np.nan,40,    np.nan,25,    15   ],  # S. maltophilia
    [40,     10,    np.nan,60,    np.nan,np.nan,np.nan,45,    55,    np.nan],  # N. gonorrhoeae
    [15,     5,     np.nan,8,     np.nan,1,     np.nan,35,    25,    40   ],  # S. pneumoniae
    [np.nan, np.nan,np.nan,20,    15,    np.nan,np.nan,np.nan,np.nan,np.nan],  # M. tuberculosis
])

# WHO Priority classification (2024 WHO Bacterial Priority Pathogens List)
WHO_PRIORITY = {
    "S. aureus (MRSA)": "High",
    "E. faecium (VRE)": "High",
    "K. pneumoniae": "Critical",
    "A. baumannii": "Critical",
    "P. aeruginosa": "Critical",
    "Enterobacter spp.": "Critical",
    "E. coli": "Critical",
    "S. maltophilia": "Special",
    "N. gonorrhoeae": "High",
    "S. pneumoniae": "Medium",
    "M. tuberculosis": "Special",
}

# Magiorakos 2012 documented phenotype — strongest documented strain phenotype
# in peer-reviewed literature (NOT a species-level claim; isolates vary).
# References:
#   * Magiorakos AP et al., Clin Microbiol Infect 2012 (definitions)
#   * Paper UPDATE v.A-29 párrs. 53–65 (CRE, CRAB, CRPA, MRSA, VRE,
#     PDR-Pa, PDR-Ab, PDR-Sm, XDR-Kp, XDR-TB)
MDR_XDR_PDR = {
    "S. aureus (MRSA)":   "MDR",   # MRSA classic
    "E. faecium (VRE)":   "XDR",   # VRE + linezolid resistance reported
    "K. pneumoniae":      "PDR",   # PDR-Kp documented (Magiorakos; Antimicrob Agents Chemother 2020)
    "A. baumannii":       "PDR",   # PDR-Ab — J. Infect. 2018; Crit. Care 2021
    "P. aeruginosa":      "PDR",   # PDR-Pa — J Infect Public Health 2019
    "Enterobacter spp.":  "PDR",   # J Glob Antimicrob Resist 2021
    "E. coli":            "XDR",   # XDR-EC widely reported
    "S. maltophilia":     "PDR",   # PDR-Sm bloodstream — J Hosp Infect 2020
    "N. gonorrhoeae":     "XDR",   # XDR-Ng (cefixime + azithro)
    "S. pneumoniae":      "MDR",
    "M. tuberculosis":    "XDR",   # XDR-TB — Lancet 2018
}

# Regional variation (resistance index by WHO region)
REGIONS = ["Africa", "Americas", "SE Asia", "Europe", "E. Mediterranean", "W. Pacific"]

REGIONAL_DATA = pd.DataFrame({
    "region": REGIONS * 4,
    "pathogen": (
        ["K. pneumoniae"] * 6 +
        ["E. coli"] * 6 +
        ["S. aureus (MRSA)"] * 6 +
        ["A. baumannii"] * 6
    ),
    "resistance_index": [
        65, 40, 70, 30, 55, 45,
        50, 25, 55, 18, 45, 40,
        30, 45, 35, 18, 50, 55,
        70, 50, 75, 55, 80, 65,
    ],
    "source": (
        ["GLASS 2022"] * 6 +
        ["GLASS 2022"] * 6 +
        ["EARS-Net/GLASS"] * 6 +
        ["GLASS 2022"] * 6
    ),
})

TEMPORAL_TRENDS = pd.DataFrame({
    "year": list(range(2000, 2026)) * 3,
    "phenotype": (
        ["MRSA"] * 26 +
        ["3GC-R E. coli"] * 26 +
        ["CRE K. pneumoniae"] * 26
    ),
    "prevalence": (
        [32, 34, 36, 38, 40, 42, 41, 39, 37, 35,
         33, 31, 29, 28, 27, 26, 25, 25, 24, 24,
         23, 23, 22, 22, 22, 21] +
        [5, 6, 7, 8, 9, 10, 11, 13, 14, 15,
         16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29, 30, 32] +
        [1, 1, 2, 2, 3, 4, 5, 7, 9, 11,
         13, 15, 17, 19, 20, 22, 23, 24, 25, 26,
         27, 28, 29, 30, 32, 35]
    ),
})
