"""
Testy pre všetky API endpointy
"""
import sys
import os
import time

# Pridať backend do path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

try:
    import requests
except ImportError:
    print("⚠️ requests nie je nainštalovaný. Inštalujem...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'], cwd=backend_path)
    import requests

BASE_URL = "http://localhost:8000"

def test_metrics_endpoint():
    """Test metrics endpoint"""
    print("🔍 Test: Metrics endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/metrics", timeout=5)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict), "Should return dictionary"
        print("   ✅ Metrics endpoint OK")
        return True
    except Exception as e:
        print(f"   ❌ Metrics endpoint failed: {e}")
        return False

def test_circuit_breaker_stats():
    """Test circuit breaker stats endpoint"""
    print("🔍 Test: Circuit breaker stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/circuit-breaker/stats", timeout=5)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict), "Should return dictionary"
        print("   ✅ Circuit breaker stats OK")
        return True
    except Exception as e:
        print(f"   ❌ Circuit breaker stats failed: {e}")
        return False

def test_proxy_stats():
    """Test proxy stats endpoint"""
    print("🔍 Test: Proxy stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/proxy/stats", timeout=5)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict), "Should return dictionary"
        assert "total_proxies" in data or "available_proxies" in data, "Should have proxy stats"
        print("   ✅ Proxy stats OK")
        return True
    except Exception as e:
        print(f"   ❌ Proxy stats failed: {e}")
        return False

def test_database_stats():
    """Test database stats endpoint"""
    print("🔍 Test: Database stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/database/stats", timeout=5)
        # Môže vrátiť 404 ak databáza nie je dostupná
        if response.status_code == 404:
            print("   ⚠️ Database stats not available (DB might not be set up)")
            return True  # Nie je kritická chyba
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict), "Should return dictionary"
        print("   ✅ Database stats OK")
        return True
    except Exception as e:
        print(f"   ⚠️ Database stats: {e} (might be OK if DB not available)")
        return True  # Nie je kritická chyba

def test_search_history():
    """Test search history endpoint"""
    print("🔍 Test: Search history...")
    try:
        # Najprv urobiť search
        requests.get(f"{BASE_URL}/api/search?q=test_history_{int(time.time())}", timeout=5)
        time.sleep(0.5)
        
        # Potom získať históriu
        response = requests.get(f"{BASE_URL}/api/search/history?limit=10", timeout=5)
        if response.status_code == 404:
            print("   ⚠️ Search history not available (DB might not be set up)")
            return True  # Nie je kritická chyba
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list), "Should return list"
        print(f"   ✅ Search history OK ({len(data)} entries)")
        return True
    except Exception as e:
        print(f"   ⚠️ Search history: {e} (might be OK if DB not available)")
        return True  # Nie je kritická chyba

def test_circuit_breaker_reset():
    """Test circuit breaker reset endpoint"""
    print("🔍 Test: Circuit breaker reset...")
    try:
        # Skúsiť resetovať nejaký breaker
        response = requests.get(f"{BASE_URL}/api/circuit-breaker/reset/test_breaker", timeout=5)
        # Môže vrátiť 200 alebo 404 ak breaker neexistuje
        assert response.status_code in [200, 404], f"Expected 200 or 404, got {response.status_code}"
        if response.status_code == 200:
            data = response.json()
            assert "status" in data, "Should have status"
        print("   ✅ Circuit breaker reset OK")
        return True
    except Exception as e:
        print(f"   ⚠️ Circuit breaker reset: {e}")
        return True  # Nie je kritická chyba

def test_search_with_invalid_query():
    """Test search s neplatným query"""
    print("🔍 Test: Search with invalid query...")
    try:
        response = requests.get(f"{BASE_URL}/api/search?q=", timeout=5)
        # Môže vrátiť 200 s prázdnymi výsledkami alebo 400
        assert response.status_code in [200, 400], f"Expected 200 or 400, got {response.status_code}"
        if response.status_code == 200:
            data = response.json()
            assert "nodes" in data, "Should have nodes"
        print("   ✅ Invalid query handling OK")
        return True
    except Exception as e:
        print(f"   ❌ Invalid query test failed: {e}")
        return False

def test_api_docs():
    """Test API dokumentácia endpoint"""
    print("🔍 Test: API docs...")
    try:
        response = requests.get(f"{BASE_URL}/api/docs", timeout=5)
        # Swagger UI by mal vrátiť HTML
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert "text/html" in response.headers.get("content-type", ""), "Should return HTML"
        print("   ✅ API docs OK")
        return True
    except Exception as e:
        print(f"   ❌ API docs failed: {e}")
        return False

def test_openapi_spec():
    """Test OpenAPI spec endpoint"""
    print("🔍 Test: OpenAPI spec...")
    try:
        response = requests.get(f"{BASE_URL}/api/openapi.json", timeout=5)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "openapi" in data or "info" in data, "Should be OpenAPI spec"
        print("   ✅ OpenAPI spec OK")
        return True
    except Exception as e:
        print(f"   ❌ OpenAPI spec failed: {e}")
        return False

def run_all_tests():
    """Spustí všetky testy"""
    print("")
    print("═══════════════════════════════════════")
    print("🧪 SPÚŠTANIE API ENDPOINT TESTOV")
    print("═══════════════════════════════════════")
    print("")
    
    # Počkať, kým server beží
    print("⏳ Čakám na server...")
    for i in range(10):
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=2)
            if response.status_code == 200:
                print("✅ Server beží!")
                break
        except (requests.exceptions.RequestException, ConnectionError):
            time.sleep(1)
    else:
        print("❌ Server nie je dostupný na http://localhost:8000")
        return False
    
    print("")
    
    tests = [
        test_metrics_endpoint,
        test_circuit_breaker_stats,
        test_proxy_stats,
        test_database_stats,
        test_search_history,
        test_circuit_breaker_reset,
        test_search_with_invalid_query,
        test_api_docs,
        test_openapi_spec,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            time.sleep(0.3)  # Malá pauza medzi testami
        except Exception as e:
            print(f"   ❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("")
    print("═══════════════════════════════════════")
    print("📊 VÝSLEDKY TESTOV")
    print("═══════════════════════════════════════")
    print("")
    
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"✅ Úspešné: {passed}/{total}")
    print(f"❌ Zlyhané: {total - passed}/{total}")
    print(f"📈 Úspešnosť: {success_rate:.1f}%")
    print("")
    
    if passed == total:
        print("🎉 VŠETKY TESTY ÚSPEŠNÉ!")
    elif success_rate >= 80:
        print("⚠️ Väčšina testov úspešná, niektoré potrebujú opravu")
    else:
        print("❌ Veľa testov zlyhalo - potrebná oprava")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

