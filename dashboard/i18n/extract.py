"""
Collect every user-visible English string the app renders, page by page.

Usage (from dashboard/):
    python -m i18n.extract            # report strings with no Spanish entry
    python -m i18n.extract --dump DIR # write DIR/<page>.json with untranslated strings

It renders each page layout and runs the page callbacks with representative
inputs, so strings built at run time (figure titles, stats, messages) are
included. Technical docs rendered as Markdown are left out on purpose: they
stay in English.
"""

import json
import os
import re
import sys
import warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import i18n  # noqa: E402

_SKIP_KEYS = {"value", "id", "href", "src", "uid", "meta", "customdata", "font", "line",
              "marker", "colorscale", "style", "className", "hoverinfo", "type", "mode",
              "fill", "xref", "yref", "xanchor", "yanchor", "textposition", "orientation",
              "barmode", "hovermode", "dash", "symbol", "side", "tickformat", "ticksuffix",
              "fillcolor", "color", "bgcolor", "paper_bgcolor", "plot_bgcolor", "family",
              "template", "texttemplate", "hoverlabel", "z", "x", "y", "ids", "legendgroup",
              "axis", "autorange", "rangemode", "valueformat", "format", "hoveron",
              "yaxis_type", "layer", "sizemode", "path", "text_auto"}
_NOISE = re.compile(r"^[\d\s.,%+\-–−→←/()·:;×x≥≤±=<>*#|\[\]'\"_—]*$")
_URLISH = re.compile(r"^(https?://|/|www\.|doi:|\./|[\w.-]+\.(py|md|json|js|css|pdf|png|svg|csv)$)")


def _keep(s):
    s = s.strip()
    if len(s) < 2 or _NOISE.match(s) or _URLISH.match(s):
        return False
    if not re.search(r"[A-Za-z]{2,}", s):
        return False
    return True


def _collect_plain(obj, out, axis_cats=False):
    if isinstance(obj, str):
        if _keep(obj):
            out.add(obj.strip())
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _collect_plain(v, out, axis_cats)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("x", "y") and axis_cats and type(v).__module__ == "numpy" and v.dtype.kind in ("O", "U", "S"):
                v = v.tolist()
            if k in ("x", "y") and axis_cats:
                # categorical axes (heatmap classes, region names) are visible text
                if isinstance(v, (list, tuple)) and v and all(isinstance(e, str) for e in v):
                    _collect_plain(v, out)
                continue
            if k in _SKIP_KEYS:
                continue
            _collect_plain(v, out, axis_cats)


def collect(obj, out):
    if obj is None:
        return
    if isinstance(obj, str):
        if _keep(obj):
            out.add(obj.strip())
        return
    if isinstance(obj, (list, tuple)):
        for v in obj:
            collect(v, out)
        return
    if hasattr(obj, "_prop_names"):
        name = type(obj).__name__
        if name in ("Store", "Markdown", "Location"):
            return
        for prop in i18n._TEXT_PROPS:
            if prop in obj._prop_names and getattr(obj, prop, None) is not None:
                val = getattr(obj, prop)
                if prop == "figure":
                    fig = val.to_plotly_json() if hasattr(val, "to_plotly_json") else val
                    _collect_plain(fig, out, axis_cats=True)
                elif prop in ("data", "marks"):
                    _collect_plain(val, out)
                else:
                    collect(val, out)
        return
    if hasattr(obj, "to_plotly_json"):
        _collect_plain(obj.to_plotly_json(), out, axis_cats=True)
    elif isinstance(obj, dict):
        _collect_plain(obj, out, axis_cats=True)


# Kept in English on purpose: bibliographic citations, identifiers, names.
_ID_LIKE = re.compile(r"^(10\.\d{4,}/\S+|orcid\.org/\S+|[\w.-]+@[\w.-]+)$")


def _no_translate():
    from data.references_data import REFERENCES
    keep = {r["citation"] for r in REFERENCES}
    from data.pathogen_data import PATHOGENS
    keep.update(PATHOGENS)
    return keep


def gather():
    import dash
    import app  # noqa: F401  (registers pages)
    from pages import (overview, scenarios, pathogens, timeseries, bibliometrics, antimetabolic,
                       methods, datasources, references, press, export, documentation, tutorial)

    pages = {}

    def page(key, mod, extra=()):
        out = set()
        collect(mod._layout, out)
        for res in extra:
            collect(res, out)
        pages[key] = out

    # Shell (header, footer, nav)
    shell = set()
    collect(app._app_body, shell)
    for label, _ in app.NAV_ITEMS:
        shell.add(label)
    shell.update({"English", "Español"})
    pages["shell"] = shell

    page("overview", overview)
    page("scenarios", scenarios, [scenarios.update_scenario.__wrapped__(15, 30, 2027),
                                  scenarios.update_scenario.__wrapped__(100, 100, 2027),
                                  scenarios.update_scenario.__wrapped__(0, 0, 2027)])
    pc = pathogens
    page("pathogens", pc, [
        pc.render_heatmap.__wrapped__({}, "matrix"),
        pc.render_heatmap.__wrapped__({"0,2": 50.0}, "delta"),
        pc.update_bulk_target.__wrapped__("pathogen"),
        pc.update_bulk_target.__wrapped__("antibiotic"),
        pc.render_preview.__wrapped__("0", "2", 50, {}),
        pc.render_preview.__wrapped__("0", "2", 50, {"0,2": 40.0}),
        pc.render_preview.__wrapped__("4", "0", 50, {}),
        pc.render_preview.__wrapped__(None, None, 50, {}),
    ])
    ts = timeseries
    ts_out = []
    for p in ts.PATHOGEN_CHOICES:
        ts_out.append(ts.update_timeseries.__wrapped__(p, "12"))
        ts_out.append(ts.update_scenario.__wrapped__(p, "12", 30, "0", True))
    ts_out.append(ts.update_scenario.__wrapped__("MRSA", "6", 30, "12", False))
    page("timeseries", ts, ts_out)
    page("bibliometrics", bibliometrics)
    page("antimetabolic", antimetabolic)
    page("methods", methods)
    page("datasources", datasources)
    page("references", references)
    page("press", press)
    exp = []
    for opt in export.CHART_OPTIONS:
        value = opt["value"] if isinstance(opt, dict) else opt
        exp.append(export.update_preview.__wrapped__(value, "dark"))
    page("export", export, exp)
    page("documentation", documentation)
    import model_cards
    mc = []
    for key, card in model_cards.CARDS.items():
        for t in card.get("terms", []):
            mc.append(model_cards.show_term.__wrapped__(t["key"], {"type": "mc-term", "card": key}))
    page("model_cards", model_cards, mc) if hasattr(model_cards, "_layout") else pages.__setitem__(
        "model_cards", (lambda o: (collect(mc, o), o)[1])(set()))
    page("tutorial", tutorial)
    return pages


def main():
    pages = gather()
    keep_en = _no_translate()
    for key in pages:
        pages[key] = {s for s in pages[key] if s not in keep_en and not _ID_LIKE.match(s)
                      and not re.match(r"^#[0-9a-fA-F]{3,8}$", s)}
    dump = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--dump" else None
    seen, total_missing = set(), 0
    for key, strings in pages.items():
        missing = sorted(s for s in strings
                         if s not in seen and i18n.T(s, "es") == s)
        seen.update(strings)
        total_missing += len(missing)
        print(f"{key:14s} {len(strings):5d} strings, {len(missing):5d} without Spanish")
        if dump and missing:
            os.makedirs(dump, exist_ok=True)
            with open(os.path.join(dump, f"{key}.json"), "w", encoding="utf-8") as fh:
                json.dump(missing, fh, ensure_ascii=False, indent=1)
    print(f"TOTAL without Spanish: {total_missing}")


if __name__ == "__main__":
    main()
