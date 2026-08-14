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

import cv2
import mediapipe as mp
import turtle
import math


# --- helpers ---
def draw_polygon(t, sides, size):
    angle = 360 / sides
    for _ in range(sides):
        t.forward(size)
        t.right(angle)

def draw_rotated_pattern(t, sides, size, repeats, color="white"):
    t.pencolor(color)
    for _ in range(repeats):
        draw_polygon(t, sides, size)
        t.right(360 / repeats)

def draw_pattern(rotation=0, pulse_scale=1.0):
    pen.clear()
    pen.setheading(rotation)

    draw_rotated_pattern(pen, SIDES, SIZE, REPEATS)
    draw_rotated_pattern(pen, L1_SIDES, SIZE * L1_SCALE * pulse_scale, L1_REPEATS)
    draw_rotated_pattern(pen, L2_SIDES, SIZE * L2_SCALE * pulse_scale, L2_REPEATS)

    screen.update()

# === AI Setup ===
mp_hands = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_face = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

rotation = 0
pulse_dir = 1
pulse_scale = 1.0
manual_pulse = False

# Hand tracking
prev_x, prev_y = None, None
hand_rotation_speed = 0

# Spacebar handler
def toggle_pulse():
    global manual_pulse
    manual_pulse = not manual_pulse

screen.listen()
screen.onkeypress(toggle_pulse, "space")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    hand_results = mp_hands.process(rgb)
    if hand_results.multi_hand_landmarks:
        h, w, _ = frame.shape
        hand = hand_results.multi_hand_landmarks[0]
        # Use tip of index finger
        x = int(hand.landmark[8].x * w)
        y = int(hand.landmark[8].y * h)

        if prev_x is not None and prev_y is not None:
            dx = x - prev_x
            # Simple heuristic: horizontal motion = rotation control
            if dx > 5:
                hand_rotation_speed = 5
            elif dx < -5:
                hand_rotation_speed = -5
            else:
                hand_rotation_speed = 0
            rotation += hand_rotation_speed

        prev_x, prev_y = x, y
    else:
        prev_x, prev_y = None, None

        # Detect face
    face_results = mp_face.process(rgb)
    smile_detected = False

    if face_results.detections:
        # Pattern rotates slowly when a face is present
        rotation += 1

        # Check "smile" proxy: large bounding box width
        for detection in face_results.detections:
            box = detection.location_data.relative_bounding_box
            if box.width > 0.25:  # heuristic: smiling
                smile_detected = True
                break

    # Apply pulse if face is detected OR manual override
    if smile_detected or manual_pulse:
        pulse_scale += 0.02 * pulse_dir
        if pulse_scale > 1.2 or pulse_scale < 0.8:
            pulse_dir *= -1
    else:
        pulse_scale = 1.0  # reset when neither smile nor manual pulse

    # Draw updated pattern
    draw_pattern(rotation, pulse_scale)

    # Show webcam feed
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
