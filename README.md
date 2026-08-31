# The Twilight of Antibiotics — Open Computational Companion

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22117640.svg)](https://doi.org/10.5281/zenodo.22117640)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Live](https://img.shields.io/badge/live-resistome.imhoit.com-2ea44f)](https://resistome.imhoit.com)

Interactive dashboard companion to the paper **“The Twilight of Antibiotics”**
(E. Prieto Gratacós & J. A. Botto). It models and forecasts the trajectory of
antimicrobial resistance (AMR) with a **deterministic, closed-form**
super-exponential model, SARIMA time-series forecasts, a carbapenem-resistance
mortality spotlight, and an ESKAPEE pathogen × antibiotic map.

**Live instance → https://resistome.imhoit.com**

Everything is embedded in the source — no database, no external API at run-time,
no parameter fitting, no random sampling. Every figure is reproducible
bit-for-bit on any machine.

---

## Run it locally — step by step

You need **Python 3.12** and **git**. That's it.

**1. Get the code**

```bash
git clone https://github.com/IMHOIT-SL/gratacos-botto.git
cd gratacos-botto
```

**2. Create a virtual environment**

```bash
python3.12 -m venv venv
```

**3. Install the dependencies**

```bash
venv/bin/pip install -r requirements.txt
```

**4. Start the dashboard**

```bash
./run-api.sh
```

*(or, without the helper script: `venv/bin/python dashboard/app.py`)*

**5. Open it in your browser**

```
http://localhost:8082
```

To stop the server, press **Ctrl+C**. To use a different port:
`PORT=9000 ./run-api.sh`.

---

## What's inside

| Page | What it shows |
|------|---------------|
| **Overview** | The super-exponential AMR curve (1990–2060) + mortality and carbapenem spotlights. |
| **Pathogens** | ESKAPEE pathogen × antibiotic resistance map with WHO priority and MDR/XDR/PDR badges. |
| **Time Series** | SARIMA forecasts with ACF/PACF diagnostics and AIC/BIC. |
| **Industry** | Publications, market (CAGR), awareness-vs-effectiveness. |
| **Metabolic** | The antimetabolic line of treatment (working hypothesis). |
| **Methods / Docs / Data Sources / References** | Methodology, model specs, cited sources. |
| **Export Studio** | Publication-grade figure export. |

---

## Production deployment

The app is a self-contained Dash/gunicorn WSGI app (entry point `app:server`).
For DigitalOcean App Platform, a self-hosted Cloudflare Tunnel, or any other
target, see **[DEPLOY.md](./DEPLOY.md)**.

```bash
# production-style local run:
venv/bin/gunicorn --chdir dashboard --bind 0.0.0.0:8082 --workers 1 --threads 4 app:server
```

---

## Reproducibility

The models are analytic and fully deterministic (SARIMA uses a fixed seed), so
the output is identical on every reload and every machine. See the **Methods**
page in the app, or `dashboard/docs/models.md`, for the full specification.

## How to cite

**Cite the paper** (Vancouver):

> Prieto Gratacós E, Botto JA. The Twilight of Antibiotics: a predictive
> mathematical model of declining antimicrobial effectiveness, and a possible
> metabolic escape route. Br J Med Health Res. 2026. (Under review; manuscript
> BJMHR-13-000038).

*(Journal abbreviated per ISO; full title: British Journal of Medical and
Health Research. Volume, issue, pages and DOI will be added on acceptance.)*

**Cite the software** (archived release):

> Prieto Gratacós, E. & Botto, J. A. (2026). *The Twilight of Antibiotics —
> open computational companion* [Software]. Zenodo.
> https://doi.org/10.5281/zenodo.22117640

The Zenodo DOI above is the **concept DOI** — it always resolves to the latest
version. To cite this exact release (v1.0.0), use `10.5281/zenodo.22117641`.
Machine-readable metadata: [`CITATION.cff`](./CITATION.cff) — GitHub's *Cite
this repository* button reads it (APA / BibTeX; GitHub does not offer Vancouver,
hence the ready-made Vancouver reference above).

## License

[MIT](./LICENSE) © 2026 Ernesto Prieto Gratacós and Julio A. Botto.
