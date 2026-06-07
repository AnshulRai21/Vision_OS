"""Runtime configuration for the VisionOS Phase 1 MVP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Application settings shared by the Python AI modules."""

    camera_index: int = 0
    frame_width: int = 1280
    frame_height: int = 720
    min_hand_detection_confidence: float = 0.70
    min_hand_tracking_confidence: float = 0.70
    min_face_detection_confidence: float = 0.60
    auto_lock_seconds: int = 30
    socket_host: str = "127.0.0.1"
    socket_port: int = 9999
    database_path: Path = Path(__file__).resolve().parents[1] / "Database" / "visionos.db"
    enable_os_actions: bool = True
    smoothing_factor: float = 0.25
