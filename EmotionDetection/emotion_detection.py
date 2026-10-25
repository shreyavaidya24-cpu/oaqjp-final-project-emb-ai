"""Watson NLP emotion detection module.

This module wraps the IBM Watson NLP *Emotion Prediction* model used by the
IBM/Coursera *Developing AI Applications with Python and Flask* final project
(oaqjp-final-project-emb-ai).

The function :func:`emotion_detector` sends a piece of text to the Watson NLP
emotion service, extracts the five emotion scores returned for that text,
determines the dominant emotion and returns them as a dictionary in the exact
format required by the course rubric.

Configuration
-------------
The Watson NLP service URL is obtained from the course lab (the Skills Network
Watson NLP service instance). Set it as an environment variable before
running the application::

    export WATSON_NLP_URL="<the Watson NLP service URL from the lab>"

If your lab instance requires an API key, set it too::

    export WATSON_NLP_API_KEY="<your-api-key>"

The function reads these from the environment, so **no secrets are ever
committed to source control**. Without a configured URL the function returns
the course's "blank" result so the UI can surface a clear error.
"""

import os
from typing import Any, Dict, Optional

import requests

# ---------------------------------------------------------------------------
# Service configuration
# ---------------------------------------------------------------------------
# Read from the environment so credentials are never stored in the repo.
# The URL comes from the Watson NLP service instance created in the course lab.
WATSON_NLP_URL = os.environ.get("WATSON_NLP_URL", "")
WATSON_NLP_API_KEY = os.environ.get("WATSON_NLP_API_KEY", "")

# Watson NLP Emotion Prediction model identifier, passed as a gRPC metadata
# header. This is the model the course lab uses.
_EMOTION_MODEL_ID = "emotion_aggregated-workflow_lang_english"

# Timeout for the Watson request, in seconds.
_REQUEST_TIMEOUT = 10

# The five emotions reported by the Watson NLP emotion model.
_EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")

# The "blank" result returned for bad input / HTTP 400 / request errors.
# Per the course, every emotion key maps to ``None`` and ``dominant_emotion``
# is ``None``. This is the exact shape required by the rubric.
_BLANK_RESULT: Dict[str, Optional[Any]] = {
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None,
}


def emotion_detector(text_to_analyze: str) -> Dict[str, Optional[Any]]:
    """Analyze the emotion of ``text_to_analyze`` using the Watson NLP model.

    Parameters
    ----------
    text_to_analyze:
        The text to analyze. May be ``None`` or empty.

    Returns
    -------
    dict
        A dictionary with the keys ``anger``, ``disgust``, ``fear``, ``joy``,
        ``sadness`` (each a float score) and ``dominant_emotion`` (the emotion
        name with the highest score). On HTTP 400, a request exception, or a
        malformed response, every value is ``None`` -- the exact "blank"
        format required by the course.
    """
    # ---- Guard: blank / missing input ------------------------------------
    if not text_to_analyze or not str(text_to_analyze).strip():
        return dict(_BLANK_RESULT)

    # ---- Guard: service not configured -----------------------------------
    if not WATSON_NLP_URL:
        return dict(_BLANK_RESULT)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "grpc-metadata-mm-model-id": _EMOTION_MODEL_ID,
    }

    payload = {
        "raw_document": {"text": text_to_analyze},
    }

    # Optional API-key authentication (some Watson NLP lab instances require
    # it; the classic Skills Network proxy URL does not).
    auth = ("apikey", WATSON_NLP_API_KEY) if WATSON_NLP_API_KEY else None

    try:
        response = requests.post(
            WATSON_NLP_URL,
            headers=headers,
            json=payload,
            auth=auth,
            timeout=_REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException:
        # Network failure, DNS error, timeout, etc. -- return blank result.
        return dict(_BLANK_RESULT)

    # ---- HTTP 400 (bad request) -> blank result --------------------------
    if response.status_code == 400:
        return dict(_BLANK_RESULT)

    # Any other non-2xx status is also treated as a failure.
    if response.status_code != 200:
        return dict(_BLANK_RESULT)

    # ---- Parse the real Watson NLP response ------------------------------
    try:
        body = response.json()
    except ValueError:
        # Not valid JSON.
        return dict(_BLANK_RESULT)

    try:
        emotions = body["emotionPredictions"][0]["emotion"]
    except (KeyError, IndexError, TypeError):
        # The response shape is not what we expect.
        return dict(_BLANK_RESULT)

    # Extract only the five required emotions.
    scores = {key: float(emotions[key]) for key in _EMOTION_KEYS if key in emotions}
    if len(scores) != len(_EMOTION_KEYS):
        # Missing an expected emotion -- treat as malformed.
        return dict(_BLANK_RESULT)

    # Dominant emotion = the one with the highest score.
    dominant_emotion = max(scores, key=scores.get)

    result: Dict[str, Optional[Any]] = dict(scores)
    result["dominant_emotion"] = dominant_emotion
    return result


if __name__ == "__main__":
    # Demonstration entry point. Run from the project root:
    #     python -m EmotionDetection.emotion_detection
    demo = emotion_detector("I am so happy and delighted today!")
    for key, val in demo.items():
        print(f"{key}: {val}")