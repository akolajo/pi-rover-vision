import threading
import cv2

from app.camera.interfaces.camera_interface import CameraInterface


class OpenCVCamera(CameraInterface):
    """Used for laptop development - any webcam OpenCV can see via V4L2/DirectShow.
    Also works on the Pi if the camera is exposed as a V4L2 device."""

    def __init__(self, source=0):
        self._source = source
        self._cap = None
        self._lock = threading.Lock()

    def start(self):
        if self._cap is None:
            self._cap = cv2.VideoCapture(self._source)
            if not self._cap.isOpened():
                raise RuntimeError(f"Could not open camera source {self._source}")
        return self

    def read(self):
        if self._cap is None:
            raise RuntimeError("Camera not started - call start() first")
        with self._lock:
            return self._cap.read()

    def stop(self):
        if self._cap is not None:
            self._cap.release()
            self._cap = None