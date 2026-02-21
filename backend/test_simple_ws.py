#!/usr/bin/env python3
"""
Simple WebSocket test to verify standalone endpoint works.
"""

import asyncio
import websockets
import json

async def test_simple_connection():
    """Test simple WebSocket connection without frames."""
    
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
            
            # Wait for any response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                print(f"✓ Received response: {json.dumps(data, indent=2)}")
                return True
            except asyncio.TimeoutError:
                print("⚠️ No response received within 5 seconds")
                return True
            except Exception as e:
                print(f"✗ Error receiving response: {e}")
                return False
            
    except Exception as e:
        print(f"✗ WebSocket test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Simple WebSocket Test ===")
    success = asyncio.run(test_simple_connection())
    
    if success:
        print("\n🎉 Simple WebSocket test PASSED")
    else:
        print("\n❌ Simple WebSocket test FAILED")
