"""MediaPipe hand tracking module for VisionOS."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Sequence

import cv2
import mediapipe as mp

from config import AppConfig
from gesture_detection import GestureRecognizer, GestureResult, GestureName


@dataclass(frozen=True)
class HandTrackingResult:
    """Result produced for a processed video frame."""

    gesture: GestureResult
    hand_detected: bool
    landmark_count: int
    fps: float
    index_position: tuple[float, float] | None


class HandTracker:
    """Detect hands, draw landmarks, and classify current gestures."""

    def __init__(self, config: AppConfig) -> None:
        self._hands_module = mp.solutions.hands
        self._drawing = mp.solutions.drawing_utils
        self._hands = self._hands_module.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=config.min_hand_detection_confidence,
            min_tracking_confidence=config.min_hand_tracking_confidence,
        )
        self._recognizer = GestureRecognizer()
        self._last_time = time.perf_counter()

    def process(self, frame: object) -> HandTrackingResult:
        """Process one BGR OpenCV frame and draw the skeleton overlay in-place."""

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb_frame)
        fps = self._measure_fps()

        if not results.multi_hand_landmarks:
            return HandTrackingResult(
                gesture=GestureResult(GestureName.NONE, "NO_ACTION", 0.0),
                hand_detected=False,
                landmark_count=0,
                fps=fps,
                index_position=None,
            )

        hand_landmarks = results.multi_hand_landmarks[0]
        self._drawing.draw_landmarks(frame, hand_landmarks, self._hands_module.HAND_CONNECTIONS)
        gesture = self._recognizer.recognize(hand_landmarks.landmark)
        index_tip = hand_landmarks.landmark[8]
        return HandTrackingResult(
            gesture=gesture,
            hand_detected=True,
            landmark_count=len(hand_landmarks.landmark),
            fps=fps,
            index_position=(index_tip.x, index_tip.y),
        )

    def close(self) -> None:
        """Release MediaPipe resources."""

        self._hands.close()

    def _measure_fps(self) -> float:
        now = time.perf_counter()
        elapsed = max(now - self._last_time, 1e-6)
        self._last_time = now
        return 1.0 / elapsed
