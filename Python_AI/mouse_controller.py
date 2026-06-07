"""Operating-system action controller for VisionOS gestures."""

from __future__ import annotations

import logging
import platform
import subprocess
import time

import pyautogui

from config import AppConfig
from gesture_detection import GestureName, GestureResult

LOGGER = logging.getLogger(__name__)


class MouseController:
    """Map recognized gestures to mouse, volume, and lock actions."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._screen_width, self._screen_height = pyautogui.size()
        self._last_x = self._screen_width / 2
        self._last_y = self._screen_height / 2
        self._last_click_time = 0.0
        self._last_volume_time = 0.0
        pyautogui.FAILSAFE = True

    def handle_gesture(self, gesture: GestureResult, index_position: tuple[float, float] | None) -> str:
        """Execute the action represented by a gesture and return the action name."""

        if not self._config.enable_os_actions:
            return gesture.action
        if gesture.name == GestureName.OPEN_PALM:
            return gesture.action
        if gesture.name == GestureName.INDEX_FINGER and index_position is not None:
            self._move_cursor(index_position)
        elif gesture.name == GestureName.PINCH:
            self._click("left")
        elif gesture.name == GestureName.TWO_FINGER_PINCH:
            self._click("right")
        elif gesture.name == GestureName.THUMBS_UP:
            self._volume("up")
        elif gesture.name == GestureName.THUMBS_DOWN:
            self._volume("down")
        return gesture.action

    def lock_system(self) -> None:
        """Lock the Windows session when the user stays away long enough."""

        if not self._config.enable_os_actions:
            LOGGER.info("OS actions disabled; simulated system lock")
            return
        if platform.system().lower() == "windows":
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=False)
        else:
            LOGGER.warning("Auto-lock is configured for Windows; skipping on %s", platform.system())

    def _move_cursor(self, index_position: tuple[float, float]) -> None:
        target_x = (1.0 - index_position[0]) * self._screen_width
        target_y = index_position[1] * self._screen_height
        alpha = self._config.smoothing_factor
        self._last_x = self._last_x + (target_x - self._last_x) * alpha
        self._last_y = self._last_y + (target_y - self._last_y) * alpha
        pyautogui.moveTo(self._last_x, self._last_y, duration=0)

    def _click(self, button: str) -> None:
        now = time.monotonic()
        if now - self._last_click_time > 0.45:
            pyautogui.click(button=button)
            self._last_click_time = now

    def _volume(self, direction: str) -> None:
        now = time.monotonic()
        if now - self._last_volume_time > 0.35:
            pyautogui.press("volumeup" if direction == "up" else "volumedown")
            self._last_volume_time = now
