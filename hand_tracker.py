"""Hand tracking with OpenCV and MediaPipe Hands."""
from __future__ import annotations

import argparse
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

LOGGER = logging.getLogger("hand_tracker")

def parse_source(value: str) -> int | str:
    """Turn numeric source strings into camera indexes; keep paths as strings."""
    try:
        return int(value)
    except ValueError:
        return value



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Track hand landmarks from a webcam or a video file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--source", default="0", help="Camera index or path to an input video")
    parser.add_argument("--output", type=Path, help="Optional path for saving the annotated video")
    parser.add_argument("--max-hands", type=int, default=2, choices=range(1, 3), metavar="{1,2}")
    parser.add_argument("--detection-confidence", type=float, default=0.6, metavar="0..1")
    parser.add_argument("--tracking-confidence", type=float, default=0.6, metavar="0..1")
    parser.add_argument("--width", type=int, help="Requested capture width (webcam only)")
    parser.add_argument("--height", type=int, help="Requested capture height (webcam only)")
    parser.add_argument("--no-mirror", action="store_true", help="Do not mirror the preview")
    parser.add_argument("--no-landmarks", action="store_true", help="Do not draw landmark connections")
    parser.add_argument("--show-coordinates", action="store_true", help="Print landmark coordinates to the console")
    parser.add_argument("--no-preview", action="store_true", help="Process/save video without opening a preview window")
    parser.add_argument("--quiet", action="store_true", help="Hide informational status messages")
    return parser


def validate_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    for name in ("detection_confidence", "tracking_confidence"):
        value = getattr(args, name)
        if not 0.0 <= value <= 1.0:
            parser.error(f"--{name.replace('_', '-')} must be between 0 and 1")
    for name in ("width", "height"):
        value = getattr(args, name)
        if value is not None and value <= 0:
            parser.error(f"--{name} must be a positive integer")
    if args.no_preview and args.output is None:
        parser.error("--no-preview requires --output so the processed result is saved")


@dataclass
class DisplayState:
    mirror: bool
    draw_landmarks: bool


def draw_hud(frame, fps: float, hand_count: int, mirror: bool, cv2) -> None:
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (12, 12), (228, 82), (24, 28, 36), -1)
    cv2.putText(frame, f"FPS  {fps:5.1f}", (24, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (118, 235, 190), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Hands  {hand_count}   {'MIRROR' if mirror else 'NORMAL'}", (24, 67), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (235, 239, 245), 1, cv2.LINE_AA)
    cv2.putText(frame, "Q: quit   M: mirror   L: landmarks", (12, h - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (235, 239, 245), 1, cv2.LINE_AA)


def run(args: argparse.Namespace) -> int:
    try:
        import cv2
        import mediapipe as mp
    except ImportError as exc:
        LOGGER.error("Missing dependency: %s. Install project requirements with: python -m pip install -r requirements.txt", exc.name)
        return 2

    source = parse_source(args.source)
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        LOGGER.error("Could not open video source %r. Check the camera index or input file.", source)
        return 1

    if isinstance(source, int):
        if args.width:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
        if args.height:
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    writer = None
    hands = None
    window_name = "Hand Tracking"
    state = DisplayState(mirror=not args.no_mirror, draw_landmarks=not args.no_landmarks)
    previous_time = time.perf_counter()
    fps = 0.0
    frame_count = 0
    try:
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)

        hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=args.max_hands,
            min_detection_confidence=args.detection_confidence,
            min_tracking_confidence=args.tracking_confidence,
            model_complexity=1,
        )
        drawing = mp.solutions.drawing_utils
        connections = mp.solutions.hands.HAND_CONNECTIONS

        while True:
            success, frame = cap.read()
            if not success:
                break
            if state.mirror:
                frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            result = hands.process(rgb)
            rgb.flags.writeable = True
            hand_landmarks = result.multi_hand_landmarks or []

            if state.draw_landmarks:
                for hand_index, landmarks in enumerate(hand_landmarks):
                    drawing.draw_landmarks(frame, landmarks, connections)
                    if result.multi_handedness and hand_index < len(result.multi_handedness):
                        classification = result.multi_handedness[hand_index].classification[0]
                        wrist = landmarks.landmark[0]
                        x = max(8, min(frame.shape[1] - 140, int(wrist.x * frame.shape[1])))
                        y = max(24, min(frame.shape[0] - 8, int(wrist.y * frame.shape[0]) - 12))
                        cv2.putText(frame, f"{classification.label} {classification.score:.0%}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (118, 235, 190), 2, cv2.LINE_AA)

            if args.show_coordinates:
                height, width = frame.shape[:2]
                for hand_index, landmarks in enumerate(hand_landmarks):
                    points = [(round(point.x * width), round(point.y * height)) for point in landmarks.landmark]
                    print(f"hand={hand_index + 1} landmarks={points}")

            now = time.perf_counter()
            elapsed = now - previous_time
            if elapsed > 0:
                instantaneous = 1.0 / elapsed
                fps = instantaneous if fps == 0 else 0.85 * fps + 0.15 * instantaneous
            previous_time = now
            draw_hud(frame, fps, len(hand_landmarks), state.mirror, cv2)

            if args.output:
                if writer is None:
                    input_fps = cap.get(cv2.CAP_PROP_FPS)
                    output_fps = input_fps if input_fps and input_fps > 0 else 30.0
                    h, w = frame.shape[:2]
                    writer = cv2.VideoWriter(str(args.output), cv2.VideoWriter_fourcc(*"mp4v"), output_fps, (w, h))
                    if not writer.isOpened():
                        LOGGER.error("Could not create output video at %s", args.output)
                        return 1
                    LOGGER.info("Saving annotated video to %s", args.output)
                writer.write(frame)

            frame_count += 1
            if not args.no_preview:
                cv2.imshow(window_name, frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q") or key == 27:
                    break
                if key == ord("m"):
                    state.mirror = not state.mirror
                if key == ord("l"):
                    state.draw_landmarks = not state.draw_landmarks

        if frame_count == 0:
            LOGGER.warning("No frames were read from the source.")
        elif not args.quiet:
            LOGGER.info("Processed %d frame(s).", frame_count)
        return 0
    except KeyboardInterrupt:
        LOGGER.info("Interrupted by user.")
        return 0
    finally:
        if hands is not None:
            hands.close()
        if writer is not None:
            writer.release()
        cap.release()
        if not args.no_preview:
            cv2.destroyAllWindows()


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_args(args, parser)
    logging.basicConfig(level=logging.WARNING if args.quiet else logging.INFO, format="%(levelname)s: %(message)s")
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
