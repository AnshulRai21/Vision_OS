# VisionOS: AI-Powered Touchless Laptop Control System

VisionOS is a Phase 1 Human Computer Interaction (HCI) MVP that lets a Windows laptop respond to webcam-based hand gestures and facial presence detection. Python performs the real-time computer-vision work, while JavaFX provides a dashboard for system status, current gesture, user presence, activity logs, and notifications.

## Phase 1 MVP Goal

Control a laptop using hand gestures and facial presence detection without touching the keyboard or mouse.

## Version 1.0 Features

### Hand Gesture Controls

| Gesture | Action |
| --- | --- |
| Index Finger | Move Mouse |
| Pinch | Left Click |
| Two Finger Pinch | Right Click |
| Open Palm | Pause Control |
| Fist | Stop Control |
| Thumbs Up | Volume Up |
| Thumbs Down | Volume Down |

### Human Interaction

- Face detection with MediaPipe.
- User presence state: `PRESENT` or `AWAY`.
- Auto-lock trigger after 30 seconds away from the camera.

### Java Dashboard

- Camera status.
- Current gesture.
- User status.
- Mouse mode.
- Activity logs.
- Security notifications.

## Technology Stack

### Python AI Core

- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy
- SQLite

### Java Dashboard

- JavaFX
- Maven
- TCP socket communication

### Target OS

- Windows 11 for real OS actions such as workstation lock and volume keys.
- Non-Windows systems can run with `--disable-os-actions` for safe demos.

## Architecture

```text
Camera Feed
    ↓
OpenCV Processing
    ↓
MediaPipe Hand Tracking + Face Detection
    ↓
Gesture Recognition Engine
    ↓
Mouse / Security Action Controller
    ↓
SQLite Activity Logger
    ↓
Socket Event Stream
    ↓
JavaFX Dashboard
```

Python owns all AI, computer-vision, automation, and persistence logic. Java owns the user-facing dashboard and consumes newline-delimited JSON events from the Python socket server on `127.0.0.1:9999`.

## Project Structure

```text
VisionOS/
├── Python_AI/
│   ├── camera.py
│   ├── config.py
│   ├── database.py
│   ├── face_detection.py
│   ├── gesture_detection.py
│   ├── hand_tracking.py
│   ├── main.py
│   ├── mouse_controller.py
│   ├── requirements.txt
│   └── socket_server.py
│
├── Java_Dashboard/
│   ├── pom.xml
│   └── src/main/java/com/visionos/dashboard/
│       ├── ActivityPanel.java
│       ├── CameraPanel.java
│       ├── Dashboard.java
│       ├── GesturePanel.java
│       ├── NotificationPanel.java
│       └── SocketClient.java
│
├── Database/
│   ├── schema.sql
│   └── visionos.db      # Created at runtime
│
├── Documentation/
│   └── architecture.md
│
└── README.md
```

## IPC Protocol

Python broadcasts UTF-8 newline-delimited JSON over TCP.

### Python → Java Events

| Event Type | Example Data | Description |
| --- | --- | --- |
| `STATUS` | `{camera, gesture, user, mouseMode, fps}` | Live system state for dashboard cards. |
| `GESTURE` | `{gesture, action, confidence, landmarks}` | Current gesture and mapped action. |
| `PRESENCE` | `{status, faceCount}` | User presence state updates. |
| `SECURITY` | `{notification, status}` | Auto-lock and future security notifications. |

Example:

```json
{"type":"GESTURE","data":{"gesture":"PINCH","action":"LEFT_CLICK","confidence":0.94,"landmarks":21}}
```

## Database Design

`ActivityLog` stores gesture detections, user-presence changes, security events, and OS actions.

| Field | Type | Purpose |
| --- | --- | --- |
| `id` | INTEGER PRIMARY KEY | Unique event id. |
| `timestamp` | TEXT | UTC ISO-8601 timestamp. |
| `gesture` | TEXT | Gesture name, if applicable. |
| `action` | TEXT | Mapped action or system event. |
| `status` | TEXT | User/system status such as `PRESENT` or `AWAY`. |

## Build and Run

### 1. Start the Java dashboard

```bash
cd Java_Dashboard
mvn javafx:run
```

### 2. Start the Python AI core

Use a virtual environment from the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r Python_AI/requirements.txt
python Python_AI/main.py
```

For a safe demo that recognizes gestures but does not move the mouse, click, change volume, or lock the machine:

```bash
python Python_AI/main.py --disable-os-actions
```

For a startup check without opening the webcam:

```bash
python Python_AI/main.py --dry-run
```

## Development Roadmap

### Week 1: Hand Tracking

- Webcam opens.
- Hand detected.
- 21 MediaPipe landmarks displayed.
- FPS counter displayed.

Expected console/window status:

```text
Hand Detected: True
Landmarks: 21
```

### Week 2: Gesture Recognition

Detect:

- Open Palm
- Fist
- Thumbs Up
- Thumbs Down
- Pinch
- Two Finger Pinch
- Index Finger

Expected output:

```text
Gesture: PINCH
```

### Week 3: Virtual Mouse

- Cursor movement.
- Left click.
- Right click.
- Future-ready drag structure.

### Week 4: Face Detection

- Face present.
- Face absent.

Expected output:

```text
User: PRESENT
```

or:

```text
User: AWAY
```

### Week 5: Auto Lock Security

If no face is detected for 30 seconds, VisionOS sends a lock command on Windows and logs the security event.

### Week 6: Java Dashboard

Dashboard displays:

```text
VisionOS Dashboard
Camera Status: ACTIVE
Gesture: PINCH
User Status: PRESENT
Mouse Mode: ON
```

## Evaluation Demo Flow

1. Start the Java dashboard.
2. Start the Python AI core.
3. Camera activates.
4. Hand landmarks appear on the OpenCV window.
5. Move the cursor using the index finger gesture.
6. Pinch to left-click.
7. Show face detection as `PRESENT`.
8. Leave the camera view.
9. After 30 seconds, VisionOS locks the Windows session and logs the event.
10. Confirm dashboard updates in real time.

## Future Scalability Recommendations

After the MVP is reliable, Phase 2 can add voice commands, emotion detection, privacy shield, application launching, productivity analytics, classroom integration, smart-home control, and AR/VR gesture interfaces.
