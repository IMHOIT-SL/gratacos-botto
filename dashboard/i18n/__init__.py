"""
Internationalisation (English / Spanish).

The app is authored in English. Spanish is applied at render time: every
string in a page layout or callback output (component text, labels, select
options, slider marks, and figure titles/axes/legends/annotations) that
exactly matches an entry of the Spanish catalog is replaced. Nothing else in
the code has to change, and strings without a translation stay in English
instead of breaking.

Language choice, in order:
  1. `?lang=es|en` in the URL (shareable links; also stored in the cookie by
     assets/i18n.js),
  2. the `amr_lang` cookie (set by the ES/EN switch in the header),
  3. the browser's Accept-Language header,
  4. English.

Catalogs live in i18n/es/*.json as {"English text": "Texto en español"}.
A catalog may also hold "__patterns__": [[regex, template], ...] for strings
built at run time (numbers, years, pathogen x antibiotic tooltips) that cannot
be listed verbatim. The regex uses named groups and the template is a
str.format string over them; a group named t_<name> is itself translated
before substitution, e.g.
    ["^(?P<p>.+?)<br>(?P<t_abx>.+?)<br><b>(?P<v>\\d+)%</b> resistant$",
     "{p}<br>{t_abx}<br><b>{v}%</b> resistente"]
"""

import copy
import glob
import json
import os
import re

LANGS = ("en", "es")
DEFAULT_LANG = "en"
COOKIE = "amr_lang"

_DIR = os.path.dirname(__file__)
_CATALOG = {"es": {}}
_PATTERNS = {"es": []}


def _load():
    for path in sorted(glob.glob(os.path.join(_DIR, "es", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        for regex, repl in data.pop("__patterns__", []):
            _PATTERNS["es"].append((re.compile(regex, re.S), repl))
        _CATALOG["es"].update(data)


_load()


def norm(lang):
    return lang if lang in LANGS else None


def current_lang(explicit=None):
    """Language for the current request (URL arg > cookie > browser > English)."""
    lang = norm(explicit)
    if lang:
        return lang
    try:
        from flask import request
        lang = norm(request.cookies.get(COOKIE))
        if lang:
            return lang
        best = request.accept_languages.best_match(list(LANGS))
        if best:
            return best
    except RuntimeError:  # outside a request (tests, startup)
        pass
    return DEFAULT_LANG


_WS = re.compile(r"^(\s*)(.*?)(\s*)$", re.S)


def T(text, lang=None):
    """Translate one string (exact catalog match, keeping outer whitespace)."""
    lang = lang or current_lang()
    if lang == "en" or not isinstance(text, str) or not text.strip():
        return text
    cat = _CATALOG.get(lang, {})
    hit = cat.get(text)
    if hit is not None:
        return hit
    lead, core, trail = _WS.match(text).groups()
    hit = cat.get(core)
    if hit is not None:
        return lead + hit + trail
    for rx, template in _PATTERNS.get(lang, []):
        m = rx.fullmatch(core)
        if m and template == "@decimal_comma":
            return lead + re.sub(r"(\d)\.(\d)", r"\1,\2", core) + trail
        if m:
            groups = {k: (T(v, lang) if k.startswith("t_") and v else (v or ""))
                      for k, v in m.groupdict().items()}
            return lead + template.format(**groups) + trail
    return text


# Component props that carry user-visible text
_TEXT_PROPS = ("children", "label", "placeholder", "title", "description", "alt",
               "data", "marks", "figure", "text", "nothingFoundMessage")


def _walk_plain(obj, lang):
    """Translate strings inside plain dicts/lists (figure JSON, select data)."""
    if isinstance(obj, str):
        return T(obj, lang)
    if type(obj).__module__ == "numpy" and getattr(obj, "dtype", None) is not None:
        # categorical axes arrive as numpy object/str arrays; numbers pass through
        if obj.dtype.kind in ("O", "U", "S"):
            return [_walk_plain(v, lang) for v in obj.tolist()]
        return obj
    if isinstance(obj, list):
        return [_walk_plain(v, lang) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_walk_plain(v, lang) for v in obj)
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            # never touch identifiers, links, styles or values used by callbacks
            if k in ("value", "id", "href", "src", "uid", "meta", "customdata", "font",
                     "line", "marker", "colorscale", "style", "className"):
                out[k] = v
            else:
                out[k] = _walk_plain(v, lang)
        return out
    return obj


def translate(obj, lang=None):
    """Return `obj` (component tree, figure, list, string...) in `lang`.

    English returns the object untouched. Other languages get a translated
    copy; the original (often a module-level layout) is never mutated.
    """
    lang = lang or current_lang()
    if lang == "en":
        return obj
    return _translate(obj, lang)


def _translate(obj, lang):
    if obj is None:
        return None
    if isinstance(obj, str):
        return T(obj, lang)
    if isinstance(obj, (list, tuple)):
        return type(obj)(_translate(v, lang) for v in obj)
    if hasattr(obj, "to_plotly_json") and hasattr(obj, "_prop_names"):  # Dash component
        if type(obj).__name__ == "Store":  # app state, never text
            return obj
        new = copy.copy(obj)
        for prop in _TEXT_PROPS:
            if prop not in obj._prop_names:
                continue
            val = getattr(obj, prop, None)
            if val is None:
                continue
            setattr(new, prop, _translate(val, lang))
        return new
    if hasattr(obj, "to_plotly_json"):  # plotly go.Figure
        return _walk_plain(obj.to_plotly_json(), lang)
    if isinstance(obj, dict):
        return _walk_plain(obj, lang)
    return obj


def translated(fn):
    """Decorator for callbacks: translate whatever the callback returns."""
    import functools

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return translate(fn(*args, **kwargs))
    return wrapper


def catalog_size(lang="es"):
    return len(_CATALOG.get(lang, {}))
