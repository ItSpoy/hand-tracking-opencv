# Hand Tracking with OpenCV and MediaPipe

A real-time hand-tracking application built with **Python**, **OpenCV**, and **MediaPipe**. Use a webcam for live tracking or process an existing video. The application can draw hand landmarks and skeletal connections, identify left and right hands, display performance information, and save an annotated video.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Keyboard Controls](#keyboard-controls)
- [Command-Line Options](#command-line-options)
- [Run the Tests](#run-the-tests)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Author](#author)

## Features

- Track up to two hands using a webcam or a video file.
- Draw MediaPipe's 21 hand landmarks and skeletal connections.
- Display left/right hand labels with classification confidence.
- Show an FPS estimate, detected hand count, and current mirror mode.
- Toggle horizontal mirroring and landmark drawing while the application runs.
- Save processed frames to an annotated MP4 video.
- Process a video without opening a preview window.
- Configure the camera index, requested capture resolution, number of hands, and detection/tracking confidence from the command line.
- Print hand landmark coordinates in pixels when requested.
- Validate command-line settings and report unavailable sources or missing dependencies.
- Release camera, video writer, tracker, and preview-window resources when the application finishes.

## Technologies

- **Python**
- **OpenCV** — video capture, image processing, drawing, and preview.
- **MediaPipe Hands** — hand landmark detection and tracking.
- **argparse** — command-line argument parsing.
- **unittest** — automated tests for source parsing and argument validation.

## Requirements

- Python **3.12 (64-bit recommended on Windows)**.
- A webcam for live tracking, or a video file for offline processing.
- A graphical desktop for the preview window. Use `--no-preview` to process a video without a window; this requires `--output`.
- The Python dependencies listed in `requirements.txt`.

> **Python compatibility:** This project pins MediaPipe to `0.10.21` and uses the `mp.solutions.hands` API. On Windows, use Python 3.12 for this setup. Python 3.14 is not recommended for this pinned dependency.

## Installation

### Windows (Command Prompt or VS Code terminal)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ItSpoy/hand-tracking-opencv.git
   cd hand-tracking-opencv
   ```

2. **Create a virtual environment using Python 3.12:**

   ```powershell
   py -3.12 -m venv .venv312
   ```

   If `py -3.12` fails, install Python 3.12 (64-bit) and reopen your terminal.

3. **Install the dependencies:**

   You do not have to activate the virtual environment. Run its Python executable directly:

   ```powershell
   .\.venv312\Scripts\python.exe -m pip install --upgrade pip
   .\.venv312\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. **Start the application:**

   ```powershell
   .\.venv312\Scripts\python.exe app.py
   ```

   The first run should open the default webcam preview if your camera is available.

### macOS / Linux

Install a compatible Python version, then run:

```bash
python3.12 -m venv .venv312
source .venv312/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

## Usage

### Start the default webcam

```bash
python app.py
```

`app.py` is the convenient entry point. You can also run the tracker directly:

```bash
python hand_tracker.py
```

If you are using the Windows virtual environment without activating it, prefix commands with `.\.venv312\Scripts\python.exe`.

### Select a different camera

```bash
python app.py --source 1
```

The default source `0` refers to the default camera. Try `1` if you have another camera connected.

### Request a specific camera resolution

```bash
python app.py --source 0 --width 1280 --height 720
```

The resolution is a request to the camera driver; the camera may choose a different supported size.

### Process a video and save the result

```bash
python app.py --source "videos/input.mp4" --output "output/annotated.mp4"
```

Replace `videos/input.mp4` with the path to your video. The output directory is created automatically when needed.

### Process a video without a preview window

```bash
python app.py --source "videos/input.mp4" --output "output/annotated.mp4" --no-preview
```

Headless mode requires `--output` so that the processed video is saved.

### Change hand-tracking settings

```bash
python app.py --max-hands 1 --detection-confidence 0.7 --tracking-confidence 0.6
```

Confidence values must be between `0` and `1`. Higher thresholds may reduce weak detections but can also cause hands to be missed more often.

### Print hand landmark coordinates

```bash
python app.py --show-coordinates
```

Coordinates are printed in pixels for each detected hand and frame. This can produce a large amount of terminal output, so it is disabled by default.

### Disable mirroring or landmark drawing at startup

```bash
python app.py --no-mirror
python app.py --no-landmarks
```

### Display all available options

```bash
python hand_tracker.py --help
```

## Keyboard Controls

With the preview window focused:

| Key | Action |
|---|---|
| `Q` or `Esc` | Quit the application |
| `M` | Toggle horizontal mirroring |
| `L` | Toggle landmark and connection drawing |

## Command-Line Options

| Option | Default | Description |
|---|---|---|
| `--source SOURCE` | `0` | Camera index or input video path |
| `--output PATH` | None | Optional path for the annotated MP4 video |
| `--max-hands {1,2}` | `2` | Maximum number of hands to detect |
| `--detection-confidence VALUE` | `0.6` | Minimum initial hand-detection confidence |
| `--tracking-confidence VALUE` | `0.6` | Minimum confidence for continued tracking |
| `--width PIXELS` | Camera default | Requested webcam capture width |
| `--height PIXELS` | Camera default | Requested webcam capture height |
| `--no-mirror` | Off | Disable horizontal mirroring |
| `--no-landmarks` | Off | Do not draw hand landmarks and connections |
| `--show-coordinates` | Off | Print landmark pixel coordinates to the terminal |
| `--no-preview` | Off | Process without a preview window; requires `--output` |
| `--quiet` | Off | Hide informational log messages |

For the complete argument descriptions and defaults, run `python hand_tracker.py --help`.

## Run the Tests

The unit tests cover source parsing and command-line argument validation. They do not require a webcam.

```bash
python -m unittest -v test_hand_tracker.py
```

If using the Windows virtual environment without activating it:

```powershell
.\.venv312\Scripts\python.exe -m unittest -v test_hand_tracker.py
```

## Troubleshooting

### MediaPipe cannot be installed

Check which Python interpreter is being used. This project pins MediaPipe `0.10.21`; use Python 3.12 on Windows and install dependencies into that environment:

```powershell
py -3.12 -m venv .venv312
.\.venv312\Scripts\python.exe -m pip install -r requirements.txt
```

### PowerShell says scripts are disabled

Activating the virtual environment is optional. Use the environment's Python executable directly, as shown in the installation instructions.

### The webcam cannot be opened

- Close other applications that may be using the camera.
- Check that Windows has granted camera access to desktop applications.
- Try another camera index, such as `--source 1`.

### The preview window does not open

Run the application from a normal desktop session. For processing without a GUI, provide both `--no-preview` and `--output` with an input video.

### Tracking is slow

Try a smaller camera image or track one hand:

```bash
python app.py --width 640 --height 480 --max-hands 1
```

### No hands are detected

- Improve the lighting.
- Keep your hand inside the camera's field of view.
- Try lowering the confidence thresholds slightly:

```bash
python app.py --detection-confidence 0.5 --tracking-confidence 0.5
```

## Project Structure

```text
hand-tracking-opencv/
├── app.py                  # Convenient application entry point
├── hand_tracker.py         # CLI, video capture, tracking, drawing, and export
├── test_hand_tracker.py    # Unit tests for parsing and validation
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── Hand Tracking with OpenCV.md
├── SKILL.md
└── .gitignore              # Files excluded from Git
```

The `.venv312/` virtual environment and Python cache files are intentionally excluded from version control.

## Author

**Souhaiel**  
GitHub: [@ItSpoy](https://github.com/ItSpoy)

---

If you find this project useful, feel free to explore the code, run the tests, and adapt it to your own hand-tracking experiments.
