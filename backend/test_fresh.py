#!/usr/bin/env python3
"""
Fresh test with no imports to isolate server issue.
"""

import asyncio
import websockets
import json

async def fresh_test():
    """Fresh test without any local imports."""
    
    try:
        # Connect to WebSocket
        uri = "ws://localhost:8000/ws/pose"
        print(f"Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("✓ Connected to WebSocket")
            
            # Send simple message
            simple_msg = {"type": "ping"}
            await websocket.send(json.dumps(simple_msg))
            print(f"✓ Sent: {simple_msg}")
            
            # Wait for any response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                print(f"✓ Received: {response}")
                return True
            except asyncio.TimeoutError:
                print("⚠️ Timeout - no response received")
                return True
            except Exception as e:
                print(f"✗ Error: {e}")
                print(f"✗ Error type: {type(e)}")
                return False
            
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print(f"✗ Error type: {type(e)}")
        return False

if __name__ == "__main__":
    print("=== Fresh WebSocket Test ===")
    success = asyncio.run(fresh_test())
    
    if success:
        print("\n🎉 Fresh test PASSED")
    else:
        print("\n❌ Fresh test FAILED")
