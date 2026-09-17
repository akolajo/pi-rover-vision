import time
import cv2

from app.camera.camera_factory import camera
from app.tracking.detector_factory import detector
from app.utils.image_utils import draw_detections
from app.state import tracking_state


def generate_frames():
    camera.start()

    while True:
        success, frame = camera.read()
        if not success:
            break

        detections = detector.detect(frame)
        tracking_state.update(detections, time.time())
        draw_detections(frame, detections)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            buffer.tobytes() +
            b'\r\n'
        )