from flask import Flask, render_template, Response, request
import cv2
import torch
import numpy as np
import os
import time

app = Flask(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Replace with your phone camera stream URL
camera_url = "http://192.168.0.102:8080/video"

# Create upload folder if not exists
if not os.path.exists('upload'):
    os.makedirs('upload')

# Video recording variables
recording = False
video_writer = None
frame_width = 1280
frame_height = 720
fps = 20
start_time = None  # Store recording start time

def generate_frames():
    global recording, video_writer, start_time
    cap = cv2.VideoCapture(camera_url)

    # Read initial frames for motion detection
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Resize frame to match resolution
        frame = cv2.resize(frame, (frame_width, frame_height))
        frame1 = cv2.resize(frame1, (frame.shape[1], frame.shape[0]))
        frame2 = cv2.resize(frame2, (frame.shape[1], frame.shape[0]))

        # Convert to grayscale for motion detection
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Compute absolute difference between frames
        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Find contours for motion detection
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Ignore small movements
                motion_detected = True
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue box for motion

        # Perform YOLO object detection only if motion is detected
        if motion_detected:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(rgb_frame)

            for *box, conf, cls in results.xyxy[0]:  
                x1, y1, x2, y2 = map(int, box)  
                label = f"{model.names[int(cls)]} {conf:.2f}"

                # Draw bounding box (Green)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

                # Draw label (Red, Bigger Font)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                            1.5, (0, 0, 255), 3, cv2.LINE_AA)

        # Show Recording Timer if Recording
        if recording:
            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)

            # Timer text
            timer_text = f"Recording {minutes}:{seconds:02d}"

            # Draw a semi-transparent background rectangle (for better visibility)
            overlay = frame.copy()
            cv2.rectangle(overlay, (15, 15), (270, 75), (0, 0, 0), -1)  # Black rectangle
            frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)  # Transparency effect

            # Draw red circle (recording icon)
            cv2.circle(frame, (40, 45), 10, (0, 0, 255), -1)  # Red filled circle

            # Draw recording timer text (White, Bold)
            cv2.putText(frame, timer_text, (60, 55), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (255, 255, 255), 3, cv2.LINE_AA)

        # Update previous frames
        frame1 = frame2
        ret, frame2 = cap.read()
        if not ret:
            break

        # Save frame to video if recording
        if recording and video_writer is not None:
            video_writer.write(frame)

        # Encode frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_record', methods=['POST'])
def start_record():
    global recording, video_writer, start_time

    if not recording:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        video_filename = f"upload/video_{timestamp}.mp4"
        video_writer = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
        start_time = time.time()  # Start recording timer
        recording = True

    return "Recording started"

@app.route('/stop_record', methods=['POST'])
def stop_record():
    global recording, video_writer, start_time

    if recording:
        recording = False
        start_time = None  # Reset timer
        if video_writer is not None:
            video_writer.release()
            video_writer = None

    return "Recording stopped"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
