
import os
import sys
import asyncio
from fastapi.testclient import TestClient

# Add backend to path
sys.path.insert(0, os.path.abspath("backend"))

from main import app

client = TestClient(app)

def test_search_cz():
    print("Testing CZ search...")
    # 27074358 is a valid CZ IČO (ARES)
    response = client.get("/api/search?q=27074358&country=CZ")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Nodes: {len(data['nodes'])}")
        for node in data['nodes']:
            print(f" - {node['label']} ({node['country']})")
    else:
        print(f"Error: {response.text}")

def test_search_text_cz():
    print("\nTesting text search for CZ...")
    # Searching for "Agrofert" - should be found in CZ
    response = client.get("/api/search?q=Agrofert&country=CZ")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Nodes: {len(data['nodes'])}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    try:
        test_search_cz()
    except Exception as e:
        print(f"CZ Test failed: {e}")
    
    try:
        test_search_text_cz()
    except Exception as e:
        print(f"Text Test failed: {e}")
