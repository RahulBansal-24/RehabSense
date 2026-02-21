#!/usr/bin/env python3
"""
Minimal WebSocket test to isolate the issue.
"""

import asyncio
import websockets
import json

async def test_minimal():
    """Test minimal WebSocket connection."""
    
    try:
        # Connect to WebSocket
        uri = "ws://localhost:8000/ws/pose"
        print(f"Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("✓ Connected to WebSocket")
            
            # Send simple message
            simple_msg = {"hello": "world"}
            await websocket.send(json.dumps(simple_msg))
            print(f"✓ Sent: {simple_msg}")
            
            # Wait for any response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                print(f"✓ Raw response: {response}")
                return True
            except asyncio.TimeoutError:
                print("⚠️ Timeout waiting for response")
                return True
            except Exception as e:
                print(f"✗ Error receiving response: {e}")
                print(f"✗ Error type: {type(e)}")
                return False
            
    except Exception as e:
        print(f"✗ WebSocket connection failed: {e}")
        print(f"✗ Error type: {type(e)}")
        return False

if __name__ == "__main__":
    print("=== Minimal WebSocket Test ===")
    success = asyncio.run(test_minimal())
    
    if success:
        print("\n🎉 Minimal WebSocket test PASSED")
    else:
        print("\n❌ Minimal WebSocket test FAILED")
