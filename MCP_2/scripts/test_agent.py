"""
Test script for the MCP-2 Gemini-powered Web Scraping Agent
Tests the complete workflow: scrape -> store -> query with Gemini
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_agent_workflow():
    """Test the complete agent workflow"""
    
    print("🤖 Testing MCP-2 Web Scraping Agent with Gemini")
    print("=" * 50)
    
    # Test data
    test_url = "https://example.com"
    test_prompt = "What is this website about? Summarize it in 2-3 sentences."
    
    print(f"📝 Test URL: {test_url}")
    print(f"❓ Test Prompt: {test_prompt}")
    print()
    
    # Test 1: Check if API is running
    print("1️⃣ Testing API connection...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API is running!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ API connection failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Could not connect to API: {e}")
        print("   Make sure the server is running: uv run uvicorn main:app --reload")
        return
    print()
    
    # Test 2: Test agent query (scrape + AI)
    print("2️⃣ Testing intelligent agent query...")
    try:
        payload = {
            "url": test_url,
            "prompt": test_prompt
        }
        
        print(f"   Sending request: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/agent/query/", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Agent query successful!")
            print(f"   URL: {result.get('url')}")
            print(f"   Prompt: {result.get('prompt')}")
            print(f"   🧠 AI Response: {result.get('agent_response')}")
        else:
            print(f"❌ Agent query failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Agent query error: {e}")
        return
    print()
    
    # Test 3: Check memory (data storage)
    print("3️⃣ Testing agent memory...")
    try:
        response = requests.get(f"{BASE_URL}/data/")
        if response.status_code == 200:
            memory = response.json()
            print("✅ Agent memory accessible!")
            print(f"   Stored items: {len(memory.get('agent_memory', []))}")
            for item in memory.get('agent_memory', [])[:3]:  # Show first 3 items
                print(f"   - {item.get('url')} (scraped: {item.get('scraped_at')})")
        else:
            print(f"❌ Memory access failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Memory access error: {e}")
    print()
    
    # Test 4: Test second query (should use memory)
    print("4️⃣ Testing memory usage (second query)...")
    try:
        payload = {
            "url": test_url,  # Same URL as before
            "prompt": "Give me just the main title or heading of this page."
        }
        
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/agent/query/", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Second query successful (using memory)!")
            print(f"   Response time: {end_time - start_time:.2f} seconds")
            print(f"   🧠 AI Response: {result.get('agent_response')}")
        else:
            print(f"❌ Second query failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Second query error: {e}")
    print()
    
    print("🎉 Agent workflow test completed!")
    print(f"🌐 Visit {BASE_URL}/docs to explore the API interactively")

if __name__ == "__main__":
    test_agent_workflow()