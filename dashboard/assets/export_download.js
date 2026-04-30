// Export Studio: Download button handler
// Attaches to #btn-download-chart and calls Plotly.downloadImage on the Plotly graph div
document.addEventListener("click", function(e) {
    var btn = e.target.closest("#btn-download-chart");
    if (!btn) return;

    var statusEl = document.getElementById("download-status");

    // Find the actual Plotly graph div inside the dcc.Graph wrapper
    var wrapper = document.getElementById("export-preview");
    if (!wrapper || !window.Plotly) {
        if (statusEl) statusEl.textContent = "Chart not loaded yet. Select a chart first.";
        return;
    }

    // The real Plotly div is the one with ._fullData or .classList contains "js-plotly-plot"
    var graphDiv = wrapper.querySelector(".js-plotly-plot") || wrapper;
    if (!graphDiv._fullData && !graphDiv.data) {
        // Try the wrapper itself (some Dash versions use the wrapper directly)
        graphDiv = wrapper;
    }

    // Read format from radio buttons inside #export-format
    var fmt = "svg";
    var fmtContainer = document.getElementById("export-format");
    if (fmtContainer) {
        var checked = fmtContainer.querySelector("input:checked");
        if (checked) fmt = checked.value;
    }

    // Read scale from radio buttons inside #export-scale
    var scale = 2;
    var scaleContainer = document.getElementById("export-scale");
    if (scaleContainer) {
        var checked = scaleContainer.querySelector("input:checked");
        if (checked) scale = parseFloat(checked.value);
    }

    var actualFmt = fmt || "svg";
    var filename = "amr_export_" + actualFmt + "_" + scale + "x";

    if (statusEl) statusEl.textContent = "Exporting...";

    try {
        Plotly.downloadImage(graphDiv, {
            format: actualFmt,
            filename: filename,
            scale: scale
        }).then(function() {
            if (statusEl) statusEl.textContent = "Download complete.";
        }).catch(function(err) {
            if (statusEl) statusEl.textContent = "Error: " + err.message;
        });
    } catch(err) {
        // Fallback: try Plotly.toImage + manual download
        try {
            Plotly.toImage(graphDiv, {format: actualFmt, scale: scale}).then(function(dataUrl) {
                var a = document.createElement("a");
                a.href = dataUrl;
                a.download = filename + "." + actualFmt;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                if (statusEl) statusEl.textContent = "Download complete.";
            });
        } catch(err2) {
            if (statusEl) statusEl.textContent = "Export failed. Use the camera icon in the chart toolbar.";
        }
    }
});
