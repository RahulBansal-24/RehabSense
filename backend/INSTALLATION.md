# RehabSense Backend Installation Guide

## Prerequisites
- Python 3.13+ installed
- Git installed
- Webcam for pose detection

## Option 1: Using Virtual Environment (Recommended)

### Step 1: Clone and Navigate
```bash
git clone <repository-url>
cd rehabsense/backend
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the Backend
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Option 2: Using Conda

### Step 1: Clone and Navigate
```bash
git clone <repository-url>
cd rehabsense/backend
```

### Step 2: Create Conda Environment
```bash
conda create -n rehabsense python=3.13 -y
```

### Step 3: Activate Conda Environment
```bash
conda activate rehabsense
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the Backend
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Verification

### Check Backend Status
- Open http://localhost:8000 in your browser
- You should see: `{"message": "Welcome to RehabSense API", ...}`
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs

### Test WebSocket Connection
The WebSocket endpoint is available at: `ws://localhost:8000/api/ws/{session_id}`

## Troubleshooting

### Common Issues

1. **MediaPipe Installation Issues**
   ```bash
   # If MediaPipe fails, try installing with specific version
   pip install mediapipe==0.10.32
   ```

2. **OpenCV Issues**
   ```bash
   # If OpenCV causes issues, try the headless version
   pip uninstall opencv-python
   pip install opencv-python-headless==4.12.0.88
   ```

3. **Permission Issues (Windows)**
   ```powershell
   # If PowerShell blocks script execution
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Port Already in Use**
   ```bash
   # Kill processes using port 8000 (Windows)
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # Or use different port
   uvicorn main:app --reload --port 8001
   ```

### Performance Optimization

For better performance with real-time pose detection:

1. **Use GPU Acceleration** (if available)
   ```bash
   # Install CUDA-enabled packages if you have NVIDIA GPU
   pip install opencv-python-contrib-python==4.12.0.88
   ```

2. **Adjust MediaPipe Settings**
   - Edit `services/pose_detector.py` to adjust `model_complexity` and confidence thresholds

3. **System Requirements**
   - Minimum: 4GB RAM, dual-core CPU
   - Recommended: 8GB RAM, quad-core CPU, dedicated GPU

## Development Setup

### Running in Development Mode
```bash
# With auto-reload enabled
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# With debug logging
uvicorn main:app --reload --log-level debug
```

### Testing the Backend
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test API docs
# Open http://localhost:8000/docs in browser
```

## Frontend Integration

The backend is designed to work with the existing frontend. Ensure:

1. Frontend runs on http://localhost:3000
2. CORS is properly configured (already done in main.py)
3. WebSocket connections use the correct endpoint format

## Dependencies Explained

- **fastapi**: Web framework for API endpoints
- **uvicorn**: ASGI server to run FastAPI
- **websockets**: WebSocket support for real-time communication
- **opencv-python**: Computer vision and image processing
- **mediapipe**: Google's pose detection library
- **numpy**: Numerical computations
- **pydantic**: Data validation and serialization

## Next Steps

1. Start the backend using one of the methods above
2. Navigate to the frontend application
3. Begin a rehab exercise session
4. The backend will process webcam frames and provide real-time feedback
