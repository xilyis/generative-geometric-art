"""
Generative Geometric Art

Deterministic geometric pattern generator using Python Turtle graphics.
Renders multi-layered concentric polygonal compositions with configurable
symmetry, scaling, and color parameters.
"""

import turtle
import math

# === MAIN SHAPE (center) ===
SIDES       = 9
SIZE        = 60
REPEATS     = 18
PENSIZE     = 2

# === OUTER LAYER 1 ===
L1_SIDES    = 6
L1_REPEATS  = 12
L1_SCALE    = 1
L1_PALETTE  = ["#FFFFFF", "#FFFFFF"]

# === OUTER LAYER 2 ===
L2_SIDES    = 9
L2_REPEATS  = 18
L2_SCALE    = 1.5
L2_PALETTE  = ["#FFFFFF", "#FFFFFF"]

# === OUTER CIRCLE ===
DRAW_OUTER_CIRCLE = True
CIRCLE_PADDING    = 0
CIRCLE_COLOR      = "#FFFFFF"

# === BACKGROUND ===
BGCOLOR = "black"

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
