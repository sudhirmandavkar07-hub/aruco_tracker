import cv2
from cv2 import aruco
import numpy as np

# --- SETUP ---
cap = cv2.VideoCapture(0)
print("Camera opened:", cap.isOpened())
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

THRESHOLD = 10

while True:
    ret, frame = cap.read() 
    if not ret:
        break

    # Frame dimensions and center point
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2

    # Draw crosshair at center
    cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (0, 255, 0), 2)
    cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (0, 255, 0), 2)

    # Detect ArUco markers
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)

    command = "NO TARGET"

    if ids is not None:
        # Get the 4 corners of the first detected marker
        marker_corners = corners[0][0]

        # Calculate centroid by averaging all 4 corners
        marker_cx = int(np.mean(marker_corners[:, 0]))
        marker_cy = int(np.mean(marker_corners[:, 1]))

        # Error vector
        error_x = marker_cx - cx
        error_y = marker_cy - cy
        # Draw error vector line (frame center to marker center)
        cv2.line(frame, (cx, cy), (marker_cx, marker_cy), (0, 0, 255), 2)

        # Draw dot at marker centroid
        cv2.circle(frame, (marker_cx, marker_cy), 5, (255, 0, 0), -1)

        # Decide command based on error
        if abs(error_x) < THRESHOLD and abs(error_y) < THRESHOLD:
            command = "LOCK ENGAGED"
        elif abs(error_x) > abs(error_y):
            if error_x < 0:
                command = "MOVE LEFT"
            else:
                command = "MOVE RIGHT"
        else:
            if error_y < 0:
                command = "MOVE UP"
            else:
                command = "MOVE DOWN"
    # Display command text
    color = (0, 255, 0) if command == "LOCK ENGAGED" else (0, 0, 255)
    cv2.putText(frame, command, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    cv2.imshow("ArUco Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Outside the loop - no indent
cap.release()
cv2.destroyAllWindows()