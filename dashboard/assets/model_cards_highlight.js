// Term highlighting in model cards: the term picked in a card is painted
// yellow everywhere it appears in that card (symbolic, numeric and live
// equations, and its row in the terms table). Equation symbols carry the
// class t-<term> through \mmlToken (see model_cards.py, SYMS / fill()).
(function () {
    "use strict";

    function paint(card) {
        var input = card.querySelector("input.mc-chip-input:checked");
        var key = input ? input.value : null;
        card.querySelectorAll(".mc-hl").forEach(function (el) { el.classList.remove("mc-hl"); });
        if (!key) return;
        var sel = ".t-" + (window.CSS && CSS.escape ? CSS.escape(key) : key);
        card.querySelectorAll(sel).forEach(function (el) { el.classList.add("mc-hl"); });
    }
    function paintAll() {
        document.querySelectorAll(".model-card").forEach(paint);
    }

    document.addEventListener("change", function (e) {
        if (!e.target.matches || !e.target.matches("input.mc-chip-input")) return;
        var card = e.target.closest(".model-card");
        if (card) paint(card);
    });

    // Equations are typeset asynchronously and live equations are replaced by
    // callbacks, so repaint (debounced) whenever the page changes.
    var pending = null;
    function schedule() {
        if (pending) return;
        pending = setTimeout(function () { pending = null; paintAll(); }, 120);
    }
    function start() {
        paintAll();
        new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
    }
    if (document.body) start();
    else document.addEventListener("DOMContentLoaded", start);
})();
