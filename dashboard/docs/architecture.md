# Architecture Reference

## Tech Stack

| Component       | Version  | Purpose                                              |
|-----------------|----------|------------------------------------------------------|
| Python          | 3.12     | Runtime                                              |
| Dash            | 4.1      | Web application framework (Flask + React under hood) |
| Plotly          | 6.6      | Interactive charting library                         |
| statsmodels     | 0.14     | SARIMAX time-series modeling, ACF/PACF computation   |
| NumPy           | latest   | Numerical computation, array operations              |
| pandas          | latest   | DataFrames for tabular data handling                 |
| matplotlib      | latest   | Used only by the standalone `docs/antibiotics.py` script, not by the dashboard |

## File Structure

```
Gratacos-Botto/
├── CLAUDE.md                    # Project-level instructions for Claude Code
├── docs/
│   ├── antibiotics.py           # Standalone matplotlib script (original logistic curve)
│   ├── curves.png               # Static chart of historical AMR publication growth
│   └── MathematicalModelsPaper.txt  # Literature review and data compilation
│
└── dashboard/
    ├── app.py                   # Application entry point — creates the Dash app,
    │                            #   defines the shell layout (header, nav, footer),
    │                            #   and serves as the WSGI target.
    ├── assets/
    │   └── style.css            # Global stylesheet — dark theme via CSS variables.
    │                            #   Automatically loaded by Dash from the assets/ folder.
    ├── data/
    │   ├── __init__.py          # Empty package marker
    │   ├── amr_data.py          # Observed + forecast resistance index DataFrames,
    │   │                        #   mortality projection data, sigmoid curve generator.
    │   ├── pathogen_data.py     # ESKAPE pathogen resistance matrix, WHO priority
    │   │                        #   classifications, regional variation data, temporal trends.
    │   └── timeseries_data.py   # Synthetic monthly resistance series generator for
    │                            #   MRSA, 3GC-R E. coli, and CRE K. pneumoniae.
    ├── pages/
    │   ├── __init__.py          # Empty package marker
    │   ├── overview.py          # "/" — Main resistance curve, mortality chart, data table
    │   ├── pathogens.py         # "/pathogens" — Heatmap, regional bars, temporal trends
    │   ├── timeseries.py        # "/timeseries" — SARIMA forecasting with diagnostics
    │   ├── datasources.py       # "/datasources" — Data source catalog and timeline
    │   └── export.py            # "/export" — Export Studio with theme switching
    └── docs/                    # This documentation folder
```

## How Pages Are Registered (Dash Multi-Page)

The dashboard uses **Dash Pages**, the built-in multi-page routing system. The mechanism works as follows:

1. **`app.py`** creates the Dash app with `use_pages=True`. This tells Dash to scan the `pages/` directory for page modules.

2. Each file in `pages/` calls `dash.register_page(__name__, path=..., name=...)` at module level. For example:

   ```python
   # pages/overview.py
   dash.register_page(__name__, path="/", name="Overview")
   ```

3. Each page module exposes a top-level `layout` variable (either an `html.Div` or a function returning one). Dash picks this up automatically.

4. In `app.py`, the shell layout includes `dash.page_container` inside the `<main>` element. Dash swaps the content of this container based on the URL path.

5. Navigation links in the header use `dcc.Link` for client-side routing (no full page reload).

### Registered Pages

| Module             | Path            | Nav Label    |
|--------------------|-----------------|--------------|
| `pages/overview.py`    | `/`             | Overview     |
| `pages/pathogens.py`   | `/pathogens`    | Pathogens    |
| `pages/timeseries.py`  | `/timeseries`   | Time Series  |
| `pages/datasources.py` | `/datasources`  | Data Sources |
| `pages/export.py`      | `/export`       | Export       |

## Data Flow

The application follows a clear pipeline from raw data through to rendered charts:

```
data modules (amr_data.py, pathogen_data.py, timeseries_data.py)
       │
       │  pandas DataFrames, numpy arrays, generator functions
       ▼
page builders (build_main_curve(), build_heatmap(), fit_sarima(), etc.)
       │
       │  plotly.graph_objects.Figure instances
       ▼
Dash layout (dcc.Graph components with figure= or callback outputs)
       │
       │  JSON serialization over websocket
       ▼
Browser (Plotly.js renders interactive charts with modebar)
```

### Data Modules

- **`amr_data.py`** — Exports `OBSERVED_DATA`, `FORECAST_DATA`, `MORTALITY_DATA` (all `pd.DataFrame`) and `compute_sigmoid_curve()` which interpolates between observed and forecast points to produce a continuous yearly series with confidence bounds.

- **`pathogen_data.py`** — Exports `PATHOGENS` (list), `ANTIBIOTIC_CLASSES` (list), `RESISTANCE_MATRIX` (10x10 numpy array), `WHO_PRIORITY` (dict), `REGIONAL_DATA` (DataFrame), and `TEMPORAL_TRENDS` (DataFrame).

- **`timeseries_data.py`** — Exports `MONTHLY_DATA` (dict of DataFrames, keyed by pathogen name) and `PATHOGEN_CHOICES` (list). Data is generated deterministically at import time using `np.random.default_rng(seed=42)`.

### Callbacks

Most pages build their charts at import time (static figures). The **Time Series** and **Export** pages use Dash callbacks for interactivity:

- **`timeseries.py`** — A single callback driven by the pathogen dropdown and horizon slider. It fits a SARIMA model on the fly, generates forecasts, computes residuals, and builds all six chart outputs (main forecast, scenario comparison, residuals, ACF, PACF) plus diagnostic statistics.

- **`export.py`** — A callback driven by chart selector, color scheme, format, and scale inputs. It rebuilds the selected chart using the chosen theme and updates the Plotly modebar download configuration.

## CSS Theming Approach

### CSS Variables (Dark Theme)

All colors are defined as CSS custom properties in `:root` within `assets/style.css`:

```css
:root {
    --bg-primary: #0f1117;
    --bg-secondary: #1a1c25;
    --bg-card: #21232d;
    --text-primary: #e8eaed;
    --text-secondary: #9aa0a6;
    --accent: #4fc3f7;
    --accent-dim: #1a3a4a;
    --danger: #ef5350;
    --warning: #ffb74d;
    --success: #66bb6a;
    --border: #2d2f3a;
}
```

These variables are referenced throughout the stylesheet. The Plotly chart backgrounds are set to match `--bg-card` (`#21232d`) using `paper_bgcolor` and `plot_bgcolor` in each chart builder.

### Key CSS Classes

| Class           | Purpose                                           |
|-----------------|---------------------------------------------------|
| `.app-container`| Full-height flex column for the entire app         |
| `.header`       | Top bar with title and navigation                  |
| `.nav-link`     | Navigation links with hover/active state           |
| `.main-content` | Central content area (max-width 1400px, centered)  |
| `.card`         | Rounded container for chart + title blocks         |
| `.stat-card`    | Summary statistic box (used in stats rows)         |
| `.stats-row`    | Auto-fit grid of stat cards                        |
| `.chart-grid-2` | Two-column responsive grid for side-by-side charts |
| `.data-table`   | Styled HTML table with hover highlighting          |
| `.source-tag`   | Inline badge for citation labels                   |
| `.chart-sources`| Block of source citation links below a chart       |

### Plotly Chart Themes

For the Export Studio page, three complete Plotly color themes are defined in `pages/export.py`:

- **Dashboard Dark** — Matches the CSS dark theme (default)
- **Publication Light** — White background, high-contrast academic colors
- **Print B&W** — Grayscale for black-and-white printing

Each theme is a dictionary controlling `paper_bgcolor`, `plot_bgcolor`, `font_color`, `gridcolor`, five accent colors, heatmap colorscales, and annotation colors.

## How to Add a New Page

1. **Create a data module** (if needed) in `dashboard/data/`. Define your DataFrames or generator functions. Import them in your page.

2. **Create a page file** in `dashboard/pages/`, e.g., `pages/newpage.py`:

   ```python
   import dash
   from dash import html, dcc

   dash.register_page(__name__, path="/newpage", name="New Page")

   # Build your charts here as Plotly Figure objects

   layout = html.Div([
       html.Div([
           html.H3("Chart Title", className="card-title"),
           html.P("Description", className="card-subtitle"),
           dcc.Graph(figure=your_figure, config={
               "toImageButtonOptions": {"format": "svg", "scale": 3},
               "displayModeBar": True,
           }),
       ], className="card"),
   ])
   ```

3. **Add a nav link** in `app.py` inside the `html.Nav` block:

   ```python
   dcc.Link("New Page", href="/newpage", className="nav-link"),
   ```

4. **If using callbacks**, define them in the same page file using the `@callback` decorator. Set `suppress_callback_exceptions=True` is already enabled in `app.py`.

5. **If adding to Export Studio**, add an entry to the `CHART_OPTIONS` list and a builder function to `CHART_BUILDERS` in `pages/export.py`. The builder must accept a `theme` dict and return a `go.Figure`.

6. **Match the chart styling** to the dark theme by using:
   ```python
   CHART_LAYOUT = dict(
       paper_bgcolor="#21232d",
       plot_bgcolor="#21232d",
       font=dict(color="#e8eaed", family="Inter, sans-serif", size=12),
       xaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
       yaxis=dict(gridcolor="#2d2f3a", zerolinecolor="#2d2f3a"),
   )
   ```
