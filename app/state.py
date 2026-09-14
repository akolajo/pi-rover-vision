import threading


class TrackingState:
    def __init__(self):
        self._lock = threading.Lock()
        self._state = {
            "target_detected": False,
            "x": None, "y": None,
            "offset_x": None, "offset_y": None,
            "confidence": 0.0,
            "timestamp": None,
        }

    def update(self, new_state: dict):
        with self._lock:
            self._state = new_state

    def get(self) -> dict:
        with self._lock:
            return dict(self._state)


tracking_state = TrackingState()