#!/usr/bin/env python3
"""
Test script to verify the entire application stack is working.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔄 Testing imports...")
    import database
    import llm_service
    import main
    print("✅ All modules imported successfully")
    
    print("🔄 Testing database initialization...")
    database.init_db()
    print("✅ Database initialized successfully")
    
    print("🔄 Testing LLM service...")
    test_response = llm_service.query_llm(
        context="This is a test webpage about artificial intelligence.",
        prompt="What is the main topic of this page?"
    )
    print(f"✅ LLM Service working: {test_response}")
    
    print("🔄 Testing database operations...")
    database.add_scraped_data("https://test.com", "Test content")
    stored_data = database.get_all_scraped_data()
    print(f"✅ Database operations working: {len(stored_data)} records found")
    
    print("✅ All components are working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()