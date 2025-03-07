LiveCam AI – Real-Time Object & Motion Detection with Recording
LiveCam AI is a real-time AI-powered object detection and motion tracking system using Flask, OpenCV, and YOLOv5. It streams live video from a mobile or IP camera, detects motion, identifies objects, and allows recording of detected events.

Features
✅ Real-Time Video Streaming – Streams video from an IP or mobile camera.
✅ AI Object Detection – Uses YOLOv5 to identify objects in real-time.
✅ Motion Tracking – Detects motion and highlights moving objects.
✅ Automatic Recording – Starts recording when motion is detected.
✅ Recording Timer – Displays elapsed recording time.
✅ Web-Based Interface – Access the camera feed and control recording via a browser.

Tech Stack
Flask (Python) – Web framework
OpenCV – Image processing
YOLOv5 – Object detection model
Torch (PyTorch) – Deep learning backend
HTML/CSS/JS – Frontend for the web interface
Setup & Installation
Clone the repository
sh
Copy
Edit
git clone https://github.com/yourusername/livecam-ai.git
cd livecam-ai
Install dependencies
sh
Copy
Edit
pip install -r requirements.txt
Run the Flask app
sh
Copy
Edit
python app.py
Access in your browser
arduino
Copy
Edit
http://localhost:5000/
Usage
Start the app and access the web interface.
Click "Start Recording" to save the video with detected motion and objects.
Click "Stop Recording" to stop and save the video to the upload folder.
