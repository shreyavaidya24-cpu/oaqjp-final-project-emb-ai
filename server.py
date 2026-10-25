"""Flask web server for the Emotion Detector application.

Run from the project root::

    python server.py

Then open http://localhost:5000 in your browser.

The ``/emotionDetector`` route accepts ``textToAnalyze`` via GET query,
POST form data, or POST JSON.
and returns a JSON document with the five emotion scores plus the dominant
emotion, as produced by :func:`EmotionDetection.emotion_detector`.
"""

import os
from typing import Any, Optional

from flask import Flask, jsonify, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Serve the main page."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route() -> Any:
    """Analyze text submitted by the frontend.

    Accepts ``textToAnalyze`` as a GET query parameter, POST form field, or
    POST JSON value. Returns JSON::

        {"anger": 0.1, "disgust": 0.0, "fear": 0.0, "joy": 0.9,
         "sadness": 0.0, "dominant_emotion": "joy"}

    On blank / whitespace-only / missing input it returns HTTP 400 with a
    friendly message. On a backend failure (Watson unreachable / not
    configured) it returns HTTP 502 with a generic error -- no stack traces
    or secrets are exposed to the client.
    """
    # The course expects the parameter name ``textToAnalyze``.
    text_to_analyze: Optional[str] = request.args.get("textToAnalyze")
    if text_to_analyze is None and request.is_json:
        text_to_analyze = (request.get_json(silent=True) or {}).get(
            "textToAnalyze"
        )
    if text_to_analyze is None and request.method == "POST":
        text_to_analyze = request.form.get("textToAnalyze")

    # ---- Blank / whitespace / missing input ----------------------------
    # A single check covers all three invalid cases required by the course:
    # missing parameter, empty string, and whitespace-only string.
    if text_to_analyze is None or not str(text_to_analyze).strip():
        return jsonify({
            "error": "blank_input",
            "message": "Please enter some text to analyze. "
                       "The input cannot be empty or only whitespace.",
        }), 400

    result = emotion_detector(text_to_analyze)

    # ---- Backend / service error ----------------------------------------
    # emotion_detector returns None for every value when Watson fails,
    # returns 400, or is unconfigured.
    if result.get("dominant_emotion") is None:
        return jsonify({
            "error": "service_error",
            "message": "The emotion analysis service could not process the "
                       "request. Please try again later.",
        }), 502

    # ---- Success ---------------------------------------------------------
    return jsonify(result)


def main() -> None:
    """Start the Flask development server."""
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()