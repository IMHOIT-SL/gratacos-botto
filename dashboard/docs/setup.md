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

With the virtual environment activated:

```bash
pip install dash plotly statsmodels numpy pandas matplotlib
```

### Package Details

| Package       | Minimum Version | Purpose                                      |
|---------------|-----------------|----------------------------------------------|
| `dash`        | 4.1             | Web framework (includes Flask, React frontend)|
| `plotly`      | 6.6             | Interactive charting library                  |
| `statsmodels` | 0.14            | SARIMAX model fitting, ACF/PACF computation  |
| `numpy`       | 1.26+           | Numerical arrays, interpolation, random generation |
| `pandas`      | 2.0+            | DataFrames for tabular data                   |
| `matplotlib`  | 3.8+            | Only needed for the standalone `docs/antibiotics.py` script, not the dashboard |

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
- **Port:** `8050`
- **Debug mode:** enabled (auto-reload on code changes, error overlays)

Open your browser to: **http://localhost:8050**

### Custom Host/Port

To change the host or port, edit the last line of `dashboard/app.py`:

```python
app.run(debug=True, host="0.0.0.0", port=8050)
```

Or set environment variables before running:

```bash
HOST=127.0.0.1 PORT=8080 python dashboard/app.py
```

(This requires modifying `app.py` to read from `os.environ`.)

## Running the Standalone Visualization

The original matplotlib-based visualization can be run separately:

```bash
python docs/antibiotics.py
```

This opens a matplotlib window showing the logistic resistance curve. It does not require Dash or Plotly.

## Accessing Each Page

Once the dashboard is running at `http://localhost:8050`:

| Page         | URL                              | Description                                    |
|--------------|----------------------------------|------------------------------------------------|
| Overview     | http://localhost:8050/            | Main resistance curve, mortality projections   |
| Pathogens    | http://localhost:8050/pathogens   | Resistance heatmap, regional data, trends      |
| Time Series  | http://localhost:8050/timeseries  | SARIMA forecasting with interactive controls   |
| Data Sources | http://localhost:8050/datasources | Data source catalog and coverage timeline      |
| Export       | http://localhost:8050/export      | Export Studio with theme selection             |

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

### "Address already in use" on port 8050
Another process is using port 8050. Either stop it or change the port in `app.py`.

### Time Series page shows "Linear extrapolation (fallback)"
This means `statsmodels` is not installed or the SARIMAX fit failed. Install it with `pip install statsmodels`.

### Charts appear with white backgrounds in the browser
This is a browser caching issue. Hard-refresh the page (Ctrl+Shift+R / Cmd+Shift+R) to reload the CSS.

### Dropdown menus are hard to read (dark text on dark background)
Dash dropdowns use browser-native styling. The dashboard sets background colors via inline styles, but some browsers may override them. Chrome and Firefox provide the best rendering.
