from flask import Flask, render_template, Response
from camera_manager import generate_frames, get_camera
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

stream = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

camera = get_camera()


@stream.route('/')
def index():
    return render_template('index.html')


@stream.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == '__main__':
    stream.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)