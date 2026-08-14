"""
Generative Geometric Art

Deterministic geometric pattern generator using Python Turtle graphics.
Renders multi-layered concentric polygonal compositions with configurable
symmetry, scaling, and color parameters.
"""

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

# =============================================================================
# IMPORTS & TYPE HINTS
# =============================================================================

import turtle
import math
from typing import List, Tuple

# =============================================================================
# GEOMETRIC ART RENDERER CLASS
# =============================================================================

class GeometricArtGenerator:
    """
    Deterministic geometric pattern renderer using Turtle graphics.

    Generates multi-layered concentric polygonal compositions with
    configurable symmetry, scaling, and color parameters.

    Attributes:
        config: Runtime configuration dictionary
        max_distance: Tracks maximum radial distance for outer circle calculation
    """

    def __init__(self, config: dict) -> None:
        """
        Initialize the geometric art generator.

        Args:
            config: Dictionary containing all rendering parameters
        """
        self.config = config
        self.max_distance: float = 0.0

        self._setup_screen()
        self._create_pen()

    def _setup_screen(self) -> None:
        """Initialize Turtle graphics display."""
        self.screen = turtle.Screen()
        self.screen.bgcolor(self.config["background_color"])
        self.screen.title(self.config["window_title"])
        self.screen.tracer(0)  # Instant render for performance

    def _create_pen(self) -> None:
        """Create and configure the drawing turtle."""
        self.pen = turtle.Turtle(visible=False)
        self.pen.speed(0)
        self.pen.pensize(self.config["pen_size"])

    # -------------------------------------------------------------------------
    # UTILITY FUNCTIONS
    # -------------------------------------------------------------------------

    @staticmethod
    def distance_from_center(x: float, y: float) -> float:
        """
        Calculate Euclidean distance from origin point (0,0).

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Distance value as float
        """
        return math.sqrt(x ** 2 + y ** 2)

    def track_max_distance(self, x: float, y: float) -> None:
        """Update maximum radial distance tracker."""
        current_distance = self.distance_from_center(x, y)
        self.max_distance = max(self.max_distance, current_distance)

    # -------------------------------------------------------------------------
    # DRAWING FUNCTIONS
    # -------------------------------------------------------------------------

    def draw_polygon(self, sides: int, size: float) -> None:
        """
        Draw a regular polygon and track vertex distances.

        Args:
            sides: Number of polygon vertices
            size: Length of each segment
        """
        angle = 360 / sides
        for _ in range(sides):
            x, y = self.pen.pos()
            self.track_max_distance(x, y)
            self.pen.forward(size)
            self.pen.right(angle)

    def draw_rotated_pattern(
        self,
        sides: int,
        size: float,
        repeats: int,
        palette: List[str]
    ) -> None:
        """
        Render a radially symmetric polygon pattern.

        Args:
            sides: Number of vertices per polygon
            size: Segment length for polygons
            repeats: Number of rotational iterations
            palette: List of color values for cycling
        """
        for i in range(repeats):
            self.pen.pencolor(palette[i % len(palette)])
            self.draw_polygon(sides, size)
            self.pen.right(360 / repeats)

    def draw_outer_circle(self) -> None:
        """
        Draw boundary circle around the entire composition.

        Radius calculated from tracked maximum distance plus padding.
        """
        if not self.config["draw_outer_circle"]:
            return

        radius = self.max_distance + self.config["circle_padding"]
        self.pen.penup()
        self.pen.goto(0, -radius)
        self.pen.setheading(0)
        self.pen.pencolor(self.config["circle_color"])
        self.pen.pendown()
        self.pen.circle(radius)

    # -------------------------------------------------------------------------
    # RENDERING ORCHESTRATION
    # -------------------------------------------------------------------------

    def render_primary_pattern(self) -> None:
        """Draw the central geometric composition."""
        self.draw_rotated_pattern(
            self.config["primary_sides"],
            self.config["segment_length"],
            self.config["repeats"],
            self.config["primary_palette"]
        )

    def render_layer1(self) -> None:
        """Draw first outer layer with hexagonal symmetry."""
        scaled_size = self.config["segment_length"] * self.config["layer1_scale"]
        self.draw_rotated_pattern(
            self.config["layer1_sides"],
            scaled_size,
            self.config["layer1_repeats"],
            self.config["layer1_palette"]
        )

    def render_layer2(self) -> None:
        """Draw second outer layer with enneagonal symmetry."""
        scaled_size = self.config["segment_length"] * self.config["layer2_scale"]
        self.draw_rotated_pattern(
            self.config["layer2_sides"],
            scaled_size,
            self.config["layer2_repeats"],
            self.config["layer2_palette"]
        )

    def render_all_layers(self) -> None:
        """Orchestrate complete layered composition rendering."""
        self.render_primary_pattern()
        self.render_layer1()
        self.render_layer2()

    def finalize_rendering(self) -> None:
        """Complete the rendering process with optional boundary circle."""
        self.draw_outer_circle()
        self.screen.update()

    def run(self) -> None:
        """Execute complete pattern generation pipeline."""
        self.render_all_layers()
        self.finalize_rendering()

    def cleanup(self) -> None:
        """Gracefully close Turtle graphics window."""
        turtle.bye()

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    generator = GeometricArtGenerator(CONFIG)
    try:
        generator.run()
    finally:
        generator.cleanup()
        turtle.done()
# --- render ---
screen.update()
turtle.done()
