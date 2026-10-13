// Resistance network on the Impact page (#impact-net).
// Each node is one pathogen x antibiotic-class cell of the surveillance
// matrix, lit by its % resistant. 2025 = published data; other years shift
// every cell on the odds scale by the same factor as the paper's index
// (illustrative, see the "network" model card). Rings: WHO AWaRe 2023.
// Deterministic: no randomness, only the year chosen by the viewer.
(function () {
    "use strict";

    var TXT = {
        en: {
            layers: ["ACCESS", "WATCH", "RESERVE"],
            classes: ["Penicillins", "Cephalosp. 3G", "Carbapenems", "Fluoroquinolones", "Aminoglycosides",
                      "Vancomycin", "Polymyxins", "Macrolides", "Tetracyclines", "SMX/TMP"],
            real: "Published data", fwd: "Illustrative projection", back: "Illustrative back-projection",
            play: "▶ Raise the pressure", pause: "❚❚ Pause", reset: "Back to 2025",
            year: "Year", pressure: "pressure", index: "(index)",
            lit: ["Access: lit neurons (≥ 50 % resistant)", "Watch: lit neurons", "Reserve (last resort): lit neurons"],
            aria: "Network of pathogen by antibiotic neurons, lit by % resistant"
        },
        es: {
            layers: ["ACCESO", "VIGILANCIA", "RESERVA"],
            classes: ["Penicilinas", "Cefalosp. 3G", "Carbapenémicos", "Fluoroquinolonas", "Aminoglucósidos",
                      "Vancomicina", "Polimixinas", "Macrólidos", "Tetraciclinas", "SMX/TMP"],
            real: "Dato publicado", fwd: "Proyección ilustrativa", back: "Retroproyección ilustrativa",
            play: "▶ Subir la presión", pause: "❚❚ Pausa", reset: "Volver a 2025",
            year: "Año", pressure: "presión", index: "(índice)",
            lit: ["Acceso: neuronas encendidas (≥ 50 % resistencia)", "Vigilancia: neuronas encendidas", "Reserva (último recurso): neuronas encendidas"],
            aria: "Red de neuronas patógeno por antibiótico, iluminadas según el % de resistencia"
        }
    };
    var LAYER_COL = ["#6c8fb3", "#ff9a3c", "#ff5a3c"];

    function init(host) {
        host.setAttribute("data-init", "1");
        var D = JSON.parse(host.getAttribute("data-model"));
        var lang = (document.documentElement.lang || "en").slice(0, 2) === "es" ? "es" : "en";
        var T = TXT[lang];
        var P = D.params;

        host.innerHTML =
            '<div class="inet-controls">' +
            '<span class="inet-year" aria-live="polite"></span>' +
            '<span class="inet-chip"></span>' +
            '<input type="range" min="1990" max="2060" step="1" value="2025" aria-label="' + T.year + '">' +
            '<button type="button" class="inet-play">' + T.play + '</button>' +
            '<button type="button" class="inet-reset">' + T.reset + '</button>' +
            '</div>' +
            '<div class="inet-box"><canvas width="1200" height="880" role="img" aria-label="' + T.aria + '"></canvas><div class="inet-tip" hidden></div></div>' +
            '<div class="inet-layers">' + [0, 1, 2].map(function (i) {
                return '<div class="inet-lstat" style="border-color:' + LAYER_COL[i] + '"><b>-</b><span>' + T.lit[i] + '</span></div>';
            }).join("") + '</div>';

        var yrEl = host.querySelector(".inet-year"), chip = host.querySelector(".inet-chip"),
            slider = host.querySelector("input"), playBtn = host.querySelector(".inet-play"),
            resetBtn = host.querySelector(".inet-reset"), cv = host.querySelector("canvas"), tip = host.querySelector(".inet-tip"),
            stats = host.querySelectorAll(".inet-lstat b"), cx = cv.getContext("2d");

        var y = function (t) { return P.K / (1 + P.A * Math.exp(-(P.r * t + P.b * t * t))); };
        var odds = function (p) { return p / (P.K - p); };
        var O25 = odds(y(35));
        function cell(p, yr) {
            if (p === null) return null;
            if (yr === 2025) return p;
            var pp = Math.min(Math.max(p, 0.5), 99.5);
            var o = (pp / (100 - pp)) * odds(y(yr - 1990)) / O25;
            return 100 * o / (1 + o);
        }

        // Target layout: one sector per pathogen, AWaRe rings from the outside in
        // (Access, Watch, Reserve), the paper's index at the core.
        var W = 1200, H = 880, C0 = 600, C1 = 440, GAP = 0.62, nP = D.pathogens.length;
        var SEC = (2 * Math.PI - GAP) / nP, RING = [354, 244, 128];
        var RAD = [[372, 336], [262, 226], [128, 128]], SPREAD = [0.105, 0.092, 0];
        var dpr = Math.min(2, window.devicePixelRatio || 1);
        cv.width = W * dpr; cv.height = H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0);
        var theta = function (p) { return -Math.PI / 2 + GAP / 2 + SEC * (p + 0.5); };
        var nodes = [];
        for (var p = 0; p < nP; p++) {
            D.layers.forEach(function (cls, li) {
                cls.forEach(function (c, k) {
                    if (D.matrix[p][c] === null) return;
                    var a = theta(p) + (k - (cls.length - 1) / 2) * SPREAD[li], rr = RAD[li][k % 2];
                    nodes.push({ p: p, c: c, li: li, x: C0 + rr * Math.cos(a), y: C1 + rr * Math.sin(a) });
                });
            });
        }
        var links = [];                                  // escalation paths inside each pathogen
        nodes.forEach(function (a, i) {
            nodes.forEach(function (b, j) { if (a.p === b.p && b.li === a.li + 1) links.push([i, j]); });
        });
        var year = 2025, phase = 0, playing = false, last = 0, acc = 0, hover = -1;
        var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        function heat(v) {
            var t = v / 100, a = [40, 52, 74], b = [255, 154, 60], c = [255, 72, 48], m;
            m = t < 0.6 ? a.map(function (q, i) { return q + (b[i] - q) * (t / 0.6); })
                        : b.map(function (q, i) { return q + (c[i] - q) * ((t - 0.6) / 0.4); });
            return "rgb(" + m.map(Math.round).join(",") + ")";
        }

        function draw() {
            var g = P.r + 2 * P.b * (year - 1990), pv = y(year - 1990);
            cx.fillStyle = "#0e1018"; cx.fillRect(0, 0, W, H);
            RING.forEach(function (rr, li) {
                cx.strokeStyle = LAYER_COL[li]; cx.globalAlpha = 0.09; cx.lineWidth = li === 2 ? 54 : 58;
                cx.beginPath(); cx.arc(C0, C1, rr, 0, 7); cx.stroke(); cx.globalAlpha = 1;
                cx.fillStyle = LAYER_COL[li]; cx.textAlign = "center"; cx.font = "600 15px Arial, Helvetica, sans-serif";
                cx.fillText(T.layers[li], C0, C1 - rr + 5);   // ring names sit in the empty top gap
            });
            cx.font = "italic 16px Arial, Helvetica, sans-serif"; cx.fillStyle = "#c9ced9";
            D.pathogens.forEach(function (name, i) {
                var th = theta(i), co = Math.cos(th);
                cx.textAlign = Math.abs(co) < 0.2 ? "center" : (co > 0 ? "left" : "right");
                cx.fillText(name, C0 + 412 * co, C1 + 412 * Math.sin(th) + 5);
            });
            nodes.forEach(function (n) { n.v = cell(D.matrix[n.p][n.c], year); });
            links.forEach(function (e, ei) {
                var a = nodes[e[0]], b = nodes[e[1]], w = Math.min(a.v, b.v) / 100;
                cx.strokeStyle = "rgba(255,154,60," + (0.04 + 0.5 * w * w) + ")"; cx.lineWidth = 0.6 + 2.2 * w * w;
                cx.beginPath(); cx.moveTo(a.x, a.y); cx.lineTo(b.x, b.y); cx.stroke();
                if (!reduce && w > 0.35) {
                    var f = (phase * g * 12 + ei * 0.137) % 1;
                    cx.fillStyle = "rgba(255,225,180," + (0.85 * w) + ")";
                    cx.beginPath(); cx.arc(a.x + (b.x - a.x) * f, a.y + (b.y - a.y) * f, 1.6 + 1.8 * w, 0, 7); cx.fill();
                }
            });
            var lit = [0, 0, 0], tot = [0, 0, 0];
            nodes.forEach(function (n, i) {
                var v = n.v, rad = 4 + 8 * v / 100, gl = v / 100;
                tot[n.li]++; if (v >= 50) lit[n.li]++;
                var gr = cx.createRadialGradient(n.x, n.y, 0, n.x, n.y, rad * 3.4);
                gr.addColorStop(0, "rgba(255,170,90," + (0.6 * gl * gl) + ")"); gr.addColorStop(1, "rgba(255,120,60,0)");
                cx.fillStyle = gr; cx.beginPath(); cx.arc(n.x, n.y, rad * 3.4, 0, 7); cx.fill();
                cx.fillStyle = heat(v); cx.beginPath(); cx.arc(n.x, n.y, rad, 0, 7); cx.fill();
                if (i === hover) { cx.strokeStyle = "#fff"; cx.lineWidth = 2; cx.stroke(); }
            });
            var gi = cx.createRadialGradient(C0, C1, 0, C0, C1, 90);
            gi.addColorStop(0, "rgba(255,110,60," + (0.2 + 0.7 * pv / 100) + ")"); gi.addColorStop(1, "rgba(255,110,60,0)");
            cx.fillStyle = gi; cx.beginPath(); cx.arc(C0, C1, 90, 0, 7); cx.fill();
            cx.fillStyle = heat(pv); cx.beginPath(); cx.arc(C0, C1, 44, 0, 7); cx.fill();
            cx.fillStyle = "#10121a"; cx.textAlign = "center"; cx.font = "600 28px Georgia, 'Times New Roman', serif";
            cx.fillText(Math.round(pv), C0, C1 + 10);
            cx.fillStyle = "#9aa1b2"; cx.font = "13px Arial, Helvetica, sans-serif";
            cx.fillText(T.pressure, C0, C1 + 64); cx.fillText(T.index, C0, C1 + 80);
            for (var k = 0; k < 3; k++) stats[k].textContent = lit[k] + " / " + tot[k];
        }

        cv.addEventListener("mousemove", function (ev) {
            var r = cv.getBoundingClientRect(), s = W / r.width, mx = (ev.clientX - r.left) * s, my = (ev.clientY - r.top) * s;
            var best = -1, bd = 22;
            nodes.forEach(function (n, i) { var d = Math.hypot(n.x - mx, n.y - my); if (d < bd) { bd = d; best = i; } });
            hover = best;
            if (best < 0) tip.hidden = true;
            else {
                var n = nodes[best];
                tip.innerHTML = "<i>" + D.pathogens[n.p] + "</i> × " + T.classes[n.c] + " · <b>" + Math.round(n.v) + " %</b>";
                tip.hidden = false;
                tip.style.left = Math.min(ev.clientX - r.left + 14, r.width - 260) + "px";
                tip.style.top = (ev.clientY - r.top + 14) + "px";
            }
            draw();
        });
        cv.addEventListener("mouseleave", function () { hover = -1; tip.hidden = true; draw(); });

        function setYear(v) {
            year = +v; yrEl.textContent = year; slider.value = year;
            if (year === 2025) { chip.textContent = T.real; chip.className = "inet-chip real"; }
            else { chip.textContent = year < 2025 ? T.back : T.fwd; chip.className = "inet-chip ill"; }
            draw();
        }
        function stop() { playing = false; playBtn.textContent = T.play; }
        slider.addEventListener("input", function () { stop(); setYear(slider.value); });
        resetBtn.addEventListener("click", function () { stop(); setYear(2025); });
        playBtn.addEventListener("click", function () {
            if (playing) { stop(); return; }
            if (year >= 2060) setYear(1990);
            playing = true; playBtn.textContent = T.pause;
        });

        function loop(ts) {
            if (!document.body.contains(cv)) return;           // page left: stop
            var dt = Math.min(50, ts - last); last = ts; phase += dt / 1000;
            if (playing) {
                acc += dt;
                if (acc > 260) { acc = 0; if (year < 2060) setYear(year + 1); else stop(); }
            }
            draw();
            window.requestAnimationFrame(loop);
        }
        setYear(2025);
        if (!reduce) window.requestAnimationFrame(loop);
        else playBtn.addEventListener("click", function tick() {
            // reduced motion: step through the years without the travelling pulses
            var id = window.setInterval(function () {
                if (!playing || !document.body.contains(cv)) { window.clearInterval(id); return; }
                if (year < 2060) setYear(year + 1); else { stop(); window.clearInterval(id); }
            }, 260);
        });
    }

    function scan() {
        var el = document.querySelector("#impact-net:not([data-init])");
        if (el && el.getAttribute("data-model")) init(el);
    }
    new MutationObserver(scan).observe(document.documentElement, { childList: true, subtree: true });
    document.addEventListener("DOMContentLoaded", scan);
})();
