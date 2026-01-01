#!/usr/bin/env python3
"""
Základné testy pre ILUMINATE SYSTEM Backend
"""
import sys
import os

# Pridaj backend do path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test, či sa všetky moduly dajú importovať"""
    print("🧪 Test 1: Kontrola importov...")
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel
        import requests
        import uvicorn
        print("   ✅ Všetky importy úspešné")
        return True
    except ImportError as e:
        print(f"   ❌ Chyba importu: {e}")
        return False

def test_models():
    """Test dátových modelov"""
    print("🧪 Test 2: Kontrola dátových modelov...")
    try:
        from pydantic import BaseModel
        from typing import List, Optional
        
        class TestNode(BaseModel):
            id: str
            label: str
            type: str
        
        node = TestNode(id="test", label="Test", type="company")
        assert node.id == "test"
        print("   ✅ Dátové modely fungujú")
        return True
    except Exception as e:
        print(f"   ❌ Chyba modelov: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI aplikácie"""
    print("🧪 Test 3: Kontrola FastAPI aplikácie...")
    try:
        import sys
        import os
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        from main import app  # type: ignore
        
        assert app is not None
        assert app.title == "ILUMINATE SYSTEM API"
        print("   ✅ FastAPI aplikácia je správne inicializovaná")
        return True
    except Exception as e:
        print(f"   ❌ Chyba FastAPI: {e}")
        return False

def test_endpoints():
    """Test endpointov"""
    print("🧪 Test 4: Kontrola endpointov...")
    try:
        import sys
        import os
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        from main import app  # type: ignore
        
        routes = [route.path for route in app.routes]
        assert "/" in routes
        assert "/api/search" in routes
        print(f"   ✅ Nájdené endpointy: {', '.join(routes)}")
        return True
    except Exception as e:
        print(f"   ❌ Chyba endpointov: {e}")
        return False

def main():
    """Spustí všetky testy"""
    print("=" * 50)
    print("🚀 Spúšťam základné testy pre ILUMINATE SYSTEM Backend")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_models,
        test_fastapi_app,
        test_endpoints
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"📊 Výsledok: {passed}/{total} testov úspešných")
    
    if passed == total:
        print("✅ Všetky testy prešli!")
        return 0
    else:
        print("❌ Niektoré testy zlyhali")
        return 1

if __name__ == "__main__":
    sys.exit(main())

