#!/usr/bin/env python3
"""
Test script for RehabSense Backend WebSocket functionality.
"""

import asyncio
import websockets
import json
import base64
import numpy as np
import cv2

async def test_websocket_connection():
    """Test WebSocket connection to /ws/pose endpoint."""
    
    try:
        # Connect to WebSocket
        uri = "ws://localhost:8000/ws/pose"
        print(f"Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("✓ Connected to WebSocket")
            
            # Send exercise selection
            exercise_msg = {"exercise": "squat"}
            await websocket.send(json.dumps(exercise_msg))
            print(f"✓ Sent exercise: {exercise_msg}")
            
            # Create a simple test frame
            test_image = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.rectangle(test_image, (100, 100), (540, 380), (255, 255, 255), -1)
            
            # Convert to base64
            _, buffer = cv2.imencode('.jpg', test_image)
            frame_data = base64.b64encode(buffer).decode('utf-8')
            
            # Send test frame
            frame_msg = {"frame": frame_data}
            await websocket.send(json.dumps(frame_msg))
            print("✓ Sent test frame")
            
            # Wait for response
            response = await websocket.recv()
            data = json.loads(response)
            print(f"✓ Received response: {json.dumps(data, indent=2)}")
            
            # Verify expected fields
            expected_fields = ['type', 'reps', 'correct_reps', 'incorrect_reps', 
                            'accuracy', 'misalignments', 'alerts', 'joint_deviation', 
                            'feedback', 'posture_correct', 'frame']
            
            missing_fields = [field for field in expected_fields if field not in data]
            if missing_fields:
                print(f"⚠️ Missing fields: {missing_fields}")
            else:
                print("✓ All expected fields present")
            
            return True
            
    except Exception as e:
        print(f"✗ WebSocket test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing RehabSense WebSocket ===")
    success = asyncio.run(test_websocket_connection())
    
    if success:
        print("\n🎉 WebSocket integration test PASSED")
    else:
        print("\n❌ WebSocket integration test FAILED")
