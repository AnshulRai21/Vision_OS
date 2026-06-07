# VisionOS — AI-Powered Touchless Laptop Control

> Control your Windows laptop using only hand gestures and facial presence detection.
> No keyboard. No mouse. Just your hands.

---

## Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Python AI engine

```bash
python main.py
```

### 3. Start the Java Dashboard (in a new terminal)

```bash
cd Java_Dashboard
mvn javafx:run
```

The dashboard will automatically connect to the Python backend via TCP on port 9999.

---

## Gesture Reference

| Gesture            | Action              | How to form it                              |
|--------------------|---------------------|---------------------------------------------|
| Index Finger Point | Move Mouse Cursor   | Extend only the index finger                |
| Pinch              | Left Click          | Touch thumb tip to index tip                |
| Two Finger Pinch   | Right Click         | Touch thumb tip to index AND middle tips    |
| Open Palm          | Pause Control       | All four fingers extended, palm facing cam  |
| Fist               | Stop Control        | Close all fingers                           |
| Thumbs Up          | Volume Up           | Only thumb up, fingers curled               |
| Thumbs Down        | Volume Down         | Only thumb down, fingers curled             |

---

## Project Structure

```
VisionOS/
│
├── config.py                   ← All tunable settings
├── main.py                     ← Entry point / orchestrator
├── requirements.txt
│
├── Python_AI/
│   ├── camera.py               ← Webcam capture + FPS tracking
│   ├── hand_tracking.py        ← MediaPipe landmark detection
│   ├── gesture_detection.py    ← Gesture classification engine
│   ├── mouse_controller.py     ← Cursor movement + click actions
│   ├── face_detection.py       ← User presence + auto-lock
│   ├── database.py             ← SQLite activity logging
│   └── socket_server.py        ← Real-time Python→Java bridge
│
├── Java_Dashboard/
│   ├── Dashboard.java          ← JavaFX main window
│   ├── SocketClient.java       ← TCP client for Python data
│   ├── StateMessage.java       ← JSON state model
│   └── pom.xml                 ← Maven build config
│
├── Database/
│   └── visionos.db             ← Auto-created on first run
│
└── Documentation/
    ├── README.md               ← This file
    └── architecture.md         ← System design details
```

---

## Architecture

```
Webcam
  │
  ▼
OpenCV (camera.py)
  │  BGR frames at 30fps
  ▼
MediaPipe (hand_tracking.py)
  │  21 hand landmarks
  ▼
Gesture Engine (gesture_detection.py)
  │  gesture name + confidence
  ▼
Action Controller (main.py)
  ├──→ PyAutoGUI (mouse_controller.py)  ─→ OS mouse/keyboard
  ├──→ Face Detector (face_detection.py) ─→ Auto-lock Windows
  ├──→ SQLite (database.py)             ─→ Activity log
  └──→ Socket Server (socket_server.py) ─→ Java Dashboard (port 9999)
```

---

## Configuration

Edit `config.py` to tune behavior without touching code:

| Setting                    | Default | Description                             |
|----------------------------|---------|-----------------------------------------|
| `CAMERA_INDEX`             | 0       | Webcam device index                     |
| `MOUSE_SMOOTHING`          | 5       | Rolling average window (1=raw, 10=slow) |
| `MOUSE_DEAD_ZONE`          | 8       | Pixels of movement to ignore (jitter)   |
| `PINCH_THRESHOLD`          | 0.06    | Normalized distance for pinch detection |
| `AUTO_LOCK_TIMEOUT`        | 30      | Seconds before auto-locking             |
| `SOCKET_PORT`              | 9999    | Port for Java dashboard connection      |

---

## Database Schema

```sql
CREATE TABLE ActivityLog (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT    NOT NULL,   -- "2026-06-07 10:15:00"
    gesture   TEXT,               -- "PINCH" or NULL
    action    TEXT    NOT NULL,   -- "Left click"
    status    TEXT    NOT NULL    -- "OK" | "PRESENT" | "AWAY" | "LOCKED"
);
```

---

## Java Dashboard

The dashboard runs independently of Python and reconnects automatically if Python restarts.

Panels:
- **System Status** — camera state, mouse mode, lock countdown
- **Current Gesture** — live gesture name with color coding
- **User Presence** — PRESENT / AWAY / LOCKED indicator
- **Notifications** — timestamped security and system alerts
- **Activity Log** — last 20 database entries, live-updating

---

## Prerequisites

| Tool         | Version  | Install                              |
|--------------|----------|--------------------------------------|
| Python       | 3.10+    | python.org                           |
| Java JDK     | 17+      | adoptium.net                         |
| Maven        | 3.8+     | maven.apache.org                     |
| Webcam       | Any      | Built-in or USB                      |
| Windows 11   | —        | Auto-lock uses Windows API           |

---

## Troubleshooting

**Camera not opening:**
- Check `CAMERA_INDEX` in config.py (try 1 or 2 for external webcams)
- Ensure no other app (Zoom, Teams) has the camera open

**Gestures not recognized:**
- Ensure good lighting
- Keep hand 30–60 cm from camera
- Lower `MP_HAND_DETECTION_CONFIDENCE` in config.py for harder lighting

**Dashboard not connecting:**
- Ensure Python `main.py` is running first
- Check firewall allows localhost:9999

**Auto-lock not working on non-Windows:**
- The lock command uses `rundll32.exe` (Windows only)
- On other OSes a warning is logged but the app continues

---

## Phase 2 Roadmap

- Voice commands (speech-to-text with Whisper)
- Emotion detection (mood-aware system)
- Application launcher via gestures
- Privacy shield (blur screen when user looks away)
- Productivity analytics dashboard
