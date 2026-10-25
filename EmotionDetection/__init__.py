"""EmotionDetection package.

Exposes the :func:`emotion_detector` entry point so the package can be
imported from the project root with::

    from EmotionDetection import emotion_detection
"""

from .emotion_detection import emotion_detector

__all__ = ["emotion_detector"]