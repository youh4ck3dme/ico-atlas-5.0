import requests
import json

BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "test_automation@example.com",
    "password": "TestPassword123!",
    "full_name": "Test Automation User"
}

def debug_auth():
    print("1. Testing Registration...")
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/register", json=TEST_USER)
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {resp.text}")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n2. Testing Login...")
    try:
        data = {
            "username": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        resp = requests.post(f"{BASE_URL}/api/auth/login", data=data)
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {resp.text}")
        
        if resp.status_code == 200:
            print(f"   Token: {resp.json().get('access_token')[:20]}...")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    debug_auth()
