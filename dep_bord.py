import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Lag-Free Air Drawing & Recorder", layout="wide")

st.title("🚀 Smooth Air Drawing with Built-in Recorder")
st.text("Camera toggle karein, draw karein aur apni recording ko direct download karein!")

# HTML + CSS + JS (MediaPipe + Canvas Recorder combined)
html_code = """
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>
  <style>
    body { margin: 0; padding: 0; overflow: hidden; background: #121212; font-family: sans-serif; }
    #container { position: relative; width: 100vw; height: 75vh; display: flex; justify-content: center; align-items: center; background: #000; }
    video { transform: scaleX(-1); position: absolute; width: 100%; height: 100%; object-fit: cover; opacity: 0.4; display: block; }
    canvas { position: absolute; width: 100%; height: 100%; object-fit: cover; z-index: 2; }
    #ui { position: fixed; top: 0; left: 0; width: 100%; height: 65px; background: rgba(0,0,0,0.9); display: flex; overflow-x: auto; white-space: nowrap; z-index: 10; padding-left: 5px; }
    .btn { padding: 8px 15px; margin: 12px 4px; background: #333; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; font-size: 13px; }
    .btn.active { background: #00ffcc; color: black; }
    .rec-btn { background: #ff3333; color: white; }
    .stop-btn { background: #ffcc00; color: black; display: none; }
    .cam-btn { background: #007bff; color: white; }
  </style>
</head>
<body>

  <div id="ui">
    <button id="camBtn" class="btn cam-btn" onclick="toggleCamera()">🎥 STOP CAM</button>
    <button id="recBtn" class="btn rec-btn" onclick="startRecording()">🔴 START REC</button>
    <button id="stopRecBtn" class="btn stop-btn" onclick="stopRecording()">💾 STOP & DOWNLOAD</button>
    <button id="btnDraw" class="btn active" onclick="setTool('Draw')">DRAW</button>
    <button id="btnRect" class="btn" onclick="setTool('Rect')">RECT</button>
    <button id="btnCircle" class="btn" onclick="setTool('Circle')">CIRCLE</button>
    <button id="btnErase" class="btn" onclick="setTool('Eraser')">ERASE</button>
    <button class="btn" onclick="clearCanvas()">CLEAR</button>
    <button class="btn" style="background:#ff00ff;" onclick="setColor('#ff00ff')">PURP</button>
    <button class="btn" style="background:#0000ff;" onclick="setColor('#0000ff')">BLUE</button>
    <button class="btn" style="background:#00ff00; color:black;" onclick="setColor('#00ff00')">GRN</button>
  </div>

  <div id="container">
    <video id="webcam" autoplay playsinline></video>
    <canvas id="paintCanvas"></canvas>
  </div>

  <script>
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('paintCanvas');
    const ctx = canvas.getContext('2d');
    
    let currentTool = 'Draw';
    let drawColor = '#ff00ff';
    let brushThickness = 8;
    let shapes = [];
    let tempShape = null;
    let isDrawing = false;
    let cameraActive = true;

    // Recording Variables
    let mediaRecorder;
    let recordedChunks = [];

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight * 0.75;
    }
    window.addEventListener('resize', resize);
    resize();

    function setTool(tool) {
      currentTool = tool;
      document.querySelectorAll('#ui .btn').forEach(b => {
        if(!b.classList.contains('rec-btn') && !b.classList.contains('stop-btn') && !b.classList.contains('cam-btn')) {
            b.classList.remove('active');
        }
      });
      event.target.classList.add('active');
    }
    function setColor(color) { drawColor = color; }
    function clearCanvas() { shapes = []; redraw(); }

    function toggleCamera() {
      const camBtn = document.getElementById('camBtn');
      if (cameraActive) {
        camera.stop();
        video.style.display = 'none';
        camBtn.innerText = '🎥 START CAM';
        camBtn.style.background = '#28a745';
      } else {
        video.style.display = 'block';
        camera.start();
        camBtn.innerText = '🎥 STOP CAM';
        camBtn.style.background = '#007bff';
      }
      cameraActive = !cameraActive;
    }

    function redraw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      shapes.forEach(s => drawSingleShape(s));
      if (tempShape) drawSingleShape(tempShape);
    }

    function drawSingleShape(s) {
      ctx.strokeStyle = s.color;
      ctx.lineWidth = s.thickness;
      ctx.fillStyle = s.color;

      if (s.type === 'stroke' && s.pts.length > 1) {
        ctx.beginPath();
        ctx.moveTo(s.pts[0].x, s.pts[0].y);
        for(let i=1; i<s.pts.length; i++) ctx.lineTo(s.pts[i].x, s.pts[i].y);
        ctx.stroke();
      } else if (s.type === 'rect') {
        ctx.strokeRect(s.p1.x, s.p1.y, s.p2.x - s.p1.x, s.p2.y - s.p1.y);
      } else if (s.type === 'circle') {
        let r = Math.hypot(s.p2.x - s.p1.x, s.p2.y - s.p1.y);
        ctx.beginPath();
        ctx.arc(s.p1.x, s.p1.y, r, 0, 2*Math.PI);
        ctx.stroke();
      }
    }

    function onResults(results) {
      redraw();
      if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        const landmarks = results.multiHandLandmarks[0];
        const x = (1 - landmarks[8].x) * canvas.width;
        const y = landmarks[8].y * canvas.height;
        const indexUp = landmarks[8].y < landmarks[6].y;
        const middleUp = landmarks[12].y < landmarks[10].y;

        ctx.fillStyle = drawColor;
        ctx.beginPath();
        ctx.arc(x, y, 10, 0, 2*Math.PI);
        ctx.fill();

        if (indexUp && !middleUp) { 
          if (currentTool === 'Draw') {
            if (!isDrawing) {
              tempShape = { type: 'stroke', pts: [{x, y}], color: drawColor, thickness: brushThickness };
              isDrawing = true;
            } else {
              tempShape.pts.push({x, y});
            }
          } else if (['Rect', 'Circle'].includes(currentTool)) {
            if (!isDrawing) {
              tempShape = { type: currentTool.toLowerCase(), p1: {x, y}, p2: {x, y}, color: drawColor, thickness: brushThickness };
              isDrawing = true;
            } else {
              tempShape.p2 = {x, y};
            }
          } else if (currentTool === 'Eraser') {
             shapes = shapes.filter(s => {
               if(s.type==='stroke') return Math.hypot(s.pts[0].x - x, s.pts[0].y - y) > 50;
               return true;
             });
          }
        } else {
          if (isDrawing && tempShape) {
            shapes.push(tempShape);
            tempShape = null;
            isDrawing = false;
          }
        }
      }
    }

    // --- High Performance Recorder Logic ---
    function startRecording() {
      recordedChunks = [];
      // Captured from the Drawing Canvas directly to ensure extreme smoothness
      const stream = canvas.captureStream(30); 
      
      mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm;codecs=vp9' });
      mediaRecorder.ondataavailable = (e) => { if (e.data.size > 0) recordedChunks.push(e.data); };
      
      mediaRecorder.onstop = () => {
        const blob = new Blob(recordedChunks, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'air_drawing_recording.webm';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      };

      mediaRecorder.start();
      document.getElementById('recBtn').style.display = 'none';
      document.getElementById('stopRecBtn').style.display = 'inline-block';
    }

    function stopRecording() {
      mediaRecorder.stop();
      document.getElementById('recBtn').style.display = 'inline-block';
      document.getElementById('stopRecBtn').style.display = 'none';
    }

    const hands = new Hands({locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`});
    hands.setOptions({ maxNumHands: 1, modelComplexity: 1, minDetectionConfidence: 0.75, minTrackingConfidence: 0.75 });
    hands.onResults(onResults);

    const camera = new Camera(video, {
      onFrame: async () => { if(cameraActive) await hands.send({image: video}); },
      width: 640, height: 480
    });
    camera.start();
  </script>
</body>
</html>
"""

# Render Component
components.html(html_code, height=750, scrolling=False)