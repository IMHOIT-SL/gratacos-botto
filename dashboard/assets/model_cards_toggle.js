// Global "Chart details" switch: opens or closes every model card (the
// equation / data card under each chart) on every page. Default ON; the
// choice is remembered in this browser only. Each card can still be opened
// or closed on its own.
(function () {
    "use strict";
    var KEY = "amr_mc_open";

    function pref() {
        try {
            var v = window.localStorage.getItem(KEY);
            return v === null ? true : v === "1";
        } catch (e) { return true; }
    }
    function save(on) {
        try { window.localStorage.setItem(KEY, on ? "1" : "0"); } catch (e) { /* private mode */ }
    }
    function syncButton(on) {
        var b = document.getElementById("mc-toggle");
        if (!b) return;
        b.setAttribute("aria-pressed", on ? "true" : "false");
        b.classList.toggle("on", on);
    }
    function applyAll() {
        var on = pref();
        document.querySelectorAll("details.model-card").forEach(function (d) {
            d.open = on;
            d.setAttribute("data-mc-seen", "1");
        });
        syncButton(on);
    }
    function applyNew() {
        var on = pref();
        document.querySelectorAll("details.model-card:not([data-mc-seen])").forEach(function (d) {
            d.open = on;
            d.setAttribute("data-mc-seen", "1");
        });
        syncButton(on);
    }

    document.addEventListener("click", function (e) {
        if (!e.target.closest("#mc-toggle")) return;
        save(!pref());
        applyAll();
    });

    function start() {
        applyNew();
        // Pages are rendered by Dash after load and on every navigation
        new MutationObserver(function () { applyNew(); })
            .observe(document.body, { childList: true, subtree: true });
    }
    if (document.body) start();
    else document.addEventListener("DOMContentLoaded", start);
})();
