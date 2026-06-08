# sudo apt update && sudo apt upgrade -y
# mkdir ~/yolo_edge_ncnn
# cd ~/yolo_edge_ncnn
# python3 -m venv --system-site-packages venv
# source venv/bin/activate
# pip install ultralytics ncnn picamera2 "numpy<2.3"
# yolo detect predict model=yolo11n.pt
# yolo detect export model=yolo11n.pt format=ncnn
# nano yolo_rpi_log.py (paste code below)
# run it: python yolo_rpi_log.py

import cv2
from datetime import datetime
import time
from ultralytics import YOLO
from picamera2 import Picamera2

# --- Project Configurations ---
MODEL_PATH = "yolo11n_ncnn_model"
LOG_FILE = "detection_log.txt"
PERSON_CLASS_ID = 0
LOG_COOLDOWN_SEC = 5

# --- Helper Functions ---

def log_detection(timestamp):
    """Writes the detection to a log file."""
    log_entry = f"[{timestamp}] - Person Detected.\n"
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)
    print(f"Log recorded: {log_entry.strip()}")

# --- Main Process ---

print("Starting Person Detection (YOLO NCNN + Picamera2)...")

# 1. Load the NCNN model
print("Loading NCNN model...")
model = YOLO(MODEL_PATH)
print("Model loaded successfully.")

# 2. Start the camera (PICAMERA2 MODE)
try:
    picam2 = Picamera2()
    # Configure for "preview" (fast) and a format that OpenCV understands
    config = picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    print("PiCamera started successfully.")
except Exception as e:
    print(f"ERROR: Could not start Picamera2. {e}")
    print("Check if 'Legacy Camera' is DISABLED in raspi-config.")
    exit()

last_log_time = time.time()
print("Press 'q' on the video window to exit...")

try:
    while True:
        # 3. Capture the frame (PICAMERA2 MODE)
        # capture_array() returns a numpy array ready to use
        frame = picam2.capture_array()

        # (Optional but recommended) Convert from RGB (Picamera2) to BGR (OpenCV)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # 4. Inference with Ultralytics
        results = model(frame_bgr, verbose=False)  # Use the BGR frame

        person_detected_in_frame = False

        # 5. Process Detections
        for box in results[0].boxes:
            confidence = box.conf[0].item()
            class_id = int(box.cls[0].item())

            if class_id == PERSON_CLASS_ID and confidence > 0.5:
                person_detected_in_frame = True
                x1, y1, x2, y2 = box.xyxy[0].int().tolist()

                # Draw on the BGR frame
                cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame_bgr, f"Person: {confidence:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                break

        # 6. Conditional Logging
        if person_detected_in_frame and (time.time() - last_log_time > LOG_COOLDOWN_SEC):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_detection(timestamp)
            last_log_time = time.time()

        # Show the video (BGR frame)
        cv2.imshow('YOLO NCNN Edge Detector (Picam2) - Press Q', frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Cleanup
    picam2.stop()  # <--- Picamera2 stop command
    cv2.destroyAllWindows()
    print("Script finished. Detection log saved to:", LOG_FILE)