// Curated chart toolbar: adds SVG, PNG 3x, CSV-data and full-screen buttons to
// every Plotly chart in the app.
//
// Dash's dcc.Graph draws through the global Plotly.react(gd, {data, layout,
// config}). Custom modebar buttons need JavaScript click handlers, which a
// Python config cannot carry, so this file wraps Plotly.react / Plotly.newPlot
// once and appends the buttons to each chart's config. The rest of the toolbar
// (which built-in tools are kept) is set in Python by components.graph_config().
(function () {
    "use strict";

    // Material Design icons (Apache-2.0), 24x24 filled paths
    var ICONS = {
        svg: "M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z",
        png: "M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z",
        csv: "M20 2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM8 20H4v-4h4v4zm0-6H4v-4h4v4zm0-6H4V4h4v4zm6 12h-4v-4h4v4zm0-6h-4v-4h4v4zm0-6h-4V4h4v4zm6 12h-4v-4h4v4zm0-6h-4v-4h4v4zm0-6h-4V4h4v4z",
        full: "M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"
    };
    function icon(path) { return { width: 24, height: 24, path: path }; }

    function baseName(gd) {
        var opts = gd._context && gd._context.toImageButtonOptions;
        if (opts && opts.filename) return opts.filename;
        var host = gd.closest("[id]");
        return (host && host.id) ? host.id.replace(/[^a-z0-9_-]+/gi, "_") : "amr_chart";
    }

    // ---- CSV: every trace with its x / y (and z for heatmaps) ----
    function cell(v) {
        if (v === null || v === undefined || (typeof v === "number" && isNaN(v))) return "";
        var s = String(v).replace(/<br>/g, " ").replace(/\n/g, " ");
        return /[",]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
    }
    function toArray(a) { return a ? Array.prototype.slice.call(a) : []; }
    function traceRows(gd) {
        var rows = [["series", "x", "y", "value"]];
        (gd.data || []).forEach(function (t, i) {
            var name = t.name || ("series " + (i + 1));
            if (t.z) {
                var zs = toArray(t.z), xs = toArray(t.x), ys = toArray(t.y);
                zs.forEach(function (row, r) {
                    toArray(row).forEach(function (v, c) {
                        rows.push([name, xs[c] !== undefined ? xs[c] : c, ys[r] !== undefined ? ys[r] : r, v]);
                    });
                });
            } else if (t.x || t.y) {
                var x = toArray(t.x), y = toArray(t.y), n = Math.max(x.length, y.length);
                for (var k = 0; k < n; k++) rows.push([name, x[k], y[k], ""]);
            } else if (t.values) {
                var labels = toArray(t.labels), vals = toArray(t.values);
                vals.forEach(function (v, k) { rows.push([name, labels[k], "", v]); });
            }
        });
        return rows.map(function (r) { return r.map(cell).join(","); }).join("\n");
    }
    function downloadText(text, filename) {
        var blob = new Blob(["﻿" + text], { type: "text/csv;charset=utf-8" });
        var a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
    }

    // ---- Full screen: the chart grows to the screen, then restores ----
    function toggleFullscreen(gd) {
        var box = gd.closest(".dash-graph") || gd.parentElement || gd;
        if (document.fullscreenElement) { document.exitFullscreen(); return; }
        if (!box.requestFullscreen) return;
        box.requestFullscreen().then(function () {
            gd._amrPrevHeight = gd.layout ? gd.layout.height : undefined;
            window.Plotly.relayout(gd, { height: window.innerHeight - 32, width: window.innerWidth - 32 });
        }).catch(function () {});
    }
    document.addEventListener("fullscreenchange", function () {
        if (document.fullscreenElement) return;
        document.querySelectorAll(".js-plotly-plot").forEach(function (gd) {
            if (!("_amrPrevHeight" in gd)) return;
            var h = gd._amrPrevHeight;
            delete gd._amrPrevHeight;
            window.Plotly.relayout(gd, { height: h === undefined ? null : h, width: null });
        });
    });

    var BUTTONS = [
        { name: "Download SVG (vector, for the paper)", icon: icon(ICONS.svg),
          click: function (gd) { window.Plotly.downloadImage(gd, { format: "svg", scale: 3, filename: baseName(gd) }); } },
        { name: "Download PNG (3x, high resolution)", icon: icon(ICONS.png),
          click: function (gd) { window.Plotly.downloadImage(gd, { format: "png", scale: 3, filename: baseName(gd) }); } },
        { name: "Download chart data (CSV)", icon: icon(ICONS.csv),
          click: function (gd) { downloadText(traceRows(gd), baseName(gd) + ".csv"); } },
        { name: "Full screen", icon: icon(ICONS.full),
          click: function (gd) { toggleFullscreen(gd); } }
    ];
    BUTTONS.forEach(function (b) { b._amr = true; });

    function patchConfig(cfg) {
        cfg = Object.assign({}, cfg || {});
        if (cfg.displayModeBar === false) return cfg;
        var add = (cfg.modeBarButtonsToAdd || []).filter(function (b) { return !(b && b._amr); });
        cfg.modeBarButtonsToAdd = add.concat(BUTTONS);
        return cfg;
    }

    function wrap(P) {
        if (!P || P.__amrToolbar) return P;
        ["react", "newPlot"].forEach(function (fn) {
            var orig = P[fn];
            if (typeof orig !== "function") return;
            P[fn] = function (gd, a, b, c) {
                // Object form used by dcc.Graph: Plotly.react(gd, {data, layout, config, frames})
                if (a && !Array.isArray(a) && typeof a === "object" && ("data" in a || "layout" in a || "config" in a)) {
                    return orig.call(this, gd, Object.assign({}, a, { config: patchConfig(a.config) }));
                }
                return orig.call(this, gd, a, b, patchConfig(c));
            };
        });
        P.__amrToolbar = true;
        return P;
    }

    // Plotly is loaded lazily by dcc.Graph; wrap it whenever it is assigned.
    if (window.Plotly) {
        wrap(window.Plotly);
    } else {
        var current;
        try {
            Object.defineProperty(window, "Plotly", {
                configurable: true,
                get: function () { return current; },
                set: function (v) { current = wrap(v); }
            });
        } catch (e) {
            var t = setInterval(function () { if (window.Plotly) { wrap(window.Plotly); clearInterval(t); } }, 50);
        }
    }
})();
