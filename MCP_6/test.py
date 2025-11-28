import asyncio
import websockets
import requests
import time
import json

async def test_websocket():
    """Test WebSocket connection and message handling."""
    try:
        async with websockets.connect("ws://127.0.0.1:5000") as ws:
            print("✓ WebSocket connected")
            
            # Receive initial scene
            msg = await ws.recv()
            data = json.loads(msg)
            print(f"✓ Received initial scene with {len(data.get('scene', {}).get('elements', []))} elements")
            
            await ws.send("test message")
            print("✓ Sent test message")
            
    except Exception as e:
        print(f"✗ WebSocket test failed: {e}")

def test_health():
    """Test health endpoint."""
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed: {data['status']}")
            print(f"  - Elements: {data['elements_count']}")
            print(f"  - Connections: {data['active_connections']}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")

def test_demo():
    """Test demo endpoint."""
    try:
        response = requests.get("http://127.0.0.1:8000/demo", timeout=5)
        if response.status_code == 200:
            print("✓ Demo endpoint working")
        else:
            print(f"✗ Demo endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Demo endpoint failed: {e}")

async def main():
    print("Running MCP Server Tests...")
    print("=" * 40)
    
    # Wait a bit for server to start
    time.sleep(2)
    
    # Test health endpoint
    test_health()
    
    # Test demo endpoint
    test_demo()
    
    # Test WebSocket
    await test_websocket()
    
    print("=" * 40)
    print("Tests completed!")

if __name__ == "__main__":
    asyncio.run(main())