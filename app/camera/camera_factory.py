from app.config import settings
from app.camera.backends.opencv_backend import OpenCVCamera


def get_camera():
    if settings.CAMERA_BACKEND == "picamera2":
        from app.camera.backends.picamera2_backend import Picamera2Camera
        return Picamera2Camera()

    if settings.CAMERA_BACKEND == "opencv":
        return OpenCVCamera(source=settings.CAMERA_SOURCE)

    raise ValueError(f"Unknown CAMERA_BACKEND: {settings.CAMERA_BACKEND}")


# Single shared instance, created once at import time.
camera = get_camera()