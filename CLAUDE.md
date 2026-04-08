# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project for a paper tentatively titled "THE TWILIGHT OF ANTIBIOTICS," focused on mathematical modeling and forecasting of antimicrobial resistance (AMR). It contains reference materials, not a runnable application.

## Structure

- `docs/antibiotics.py` — Python script (numpy, matplotlib) that generates a conceptual logistic/sigmoid curve plotting AMR resistance pressure from 1990 to 2060, with a forecasted critical point around 2040-2045.
- `docs/MathematicalModelsPaper.txt` — Literature review and data compilation covering time-series forecasting (SARIMA), global burden models (hierarchical Bayesian), transmission-dynamic compartmental models, and One-Health integrated frameworks for AMR prediction.
- `docs/curves.png` — Chart showing historical growth in AMR-related records/publications over time.

## Running the Visualization

```bash
python docs/antibiotics.py
```

Requires `numpy` and `matplotlib`.

## Key Domain Context

- The normalized "resistance pressure index" (0-100) is a conceptual composite, not a raw epidemiological metric.
- Data points in the paper are anchored to ~10+ published sources (Lancet GBD, O'Neill Review, GRAM forecasts, CIDRAP).
- The critical threshold (~95 on the index) represents near-total ineffectiveness of first-line antibiotics for hospital-acquired Gram-negative infections, projected around 2040-2045.
