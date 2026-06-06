"""Vision_OS Python processing engine entry point.

Run from the ``python`` directory with:

    python -m core.main
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class EngineConfig:
    """Runtime configuration for the webcam processing engine."""

    camera_index: int = 0
    model_selection: int = 0
    min_detection_confidence: float = 0.5


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the processing engine."""

    parser = argparse.ArgumentParser(description="Start the Vision_OS Python processing engine.")
    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="Camera index to open with OpenCV. Defaults to 0.",
    )
    parser.add_argument(
        "--min-detection-confidence",
        type=float,
        default=0.5,
        help="Minimum MediaPipe face-detection confidence. Defaults to 0.5.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate startup without importing webcam/AI dependencies or opening a camera.",
    )
    return parser.parse_args(argv)


def run_engine(config: EngineConfig) -> int:
    """Start the webcam loop and run Phase 1 face detection."""

    try:
        import cv2
        import mediapipe as mp
    except ImportError as exc:
        print(
            "Missing Python dependency. Install dependencies with `pip install -r requirements.txt`.",
            file=sys.stderr,
        )
        print(f"Import error: {exc}", file=sys.stderr)
        return 1

    cap = cv2.VideoCapture(config.camera_index)
    if not cap.isOpened():
        print(
            f"Vision_OS started, but camera index {config.camera_index} could not be opened. "
            "Connect a webcam or choose another --camera-index.",
            file=sys.stderr,
        )
        return 0

    face_detection = mp.solutions.face_detection.FaceDetection(
        model_selection=config.model_selection,
        min_detection_confidence=config.min_detection_confidence,
    )

    print("Vision_OS Python engine running. Press 'q' or Escape in the camera window to exit.")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Unable to read from camera; stopping engine.", file=sys.stderr)
                return 1

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb_frame)

            if results.detections:
                for detection in results.detections:
                    mp.solutions.drawing_utils.draw_detection(frame, detection)

            cv2.imshow("Vision_OS Phase 1", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                return 0
    finally:
        face_detection.close()
        cap.release()
        cv2.destroyAllWindows()


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""

    args = parse_args(argv)
    config = EngineConfig(
        camera_index=args.camera_index,
        min_detection_confidence=args.min_detection_confidence,
    )

    if args.dry_run:
        print("Vision_OS Python engine startup validated.")
        return 0

    return run_engine(config)


if __name__ == "__main__":
    raise SystemExit(main())
