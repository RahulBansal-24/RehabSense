#!/usr/bin/env python3
"""
Test script for RehabSense Backend WebSocket functionality.
This script tests the pose detection pipeline with a sample image.
"""

import asyncio
import websockets
import json
import base64
import numpy as np
import cv2
from pathlib import Path

async def test_websocket_connection():
    """Test WebSocket connection and pose detection."""
    
    # Create a simple test image (black rectangle)
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some simple features to make it more realistic
    cv2.rectangle(test_image, (100, 100), (540, 380), (255, 255, 255), -1)
    cv2.circle(test_image, (320, 240), 50, (0, 0, 255), -1)
    
    # Convert to base64
    _, buffer = cv2.imencode('.jpg', test_image)
    frame_data = base64.b64encode(buffer).decode('utf-8')
    
    # Start a session first
    import requests
    session_response = requests.post(
        'http://localhost:8000/api/sessions/start',
        json={"exercise": "squat", "userId": "test-user"}
    )
    
    if session_response.status_code != 200:
        print(f"Failed to start session: {session_response.status_code}")
        return
    
    session_data = session_response.json()
    session_id = session_data['sessionId']
    print(f"Started session: {session_id}")
    
    # Connect to WebSocket
    uri = f"ws://localhost:8000/api/ws/{session_id}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket: {uri}")
            
            # Send test frame
            message = {
                "type": "frame",
                "data": {
                    "frame": f"data:image/jpeg;base64,{frame_data}",
                    "timestamp": 1234567890
                }
            }
            
            await websocket.send(json.dumps(message))
            print("Sent test frame")
            
            # Wait for response
            response = await websocket.recv()
            print(f"Received response: {response}")
            
            # Send ping
            await websocket.send(json.dumps({"type": "ping", "data": {}}))
            ping_response = await websocket.recv()
            print(f"Ping response: {ping_response}")
            
    except Exception as e:
        print(f"WebSocket test failed: {e}")
    
    finally:
        # End session
        end_response = requests.post(
            f'http://localhost:8000/api/sessions/{session_id}/end',
            json={"sessionId": session_id}
        )
        print(f"Session ended: {end_response.status_code}")

def test_pose_detector_directly():
    """Test pose detector service directly."""
    try:
        from services.pose_detector import get_pose_detector
        
        detector = get_pose_detector()
        print("✓ Pose detector initialized successfully")
        
        # Test with a simple image
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        landmarks = detector.detect_pose(test_image)
        
        if landmarks:
            print("✓ Pose detection works (may return None for test image)")
        else:
            print("✓ Pose detection runs without errors")
            
        # Test key points extraction
        if landmarks and landmarks.get('pose'):
            key_points = detector.get_key_points(landmarks)
            print(f"✓ Key points extraction works: {len(key_points) if key_points else 0} points")
        
        return True
        
    except Exception as e:
        print(f"✗ Pose detector test failed: {e}")
        return False

def test_all_services():
    """Test all backend services."""
    print("\n=== Testing RehabSense Backend Services ===\n")
    
    tests = [
        ("Pose Detector", test_pose_detector_directly),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"{'✓' if result else '✗'} {test_name}: {'PASS' if result else 'FAIL'}\n")
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}\n")
            results.append((test_name, False))
    
    # Summary
    print("=== Test Summary ===")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready.")
    else:
        print("⚠️  Some tests failed. Check the logs above.")
    
    return passed == total

if __name__ == "__main__":
    # Run service tests
    success = test_all_services()
    
    # Optional: Run WebSocket test if services pass
    if success:
        print("\n=== Testing WebSocket Connection ===")
        try:
            asyncio.run(test_websocket_connection())
        except Exception as e:
            print(f"WebSocket test failed: {e}")
            print("Make sure the backend is running with: uvicorn main:app --reload")
