"""
Generative Geometric Art

Deterministic geometric pattern generator using Python Turtle graphics.
Renders multi-layered concentric polygonal compositions with configurable
symmetry, scaling, and color parameters.
"""

import turtle
import math

# =============================================================================
# CONFIGURATION
# =============================================================================

CONFIG = {
    # Primary pattern (center)
    "primary_sides": 9,
    "segment_length": 60,
    "repeats": 18,
    "pen_size": 2,
    "primary_palette": ["#FFFFFF"],

    # Outer layer 1
    "layer1_sides": 6,
    "layer1_repeats": 12,
    "layer1_scale": 1.0,
    "layer1_palette": ["#FFFFFF", "#FFFFFF"],

    # Outer layer 2
    "layer2_sides": 9,
    "layer2_repeats": 18,
    "layer2_scale": 1.5,
    "layer2_palette": ["#FFFFFF", "#FFFFFF"],

    # Outer boundary circle
    "draw_outer_circle": True,
    "circle_padding": 0,
    "circle_color": "#FFFFFF",

    # Background
    "background_color": "black",

    # Window settings
    "window_title": "Generative Geometric Art — Part A"
}

# --- setup ---
screen = turtle.Screen()
screen.bgcolor(BGCOLOR)
screen.title("Generative Geometric Art")
screen.tracer()    # instant render

pen = turtle.Turtle(visible=False)
pen.speed(0)
pen.pensize(PENSIZE)

# track max distance
max_distance = 0

# --- helpers ---
def distance_from_center(x, y):
    """Return distance of (x,y) from (0,0)."""
    return math.sqrt(x**2 + y**2)

def draw_polygon(t, sides, size):
    """Draw a regular polygon and update max distance."""
    global max_distance
    angle = 360 / sides
    for _ in range(sides):
        x, y = t.pos()
        max_distance = max(max_distance, distance_from_center(x, y))
        t.forward(size)
        t.right(angle)

def draw_rotated_pattern(t, sides, size, repeats, palette):
    for i in range(repeats):
        t.pencolor(palette[i % len(palette)])
        draw_polygon(t, sides, size)
        t.right(360 / repeats)

# --- draw layers ---
draw_rotated_pattern(pen, SIDES, SIZE, REPEATS, ["#FFFFFF"])
draw_rotated_pattern(pen, L1_SIDES, SIZE * L1_SCALE, L1_REPEATS, L1_PALETTE)
draw_rotated_pattern(pen, L2_SIDES, SIZE * L2_SCALE, L2_REPEATS, L2_PALETTE)

# --- outer circle ---
if DRAW_OUTER_CIRCLE:
    radius = max_distance + CIRCLE_PADDING
    pen.penup()
    pen.goto(0, -radius)
    pen.setheading(0)
    pen.pencolor(CIRCLE_COLOR)
    pen.pendown()
    pen.circle(radius)

# --- render ---
screen.update()
turtle.done()
