"""
/live: one light, phone-first page for an audience that arrives from a QR code.

Plain Flask route (no Dash shell, no callbacks): the four impact figures, the
resistance target (assets/impact_network.js) and a scenario slider computed
in the browser with the same closed form as scenario_crossing_year(). Nothing
is computed per interaction on the server, so a full room can open it at once.
Installable as a home-screen app through /live/manifest.webmanifest.
"""

import datetime as _dt
import html as _h
import json

from flask import Response, request

from data.amr_data import SUPER_EXP_PARAMS as P, CRITICAL_THRESHOLD
from i18n import T, current_lang
from pages import impact

PAPER_URL = "https://doi.org/10.5281/zenodo.21898960"
MURRAY_URL = "https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext"
AWARE_URL = "https://www.who.int/publications/i/item/WHO-MHP-HPS-EML-2023.04"

# Every user-visible string, in English; Spanish lives in i18n/es/live.json.
STRINGS = [
    "The Twilight of Antibiotics",
    "The paper's model, live",
    "Until the critical window (2040)",
    "Margin of the index left today (88 in 1990)",
    "Years the resistance odds take to double (9.8 in 1990)",
    "Observed speed-up of the published anchors, 1990-2000 vs 2015-2025",
    "years", "months", "days", "of 100",
    "The human cost, as a single fact: 1.27 million deaths attributable to AMR in 2019",
    "The resistance target",
    "Each point is a pathogen × antibiotic class; the brighter, the higher the % of resistant isolates. Rings, from the outside in: Access (first choice), Watch, Reserve (last resort). The core is the paper's index. Tap a point to see its value.",
    "2025 is published data; other years are an illustration of the model, not a forecast per pathogen.",
    "What if we act?",
    "Move the levers. The percentages are illustrative assumptions: the paper does not quantify any intervention.",
    "Stewardship (slows the base rate r)",
    "New antibiotics (slows the acceleration b)",
    "Starting in",
    "The threshold (95) arrives in",
    "years gained",
    "never, under this extreme assumption",
    "No scenario avoids the threshold; each one only postpones it.",
    "Nothing changes", "Moderate", "Ambitious", "Late (2035)",
    "Open the full app", "Read the paper",
    "Add it to your home screen from the browser menu to open it like an app.",
    "Sources",
]


def _figures(lang):
    today = _dt.date.today()
    tau_now = today.year + (today.timetuple().tm_yday - 1) / 365.25 - 1990
    yrs, mos, days = impact._countdown(today)
    margin = P["K"] - impact._y(tau_now)
    speed = ((impact._anchor(2025) - impact._anchor(2015)) / 10) / ((impact._anchor(2000) - impact._anchor(1990)) / 10)
    t = lambda s: _h.escape(T(s, lang))
    return [
        ("danger", f'{yrs}<small>{t("years")}</small>{mos}<small>{t("months")}</small>{days}<small>{t("days")}</small>',
         t("Until the critical window (2040)")),
        ("warning", f'{impact._fmt(margin, lang, 0)}<small>{t("of 100")}</small>',
         t("Margin of the index left today (88 in 1990)")),
        ("accent", f'{impact._fmt(impact._doubling(tau_now), lang)}<small>{t("years")}</small>',
         t("Years the resistance odds take to double (9.8 in 1990)")),
        ("warning", f'× {impact._fmt(speed, lang)}',
         t("Observed speed-up of the published anchors, 1990-2000 vs 2015-2025")),
    ]


_CSS = """
body.live{background:var(--bg-primary);color:var(--text-primary);font-size:16px}
.lv{max-width:980px;margin:0 auto;padding:20px 16px 48px;display:flex;flex-direction:column;gap:22px}
.lv-top{display:flex;justify-content:space-between;align-items:center;gap:12px}
.lv-top a{color:var(--text-secondary);font-size:.8rem}
.lv-lang{display:flex;gap:6px}
.lv-lang a{border:1px solid var(--border);border-radius:6px;padding:.15rem .55rem;text-decoration:none;color:var(--text-primary)}
.lv-lang a.on{background:var(--accent);border-color:var(--accent);color:#0f1117}
.lv h1{font-family:Georgia,'Times New Roman',serif;font-weight:400;font-size:clamp(1.9rem,6vw,2.8rem);line-height:1.1}
.lv h2{font-size:1.25rem}
.lv .sub{color:var(--text-secondary)}
.lv .stats-row{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:0}
.lv .stat-card{padding:14px 10px;min-width:0}
.lv .stat-card:first-child,.lv .stat-card:last-child{grid-column:1/-1}
.lv .stat-value{font-size:clamp(1.5rem,6vw,2.2rem)}
.lv .stat-label{font-size:.75rem}
@media(min-width:760px){.lv .stats-row{grid-template-columns:repeat(4,minmax(0,1fr))}.lv .stat-card:first-child,.lv .stat-card:last-child{grid-column:auto}}
.lv-card{background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:12px}
.lv-note{font-size:.85rem;color:var(--text-secondary)}
.lv-note a,.lv-cost a{color:var(--accent)}
.lv-cost{border-left:3px solid var(--danger);padding-left:12px}
.lv-presets{display:flex;flex-wrap:wrap;gap:8px}
.lv-presets button{font:500 .9rem var(--font-sans);border:1px solid var(--border);background:transparent;color:var(--text-primary);border-radius:20px;padding:.4rem .8rem;cursor:pointer}
.lv-presets button.on{background:var(--accent);border-color:var(--accent);color:#0f1117}
.lv-ctl{display:flex;flex-direction:column;gap:4px}
.lv-ctl label{display:flex;justify-content:space-between;gap:12px;font-size:.95rem}
.lv-ctl output{font-family:var(--font-mono);color:var(--accent);white-space:nowrap}
.lv-ctl input{width:100%;accent-color:var(--accent);height:28px}
.lv-res{display:flex;align-items:baseline;flex-wrap:wrap;gap:6px 14px}
.lv-res b{font-family:var(--font-mono);font-size:2.6rem;line-height:1;color:var(--warning)}
.lv-res span.gain{font-family:var(--font-mono);color:var(--success)}
.lv-links{display:flex;flex-wrap:wrap;gap:10px}
.lv-links a{flex:1 1 200px;text-align:center;border:1px solid var(--accent);color:var(--accent);border-radius:10px;padding:.7rem;text-decoration:none;font-weight:600}
.lv-links a.solid{background:var(--accent);color:#0f1117}
.lv button:focus-visible,.lv a:focus-visible,.lv input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
"""

_JS = """
(function(){
  var P=%(params)s, TH=%(th)s, el=document.getElementById('lv-scn');
  var s=document.getElementById('lv-s'), p=document.getElementById('lv-p'), st=document.getElementById('lv-t');
  function cross(sv,pv,ys){
    var r=P.r,b=P.b,gs0=Math.log(P.A*TH/(P.K-TH)),ts=ys-1990,gs=r*ts+b*ts*ts;
    if(gs>=gs0) return 1990+(-r+Math.sqrt(r*r+4*b*gs0))/(2*b);
    var r2=r*(1-sv),b2=b*(1-pv),c=gs0-gs+r2*ts+b2*ts*ts;
    if(b2>0) return 1990+(-r2+Math.sqrt(r2*r2+4*b2*c))/(2*b2);
    if(r2>0) return 1990+c/r2;
    return null;
  }
  var base=Math.ceil(cross(0,0,2027)-1e-9);
  function upd(){
    document.getElementById('lv-so').textContent=s.value+' %%';
    document.getElementById('lv-po').textContent=p.value+' %%';
    document.getElementById('lv-to').textContent=st.value;
    var y=cross(s.value/100,p.value/100,+st.value);
    if(y===null){document.getElementById('lv-y').textContent='-';document.getElementById('lv-g').textContent=el.dataset.never;}
    else{y=Math.ceil(y-1e-9);document.getElementById('lv-y').textContent=y;
      document.getElementById('lv-g').textContent='+'+(y-base)+' '+el.dataset.gained;}
    document.querySelectorAll('.lv-presets button').forEach(function(b){
      var v=b.dataset.v.split(',');b.classList.toggle('on',v[0]===s.value&&v[1]===p.value&&v[2]===st.value);});
  }
  [s,p,st].forEach(function(i){i.addEventListener('input',upd);});
  document.querySelectorAll('.lv-presets button').forEach(function(b){b.addEventListener('click',function(){
    var v=b.dataset.v.split(',');s.value=v[0];p.value=v[1];st.value=v[2];upd();});});
  upd();
})();
"""


def _page(lang):
    t = lambda s: _h.escape(T(s, lang))
    q = f"?lang={lang}"
    stats = "".join(f'<div class="stat-card"><div class="stat-value {c}">{v}</div><div class="stat-label">{l}</div></div>'
                    for c, v, l in _figures(lang))
    presets = [("Nothing changes", "0,0,2027"), ("Moderate", "15,30,2027"),
               ("Ambitious", "30,60,2027"), ("Late (2035)", "30,60,2035")]
    pbtn = "".join(f'<button type="button" data-v="{v}">{t(n)}</button>' for n, v in presets)
    model = _h.escape(json.dumps(impact.network_data()), quote=True)
    js = _JS % {"params": json.dumps({k: P[k] for k in ("K", "A", "r", "b")}), "th": CRITICAL_THRESHOLD}
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0f1117">
<title>Resistome · {t("The paper's model, live")}</title>
<link rel="manifest" href="/live/manifest.webmanifest?lang={lang}">
<link rel="icon" href="/assets/live/icon-192.png">
<link rel="apple-touch-icon" href="/assets/live/icon-192.png">
<link rel="stylesheet" href="/assets/style.css">
<style>{_CSS}</style>
</head>
<body class="live">
<main class="lv">
  <div class="lv-top">
    <a href="{PAPER_URL}" target="_blank" rel="noopener">Prieto Gratacós &amp; Botto · Br J Med Health Res 2026</a>
    <div class="lv-lang"><a href="?lang=en" class="{'on' if lang == 'en' else ''}">EN</a><a href="?lang=es" class="{'on' if lang == 'es' else ''}">ES</a></div>
  </div>
  <div><h1>{t("The Twilight of Antibiotics")}</h1><p class="sub">{t("The paper's model, live")}</p></div>
  <div class="stats-row">{stats}</div>
  <p class="lv-cost">{t("The human cost, as a single fact: 1.27 million deaths attributable to AMR in 2019")} (<a href="{MURRAY_URL}" target="_blank" rel="noopener">Murray et al., Lancet 2022</a>).</p>

  <section class="lv-card">
    <h2>{t("The resistance target")}</h2>
    <p class="lv-note">{t("Each point is a pathogen × antibiotic class; the brighter, the higher the % of resistant isolates. Rings, from the outside in: Access (first choice), Watch, Reserve (last resort). The core is the paper's index. Tap a point to see its value.")}</p>
    <div id="impact-net" class="impact-net" data-model="{model}"></div>
    <p class="lv-note">{t("2025 is published data; other years are an illustration of the model, not a forecast per pathogen.")}
      {t("Sources")}: <a href="https://www.who.int/publications/i/item/9789240062702" target="_blank" rel="noopener">WHO GLASS 2022</a> ·
      <a href="https://www.ecdc.europa.eu/en/antimicrobial-resistance/surveillance-and-disease-data/data-ecdc" target="_blank" rel="noopener">ECDC EARS-Net</a> ·
      <a href="https://www.cdc.gov/antimicrobial-resistance/data-research/threats/index.html" target="_blank" rel="noopener">CDC</a> ·
      <a href="{AWARE_URL}" target="_blank" rel="noopener">WHO AWaRe 2023</a></p>
  </section>

  <section class="lv-card" id="lv-scn" data-gained="{t("years gained")}" data-never="{t("never, under this extreme assumption")}">
    <h2>{t("What if we act?")}</h2>
    <p class="lv-note">{t("Move the levers. The percentages are illustrative assumptions: the paper does not quantify any intervention.")}</p>
    <div class="lv-presets">{pbtn}</div>
    <div class="lv-ctl"><label for="lv-s">{t("Stewardship (slows the base rate r)")}<output id="lv-so"></output></label>
      <input id="lv-s" type="range" min="0" max="100" step="5" value="15"></div>
    <div class="lv-ctl"><label for="lv-p">{t("New antibiotics (slows the acceleration b)")}<output id="lv-po"></output></label>
      <input id="lv-p" type="range" min="0" max="100" step="5" value="30"></div>
    <div class="lv-ctl"><label for="lv-t">{t("Starting in")}<output id="lv-to"></output></label>
      <input id="lv-t" type="range" min="2026" max="2045" step="1" value="2027"></div>
    <div class="lv-res" aria-live="polite"><span>{t("The threshold (95) arrives in")}</span><b id="lv-y">-</b><span class="gain" id="lv-g"></span></div>
    <p class="lv-note">{t("No scenario avoids the threshold; each one only postpones it.")}</p>
  </section>

  <div class="lv-links">
    <a class="solid" href="/{q}">{t("Open the full app")}</a>
    <a href="{PAPER_URL}" target="_blank" rel="noopener">{t("Read the paper")}</a>
  </div>
  <p class="lv-note">{t("Add it to your home screen from the browser menu to open it like an app.")}</p>
</main>
<script src="/assets/impact_network.js"></script>
<script>{js}</script>
</body>
</html>"""


def register(server):
    @server.route("/live")
    def live():
        lang = current_lang(request.args.get("lang"))
        resp = Response(_page(lang), mimetype="text/html")
        resp.headers["Cache-Control"] = "no-cache"
        return resp

    @server.route("/live/manifest.webmanifest")
    def live_manifest():
        lang = current_lang(request.args.get("lang"))
        data = {
            "name": "Resistome · " + T("The Twilight of Antibiotics", lang),
            "short_name": "Resistome",
            "start_url": f"/live?lang={lang}",
            "scope": "/",
            "display": "standalone",
            "background_color": "#0f1117",
            "theme_color": "#0f1117",
            "icons": [{"src": "/assets/live/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
                      {"src": "/assets/live/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}],
        }
        return Response(json.dumps(data), mimetype="application/manifest+json")
