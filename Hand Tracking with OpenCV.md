# Hand Tracking with OpenCV

A small Python application for real-time hand tracking using OpenCV and MediaPipe. Use your webcam or process a video file, display up to two hands, and optionally save an annotated video.

## Features

- Webcam and video-file input from one command.
- Hand landmarks and left/right classification with confidence.
- Smoothed FPS and hand-count overlay.
- Optional annotated video recording and headless processing.
- Configurable camera resolution, number of hands, and confidence thresholds.
- Friendly errors when a camera, video, or dependency is unavailable.

## Requirements

Python 3.10–3.12 and a webcam for live tracking. The preview uses OpenCV's desktop GUI, so a graphical desktop is needed unless you use `--no-preview`.

## Install

```bash
git clone https://github.com/KalyanM45/Hand-Tracking-Using-Opencv.git
cd Hand-Tracking-Using-Opencv
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

The default source is webcam 0:

```bash
python app.py
```

Quit with **Q** or **Esc**. Press **M** to toggle mirroring and **L** to toggle landmark drawing. You can also run the engine directly with `python hand_tracker.py`.

Use a different camera, request a capture size, or save the annotated stream:

```bash
python app.py --source 1 --width 1280 --height 720
python app.py --output recordings/hands.mp4
```

Process an existing video:

```bash
python app.py --source path/to/input.mp4 --output output/annotated.mp4
```

Process without opening a window (an output path is required):

```bash
python app.py --source path/to/input.mp4 --output output/annotated.mp4 --no-preview
```

Use `python app.py --help` to see all options. For example, adjust detection settings and print pixel coordinates:

```bash
python app.py --max-hands 1 --detection-confidence 0.7 --tracking-confidence 0.65 --show-coordinates
```

## Troubleshooting

- **Camera won't open:** close other camera applications and try another index with `--source 1`.
- **No preview window:** use a desktop session with GUI support, or run with `--no-preview --output result.mp4`.
- **Installation issues:** use Python 3.10–3.12 in a fresh virtual environment and install from `requirements.txt`.
- **Slow tracking:** reduce the camera resolution with `--width 640 --height 480`.

## License

Distributed under the MIT License. See [LICENSE](LICENSE).
