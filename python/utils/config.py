"""Configuration helpers for the VisionOS AI core."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VisionOSConfig:
    """Minimal configuration placeholder for core services."""

    camera_index: int = 0
    ipc_host: str = "127.0.0.1"
    ipc_port: int = 8765


def load_config() -> VisionOSConfig:
    """Load and return the default placeholder configuration."""
    return VisionOSConfig()
