SACRED GEOMETRY — QUICK SETUP 
=============================================

Geometry is the hidden arithmetic of the universe. It can be discovered by inspecting ratios like the golden mean 
and the vesica piscis which appear in shells, star clusters, and ancient temples alike. Artisans have long encoded 
these patterns to mirror divine and cosmic order. These same shapes can be weaved through programming into 
software and stored on‑chain, not only preserving this sacred art and practice but solidifying it through digital 
realities. 


Overview:
- Part A: Experiment with variables to generate ancient geometric patterns.
- Part B (AI + User Dection): AI pattern that changes once a user or hand is detected. Includes a manual fallback.


1) Install Python 3.10–3.12
---
Check:
  python --version     (Windows/macOS)
  or
  python3 --version    (macOS/Linux)

2) Create a virtual environment
---
Windows (PowerShell):
  py -m venv venv
  .\venv\Scripts\activate

macOS/Linux (bash/zsh):
  python3 -m venv venv
  source venv/bin/activate

3) Install packages
---
pip install pygame opencv-python mediapipe

If MediaPipe install fails on your machine, continue anyway — Part B has a manual fallback (SPACE toggles palette).

4) Run scripts
---
Part A (Turtle):
  python Sacred_Patterns.py

Part B (AI Gesture Tracking + Pattern Interaction):
  python Sacred_PatternsAI.py
  - If "AI mode ON" appears, activate webcam and raise a hand to interact with the rotation and pulsing.
  - If "AI mode OFF", press SPACE to toggle the rotation and pulsing manually .


Tips
----
- Experiment with parameters for a beautiful pattern.
- If webcam lighting is poor, switch to manual mode (SPACE) for the same functionality.
