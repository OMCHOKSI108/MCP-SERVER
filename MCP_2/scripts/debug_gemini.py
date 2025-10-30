import os
import requests

def list_gemini_models():
    api_key = "AIzaSyCnoNFn3zm8AIh0PXCBofxC95l_EKEf_rs"
    

    url = "https://generativelanguage.googleapis.com/v1/models"
    resp = requests.get(url, params={"key": api_key}, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    models = data.get("models", [])
    if not models:
        print("No models returned")
        return

    print("Available models:")
    for m in models:
        # typical model entry has 'name' and optional 'displayName'/'description'
        print("-", m.get("name"), "|", m.get("displayName", m.get("description", "")))

if __name__ == "__main__":
    list_gemini_models()
