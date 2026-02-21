"""
RehabSense Backend - FastAPI Application Entry Point

This module initializes the FastAPI application, configures CORS middleware
for frontend integration, and includes all API routers.

The backend runs on http://localhost:8000 and serves the frontend at http://localhost:3000
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import base64
import time
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

# Standalone WebSocket endpoint for frontend
@app.websocket("/ws/pose")
async def websocket_pose_endpoint(websocket: WebSocket):
    """
    Standalone WebSocket endpoint for frontend integration.
    
    Accepts exercise selection and provides real-time pose feedback.
    Matches frontend expected format exactly.
    """
    print("DEBUG: WebSocket endpoint called")
    await websocket.accept()
    print("✓ WebSocket connection accepted for /ws/pose")
    
    # Initialize pose detector and session state
    pose_detector = get_pose_detector()
    session_data = {
        'exercise': 'squat',
        'total_reps': 0,
        'correct_reps': 0,
        'incorrect_reps': 0,
        'accuracy': 0,
        'misalignments': 0,
        'alerts': 0,
        'joint_deviation': 0,
        'feedback': 'Analyzing...',
        'posture_correct': True
    }
    
    try:
        while True:
            # Part 8: Add server FPS log
            start_time = time.time()
            
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                # Handle exercise selection
                if 'exercise' in message:
                    session_data['exercise'] = message['exercise']
                    print(f"Exercise set to: {message['exercise']}")
                    await websocket.send_json({
                        'type': 'exercise_set',
                        'exercise': message['exercise']
                    })
                    continue
                
                # Handle frame data
                if 'frame' in message:
                    frame_data = message['frame']
                    print(f"Step 3: Backend receiving frame of length: {len(frame_data)}")
                    
                    # Decode frame
                    image = pose_detector.decode_frame(frame_data)
                    
                    if image is None:
                        print("❌ Frame decode failed")
                        continue
                    
                    print(f"✅ Frame decoded successfully, shape: {image.shape}")
                    
                    # Part 2: Verify MediaPipe pose execution
                    if pose_detector.use_mediapipe:
                        # Convert BGR to RGB for MediaPipe
                        rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        results = pose_detector.pose.process(rgb_frame)
                        
                        # Part 2: Add debug for landmarks
                        if not results.pose_landmarks:
                            print("❌ NO LANDMARKS DETECTED")
                        else:
                            print(f"✅ Landmarks detected: {len(results.pose_landmarks.landmark)}")
                    else:
                        # Fallback mode - no landmarks
                        results = None
                        print("⚠️ Using fallback mode - no landmarks")
                    
                    # Part 3: Ensure landmark drawing
                    if results and results.pose_landmarks:
                        # Determine color based on posture correctness
                        color = (0, 255, 0) if session_data['posture_correct'] else (0, 0, 255)
                        
                        # Draw landmarks on frame
                        pose_detector.mp_drawing.draw_landmarks(
                            image,
                            results.pose_landmarks,
                            pose_detector.mp_pose.POSE_CONNECTIONS,
                            landmark_drawing_spec=pose_detector.mp_drawing.DrawingSpec(color=color, thickness=2),
                            connection_drawing_spec=pose_detector.mp_drawing.DrawingSpec(color=color, thickness=2)
                        )
                        print("✅ Landmarks drawn on frame")
                    else:
                        print("❌ No landmarks to draw")
                    
                    # Part 7: Optimize encoding speed
                    h, w = image.shape[:2]
                    if w > 640:
                        new_w = 640
                        new_h = int(h * 640 / w)
                        image = cv2.resize(image, (new_w, new_h))
                        print(f"🔧 Frame resized to: {image.shape}")
                    
                    # Encode frame with lower quality
                    success, encoded_img = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 70])
                    if success:
                        frame_b64 = base64.b64encode(encoded_img.tobytes()).decode('utf-8')
                        frame_url = f"data:image/jpeg;base64,{frame_b64}"
                        print(f"✅ Frame encoded successfully, URL length: {len(frame_url)}")
                    else:
                        frame_url = None
                        print("❌ Frame encoding failed")
                    
                    # Part 4: Fix NaN stats
                    if session_data['total_reps'] > 0:
                        accuracy = (session_data['correct_reps'] / session_data['total_reps']) * 100
                    else:
                        accuracy = 0
                    
                    print(f"📊 Stats before return: reps={session_data['total_reps']}, accuracy={accuracy}")
                    
                    # Simulate rep counting (replace with real logic)
                    if results and results.pose_landmarks:
                        import random
                        if random.random() > 0.95:  # 5% chance of rep increment
                            session_data['total_reps'] += 1
                            if random.random() > 0.2:  # 80% chance of correct rep
                                session_data['correct_reps'] += 1
                                session_data['posture_correct'] = True
                                session_data['feedback'] = 'Good form! Keep it up.'
                            else:
                                session_data['incorrect_reps'] += 1
                                session_data['posture_correct'] = False
                                session_data['feedback'] = 'Adjust your form slightly.'
                    
                    # Prepare response with proper data types
                    response = {
                        "type": "feedback",
                        "frame": frame_url,
                        "reps": int(session_data['total_reps']),
                        "correct_reps": int(session_data['correct_reps']),
                        "incorrect_reps": int(session_data['incorrect_reps']),
                        "accuracy": float(accuracy),
                        "feedback": str(session_data['feedback'])
                    }
                    
                    print(f"📤 Sending response: reps={response['reps']}, accuracy={response['accuracy']}")
                    
                    # Send response back to client
                    await websocket.send_json(response)
                    
                    # Part 8: Log processing time
                    processing_time = time.time() - start_time
                    print(f"Processing time: {processing_time:.3f}s")
                    if processing_time > 0.2:
                        print("⚠️ Backend bottleneck detected!")
                
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

# Include API routers (session router removed to avoid conflicts)
# app.include_router(session.router, prefix="/api", tags=["sessions"])


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
