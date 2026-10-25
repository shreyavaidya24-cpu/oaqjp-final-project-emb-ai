"""Unit tests for EmotionDetection.emotion_detection.

Run from the project root with::

    python -m unittest -v test_emotion_detection.py

The Watson NLP service is mocked so the tests run offline and do not depend
on credentials. They exercise the *real* :func:`emotion_detector`
implementation; only the outbound HTTP call is replaced.
"""

import unittest
from unittest.mock import MagicMock, patch

import requests

from EmotionDetection.emotion_detection import emotion_detector


# A realistic Watson NLP Emotion Prediction response payload.
# The model returns ``emotionPredictions`` -> list of predictions, each with
# an ``emotion`` dict holding the five scores.
_VALID_RESPONSE = {
    "language": "en",
    "emotionPredictions": [
        {
            "emotion": {
                "sadness": 0.052251,
                "joy": 0.917211,
                "fear": 0.0186332,
                "disgust": 0.0206774,
                "anger": 0.0126476,
            },
            "target": "",
            "sentence_id": 0,
        }
    ],
}


def _make_response(status_code=200, json_body=None):
    """Build a fake ``requests.Response`` object."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_body if json_body is not None else _VALID_RESPONSE
    return resp


class EmotionDetectorTests(unittest.TestCase):
    """Tests covering the course rubric requirements."""

    # ---- Happy path -------------------------------------------------
    @patch("EmotionDetection.emotion_detection.requests.post")
    @patch(
        "EmotionDetection.emotion_detection.WATSON_NLP_URL",
        "https://example.watson.cloud.ibm.com",
    )
    @patch("EmotionDetection.emotion_detection.WATSON_NLP_API_KEY", "test-key")
    def test_returns_five_emotion_keys(self, mock_post):
        """All five required emotion keys must be present with float scores."""
        mock_post.return_value = _make_response()
        result = emotion_detector("I am very happy today!")
        for key in ("anger", "disgust", "fear", "joy", "sadness"):
            self.assertIn(key, result, f"missing emotion key: {key}")
            self.assertIsInstance(result[key], float)

    @patch("EmotionDetection.emotion_detection.requests.post")
    @patch(
        "EmotionDetection.emotion_detection.WATSON_NLP_URL",
        "https://example.watson.cloud.ibm.com",
    )
    @patch("EmotionDetection.emotion_detection.WATSON_NLP_API_KEY", "test-key")
    def test_dominant_emotion_is_joy(self, mock_post):
        """The dominant emotion for the joyful example must be joy."""
        mock_post.return_value = _make_response()
        result = emotion_detector("I am very happy today!")
        self.assertEqual(result["dominant_emotion"], "joy")

    @patch("EmotionDetection.emotion_detection.requests.post")
    @patch(
        "EmotionDetection.emotion_detection.WATSON_NLP_URL",
        "https://example.watson.cloud.ibm.com",
    )
    @patch("EmotionDetection.emotion_detection.WATSON_NLP_API_KEY", "test-key")
    def test_correct_output_format(self, mock_post):
        """The returned dictionary must have exactly the required keys."""
        mock_post.return_value = _make_response()
        result = emotion_detector("I am very happy today!")
        expected_keys = {"anger", "disgust", "fear", "joy", "sadness",
                         "dominant_emotion"}
        self.assertEqual(set(result.keys()), expected_keys)

    @patch("EmotionDetection.emotion_detection.requests.post")
    @patch(
        "EmotionDetection.emotion_detection.WATSON_NLP_URL",
        "https://example.watson.cloud.ibm.com",
    )
    @patch("EmotionDetection.emotion_detection.WATSON_NLP_API_KEY", "test-key")
    def test_dominant_matches_highest_score(self, mock_post):
        """The dominant emotion must correspond to the highest score."""
        mock_post.return_value = _make_response()
        result = emotion_detector("I am very happy today!")
        scores = {k: result[k] for k in
                  ("anger", "disgust", "fear", "joy", "sadness")}
        self.assertEqual(result["dominant_emotion"], max(scores, key=scores.get))

    # ---- HTTP 400 ---------------------------------------------------
    @patch("EmotionDetection.emotion_detection.requests.post")
    @patch(
        "EmotionDetection.emotion_detection.WATSON_NLP_URL",
        "https://example.watson.cloud.ibm.com",
    )
    @patch("EmotionDetection.emotion_detection.WATSON_NLP_API_KEY", "test-key")
    def test_http_400_returns_blank(self, mock_post):
        """HTTP 400 must return None for every emotion and dominant_emotion."""
        mock_post.return_value = _make_response(status_code=400, json_body={})
        result = emotion_detector("some text")
        for key in ("anger", "disgust", "fear", "joy", "sadness",
                    "dominant_emotion"):
            self.assertIsNone(result[key], f"{key} should be None on HTTP 400")

    # ---- Request exceptions ----------------------------------------
    @patch("EmotionDetection.emotion_detection.requests.post")
    @patch(
        "EmotionDetection.emotion_detection.WATSON_NLP_URL",
        "https://example.watson.cloud.ibm.com",
    )
    @patch("EmotionDetection.emotion_detection.WATSON_NLP_API_KEY", "test-key")
    def test_request_exception_returns_blank(self, mock_post):
        """A network/timeout error must return the blank result, not raise."""
        mock_post.side_effect = requests.exceptions.ConnectionError("boom")
        result = emotion_detector("some text")
        self.assertIsNone(result["dominant_emotion"])
        self.assertIsNone(result["anger"])

    # ---- Malformed responses ---------------------------------------
    @patch("EmotionDetection.emotion_detection.requests.post")
    @patch(
        "EmotionDetection.emotion_detection.WATSON_NLP_URL",
        "https://example.watson.cloud.ibm.com",
    )
    @patch("EmotionDetection.emotion_detection.WATSON_NLP_API_KEY", "test-key")
    def test_malformed_json_returns_blank(self, mock_post):
        """Non-JSON body must return the blank result."""
        resp = MagicMock()
        resp.status_code = 200
        resp.json.side_effect = ValueError("not json")
        mock_post.return_value = resp
        result = emotion_detector("some text")
        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    @patch(
        "EmotionDetection.emotion_detection.WATSON_NLP_URL",
        "https://example.watson.cloud.ibm.com",
    )
    @patch("EmotionDetection.emotion_detection.WATSON_NLP_API_KEY", "test-key")
    def test_missing_emotion_node_returns_blank(self, mock_post):
        """A JSON response without emotionPredictions must return blank."""
        mock_post.return_value = _make_response(
            status_code=200, json_body={"language": "en"}
        )
        result = emotion_detector("some text")
        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    @patch(
        "EmotionDetection.emotion_detection.WATSON_NLP_URL",
        "https://example.watson.cloud.ibm.com",
    )
    @patch("EmotionDetection.emotion_detection.WATSON_NLP_API_KEY", "test-key")
    def test_missing_emotion_key_returns_blank(self, mock_post):
        """If the model omits one of the five emotions, return blank."""
        partial = {
            "emotionPredictions": [
                {"emotion": {"joy": 0.9, "sadness": 0.1}}
            ]
        }
        mock_post.return_value = _make_response(
            status_code=200, json_body=partial
        )
        result = emotion_detector("some text")
        self.assertIsNone(result["dominant_emotion"])

    # ---- Blank input ------------------------------------------------
    def test_blank_input_returns_blank(self):
        """Empty / whitespace input must not call the service."""
        for empty in ("", "    ", None):
            result = emotion_detector(empty)
            self.assertIsNone(result["dominant_emotion"])

    # ---- Unconfigured service --------------------------------------
    def test_unconfigured_service_returns_blank(self):
        """Without a configured URL the function returns the blank result."""
        with patch("EmotionDetection.emotion_detection.WATSON_NLP_URL", ""):
            result = emotion_detector("I am happy")
            self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()