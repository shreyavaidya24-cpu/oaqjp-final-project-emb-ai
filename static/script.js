/* ------------------------------------------------------------------ */
/* Emotion Detector - script.js                                        */
/* Talks to the real Flask backend. Never fabricates results.          */
/* ------------------------------------------------------------------ */

(function () {
    "use strict";

    const EMOTIONS = ["anger", "disgust", "fear", "joy", "sadness"];

    const els = {
        text: document.getElementById("textToAnalyze"),
        analyzeBtn: document.getElementById("analyzeBtn"),
        clearBtn: document.getElementById("clearBtn"),
        message: document.getElementById("messageArea"),
        results: document.getElementById("results"),
        grid: document.getElementById("emotionGrid"),
        dominantSummary: document.getElementById("dominantSummary"),
        chips: document.querySelectorAll(".chip"),
    };

    // ---- Helpers ---------------------------------------------------
    function showMessage(type, text) {
        els.message.hidden = false;
        els.message.className = "message-area " + type;
        els.message.textContent = text;
    }

    function hideMessage() {
        els.message.hidden = true;
        els.message.textContent = "";
    }

    function hideResults() {
        els.results.hidden = true;
        els.grid.innerHTML = "";
        els.dominantSummary.textContent = "";
    }

    function setLoading(isLoading) {
        els.analyzeBtn.classList.toggle("is-loading", isLoading);
        els.analyzeBtn.disabled = isLoading;
        els.clearBtn.disabled = isLoading;
    }

    function fmtScore(value) {
        if (value === null || value === undefined) return "0.000";
        return Number(value).toFixed(3);
    }

    // ---- Render ----------------------------------------------------
    function renderResults(data) {
        hideMessage();
        const dominant = data.dominant_emotion;

        els.dominantSummary.innerHTML =
            'The dominant emotion is <span class="dom-name">' +
            String(dominant).charAt(0).toUpperCase() + String(dominant).slice(1) +
            "</span>.";

        els.grid.innerHTML = "";
        EMOTIONS.forEach((emo) => {
            const score = data[emo];
            const pct = Math.max(0, Math.min(100, Number(score || 0) * 100));

            const card = document.createElement("div");
            card.className = "emotion-card" + (emo === dominant ? " is-dominant" : "");
            card.setAttribute("data-emotion", emo);

            card.innerHTML =
                '<div class="emotion-name">' + emo + '</div>' +
                '<div class="emotion-score">' + fmtScore(score) + '</div>' +
                '<div class="progress"><div class="bar" style="width:0%"></div></div>' +
                '<span class="dominant-badge">Dominant</span>';

            els.grid.appendChild(card);

            // Animate the bar after insertion.
            requestAnimationFrame(() => {
                const bar = card.querySelector(".bar");
                if (bar) bar.style.width = pct.toFixed(1) + "%";
            });
        });

        els.results.hidden = false;
        els.results.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // ---- Network ---------------------------------------------------
    async function analyze() {
        hideMessage();
        const text = els.text.value.trim();

        if (!text) {
            hideResults();
            showMessage("warning",
                "Please enter some text to analyze. The input cannot be empty or only whitespace.");
            els.text.focus();
            return;
        }

        setLoading(true);
        try {
            const response = await fetch("/emotionDetector", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ textToAnalyze: text }),
            });

            const payload = await response.json().catch(() => ({}));

            if (!response.ok) {
                hideResults();
                if (response.status === 400 && payload && payload.error === "blank_input") {
                    showMessage("warning", payload.message);
                } else if (response.status === 502 || (payload && payload.error === "service_error")) {
                    showMessage("error",
                        payload.message ||
                        "The emotion analysis service could not be reached. " +
                        "Make sure Watson NLP is configured and the Flask server is running.");
                } else {
                    showMessage("error",
                        (payload && payload.message) ||
                        ("Request failed (HTTP " + response.status + ")."));
                }
                return;
            }

            // Guard: never display a partial / fabricated result.
            if (!payload || payload.dominant_emotion === null || payload.dominant_emotion === undefined) {
                hideResults();
                showMessage("error",
                    "The backend did not return a valid analysis. " +
                    "Check that Watson NLP credentials are configured.");
                return;
            }

            renderResults(payload);
        } catch (err) {
            hideResults();
            showMessage("error",
                "Could not reach the server. Make sure Flask is running " +
                "and you are viewing the page through http://localhost:5000.");
        } finally {
            setLoading(false);
        }
    }

    // ---- Wire up events --------------------------------------------
    els.analyzeBtn.addEventListener("click", analyze);

    els.clearBtn.addEventListener("click", () => {
        els.text.value = "";
        hideMessage();
        hideResults();
        els.text.focus();
    });

    els.chips.forEach((chip) => {
        chip.addEventListener("click", () => {
            els.text.value = chip.getAttribute("data-example");
            els.text.focus();
            hideMessage();
            hideResults();
        });
    });

    // Ctrl/Cmd+Enter triggers analysis from the textarea.
    els.text.addEventListener("keydown", (ev) => {
        if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") {
            ev.preventDefault();
            analyze();
        }
    });
})();