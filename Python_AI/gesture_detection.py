"""Rule-based hand gesture recognition for the Phase 1 MVP.

The recognizer intentionally uses transparent geometry rules instead of a black-box
model so students can demonstrate, debug, and extend every gesture during the MVP.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Sequence


class GestureName(str, Enum):
    """Supported Version 1.0 gestures."""

    NONE = "NONE"
    OPEN_PALM = "OPEN_PALM"
    FIST = "FIST"
    THUMBS_UP = "THUMBS_UP"
    THUMBS_DOWN = "THUMBS_DOWN"
    INDEX_FINGER = "INDEX_FINGER"
    PINCH = "PINCH"
    TWO_FINGER_PINCH = "TWO_FINGER_PINCH"


GESTURE_ACTIONS: dict[GestureName, str] = {
    GestureName.NONE: "NO_ACTION",
    GestureName.OPEN_PALM: "PAUSE_CONTROL",
    GestureName.FIST: "STOP_CONTROL",
    GestureName.THUMBS_UP: "VOLUME_UP",
    GestureName.THUMBS_DOWN: "VOLUME_DOWN",
    GestureName.INDEX_FINGER: "MOVE_MOUSE",
    GestureName.PINCH: "LEFT_CLICK",
    GestureName.TWO_FINGER_PINCH: "RIGHT_CLICK",
}


@dataclass(frozen=True)
class GestureResult:
    """Recognized gesture, mapped action, and confidence value."""

    name: GestureName
    action: str
    confidence: float


class GestureRecognizer:
    """Recognize MVP gestures from the 21 MediaPipe hand landmarks."""

    TIP_IDS = (4, 8, 12, 16, 20)
    PIP_IDS = (3, 6, 10, 14, 18)

    def recognize(self, landmarks: Sequence[object]) -> GestureResult:
        """Return the best gesture estimate for one detected hand."""

        fingers = self._extended_fingers(landmarks)
        pinch_distance = self._distance(landmarks[4], landmarks[8])
        middle_pinch_distance = self._distance(landmarks[4], landmarks[12])

        if pinch_distance < 0.045:
            return self._result(GestureName.PINCH, 0.95 - pinch_distance)
        if pinch_distance < 0.075 and middle_pinch_distance < 0.075:
            return self._result(GestureName.TWO_FINGER_PINCH, 0.88)
        if self._is_thumbs_up(landmarks, fingers):
            return self._result(GestureName.THUMBS_UP, 0.86)
        if self._is_thumbs_down(landmarks, fingers):
            return self._result(GestureName.THUMBS_DOWN, 0.86)
        if fingers == [False, True, False, False, False]:
            return self._result(GestureName.INDEX_FINGER, 0.90)
        if all(fingers):
            return self._result(GestureName.OPEN_PALM, 0.90)
        if not any(fingers):
            return self._result(GestureName.FIST, 0.85)
        return self._result(GestureName.NONE, 0.0)

    def _result(self, name: GestureName, confidence: float) -> GestureResult:
        return GestureResult(name=name, action=GESTURE_ACTIONS[name], confidence=max(0.0, min(confidence, 1.0)))

    def _extended_fingers(self, landmarks: Sequence[object]) -> list[bool]:
        """Estimate whether thumb, index, middle, ring, and pinky are extended."""

        thumb_extended = abs(landmarks[4].x - landmarks[0].x) > abs(landmarks[3].x - landmarks[0].x)
        other_fingers = [landmarks[tip].y < landmarks[pip].y for tip, pip in zip(self.TIP_IDS[1:], self.PIP_IDS[1:])]
        return [thumb_extended, *other_fingers]

    def _is_thumbs_up(self, landmarks: Sequence[object], fingers: list[bool]) -> bool:
        return fingers[0] and not any(fingers[1:]) and landmarks[4].y < landmarks[3].y < landmarks[2].y

    def _is_thumbs_down(self, landmarks: Sequence[object], fingers: list[bool]) -> bool:
        return fingers[0] and not any(fingers[1:]) and landmarks[4].y > landmarks[3].y > landmarks[2].y

    def _distance(self, first: object, second: object) -> float:
        return math.hypot(first.x - second.x, first.y - second.y)
