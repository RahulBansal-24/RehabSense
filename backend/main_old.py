"""
RehabSense Backend - FastAPI Application Entry Point

This module initializes the FastAPI application, configures CORS middleware
for frontend integration, and includes all API routers.

The backend runs on http://localhost:8000 and serves the frontend at http://localhost:3000
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routers import session, websocket
import json
import base64
import numpy as np
import cv2
from services.pose_detector import get_pose_detector

# Initialize FastAPI application
app = FastAPI(
    title="RehabSense API",
    description="AI Physiotherapy Platform Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware to allow frontend requests
# Frontend runs on http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "ws://localhost:3000",
        "ws://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standalone WebSocket endpoint for frontend (must be before router inclusion)
@app.websocket("/ws/pose")
async def websocket_pose_endpoint(websocket: WebSocket):
    """
    Standalone WebSocket endpoint for frontend integration.
    
    Accepts exercise selection and provides real-time pose feedback.
    Matches frontend expected format exactly.
    """
    await websocket.accept()
    print("WebSocket connection accepted for /ws/pose")
    
    pose_detector = get_pose_detector()
    session_data = {
        'exercise': 'squat',
        'metrics': {
            'totalReps': 0,
            'correctReps': 0,
            'incorrectReps': 0,
            'postureAccuracy': 95.0,
            'misalignmentsCount': 0,
            'incorrectFormAlerts': 0,
            'averageJointDeviation': 2.5
        }
    }
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                print(f"Received message: {message}")
                
                # Handle exercise selection
                if 'exercise' in message:
                    session_data['exercise'] = message['exercise']
                    print(f"Exercise set to: {message['exercise']}")
                    # Acknowledge exercise selection
                    await websocket.send_json({
                        'type': 'exercise_set',
                        'exercise': message['exercise']
                    })
                    continue
                
                # Handle frame data
                if 'frame' in message:
                    frame_data = message['frame']
                    
                    # Decode frame
                    image = pose_detector.decode_frame(frame_data)
                    
                    if image is None:
                        continue
                    
                    # Detect pose
                    landmarks = pose_detector.detect_pose(image)
                    
                    # Generate mock data for now (replace with real processing)
                    is_correct_form = True
                    reps = session_data['metrics']['totalReps']
                    
                    # Simulate rep counting (replace with real logic)
                    if landmarks and landmarks.get('pose'):
                        import random
                        if random.random() > 0.95:  # 5% chance of rep increment
                            reps += 1
                            session_data['metrics']['totalReps'] = reps
                            session_data['metrics']['correctReps'] = int(reps * 0.85)
                            session_data['metrics']['incorrectReps'] = reps - session_data['metrics']['correctReps']
                    
                    # Prepare response in exact frontend format
                    response = {
                        'type': 'feedback',
                        'reps': session_data['metrics']['totalReps'],
                        'correct_reps': session_data['metrics']['correctReps'],
                        'incorrect_reps': session_data['metrics']['incorrectReps'],
                        'accuracy': session_data['metrics']['postureAccuracy'],
                        'misalignments': session_data['metrics']['misalignmentsCount'],
                        'alerts': session_data['metrics']['incorrectFormAlerts'],
                        'joint_deviation': session_data['metrics']['averageJointDeviation'],
                        'feedback': 'Perfect form! Keep maintaining this posture' if is_correct_form else 'Slight adjustment needed - watch your alignment',
                        'posture_correct': is_correct_form,
                        'frame': frame_data
                    }
                    
                    print(f"Sending response: {response['type']}")
                    # Send response back to client
                    await websocket.send_json(response)
                
            except json.JSONDecodeError:
                # Invalid JSON, skip
                continue
            except Exception as e:
                print(f"WebSocket processing error: {e}")
                continue
    
    except WebSocketDisconnect:
        print("WebSocket disconnected normally")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass

# Test endpoint with different path
@app.websocket("/ws/test")
async def websocket_test_endpoint(websocket: WebSocket):
    """Simple test WebSocket endpoint."""
    await websocket.accept()
    print("Test WebSocket connection accepted")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(f"Test received: {message}")
            
            await websocket.send_json({
                'type': 'test_response',
                'received': message
            })
    except WebSocketDisconnect:
        print("Test WebSocket disconnected")
    except Exception as e:
        print(f"Test WebSocket error: {e}")

# Include API routers
# Session routes will be prefixed with /api
app.include_router(session.router, prefix="/api", tags=["sessions"])


@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running.
    
    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "Welcome to RehabSense API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy", "service": "rehabsense-backend"}


if __name__ == "__main__":
    """
    Run the server using uvicorn when executed directly.
    
    Usage:
        python main.py
        or
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
