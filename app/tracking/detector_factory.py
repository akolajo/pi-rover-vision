from app.config import settings
from app.tracking.detectors.colour_blob_detector import ColourBlobDetector


def get_detector():
    if settings.DETECTOR_BACKEND == "tflite":
        from app.tracking.detectors.tflite_detector import TFLiteDetector
        return TFLiteDetector(
            model_path=settings.TFLITE_MODEL_PATH,
            labels_path=settings.TFLITE_LABELS_PATH,
            confidence_threshold=settings.DETECTION_CONFIDENCE_THRESHOLD,
        )

    if settings.DETECTOR_BACKEND == "colour":
        return ColourBlobDetector()

    raise ValueError(f"Unknown DETECTOR_BACKEND: {settings.DETECTOR_BACKEND}")


# Single shared instance, created once at import time.
detector = get_detector()