# ArUco Marker Tracking System

A real-time autonomous spatial tracking system using computer vision.

## Dependencies
- Python 3.x
- opencv-contrib-python
- numpy

## Installation
pip install opencv-contrib-python numpy

## How to Run
python main.py

## Tracking Logic
- Detects a 5x5 ArUco marker (ID 0) using webcam
- Calculates error vector between frame center and marker centroid
- Displays movement commands (MOVE LEFT/RIGHT/UP/DOWN) based on offset
- Shows LOCK ENGAGED when marker is within ±10 pixels of center

## Target Setup
- Go to https://chev.me/arucogen/
- Select Dictionary: 5x5_50, Marker ID: 0
- Display on phone at max brightness
