// "Share" button in the header: opens the dialog with the QR code and link to
// the phone page (/live). The dialog itself is built by app._share_dialog().
(function () {
    "use strict";
    document.addEventListener("click", function (ev) {
        var dlg = document.getElementById("share-dialog");
        if (!dlg) return;
        if (ev.target.closest("#share-open")) {
            if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
        } else if (ev.target.closest("#share-close") || ev.target === dlg) {   // button or backdrop
            dlg.close ? dlg.close() : dlg.removeAttribute("open");
        } else if (ev.target.closest("#share-copy")) {
            var btn = ev.target.closest("#share-copy"), url = btn.getAttribute("data-url");
            var done = function () {
                var old = btn.textContent; btn.textContent = btn.getAttribute("data-done");
                setTimeout(function () { btn.textContent = old; }, 1800);
            };
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(url).then(done, function () { selectUrl(dlg); });
            } else { selectUrl(dlg); }
        }
    });
    // clipboard refused: select the link so it can be copied by hand
    function selectUrl(dlg) {
        var code = dlg.querySelector(".share-url"), r = document.createRange();
        r.selectNodeContents(code); var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
    }
})();
