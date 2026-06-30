# 🚀 High-Performance Computer Vision Air Drawing Tool with Built-in Media Recorder

An advanced, zero-lag, web-based **Air Drawing and Gesture Recognition Application** built using **Streamlit** and **MediaPipe (JavaScript-side Edge Computing)**. This architecture offloads heavy AI inference directly to the client's browser, enabling real-time 60 FPS hand tracking, custom geometric shape drawing, object manipulation (drag/erase), and native video recording even on low-end mobile devices.

---

## 🌟 Key Features

* **⚡ Zero-Lag Client-Side Processing**: Shifted MediaPipe hand-tracking from Python server-side to Web Browser JS, solving stream freezing and high CPU bottleneck over cloud deployment.
* **📲 Fully Mobile Responsive**: Engineered with dynamic CSS breakpoints to automatically adapt to desktop webcams and smartphone viewports (iOS/Android).
* **🔴 Native 30 FPS Media Recorder**: Capture high-definition canvas sessions instantly utilizing the WebRTC Canvas Capture Stream API.
* **💾 One-Click Local Downloads**: High-speed local compression (`video/webm;codecs=vp9`) that downloads files directly onto device storage without utilizing server bandwidth.
* **🛠️ Multi-Functional AI Tool Panel**:
    * `DRAW`: Freehand air writing with real-time positional smoothing.
    * `RECT` & `CIRCLE`: Dynamic continuous gesture shape sizing.
    * `ERASER`: Mathematical spatial distance bounding-box clearing.
    * `CLEAR` & `PALETTE`: Quick canvas resets along with digital color indexing (PURPLE, BLUE, GREEN).
* **🎥 Stream Management**: Native camera injection wrapper allowing users to toggle webcam access seamlessly on the fly.

---

## 🛠️ Tech Stack & Architecture

* **Frontend UI Wrapper**: Streamlit (Python)
* **Core Computer Vision Engine**: MediaPipe Hands API (Web Ecosystem)
* **Rendering Pipeline**: HTML5 Canvas API & WebRTC Streams
* **Encoding Module**: JavaScript MediaRecorder API (VP9/WebM)

---

## 📂 Project Structure

```text
├── app.py             # Optimized Main Production Application (Streamlit + Embedded HTML/JS)
└── README.md          # Comprehensive Documentation (This File)


🚀 Local Installation & Setup
git clone [https://github.com/YOUR_USERNAME/air-drawing-app.git](https://github.com/YOUR_USERNAME/air-drawing-app.git)
cd air-drawing-app


