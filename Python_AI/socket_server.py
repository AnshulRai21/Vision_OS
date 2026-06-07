"""Newline-delimited JSON socket broadcaster for the Java dashboard."""

from __future__ import annotations

import json
import logging
import socket
import threading
from dataclasses import asdict, is_dataclass
from typing import Any

from config import AppConfig

LOGGER = logging.getLogger(__name__)


class DashboardSocketServer:
    """Small TCP server that streams VisionOS events to one or more dashboards."""

    def __init__(self, config: AppConfig) -> None:
        self._host = config.socket_host
        self._port = config.socket_port
        self._server_socket: socket.socket | None = None
        self._clients: list[socket.socket] = []
        self._lock = threading.Lock()
        self._running = False

    def start(self) -> None:
        """Start accepting dashboard clients on a background thread."""

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        self._running = True
        threading.Thread(target=self._accept_loop, daemon=True, name="visionos-socket-server").start()
        LOGGER.info("Dashboard socket server listening on %s:%s", self._host, self._port)

    def broadcast(self, event_type: str, payload: dict[str, Any]) -> None:
        """Send a JSON event to all connected Java dashboard clients."""

        message = json.dumps({"type": event_type, "data": self._json_safe(payload)}) + "\n"
        encoded = message.encode("utf-8")
        with self._lock:
            clients = list(self._clients)
        stale_clients: list[socket.socket] = []
        for client in clients:
            try:
                client.sendall(encoded)
            except OSError:
                stale_clients.append(client)
        if stale_clients:
            with self._lock:
                self._clients = [client for client in self._clients if client not in stale_clients]

    def stop(self) -> None:
        """Stop accepting clients and close all sockets."""

        self._running = False
        if self._server_socket is not None:
            self._server_socket.close()
        with self._lock:
            clients = list(self._clients)
            self._clients.clear()
        for client in clients:
            client.close()

    def _accept_loop(self) -> None:
        while self._running and self._server_socket is not None:
            try:
                client, address = self._server_socket.accept()
            except OSError:
                return
            with self._lock:
                self._clients.append(client)
            LOGGER.info("Dashboard client connected from %s", address)

    def _json_safe(self, value: Any) -> Any:
        if is_dataclass(value):
            return asdict(value)
        if isinstance(value, dict):
            return {key: self._json_safe(item) for key, item in value.items()}
        if isinstance(value, list | tuple):
            return [self._json_safe(item) for item in value]
        if hasattr(value, "value"):
            return value.value
        return value
