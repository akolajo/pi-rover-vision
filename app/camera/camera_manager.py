import cv2
import numpy as np

def get_camera():
    return cv2.VideoCapture(0)

def generate_frames(camera):

    while True:

        success, frame = camera.read()

        if not success:
            break

        # Convert to HSV color space
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        # Define range of red color in HSV
        lower_red1 = np.array([0,120,70])
        upper_red1 = np.array([10,255,255])

        lower_red2 = np.array([170,120,70])
        upper_red2 = np.array([180,255,255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        
        mask = mask1 + mask2

        # Clean noise
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area > 1000: #ignore small noise 
                x,y,w,h = cv2.boundingRect(cnt)

                # Draw bounding box
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

                # Draw center point
                cx = x + w//2
                cy = y + h//2
                cv2.circle(frame, (cx,cy), 5, (255,0,0), -1)

                # Label
                cv2.putText(frame, 'Target', (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                

        ret, buffer = cv2.imencode('.jpg', frame)

        if not ret:
            continue

        yield(
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            buffer.tobytes() +
            b'\r\n'
        )