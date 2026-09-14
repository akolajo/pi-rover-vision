import os


class Settings:
    # "opencv" for laptop webcam dev, "picamera2" for real Pi hardware.
    CAMERA_BACKEND: str = os.getenv("CAMERA_BACKEND", "opencv")
    CAMERA_SOURCE: int = int(os.getenv("CAMERA_SOURCE", "0"))


settings = Settings()