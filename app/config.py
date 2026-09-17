import os


class Settings:
    # "opencv" for laptop webcam dev, "picamera2" for real Pi hardware.
    CAMERA_BACKEND: str = os.getenv("CAMERA_BACKEND", "opencv")
    CAMERA_SOURCE: int = int(os.getenv("CAMERA_SOURCE", "0"))
    
    # "colour" for the HSV blob detector, "tflite" for MobileNet-SSD.
    DETECTOR_BACKEND: str = os.getenv("DETECTOR_BACKEND", "colour")
    TFLITE_MODEL_PATH: str = os.getenv("TFLITE_MODEL_PATH", "models/detect.tflite")
    TFLITE_LABELS_PATH: str = os.getenv("TFLITE_LABELS_PATH", "models/labelmap.txt")
    DETECTION_CONFIDENCE_THRESHOLD: float = float(os.getenv("DETECTION_CONFIDENCE_THRESHOLD", "0.5"))


settings = Settings()