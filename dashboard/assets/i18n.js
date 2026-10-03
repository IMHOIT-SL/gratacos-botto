// Language switch (EN / ES). The server picks the language from the amr_lang
// cookie (see dashboard/i18n), so switching = set the cookie and reload.
// A ?lang=es|en URL parameter (shareable links) is stored the same way.
(function () {
    "use strict";
    var COOKIE = "amr_lang";
    function getCookie() {
        var m = document.cookie.match(/(?:^|;\s*)amr_lang=(en|es)/);
        return m ? m[1] : null;
    }
    function setCookie(lang) {
        document.cookie = COOKIE + "=" + lang + ";path=/;max-age=31536000;SameSite=Lax";
    }
    var q = new URLSearchParams(window.location.search).get("lang");
    if ((q === "en" || q === "es") && getCookie() !== q) {
        setCookie(q);
        window.location.reload();
        return;
    }
    var lang = getCookie() || ((navigator.language || "").toLowerCase().indexOf("es") === 0 ? "es" : "en");
    document.documentElement.lang = lang;

    document.addEventListener("click", function (e) {
        var btn = e.target.closest("[data-lang]");
        if (!btn) return;
        e.preventDefault();
        var target = btn.getAttribute("data-lang");
        if (target === getCookie() && target === document.documentElement.lang) return;
        setCookie(target);
        var url = new URL(window.location.href);
        url.searchParams.delete("lang");
        window.location.href = url.toString();
    });
})();
