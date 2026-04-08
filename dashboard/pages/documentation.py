"""
Documentation page — Renders markdown docs from dashboard/docs/ in the web UI.
"""

import dash
from dash import html, dcc, callback, Input, Output
from pathlib import Path

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from components import help_section

dash.register_page(__name__, path="/docs", name="Docs")

# ---------------------------------------------------------------------------
# Read all markdown files at module load
# ---------------------------------------------------------------------------
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

DOC_FILES = {
    "Architecture": "architecture.md",
    "Data Sources": "data_sources.md",
    "Charts Guide": "charts_guide.md",
    "Models": "models.md",
    "Setup": "setup.md",
}

DOC_CONTENTS = {}
for label, filename in DOC_FILES.items():
    filepath = DOCS_DIR / filename
    if filepath.exists():
        DOC_CONTENTS[label] = filepath.read_text(encoding="utf-8")
    else:
        DOC_CONTENTS[label] = f"*File `{filename}` not found.*"

DOC_LABELS = list(DOC_FILES.keys())

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
layout = html.Div([
    help_section(
        "Documentation",
        [
            "This page provides access to the complete technical documentation for the AMR Research Dashboard.",
            "Select a document from the tabs to view architecture details, data source references, chart guides, mathematical model specifications, or setup instructions.",
        ],
    ),
    html.Div([
        dcc.Tabs(
            id="docs-tab-selector",
            value=DOC_LABELS[0],
            children=[dcc.Tab(label=label, value=label) for label in DOC_LABELS],
            className="docs-tabs",
        ),
        html.Div(
            dcc.Markdown(
                DOC_CONTENTS.get(DOC_LABELS[0], ""),
                id="docs-markdown-content",
                className="docs-content",
                dangerously_allow_html=False,
            ),
            className="docs-content-wrapper",
        ),
    ], className="card"),
])

# ---------------------------------------------------------------------------
# Callback
# ---------------------------------------------------------------------------
@callback(
    Output("docs-markdown-content", "children"),
    Input("docs-tab-selector", "value"),
)
def switch_doc(selected_tab):
    return DOC_CONTENTS.get(selected_tab, "Document not found.")
