import cv2
import numpy as np

from app.tracking.detector_interface import Detection, DetectorInterface

LOWER_RED_1 = np.array([0, 120, 70])
UPPER_RED_1 = np.array([10, 255, 255])
LOWER_RED_2 = np.array([170, 120, 70])
UPPER_RED_2 = np.array([180, 255, 255])

MIN_CONTOUR_AREA = 1000


class ColourBlobDetector(DetectorInterface):
    """Classical HSV threshold detector. Cheap and deterministic, but only
    ever finds objects matching a fixed colour range. Returns one Detection
    per qualifying contour rather than just the largest, so multiple red
    objects in frame are all reported."""

    def __init__(self, lower1=LOWER_RED_1, upper1=UPPER_RED_1,
                 lower2=LOWER_RED_2, upper2=UPPER_RED_2,
                 min_area=MIN_CONTOUR_AREA, label="red_object"):
        self._lower1, self._upper1 = lower1, upper1
        self._lower2, self._upper2 = lower2, upper2
        self._min_area = min_area
        self._label = label
        self._kernel = np.ones((5, 5), np.uint8)

    def detect(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self._lower1, self._upper1) + \
            cv2.inRange(hsv, self._lower2, self._upper2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self._kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, self._kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        frame_area = frame.shape[0] * frame.shape[1]

        detections = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self._min_area:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            confidence = min(area / frame_area, 1.0)
            detections.append(Detection(self._label, confidence, x, y, w, h))

        return detections