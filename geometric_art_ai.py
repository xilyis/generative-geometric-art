"""
Generative Geometric Art with Interactive AI

Gesture-controlled geometric pattern rendering using MediaPipe computer vision.
Extends the generator with real-time hand and face tracking.
"""

# =============================================================================
# CONFIGURATION
# =============================================================================

CONFIG = {
    # Pattern parameters
    "primary_sides": 9,
    "segment_length": 60,
    "repeats": 18,
    "pen_size": 2,

    # Layer 1 (hexagonal)
    "layer1_sides": 6,
    "layer1_repeats": 12,
    "layer1_scale": 1.0,

    # Layer 2 (enneagonal)
    "layer2_sides": 9,
    "layer2_repeats": 18,
    "layer2_scale": 1.5,

    # Colors
    "background": "black",
    "pattern_color": "white",

    # Detection thresholds
    "hand_motion_threshold": 5,
    "smile_bbox_width": 0.25,
    "pulse_min": 0.8,
    "pulse_max": 1.2,
    "pulse_increment": 0.02,
    "face_rotation_speed": 1,
    "hand_rotation_speed": 5,

    # MediaPipe confidence
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5,
}

# =============================================================================
# IMPORTS & SETUP
# =============================================================================

import cv2
import mediapipe as mp
import turtle
import sys
from typing import Optional, Tuple, Dict, Any


class GeometricArtAI:
    """
    AI-enhanced geometric pattern renderer with gesture-controlled interaction.

    Attributes:
        config: Runtime configuration dictionary
        rotation: Current canvas rotation angle
        pulse_scale: Dynamic scaling factor for pulsing effect
        manual_pulse: Spacebar override state
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.rotation: float = 0.0
        self.pulse_scale: float = 1.0
        self.pulse_direction: int = 1
        self.manual_pulse: bool = False
        self.prev_hand_pos: Optional[Tuple[int, int]] = None

        self._setup_screen()
        self._setup_media_pipe()
        self._setup_key_bindings()

    def _setup_screen(self) -> None:
        """Initialize Turtle graphics display."""
        self.screen = turtle.Screen()
        self.screen.bgcolor(self.config["background"])
        self.screen.title("Generative Geometric Art — AI Demo")
        self.screen.tracer(0)

        self.pen = turtle.Turtle(visible=False)
        self.pen.speed(0)
        self.pen.pensize(self.config["pen_size"])

    def _setup_media_pipe(self) -> None:
        """Initialize MediaPipe hand and face detection models."""
        try:
            self.mp_hands = mp.solutions.hands.Hands(
                min_detection_confidence=self.config["min_detection_confidence"],
                min_tracking_confidence=self.config["min_tracking_confidence"]
            )
            self.mp_face = mp.solutions.face_detection.FaceDetection(
                model_selection=0,
                min_detection_confidence=self.config["min_detection_confidence"]
            )
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise RuntimeError("Webcam unavailable. Check device permissions.")
        except Exception as e:
            print(f"[ERROR] Computer vision initialization failed: {e}")
            sys.exit(1)

    def _setup_key_bindings(self) -> None:
        """Register keyboard shortcuts."""
        self.screen.listen()
        self.screen.onkeypress(self._toggle_manual_pulse, "space")
        self.screen.onkeypress(self._quit_app, "q")

    # -------------------------------------------------------------------------
    # DRAWING FUNCTIONS
    # -------------------------------------------------------------------------

    def draw_polygon(self, t: turtle.Turtle, sides: int, size: float) -> None:
        """Render a regular polygon."""
        angle = 360 / sides
        for _ in range(sides):
            t.forward(size)
            t.right(angle)

    def draw_rotated_pattern(
        self,
        t: turtle.Turtle,
        sides: int,
        size: float,
        repeats: int,
        color: str = "white"
    ) -> None:
        """Render a radially symmetric polygon pattern."""
        t.pencolor(color)
        for _ in range(repeats):
            self.draw_polygon(t, sides, size)
            t.right(360 / repeats)

    def render_frame(self) -> None:
        """Clear and redraw the complete geometric pattern."""
        self.pen.clear()
        self.pen.setheading(int(self.rotation))

        # Primary layer
        self.draw_rotated_pattern(
            self.pen,
            self.config["primary_sides"],
            self.config["segment_length"],
            self.config["repeats"]
        )

        # Layer 1
        size_l1 = self.config["segment_length"] * self.config["layer1_scale"] * self.pulse_scale
        self.draw_rotated_pattern(
            self.pen,
            self.config["layer1_sides"],
            size_l1,
            self.config["layer1_repeats"]
        )

        # Layer 2
        size_l2 = self.config["segment_length"] * self.config["layer2_scale"] * self.pulse_scale
        self.draw_rotated_pattern(
            self.pen,
            self.config["layer2_sides"],
            size_l2,
            self.config["layer2_repeats"]
        )

        self.screen.update()

    # -------------------------------------------------------------------------
    # INTERACTION HANDLERS
    # -------------------------------------------------------------------------

    def _toggle_manual_pulse(self) -> None:
        """Toggle spacebar pulse override."""
        self.manual_pulse = not self.manual_pulse

    def _quit_app(self) -> None:
        """Graceful application termination."""
        self.running = False

    def _process_hands(self, frame: Any) -> Optional[float]:
        """Detect hand position and return rotation delta."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(rgb_frame)

        if not results.multi_hand_landmarks:
            self.prev_hand_pos = None
            return None

        h, w, _ = frame.shape
        hand = results.multi_hand_landmarks[0]
        x = int(hand.landmark[8].x * w)
        y = int(hand.landmark[8].y * h)

        if self.prev_hand_pos is not None:
            dx = x - self.prev_hand_pos[0]
            if dx > self.config["hand_motion_threshold"]:
                return self.config["hand_rotation_speed"]
            elif dx < -self.config["hand_motion_threshold"]:
                return -self.config["hand_rotation_speed"]

        self.prev_hand_pos = (x, y)
        return None

    def _process_face(self, frame: Any) -> Tuple[bool, bool]:
        """Detect face presence and approximate smile. Returns (face_present, smile)."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_face.process(rgb_frame)

        if not results.detections:
            return False, False

        for detection in results.detections:
            box = detection.location_data.relative_bounding_box
            if box.width > self.config["smile_bbox_width"]:
                return True, True
        return True, False

    def _update_pulse(self, smile_detected: bool) -> None:
        """Apply pulse animation if triggered."""
        if smile_detected or self.manual_pulse:
            self.pulse_scale += self.config["pulse_increment"] * self.pulse_direction
            if self.pulse_scale >= self.config["pulse_max"] or self.pulse_scale <= self.config["pulse_min"]:
                self.pulse_direction *= -1
        else:
            self.pulse_scale = 1.0

    # -------------------------------------------------------------------------
    # MAIN LOOP
    # -------------------------------------------------------------------------

    def run(self) -> None:
        """Main rendering and interaction loop."""
        self.running = True

        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    break

                # Process AI inputs
                hand_delta = self._process_hands(frame)
                if hand_delta is not None:
                    self.rotation += hand_delta
                else:
                    face_present, smile = self._process_face(frame)
                    if face_present:
                        self.rotation += self.config["face_rotation_speed"]
                    self._update_pulse(smile)

                # Render
                self.render_frame()
                cv2.imshow("Webcam", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        finally:
            self._cleanup()

    def _cleanup(self) -> None:
        """Release resources on exit."""
        self.cap.release()
        cv2.destroyAllWindows()
        if hasattr(self, "mp_hands"):
            self.mp_hands.close()
        if hasattr(self, "mp_face"):
            self.mp_face.close()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    app = GeometricArtAI(CONFIG)
    app.run()

cap.release()
cv2.destroyAllWindows()
