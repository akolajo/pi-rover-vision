import threading
import cv2


class CameraManager:
    """Owns the physical camera. Only responsibility: open it, grab frames,
    release it. No detection/tracking logic lives here."""

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
            success, frame = self._cap.read()
        return success, frame

    def stop(self):
        if self._cap is not None:
            self._cap.release()
            self._cap = None


# Single shared instance - open the camera exactly once, reuse it everywhere.
camera_manager = CameraManager()