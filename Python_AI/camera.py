"""Camera access layer for VisionOS.

The Camera class owns the OpenCV capture object so the rest of the application can
focus on AI processing instead of device setup and cleanup details.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import cv2

from config import AppConfig

LOGGER = logging.getLogger(__name__)


@dataclass
class CameraFrame:
    """A captured webcam frame and its measured dimensions."""

    image: object
    width: int
    height: int


class Camera:
    """Thin wrapper around ``cv2.VideoCapture`` with predictable lifecycle hooks."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._capture: cv2.VideoCapture | None = None

    def open(self) -> None:
        """Open the configured webcam and apply the requested resolution."""

        self._capture = cv2.VideoCapture(self.config.camera_index)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.frame_width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.frame_height)
        if not self._capture.isOpened():
            raise RuntimeError(f"Unable to open camera index {self.config.camera_index}")
        LOGGER.info("Camera index %s opened", self.config.camera_index)

    def read(self) -> CameraFrame | None:
        """Return the next frame, or ``None`` when the camera read fails."""

        if self._capture is None:
            raise RuntimeError("Camera.read() called before Camera.open()")
        ok, frame = self._capture.read()
        if not ok:
            return None
        height, width = frame.shape[:2]
        return CameraFrame(image=frame, width=width, height=height)

    def release(self) -> None:
        """Release the webcam handle."""

        if self._capture is not None:
            self._capture.release()
            self._capture = None
            LOGGER.info("Camera released")
