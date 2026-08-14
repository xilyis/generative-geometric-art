# Generative Geometric Art with Interactive AI

A generative art system that synthesizes geometric patterns with computer vision-based interaction. Part A produces deterministic geometric compositions using Python Turtle. The project is extended with real-time hand and face tracking, enabling gesture-controlled manipulation of the visual output.

---

## Overview

Geometric art encodes mathematical proportions found throughout natural systems — shells, star clusters, crystalline structures, and classical architecture. This project translates those ratios into algorithmic art, rendering them through programmatic geometry and allowing real-time interaction through computer vision.

**Key Capabilities:**
- Parametric generation of layered polygonal patterns (enneagons, hexagons, circles)
- Golden ratio-inspired scaling across concentric layers
- Real-time rotation and pulse animation controlled by hand gestures or facial presence
- Manual fallback mode for environments without webcam access

---

## Installation

### Prerequisites

- Python 3.10–3.12
- pip package manager
- Webcam (for Part B AI interaction only)

### Steps

1. **Clone the repository**
      git clone <repository-url>
   cd generative-geometric-art
   ```

2. **Create a virtual environment**
   ```bash
   # Windows (PowerShell)
   py -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux (bash/zsh)
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install pygame opencv-python mediapipe
   ```

   **Note:** If MediaPipe installation fails on your system, Part B operates in manual mode using keyboard input. Part A functions without this dependency.

---

## Usage

### Part A — Generative Geometry

Run the deterministic pattern generator:bash
python geometric_art.py
This script renders a multi-layered geometric composition using Python's Turtle graphics module. Parameters are configurable in the source file to adjust polygon sides, scale factors, repetition counts, and color palettes.

### Part B — Interactive AI Mode

Run the gesture-controlled variant:bash
python geometric_art_ai.py
**Interaction Methods:**

| Input | Effect |
|---|---|
| Hand present in frame | Controls rotation direction based on lateral movement |
| Face detected | Slows baseline rotation rate |
| Smile detected (bounding box heuristic) | Triggers pulse animation on outer layers |
| Spacebar (keyboard) | Manual pulse toggle (fallback mode) |
| Press 'q' | Exit application |

---

## Project Structuregenerative-geometric-art/
├── geometric_art.py        # Part A: Static generative geometry
├── geometric_art_ai.py     # Part B: AI-enhanced interactive variant
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies list

---

## Configuration

All runtime parameters are centralized in the `CONFIG` dictionary within each script.

### Configurable Parameters in `geometric_art.py`:

| Parameter Key | Description | Default Value |
|---|---|---|
| `"primary_sides"` | Primary polygon vertex count | 9 |
| `"segment_length"` | Base segment length | 60 |
| `"repeats"` | Rotation iterations for primary layer | 18 |
| `"layer1_scale"`, `"layer2_scale"` | Relative sizing of outer layers | 1.0, 1.5 |
| `"background_color"` | Canvas background | black |
| `"circle_color"` | Outer boundary ring | white |
| `"draw_outer_circle"` | Toggle bounding ring | true |

### Additional Parameters in `geometric_art_ai.py`:

| Parameter Key | Description | Default Value |
|---|---|---|
| `"hand_motion_threshold"` | Pixels for hand motion detection | 5 |
| `"smile_bbox_width"` | Bounding box width threshold for smile | 0.25 |
| `"pulse_min"`, `"pulse_max"` | Pulse animation boundaries | 0.8, 1.2 |
| `"face_rotation_speed"` | Rotation speed when face detected | 1 |
| `"hand_rotation_speed"` | Rotation speed from hand control | 5 |
| `"min_detection_confidence"` | MediaPipe detection threshold | 0.5 |

Adjust values to explore variations in symmetry, density, and visual rhythm.

---

## Technical Stack

| Component | Purpose |
|---|---|
| Python Turtle | Vector-based rendering of geometric primitives |
| OpenCV | Webcam capture and frame processing |
| MediaPipe | Hand landmark detection and face bounding box extraction |
| NumPy (implicit) | Coordinate mathematics and distance calculations |

---

## Known Limitations

- **Illumination Sensitivity:** Facial and hand detection accuracy depends on ambient lighting conditions
- **Cross-Platform Compatibility:** MediaPipe demonstrates variable success rates across operating systems
- **Performance Constraints:** Real-time rendering may experience latency on lower-end hardware with elevated repeat counts
- **Smile Detection Mechanism:** Employs bounding box width heuristic; does not constitute a true facial expression classifier

---

## Planned Enhancements

- Export rendered patterns to SVG or PNG for archival preservation
- Expand gesture vocabulary (pinch, fist, open palm states)

---

## Credits

Influenced by classical geometric tradition and contemporary creative coding methodology. Implementation adheres to open-source computer vision framework specifications.

---

## License

MIT License — Refer to LICENSE file for complete terms and conditions.
