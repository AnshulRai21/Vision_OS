"""SQLite activity logging for VisionOS."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from config import AppConfig


class ActivityDatabase:
    """Persist gesture, presence, and security events."""

    def __init__(self, config: AppConfig) -> None:
        self._path = Path(config.database_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self._path)
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS ActivityLog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                gesture TEXT,
                action TEXT,
                status TEXT
            )
            """
        )
        self._connection.commit()

    def log(self, gesture: str | None, action: str | None, status: str | None) -> None:
        """Insert one activity row."""

        self._connection.execute(
            "INSERT INTO ActivityLog(timestamp, gesture, action, status) VALUES (?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(timespec="seconds"), gesture, action, status),
        )
        self._connection.commit()

    def close(self) -> None:
        """Close the SQLite connection."""

        self._connection.close()
