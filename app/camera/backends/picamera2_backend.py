import threading


class Picamera2Camera:
    """Pi-only backend. picamera2 is imported lazily inside start() so this
    module can exist in the codebase without breaking laptop dev, where
    picamera2 isn't installed."""

    def __init__(self, resolution=(640, 480)):
        self._resolution = resolution
        self._picam = None
        self._lock = threading.Lock()

    def start(self):
        if self._picam is None:
            from picamera2 import Picamera2  # deferred import - Pi only

            self._picam = Picamera2()
            config = self._picam.create_video_configuration(
                main={"size": self._resolution, "format": "BGR888"}
            )
            self._picam.configure(config)
            self._picam.start()
        return self

    def read(self):
        if self._picam is None:
            raise RuntimeError("Camera not started - call start() first")
        with self._lock:
            frame = self._picam.capture_array()
        return True, frame

    def stop(self):
        if self._picam is not None:
            self._picam.stop()
            self._picam = None