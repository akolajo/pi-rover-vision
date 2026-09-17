import threading


class TrackingState:
    """Holds the most recent detection results so the API layer can read
    them without touching the camera loop directly."""

    def __init__(self):
        self._lock = threading.Lock()
        self._state = {"detections": [], "timestamp": None}

    def update(self, detections, timestamp):
        with self._lock:
            self._state = {
                "detections": [
                    {
                        "label": d.label,
                        "confidence": d.confidence,
                        "x": d.x, "y": d.y, "w": d.w, "h": d.h,
                        "center_x": d.center[0], "center_y": d.center[1],
                    }
                    for d in detections
                ],
                "timestamp": timestamp,
            }

    def get(self):
        with self._lock:
            return dict(self._state)


tracking_state = TrackingState()