# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is the **open computational companion** to the paper
**"The Twilight of Antibiotics: A predictive mathematical model of declining
antimicrobial effectiveness, and a possible metabolic escape route"**
(Prieto Gratacós E, Botto J. *Br J Med Health Res*. 2026;13(8):43-56.
doi:10.5281/zenodo.21898960).

It is a **runnable multi-page Dash/Plotly dashboard** that models and forecasts
antimicrobial-resistance (AMR) dynamics. It is deployed live at
**https://resistome.imhoit.com** and archived on Zenodo
(software concept DOI **10.5281/zenodo.22117640**, MIT license).

## Structure

Everything runs from `dashboard/`:

- `dashboard/app.py` — Dash app (`use_pages=True`), shell layout, `NAV_ITEMS` (11 pages). WSGI target `app:server`.
- `dashboard/pages/` — one module per page (11): `overview`, `pathogens`, `timeseries`, `bibliometrics` (`/industry`), `antimetabolic` (`/metabolic`), `methods`, `datasources`, `references`, `export`, `documentation` (`/docs`), `tutorial`.
- `dashboard/data/` — the data/model layer: `amr_data.py` (super-exponential curve), `pathogen_data.py`, `timeseries_data.py`, `bibliometrics_data.py`, `references_data.py` (60 refs).
- `dashboard/docs/` — in-app markdown documentation (`architecture`, `setup`, `charts_guide`, `models`, `data_sources`), rendered by the Documentation page.
- `dashboard/assets/` — `style.css` (dark theme) + `export_download.js`.
- Deploy: `Procfile`, `.do/app.yaml` (DigitalOcean App Platform), `deploy/systemd/` (self-host fallback), `run-api.sh` / `run-web.sh`. See `DEPLOY.md`.
- Citation/metadata: `CITATION.cff`, `.zenodo.json`, `LICENSE` (MIT).

## Running

```bash
python3.12 -m venv venv && venv/bin/pip install -r requirements.txt
./run-api.sh            # dev server on http://localhost:8082
# production-style:
venv/bin/gunicorn --chdir dashboard --bind 0.0.0.0:8082 --workers 1 --threads 4 app:server
```

## Key Constraints (do not violate)

- **Deterministic only.** Closed-form/analytic models, no parameter fitting, no random sampling; SARIMA uses a fixed seed (42). Every figure must reproduce bit-for-bit on any machine. Transient UI state goes through `dcc.Store(storage_type="memory")`.
- **Sources are cited, not invented.** Mortality/surveillance values come from named published sources; every source mention gets a clickable link.
- Keep the app self-contained: no database, no external API at run-time — all coefficients embedded.

## Key Domain Context

- The normalized "resistance pressure index" (0–100) is a conceptual composite, not a raw epidemiological metric.
- Data are anchored to ~10+ published sources (Lancet GBD / Murray 2022, O'Neill Review, GRAM/CIDRAP, Tai 2025, WHO GLASS, Magiorakos 2012).
- The critical threshold (~95 on the index) represents near-total ineffectiveness of first-line antibiotics for hospital-acquired Gram-negative infections, projected ~2040–2047.
