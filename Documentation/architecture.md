# VisionOS Phase 1 MVP Architecture

## Scope

Phase 1 intentionally focuses on a small, demonstrable MVP instead of all future modules. The implemented scope is hand tracking, gesture recognition, virtual mouse actions, face presence detection, auto-lock security, activity logging, and Java dashboard communication.

## Runtime Components

```text
Python_AI/main.py
├── Camera
├── HandTracker
│   └── GestureRecognizer
├── FacePresenceDetector
├── MouseController
├── ActivityDatabase
└── DashboardSocketServer

Java_Dashboard/Dashboard.java
├── CameraPanel
├── GesturePanel
├── ActivityPanel
├── NotificationPanel
└── SocketClient
```

## Python_AI Modules

| File | Responsibility |
| --- | --- |
| `camera.py` | Owns OpenCV camera initialization, frame reads, and release. |
| `hand_tracking.py` | Runs MediaPipe Hands, draws all 21 landmarks, measures FPS, and forwards landmarks to gesture recognition. |
| `gesture_detection.py` | Provides rule-based recognition for MVP gestures and maps them to action names. |
| `face_detection.py` | Runs MediaPipe face detection and maintains `PRESENT` / `AWAY` state with an auto-lock timer. |
| `mouse_controller.py` | Converts gestures to PyAutoGUI actions and Windows lock commands. |
| `database.py` | Creates and writes SQLite `ActivityLog` records. |
| `socket_server.py` | Broadcasts newline-delimited JSON events to dashboard clients. |
| `main.py` | Orchestrates the real-time loop and connects all modules. |

## Gesture Recognition Strategy

The MVP uses transparent geometric rules based on MediaPipe landmarks:

- Pinch: thumb tip close to index tip.
- Two finger pinch: thumb tip close to both index and middle tips.
- Index finger: only the index finger is extended.
- Open palm: all five fingers are extended.
- Fist: no fingers are extended.
- Thumbs up/down: thumb extended while other fingers are closed, with thumb tip above or below its joints.

This approach is fast, explainable, and easy to improve with a trained classifier later.

## Socket Events

All messages are newline-delimited JSON over TCP port `9999`.

```json
{"type":"STATUS","data":{"camera":"ACTIVE","gesture":"INDEX_FINGER","user":"PRESENT","mouseMode":"ON","fps":28.4}}
```

```json
{"type":"GESTURE","data":{"gesture":"PINCH","action":"LEFT_CLICK","confidence":0.93,"landmarks":21}}
```

```json
{"type":"PRESENCE","data":{"status":"AWAY","faceCount":0}}
```

```json
{"type":"SECURITY","data":{"notification":"System Locked","status":"AWAY"}}
```

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS ActivityLog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    gesture TEXT,
    action TEXT,
    status TEXT
);
```

## Incremental Build Order

1. Project setup and documentation.
2. Hand detection module.
3. Gesture recognition module.
4. Virtual mouse controller.
5. Face detection and presence state.
6. Auto-lock security.
7. SQLite activity logs.
8. JavaFX dashboard and socket communication.

## Notes for Production Hardening

- Add a trained gesture classifier after collecting real user samples.
- Add cooldowns per gesture type and configurable sensitivity.
- Add TLS or localhost-only firewall rules if remote dashboard access is introduced.
- Add automated UI tests for JavaFX and hardware-in-the-loop tests for the Python camera loop.
- Add packaging scripts for Windows startup and bundled dependencies.
