"""Face and user-presence detection for VisionOS Phase 1."""

from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum

import cv2
import mediapipe as mp

from config import AppConfig


class PresenceState(str, Enum):
    """Dashboard states for the active user."""

    PRESENT = "PRESENT"
    AWAY = "AWAY"


@dataclass(frozen=True)
class FaceDetectionResult:
    """Presence information generated from the current frame."""

    state: PresenceState
    face_count: int
    seconds_absent: float
    should_lock: bool


class FacePresenceDetector:
    """Detect whether a user is visible and trigger auto-lock after absence."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=config.min_face_detection_confidence,
        )
        self._drawing = mp.solutions.drawing_utils
        self._absent_since: float | None = None
        self._lock_reported = False

    def process(self, frame: object) -> FaceDetectionResult:
        """Detect faces, draw bounding boxes, and calculate presence state."""

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._face_detection.process(rgb_frame)
        face_count = len(results.detections or [])
        for detection in results.detections or []:
            self._drawing.draw_detection(frame, detection)

        if face_count > 0:
            self._absent_since = None
            self._lock_reported = False
            return FaceDetectionResult(PresenceState.PRESENT, face_count, 0.0, False)

        now = time.monotonic()
        if self._absent_since is None:
            self._absent_since = now
        seconds_absent = now - self._absent_since
        should_lock = seconds_absent >= self._config.auto_lock_seconds and not self._lock_reported
        if should_lock:
            self._lock_reported = True
        return FaceDetectionResult(PresenceState.AWAY, 0, seconds_absent, should_lock)

    def close(self) -> None:
        """Release MediaPipe resources."""

        self._face_detection.close()
