# 🏥 RehabSense  

AI-Powered Smart Physiotherapy & Rehabilitation Platform  

---

## 📌 Project Overview  

**RehabSense** is a real-time AI-driven physiotherapy platform designed to assist users in performing rehabilitation exercises with visual guidance and performance tracking.

The platform provides:

- 🎥 Live camera-based session monitoring  
- 🧠 AI-assisted posture analysis (backend pipeline connected)  
- 📊 Real-time session stats & performance tracking  
- 🏋️ 3 guided exercise sessions  
- 📈 Dashboard & summary analytics  

The frontend is fully functional and supports complete exercise sessions, live tracking UI, dashboard insights, and session summaries.  

The backend pipeline is connected via OpenCV and WebSocket communication. However, **pose landmark dot annotations and final stat calculations based on model results are pending integration and refinement.**

---

## 🚀 Features  

### 🎯 Exercise Sessions
- 3 physiotherapy exercise modes
- Real-time session tracking
- Live stat placeholders (reps, accuracy, feedback)
- Session summary page after completion

### 📊 Dashboard
- Overview of sessions
- Exercise performance tracking
- Clean UI with session analytics

### 🎥 Live Camera Integration
- OpenCV-based backend camera processing
- WebSocket streaming between frontend and backend
- Frame throttling & pipeline stabilization implemented

### ⚙️ Backend Processing
- Python 3.13 compatible
- OpenCV frame capture
- WebSocket frame communication
- Modular service-based structure
- Testing utilities for WebSocket stability

---

## 🏗️ Project Structure  

```
RehabSense
│
├── .vscode
│
├── backend
│ ├── pycache
│ ├── models
│ ├── routers
│ ├── services
│ ├── utils
│ ├── INSTALLATION.md
│ ├── INTEGRATION_COMPLETE.md
│ ├── PYTHON313_COMPATIBILITY.md
│ ├── README.md
│ ├── main.py
│ ├── main_old.py
│ ├── requirements.txt
│ ├── test_fresh.py
│ ├── test_minimal_ws.py
│ ├── test_new_ws.py
│ ├── test_simple_ws.py
│ └── test_websocket.py
│
├── frontend
│ ├── app
│ ├── components
│ ├── hooks
│ ├── lib
│ ├── styles
│ ├── .env.example
│ ├── .gitignore
│ ├── COMPLETELY_FIXED.md
│ ├── FINAL_FIXES.md
│ ├── FRONTEND_FIXED.md
│ ├── components.json
│ ├── next-env.d.ts
│ ├── next.config.mjs
│ ├── package-lock.json
│ ├── package.json
│ ├── pnpm-lock.yaml
│ ├── postcss.config.mjs
│ └── tsconfig.json
│
├── PIPELINE_STABILIZED.md
├── README.md
└── VISUAL_ANALYSIS_DEBUGGED.md  
```

---

## 🧠 Tech Stack  

### Frontend
- Next.js (App Router)
- TypeScript
- React Hooks
- Tailwind CSS
- WebSocket integration
- Canvas rendering for frame display

### Backend
- Python 3.13
- FastAPI (WebSocket routing)
- OpenCV (camera input & frame processing)
- Modular service architecture
- WebSocket testing utilities

---

## 🔄 Current Backend Status  

✅ WebSocket pipeline stabilized  
✅ Camera capture via OpenCV  
✅ Frame transmission to frontend  
✅ Python 3.13 compatibility ensured  
✅ Modular backend structure  

⏳ Pending Integration:
- Pose landmark dot annotations over processed frames  
- Final stat calculations (reps, accuracy, correctness logic)  
- Model-driven real-time feedback generation  
- Fully connected metric update system  

---

## 📈 How Sessions Work  

1. User selects an exercise.
2. Frontend initializes session screen.
3. Camera stream starts.
4. Frames are transmitted to backend.
5. Backend processes frames (currently basic pipeline).
6. Processed frames returned to frontend.
7. Stats & feedback display dynamically.
8. After completion → summary page generated.

---

## 🛠 Installation & Setup  

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Frontend runs on:
```
http://localhost:3000
```

### Backend typically runs on:
```
http://localhost:8000
```

---

## 🔮 Future Improvements

- 🧠 Full MediaPipe / Pose model integration  
- 🟢🔴 Real-time green/red landmark annotations  
- 🔢 Accurate rep counting algorithm  
- 📊 Exercise form validation scoring  
- 🗄️ Multi-user progress storage (database integration)  
- 🔐 User authentication & profiles  
- ☁️ Cloud deployment  
- 📱 Mobile optimization  
- 📈 Performance analytics dashboard  
- 🤖 AI-based recovery recommendations  

---

## 🧪 Debug Documentation

- `PIPELINE_STABILIZED.md` → WebSocket & frame performance fixes  
- `VISUAL_ANALYSIS_DEBUGGED.md` → Analysis & debugging logs  

---

## 👨‍💻 Author

**Rahul Bansal**  
Programming Enthusiast | Learning AI & Real-Time Systems 

---

## 📄 License

This project is currently for educational and development purposes.  
A formal license can be added based on future deployment and distribution plans.

---

## ⭐ Final Note

RehabSense demonstrates a full-stack AI physiotherapy architecture combining:

- 🎥 Real-time streaming  
- 🧠 Computer vision processing  
- 🔌 WebSocket communication  
- 🖥️ Interactive frontend session management  

The system foundation is stable, and the final step remaining is complete pose-analysis logic integration for intelligent rehabilitation scoring.