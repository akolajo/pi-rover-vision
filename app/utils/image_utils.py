import cv2


def draw_detections(frame, detections):
    """Draws bounding boxes, labels and confidence for a list of Detection
    objects onto frame in place. Shared by every detector so annotated
    output looks the same regardless of which strategy produced it."""
    for det in detections:
        cv2.rectangle(frame, (det.x, det.y), (det.x + det.w, det.y + det.h), (0, 255, 0), 2)
        cx, cy = det.center
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
        label = f"{det.label} {det.confidence:.2f}"
        cv2.putText(frame, label, (det.x, max(det.y - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return frame