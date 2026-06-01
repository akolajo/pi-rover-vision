import cv2

def get_camera():
    return cv2.VideoCapture(0)

def generate_frames(camera):

    while True:

        success, frame = camera.read()

        if not success:
            break

        ret, buffer = cv2.imencode('.jpg', frame)

        if not ret:
            continue

        yield(
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            buffer.tobytes() +
            b'\r\n'
        )