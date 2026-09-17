import cv2
import numpy as np

from app.tracking.detector_interface import Detection, DetectorInterface

try:
    # Lightweight, ARM-friendly. Installed on the Pi via requirements-pi.txt.
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    # tflite-runtime has no official Windows wheel, so on the laptop we fall
    # back to the interpreter bundled inside full TensorFlow instead.
    from tensorflow.lite import Interpreter


class TFLiteDetector(DetectorInterface):
    """Wraps a quantised SSD-style TFLite model (e.g. COCO SSD MobileNet v1).
    Assumes the standard TF Object Detection API output layout:
    [boxes, classes, scores, count]."""

    def __init__(self, model_path, labels_path, confidence_threshold=0.5):
        self._interpreter = Interpreter(model_path=model_path)
        self._interpreter.allocate_tensors()
        self._input_details = self._interpreter.get_input_details()
        self._output_details = self._interpreter.get_output_details()
        _, self._input_h, self._input_w, _ = self._input_details[0]["shape"]
        self._confidence_threshold = confidence_threshold
        self._labels = self._load_labels(labels_path)

    @staticmethod
    def _load_labels(path):
        with open(path, "r") as f:
            labels = [line.strip() for line in f.readlines()]
        # The Google-provided labelmap reserves index 0 as a background
        # placeholder ("???"). Drop it so label indices line up with scores.
        if labels and labels[0] == "???":
            labels.pop(0)
        return labels

    def detect(self, frame):
        height, width = frame.shape[:2]

        resized = cv2.resize(frame, (self._input_w, self._input_h))
        input_data = np.expand_dims(resized, axis=0)

        input_dtype = self._input_details[0]["dtype"]
        if input_dtype == np.float32:
            input_data = (np.float32(input_data) - 127.5) / 127.5

        self._interpreter.set_tensor(self._input_details[0]["index"], input_data)
        self._interpreter.invoke()

        boxes = self._interpreter.get_tensor(self._output_details[0]["index"])[0]
        classes = self._interpreter.get_tensor(self._output_details[1]["index"])[0]
        scores = self._interpreter.get_tensor(self._output_details[2]["index"])[0]

        detections = []
        for box, class_id, score in zip(boxes, classes, scores):
            if score < self._confidence_threshold:
                continue

            ymin, xmin, ymax, xmax = box
            x = int(xmin * width)
            y = int(ymin * height)
            w = int((xmax - xmin) * width)
            h = int((ymax - ymin) * height)

            label_index = int(class_id)
            label = self._labels[label_index] if label_index < len(self._labels) else "unknown"

            detections.append(Detection(label, float(score), x, y, w, h))

        return detections