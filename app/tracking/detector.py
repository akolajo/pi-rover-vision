"""Detection logic only. Takes a frame, returns (annotated_frame, tracking_info).
No camera access, no GPIO - keeps this testable off the Pi."""

import time
import cv2
import numpy as np

LOWER_RED_1 = np.array([0, 120, 70])
UPPER_RED_1 = np.array([10, 255, 255])
LOWER_RED_2 = np.array([170, 120, 70])
UPPER_RED_2 = np.array([180, 255, 255])

MIN_CONTOUR_AREA = 1000


def detect_red_target(frame):
    height, width = frame.shape[:2]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, LOWER_RED_1, UPPER_RED_1)
    mask2 = cv2.inRange(hsv, LOWER_RED_2, UPPER_RED_2)
    mask = mask1 + mask2

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    tracking_info = {
        "target_detected": False,
        "x": None, "y": None,
        "offset_x": None, "offset_y": None,
        "confidence": 0.0,
        "timestamp": time.time(),
    }

    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area > MIN_CONTOUR_AREA:
            x, y, w, h = cv2.boundingRect(largest)
            cx, cy = x + w // 2, y + h // 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
            cv2.putText(frame, "Target", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            tracking_info.update({
                "target_detected": True,
                "x": cx, "y": cy,
                "offset_x": cx - width // 2,
                "offset_y": cy - height // 2,
                "confidence": min(area / (width * height), 1.0),
            })

    return frame, tracking_info