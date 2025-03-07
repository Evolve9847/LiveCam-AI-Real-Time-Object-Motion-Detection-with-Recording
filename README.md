# **LiveCam AI – Real-Time Object Detection & Motion Tracking**

LiveCam AI is a real-time video streaming and AI-powered object detection system using **Flask, OpenCV, and YOLOv5**. It detects motion, identifies objects, and records videos with detected events. Designed for **surveillance and smart monitoring**, it features a web-based interface for live streaming, motion tracking, and recording control. 🚀

## **Features**
✅ **Real-Time Video Streaming** – Streams video from an IP or mobile camera.  
✅ **AI Object Detection** – Uses YOLOv5 to detect objects in real-time.  
✅ **Motion Tracking** – Highlights moving objects with bounding boxes.  
✅ **Automatic Recording** – Saves videos when motion is detected.  
✅ **Recording Timer** – Displays elapsed recording time.  
✅ **Web-Based Interface** – Control and monitor the stream via a browser.  

## **Tech Stack**
- **Flask** (Python) – Web framework
- **OpenCV** – Image processing
- **YOLOv5** – Object detection model
- **Torch (PyTorch)** – Deep learning backend
- **HTML/CSS/JS** – Frontend for the web interface

## **Installation & Setup**
### **1. Clone the Repository**
```sh
git clone https://github.com/yourusername/livecam-ai.git
cd livecam-ai
```

### **2. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3. Run the Flask App**
```sh
python app.py
```

### **4. Access in Your Browser**
```
http://localhost:5000/
```

## **Usage**
- Open the **web interface** in a browser.
- Click **"Start Recording"** to save detected motion and objects.
- Click **"Stop Recording"** to save the recorded video.
- Recorded videos are stored in the **upload** folder.

## **Contributing**
Contributions are welcome! Feel free to submit a pull request or report issues.

## **License**
This project is licensed under the **MIT License**.

---



