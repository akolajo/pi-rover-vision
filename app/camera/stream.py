import cv2

from app.camera.camera_manager import camera_manager
from app.tracking.detector import detect_red_target
from app.state import tracking_state


def generate_frames():
    camera_manager.start()

    while True:
        success, frame = camera_manager.read()
        if not success:
            break

        frame, tracking_info = detect_red_target(frame)
        tracking_state.update(tracking_info)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            buffer.tobytes() +
            b'\r\n'
        )