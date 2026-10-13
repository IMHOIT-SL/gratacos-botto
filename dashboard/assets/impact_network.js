// Resistance network on the Impact page (#impact-net).
// Each node is one pathogen x antibiotic-class cell of the surveillance
// matrix, lit by its % resistant. 2025 = published data; other years shift
// every cell on the odds scale by the same factor as the paper's index
// (illustrative, see the "network" model card). Layers: WHO AWaRe 2023.
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
            '<div class="inet-box"><canvas width="1440" height="760" role="img" aria-label="' + T.aria + '"></canvas></div>' +
            '<div class="inet-layers">' + [0, 1, 2].map(function (i) {
                return '<div class="inet-lstat" style="border-color:' + LAYER_COL[i] + '"><b>-</b><span>' + T.lit[i] + '</span></div>';
            }).join("") + '</div>';

        var yrEl = host.querySelector(".inet-year"), chip = host.querySelector(".inet-chip"),
            slider = host.querySelector("input"), playBtn = host.querySelector(".inet-play"),
            resetBtn = host.querySelector(".inet-reset"), cv = host.querySelector("canvas"),
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

        var W = cv.width, H = cv.height, left = 240, top = 96, bottom = 40, right = 170;
        var cols = [];
        D.layers.forEach(function (L, li) { L.forEach(function (c) { cols.push({ c: c, li: li }); }); });
        var gapL = 60, usable = W - left - right - gapL * 2 - 120, step = usable / (cols.length - 1);
        var x = left + 120, colX = [];
        cols.forEach(function (o, i) { if (i > 0 && cols[i - 1].li !== o.li) x += gapL; colX.push(x); x += step; });
        var nP = D.pathogens.length;
        var rowY = D.pathogens.map(function (_, i) { return top + i * ((H - top - bottom) / (nP - 1)); });
        var inX = left + 42, inY = (top + H - bottom) / 2;
        var year = 2025, phase = 0, playing = false, last = 0, acc = 0;
        var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        function heat(v) {
            var t = v / 100, a = [34, 48, 70], b = [255, 154, 60], c = [255, 72, 48], m;
            m = t < 0.6 ? a.map(function (q, i) { return q + (b[i] - q) * (t / 0.6); })
                        : b.map(function (q, i) { return q + (c[i] - q) * ((t - 0.6) / 0.4); });
            return "rgb(" + m.map(Math.round).join(",") + ")";
        }

        function draw() {
            var g = P.r + 2 * P.b * (year - 1990), pv = y(year - 1990);
            cx.clearRect(0, 0, W, H);
            cx.fillStyle = "#1a1c24"; cx.fillRect(0, 0, W, H);
            D.layers.forEach(function (_, li) {
                var xs = colX.filter(function (_, i) { return cols[i].li === li; });
                var x0 = xs[0] - 34, x1 = xs[xs.length - 1] + 34;
                cx.fillStyle = "rgba(255,255,255,0.03)"; cx.fillRect(x0, top - 60, x1 - x0, H - top - bottom + 80);
                cx.fillStyle = LAYER_COL[li]; cx.font = "600 18px Inter, Arial, sans-serif"; cx.textAlign = "center";
                cx.fillText(T.layers[li], (x0 + x1) / 2, 30);
            });
            cx.font = "15px Inter, Arial, sans-serif"; cx.fillStyle = "#9aa3b5";
            cols.forEach(function (o, i) {
                cx.save(); cx.translate(colX[i], top - 22); cx.rotate(-0.5); cx.textAlign = "left";
                cx.fillText(T.classes[o.c], 0, 0); cx.restore();
            });
            cx.textAlign = "right"; cx.font = "italic 16px Inter, Arial, sans-serif"; cx.fillStyle = "#c9ced9";
            D.pathogens.forEach(function (p, r) { cx.fillText(p, left - 30, rowY[r] + 5); });

            for (var r = 0; r < nP; r++) {
                var px = inX, py = inY, pval = pv;
                for (var i = 0; i < cols.length; i++) {
                    var v = cell(D.matrix[r][cols[i].c], year);
                    if (v === null) continue;
                    var w = Math.min(pval, v) / 100;
                    cx.strokeStyle = "rgba(255,154,60," + (0.05 + 0.45 * w * w) + ")";
                    cx.lineWidth = 1 + 2.5 * w * w;
                    cx.beginPath(); cx.moveTo(px, py); cx.lineTo(colX[i], rowY[r]); cx.stroke();
                    if (!reduce && w > 0.25) {
                        var f = ((phase * g * 14) + r * 0.13 + i * 0.07) % 1;
                        cx.fillStyle = "rgba(255,220,170," + (0.8 * w) + ")";
                        cx.beginPath(); cx.arc(px + (colX[i] - px) * f, py + (rowY[r] - py) * f, 2.2 + 2 * w, 0, 7); cx.fill();
                    }
                    px = colX[i]; py = rowY[r]; pval = v;
                }
            }
            var lit = [0, 0, 0], tot = [0, 0, 0];
            for (r = 0; r < nP; r++) {
                cols.forEach(function (o, i) {
                    var v = cell(D.matrix[r][o.c], year), X = colX[i], Y = rowY[r];
                    if (v === null) { cx.strokeStyle = "#2f3446"; cx.lineWidth = 1; cx.beginPath(); cx.arc(X, Y, 4, 0, 7); cx.stroke(); return; }
                    tot[o.li]++; if (v >= 50) lit[o.li]++;
                    var rad = 9 + 9 * (v / 100), gl = v / 100;
                    var gr = cx.createRadialGradient(X, Y, 0, X, Y, rad * 3.2);
                    gr.addColorStop(0, "rgba(255,170,90," + (0.55 * gl * gl) + ")"); gr.addColorStop(1, "rgba(255,120,60,0)");
                    cx.fillStyle = gr; cx.beginPath(); cx.arc(X, Y, rad * 3.2, 0, 7); cx.fill();
                    cx.fillStyle = heat(v); cx.beginPath(); cx.arc(X, Y, rad, 0, 7); cx.fill();
                    if (v >= 50) {
                        cx.fillStyle = "#0d1119"; cx.font = "600 12px Inter, Arial, sans-serif"; cx.textAlign = "center";
                        cx.fillText(Math.round(v), X, Y + 4);
                    }
                });
            }
            var gi = cx.createRadialGradient(inX, inY, 0, inX, inY, 70);
            gi.addColorStop(0, "rgba(255,120,60," + (0.25 + 0.6 * pv / 100) + ")"); gi.addColorStop(1, "rgba(255,120,60,0)");
            cx.fillStyle = gi; cx.beginPath(); cx.arc(inX, inY, 70, 0, 7); cx.fill();
            cx.fillStyle = heat(pv); cx.beginPath(); cx.arc(inX, inY, 26, 0, 7); cx.fill();
            cx.fillStyle = "#0d1119"; cx.font = "600 16px Inter, Arial, sans-serif"; cx.textAlign = "center";
            cx.fillText(Math.round(pv), inX, inY + 6);
            cx.fillStyle = "#e8eaed"; cx.font = "13px Inter, Arial, sans-serif";
            cx.fillText(T.pressure, inX, inY + 48); cx.fillText(T.index, inX, inY + 64);
            for (var k = 0; k < 3; k++) stats[k].textContent = lit[k] + " / " + tot[k];
        }

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
