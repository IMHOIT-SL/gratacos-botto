# Setup and Running Instructions

## Prerequisites

- **Python 3.12** (3.10+ should also work, but 3.12 is the tested version)
- **pip** (included with Python)
- A modern web browser (Chrome, Firefox, Edge, or Safari)

## Virtual Environment Setup

A virtual environment already exists at the project root (`venv/`). To use it or create a new one:

### Using the existing environment

```bash
cd /path/to/Gratacos-Botto
source venv/bin/activate
```

### Creating a fresh environment

```bash
cd /path/to/Gratacos-Botto
python3.12 -m venv venv
source venv/bin/activate
```

On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

## Installing Dependencies

The project ships a pinned `requirements.txt` at the repository root.

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs the runtime dependencies (Dash, Plotly, statsmodels, numpy, pandas, Flask, gunicorn) at the exact versions used in development.

If you only want to develop locally without gunicorn:

```bash
pip install dash plotly statsmodels numpy pandas
```

### Package Details

| Package       | Minimum Version | Purpose                                      |
|---------------|-----------------|----------------------------------------------|
| `dash`        | 4.1             | Web framework (includes Flask, React frontend)|
| `plotly`      | 6.6             | Interactive charting library                  |
| `statsmodels` | 0.14            | SARIMAX model fitting, ACF/PACF computation  |
| `numpy`       | 1.26+           | Numerical arrays, interpolation, random generation |
| `pandas`      | 2.0+            | DataFrames for tabular data                   |

Note: `statsmodels` is a soft dependency for the Time Series page. If it is not installed, the SARIMA model falls back to linear extrapolation, and ACF/PACF computation uses a simplified manual method. All other pages work without it.

## Running the Dashboard

With the virtual environment activated:

```bash
cd dashboard
python app.py
```

Or from the project root:

```bash
python dashboard/app.py
```

The application starts a development server with these defaults:
- **Host:** `0.0.0.0` (accessible from any network interface)
- **Port:** `8082`
- **Debug mode:** enabled (auto-reload on code changes, error overlays)

Open your browser to: **http://localhost:8082**

### Custom Host/Port

Set environment variables before running (read by `app.py` via `os.environ`):

```bash
HOST=127.0.0.1 PORT=8080 DEBUG=false python dashboard/app.py
```

Defaults are `HOST=0.0.0.0`, `PORT=8082`, `DEBUG=true`.

## Accessing Each Page

Once the dashboard is running at `http://localhost:8082`:

| Page         | URL                              | Description                                    |
|--------------|----------------------------------|------------------------------------------------|
| Overview     | http://localhost:8082/            | Super-exp curve + mortality + Carbapenem 2035 spotlight |
| Pathogens    | http://localhost:8082/pathogens   | ESKAPEE heatmap + Sensitivity Analysis + regional + trends |
| Time Series  | http://localhost:8082/timeseries  | SARIMA forecasting with interactive controls   |
| Industry     | http://localhost:8082/industry    | PubMed scientometric + market CAGR + drug class + divergence |
| Metabolic    | http://localhost:8082/metabolic   | Antimetabolic solution scaffold (working hypothesis) |
| Methods      | http://localhost:8082/methods     | Materials & Methods + reproducibility + citation |
| Data Sources | http://localhost:8082/datasources | Data source catalog and coverage timeline      |
| References   | http://localhost:8082/references  | 60 peer-reviewed citations grouped by paper section |
| Export       | http://localhost:8082/export      | Export Studio (11 charts × 3 themes)           |
| Docs         | http://localhost:8082/docs        | This documentation viewer                      |
| Tutorial     | http://localhost:8082/tutorial    | Interactive guide for Plotly chart controls    |

Use the navigation links in the top header bar to switch between pages. Navigation uses client-side routing (no full page reload).

## Exporting Charts

### From Any Chart

Every chart in the dashboard has a Plotly modebar that appears when you hover over the top-right corner of the chart. The modebar includes a camera icon for downloading the chart as an image.

Default export settings:
- **Format:** SVG
- **Scale:** 3x (approximately 300 DPI for publication use)

### From the Export Studio

The Export page (`/export`) provides more control:

1. Select the chart you want to export from the dropdown.
2. Choose a color scheme:
   - **Dashboard Dark** — matches the on-screen appearance
   - **Publication Light** — white background suitable for journal submissions
   - **Print B&W** — grayscale for black-and-white printing
3. Choose the output format (SVG, PNG, or PDF).
4. Choose the resolution scale (1x, 2x, or 3x).
5. Click the camera icon in the preview chart's modebar to download.

### Post-Processing

For PDF output from SVG exports:

```bash
# Using cairosvg (pip install cairosvg)
cairosvg input.svg -o output.pdf

# Using Inkscape
inkscape input.svg --export-type=pdf --export-filename=output.pdf
```

For cropping or combining figures:

```bash
# Using ImageMagick (for PNG)
convert -trim input.png output.png
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'dash'"
Ensure the virtual environment is activated (`source venv/bin/activate`) and all dependencies are installed.

### "Address already in use" on port 8082
Another process is using port 8082. Either stop it or change the port in `app.py`.

### Time Series page shows "Linear extrapolation (fallback)"
This means `statsmodels` is not installed or the SARIMAX fit failed. Install it with `pip install statsmodels`.

### Charts appear with white backgrounds in the browser
This is a browser caching issue. Hard-refresh the page (Ctrl+Shift+R / Cmd+Shift+R) to reload the CSS.

### Dropdown menus are hard to read (dark text on dark background)
Dash dropdowns use browser-native styling. The dashboard sets background colors via inline styles, but some browsers may override them. Chrome and Firefox provide the best rendering.

---

## Deployment

The repository ships with deployment artifacts at the project root: `requirements.txt` and `Procfile`. Three options are documented; pick whichever matches your operational preference.

### Option 1 — Cloudflare Tunnel (local + public URL, zero deploy)

Run the dashboard on your own machine and expose it through a Cloudflare tunnel. Best for paper revision / pre-publication when you only need occasional public access:

```bash
# In one terminal:
source venv/bin/activate
python dashboard/app.py        # serves on :8082

# In another terminal:
cloudflared tunnel --url http://localhost:8082
```

`cloudflared` prints a public HTTPS URL you can share. Stop the tunnel when done.

For named (stable) tunnels with auth via Cloudflare Access, see Cloudflare's tunnel documentation. Zero infrastructure cost; depends on your machine being on.

### Option 2 — DigitalOcean App Platform (managed PaaS)

Push the repo to GitHub, then create an App on DigitalOcean App Platform pointing at the repo. The platform autodetects:

- `requirements.txt` → installs Python dependencies
- `Procfile` → uses the `web:` line to run gunicorn

The Procfile ships with:

```
web: gunicorn --chdir dashboard --bind 0.0.0.0:${PORT:-8082} --workers 2 --timeout 120 app:server
```

This serves the Dash app via the Flask WSGI object exposed by Dash (`app.server`). DigitalOcean injects `$PORT` automatically.

Alternatives that read the same artifacts: Render.com, Fly.io (with a Dockerfile), Railway, Heroku.

### Option 3 — DigitalOcean Droplet + nginx + systemd

For full control on a VPS, run gunicorn under systemd and proxy through nginx for HTTPS. Outline (production hardening omitted):

```bash
# On the droplet, after cloning the repo and installing requirements:
gunicorn --chdir dashboard --bind 127.0.0.1:8082 --workers 2 app:server
```

Front with nginx (reverse proxy, TLS via certbot) and run gunicorn as a systemd service. This option is the most flexible but requires the most setup.

### Note: Cloudflare Pages is NOT compatible

Cloudflare Pages hosts only static assets and Workers (JS/TS). Dash needs a persistent Python process to run callbacks; it cannot be deployed there directly. Use one of the options above.
