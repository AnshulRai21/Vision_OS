"""VisionOS Phase 1 MVP entry point.

Start from the repository root with:

    python Python_AI/main.py
"""

from __future__ import annotations

import argparse
import logging
from dataclasses import replace

from config import AppConfig

LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line switches used during development and demos."""

    parser = argparse.ArgumentParser(description="Run the VisionOS touchless laptop control MVP.")
    parser.add_argument("--camera-index", type=int, default=0, help="OpenCV camera index. Defaults to 0.")
    parser.add_argument("--disable-os-actions", action="store_true", help="Recognize gestures without moving/clicking/locking.")
    parser.add_argument("--auto-lock-seconds", type=int, default=30, help="Seconds away before Windows auto-lock.")
    parser.add_argument("--dry-run", action="store_true", help="Validate configuration without opening camera.")
    return parser.parse_args()


def draw_status_overlay(frame: object, hand_result: object, face_result: object, cv2_module: object) -> None:
    """Draw demo-friendly status text on the webcam frame."""

    cv2 = cv2_module
    color = (0, 255, 0) if hand_result.hand_detected else (0, 0, 255)
    cv2.putText(frame, f"FPS: {hand_result.fps:.1f}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv2.putText(frame, f"Hand Detected: {hand_result.hand_detected}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(frame, f"Landmarks: {hand_result.landmark_count}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(frame, f"Gesture: {hand_result.gesture.name.value}", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Action: {hand_result.gesture.action}", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"User: {face_result.state.value}", (20, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)


def main() -> int:
    """Run the camera processing loop and publish real-time dashboard events."""

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    args = parse_args()
    config = replace(
        AppConfig(),
        camera_index=args.camera_index,
        auto_lock_seconds=args.auto_lock_seconds,
        enable_os_actions=not args.disable_os_actions,
    )
    if args.dry_run:
        print("VisionOS Phase 1 MVP configuration validated.")
        print(f"Socket: {config.socket_host}:{config.socket_port}")
        print(f"Database: {config.database_path}")
        return 0

    import cv2

    from camera import Camera
    from database import ActivityDatabase
    from face_detection import FacePresenceDetector, PresenceState
    from hand_tracking import HandTracker
    from mouse_controller import MouseController
    from socket_server import DashboardSocketServer

    camera = Camera(config)
    hand_tracker = HandTracker(config)
    face_detector = FacePresenceDetector(config)
    mouse_controller = MouseController(config)
    database = ActivityDatabase(config)
    socket_server = DashboardSocketServer(config)
    last_gesture = "NONE"
    last_presence = PresenceState.AWAY.value

    socket_server.start()
    camera.open()
    try:
        while True:
            camera_frame = camera.read()
            if camera_frame is None:
                LOGGER.error("Unable to read camera frame")
                return 1

            frame = camera_frame.image
            hand_result = hand_tracker.process(frame)
            face_result = face_detector.process(frame)
            action = mouse_controller.handle_gesture(hand_result.gesture, hand_result.index_position)

            if hand_result.gesture.name.value != last_gesture:
                database.log(hand_result.gesture.name.value, action, face_result.state.value)
                socket_server.broadcast(
                    "GESTURE",
                    {
                        "gesture": hand_result.gesture.name.value,
                        "action": action,
                        "confidence": hand_result.gesture.confidence,
                        "landmarks": hand_result.landmark_count,
                    },
                )
                last_gesture = hand_result.gesture.name.value

            if face_result.state.value != last_presence:
                database.log(None, "USER_PRESENCE", face_result.state.value)
                socket_server.broadcast("PRESENCE", {"status": face_result.state.value, "faceCount": face_result.face_count})
                last_presence = face_result.state.value

            if face_result.should_lock:
                mouse_controller.lock_system()
                database.log(None, "SYSTEM_LOCKED", face_result.state.value)
                socket_server.broadcast("SECURITY", {"notification": "System Locked", "status": face_result.state.value})

            socket_server.broadcast(
                "STATUS",
                {
                    "camera": "ACTIVE",
                    "gesture": hand_result.gesture.name.value,
                    "user": face_result.state.value,
                    "mouseMode": "ON" if config.enable_os_actions else "SIMULATION",
                    "fps": round(hand_result.fps, 1),
                },
            )
            draw_status_overlay(frame, hand_result, face_result, cv2)
            cv2.imshow("VisionOS Phase 1 MVP", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                return 0
    finally:
        camera.release()
        hand_tracker.close()
        face_detector.close()
        database.close()
        socket_server.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    raise SystemExit(main())
