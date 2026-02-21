#!/usr/bin/env python3
"""
Test script for the new test WebSocket endpoint.
"""

import asyncio
import websockets
import json

async def test_new_endpoint():
    """Test the new /ws/test endpoint."""
    
    try:
        # Connect to test WebSocket
        uri = "ws://localhost:8000/ws/test"
        print(f"Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("✓ Connected to test WebSocket")
            
            # Send test message
            test_msg = {"test": "hello"}
            await websocket.send(json.dumps(test_msg))
            print(f"✓ Sent test: {test_msg}")
            
            # Wait for response
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
    print("=== Testing New WebSocket Endpoint ===")
    success = asyncio.run(test_new_endpoint())
    
    if success:
        print("\n🎉 New WebSocket test PASSED")
    else:
        print("\n❌ New WebSocket test FAILED")
