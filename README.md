

# Vision System Repository Architecture for the CamJam EduKit Rover

## Goals

You already have:

* A rover repository running on a Raspberry Pi Zero 2W
* A web UI for remote control
* Motor control for the rover chassis

You want to build:

* A completely separate vision system repo first
* Face/object detection and tracking
* Pan/tilt camera control using two servos/motors
* Video streaming to the existing rover webpage
* Eventually autonomous rover-following behavior

This is the correct approach.

The key architectural principle is:

> Treat the vision system as an independent subsystem with clean interfaces.

That will let you:

* Develop independently
* Test without the rover moving
* Swap tracking models later
* Reuse the system on another robot
* Merge cleanly into the rover project later

---

# Recommended High-Level Architecture

You should structure this as:

```text
+-----------------------------+
|         Web Frontend        |
|  video stream + controls    |
+-------------+---------------+
              |
              v
+-----------------------------+
|        Vision Server        |
|  detection/tracking logic   |
|  pan/tilt controller        |
|  camera streaming           |
+-------------+---------------+
              |
     +--------+--------+
     |                 |
     v                 v
+----------+     +-----------+
| Camera   |     | Pan/Tilt  |
| Module   |     | Servos    |
+----------+     +-----------+
```

Later:

```text
+-----------------------------+
|     Rover Control System    |
+-------------+---------------+
              ^
              |
     tracking target position
```

The important thing:

The vision system should expose:

* video stream
* tracking state
* target coordinates
* pan/tilt state
* control API

through APIs/websockets.

---

# Recommended Repository Strategy

## Phase 1 — Separate Repo (Recommended)

Create a standalone repo:

```text
rover-vision-system/
```

Do NOT merge yet.

You want rapid iteration without worrying about:

* rover motor regressions
* deployment coupling
* dependency conflicts
* GPIO conflicts
* camera integration issues

Once stable:

* integrate as submodule
* or merge into monorepo
* or run both services independently

---

# Recommended Repo Structure

## Root Layout

```text
rover-vision-system/
│
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env
├── .gitignore
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── state.py
│   │
│   ├── camera/
│   │   ├── camera_manager.py
│   │   ├── stream.py
│   │   └── calibration.py
│   │
│   ├── tracking/
│   │   ├── detector.py
│   │   ├── tracker.py
│   │   ├── face_tracking.py
│   │   ├── object_tracking.py
│   │   └── pid_controller.py
│   │
│   ├── motion/
│   │   ├── pan_tilt_controller.py
│   │   ├── servo_driver.py
│   │   └── limits.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   ├── websocket.py
│   │   └── schemas.py
│   │
│   ├── web/
│   │   ├── static/
│   │   └── templates/
│   │
│   └── utils/
│       ├── logging.py
│       ├── fps.py
│       └── image_utils.py
│
├── tests/
│   ├── test_tracking.py
│   ├── test_servos.py
│   └── test_api.py
│
├── scripts/
│   ├── start.sh
│   ├── calibrate_servos.py
│   └── benchmark_camera.py
│
├── models/
│   ├── haarcascades/
│   └── yolov8/
│
└── docs/
    ├── hardware.md
    ├── gpio-map.md
    ├── architecture.md
    └── tuning.md
```

---

# Why This Structure Works

## camera/

Responsible ONLY for:

* capturing frames
* camera settings
* streaming
* calibration

No tracking logic here.

This separation matters later when:

* you switch cameras
* use Picamera2
* add CSI camera
* add USB camera support

---

## tracking/

This becomes your AI/computer vision layer.

Keep:

* detection
* tracking
* smoothing
* PID control

isolated from hardware.

That lets you:

* test on recorded video
* run on desktop
* benchmark models
* improve algorithms without GPIO attached

---

## motion/

Hardware abstraction.

This layer should expose simple commands:

```python
pan_tilt.move_to(pan=90, tilt=45)
pan_tilt.center()
pan_tilt.track(offset_x, offset_y)
```

The tracking system should NEVER directly manipulate GPIO.

This separation is extremely important.

---

## api/

Your integration layer.

This will eventually connect:

* rover repo
* browser UI
* websocket stream
* autonomous driving logic

Keep it clean and thin.

---

# Technology Recommendations

## Raspberry Pi Zero 2W Constraints

The Pi Zero 2W is limited.

Be careful with:

* large ML models
* high-resolution streaming
* heavy OpenCV pipelines

Recommended stack:

| Purpose               | Recommendation         |
| --------------------- | ---------------------- |
| Camera                | Picamera2              |
| CV library            | OpenCV                 |
| Face detection        | Haar Cascade initially |
| Better tracking later | MediaPipe or YOLOv8n   |
| Web server            | FastAPI                |
| Streaming             | MJPEG first            |
| Realtime UI           | WebSockets             |
| Servo control         | PCA9685 recommended    |

---

# Strong Recommendation: Use PCA9685

Do NOT directly PWM servos from the Pi.

Use:

* PCA9685 servo controller board

Benefits:

* stable PWM
* lower CPU usage
* cleaner motion
* avoids jitter
* supports future expansion

Especially important while simultaneously:

* streaming video
* running OpenCV
* serving webpages

---

# Suggested Development Phases

## Phase 1 — Camera Streaming

Goal:

* Get camera working
* Stream to webpage
* Stable FPS

Build:

```text
camera -> FastAPI -> MJPEG stream -> browser
```

Ignore tracking completely.

Success criteria:

* stable stream
* low latency
* acceptable CPU usage

---

## Phase 2 — Pan/Tilt Hardware

Goal:

* Manually control pan/tilt

Build:

* API endpoints
* keyboard control
* browser joystick/sliders

Success criteria:

* smooth movement
* no jitter
* safe motion limits

---

## Phase 3 — Detection

Goal:

* Detect faces/objects

Start SIMPLE:

### Best first option

OpenCV Haar Cascades.

Why:

* lightweight
* fast enough on Pi Zero 2W
* easy to debug

Do NOT start with YOLO.

Success criteria:

* reliable face box detection
* stable FPS

---

## Phase 4 — Tracking

Goal:

* Keep target centered

Add:

* PID controller
* smoothing
* deadzone
* confidence threshold

Pipeline:

```text
camera frame
 -> detect face
 -> compute center offset
 -> PID controller
 -> pan/tilt motion
```

Success criteria:

* smooth tracking
* no oscillation
* no servo hunting

---

## Phase 5 — Web Integration

Goal:

Merge stream into rover UI.

Recommended:

The rover webpage should NOT directly own the vision logic.

Instead:

```text
rover web ui
    |
    +---- rover api
    |
    +---- vision api
```

This keeps systems modular.

---

## Phase 6 — Rover Following

Goal:

Use tracking to drive rover.

Add:

```text
target_x_offset
target_size
```

To compute:

* steering
* distance
* movement

Example:

```python
if target_x < center:
    rover.turn_left()

if target_too_small:
    rover.forward()
```

At this phase your architecture pays off.

---

# Recommended Initial Interfaces

## Internal Tracking Output

Define a clean tracking object:

```python
{
    "target_detected": True,
    "x": 320,
    "y": 180,
    "offset_x": -22,
    "offset_y": 10,
    "confidence": 0.91,
    "timestamp": 123456789
}
```

This becomes the universal interface.

Everything downstream consumes this.

---

# Recommended APIs

## REST Endpoints

```text
GET  /stream
POST /pan
POST /tilt
POST /center
POST /tracking/start
POST /tracking/stop
GET  /tracking/status
```

---

## WebSocket Events

```json
{
  "type": "tracking_update",
  "target_detected": true,
  "offset_x": -15,
  "offset_y": 6
}
```

---

# Recommended Software Stack

## Python Dependencies

Start lightweight.

```text
fastapi
uvicorn
opencv-python
picamera2
numpy
adafruit-circuitpython-pca9685
```

Optional later:

```text
mediapipe
ultralytics
```

---

# Recommended Concurrency Model

You will eventually need:

* camera loop
* tracking loop
* web server
* servo updates
* websocket events

Do NOT put everything in one loop.

Recommended:

```text
Main Process
├── Camera Thread
├── Tracking Thread
├── Servo Control Thread
└── FastAPI Server
```

Shared state:

```python
app/state.py
```

---

# Important Engineering Advice

## 1. Keep Hardware Abstracted

Never do:

```python
GPIO.output(...)
```

inside tracking code.

Always:

```python
pan_tilt.move(...)
```

---

## 2. Start with MJPEG Streaming

Do NOT start with WebRTC.

MJPEG is dramatically easier.

Upgrade later if needed.

---

## 3. Optimize Resolution Early

Pi Zero 2W limits matter.

Suggested:

```text
320x240
```

or:

```text
640x480
```

initially.

---

## 4. Add Debug Overlays

Critical for debugging.

Overlay:

* FPS
* target box
* center crosshair
* PID values
* tracking confidence

---

## 5. Save Recorded Sessions

Huge debugging win.

Record:

```text
video + tracking metadata
```

Then replay offline.

---

# Suggested First Milestone

Your immediate target should be:

## MVP

```text
Pi camera streams video to webpage
AND
camera pan/tilt can be manually controlled
```

No AI yet.

That milestone validates:

* camera pipeline
* streaming
* servo hardware
* web integration
* concurrency

Only then add tracking.

---

# Future Integration Strategy

Eventually you can:

## Option A — Separate Services (Recommended)

```text
rover-control-service
vision-service
```

Communicate over:

* websockets
* REST
* MQTT

This is the cleanest architecture.

---

## Option B — Monorepo

```text
rover/
├── control/
├── vision/
├── shared/
└── web/
```

Good later.

Not ideal during experimentation.

---

# My Recommendation for Your Exact Situation

Right now:

1. Create:

```text
rover-vision-system
```

2. Build ONLY:

* camera streaming
* pan/tilt control
* lightweight face detection

3. Use:

* FastAPI
* Picamera2
* OpenCV
* PCA9685

4. Keep all rover movement logic OUT.

5. Define clean APIs now.

Then:

When stable, integrate the vision system into the rover ecosystem.

That sequence will save you a huge amount of complexity.

---

# Suggested Next Step

The next thing to design should be:

## The runtime architecture

Specifically:

* process/thread model
* frame pipeline
* shared state management
* streaming mechanism
* tracking loop timing

That is the foundation that determines how maintainable the system becomes.
