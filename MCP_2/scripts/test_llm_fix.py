#!/usr/bin/env python3
"""
Test script to verify the llm_service.py is working correctly.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import llm_service
    print("✅ llm_service imported successfully")
    
    # Test the query_llm function with simple content
    test_context = "This is a test webpage about Python programming. Python is a versatile programming language."
    test_prompt = "What is this page about?"
    
    print("🔄 Testing LLM query...")
    response = llm_service.query_llm(test_context, test_prompt)
    print(f"✅ LLM Response: {response}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()