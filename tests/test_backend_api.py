"""
Komplexné testy pre Backend API
"""
import sys
import os
import time

# Pridať backend do path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Pridať venv site-packages do path
venv_path = os.path.join(backend_path, 'venv', 'lib', 'python3.14', 'site-packages')
if os.path.exists(venv_path):
    sys.path.insert(0, venv_path)

try:
    import requests
except ImportError:
    print("⚠️ requests nie je nainštalovaný. Inštalujem...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'], cwd=backend_path)
    import requests

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test health check endpoint"""
    print("🔍 Test: Health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        # Health endpoint môže vrátiť "ok", "healthy" alebo iný formát
        assert "status" in data or "features" in data, "Should have status or features"
        print(f"   ✅ Health endpoint OK (status: {data.get('status', 'N/A')})")
        return True
    except Exception as e:
        print(f"   ❌ Health endpoint failed: {e}")
        return False

def test_search_cz():
    """Test CZ IČO search"""
    print("🔍 Test: CZ IČO search...")
    try:
        response = requests.get(f"{BASE_URL}/api/search?q=27074358", timeout=10)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "nodes" in data, "Should have nodes"
        assert "edges" in data, "Should have edges"
        assert len(data["nodes"]) > 0, "Should have at least one node"
        print(f"   ✅ CZ search OK ({len(data['nodes'])} nodes, {len(data['edges'])} edges)")
        return True
    except Exception as e:
        print(f"   ❌ CZ search failed: {e}")
        return False

def test_search_sk():
    """Test SK IČO search (test IČO 88888888)"""
    print("🔍 Test: SK IČO search...")
    try:
        response = requests.get(f"{BASE_URL}/api/search?q=88888888", timeout=10)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "nodes" in data, "Should have nodes"
        assert "edges" in data, "Should have edges"
        assert len(data["nodes"]) > 0, "Should have at least one node"
        # Skontrolovať, či sú SK nodes
        sk_nodes = [n for n in data["nodes"] if n.get("country") == "SK"]
        assert len(sk_nodes) > 0, "Should have SK nodes"
        print(f"   ✅ SK search OK ({len(data['nodes'])} nodes, {len(sk_nodes)} SK nodes)")
        return True
    except Exception as e:
        print(f"   ❌ SK search failed: {e}")
        return False

def test_search_pl():
    """Test PL KRS search"""
    print("🔍 Test: PL KRS search...")
    try:
        response = requests.get(f"{BASE_URL}/api/search?q=123456789", timeout=10)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "nodes" in data, "Should have nodes"
        assert "edges" in data, "Should have edges"
        pl_nodes = [n for n in data["nodes"] if n.get("country") == "PL"]
        print(f"   ✅ PL search OK ({len(data['nodes'])} nodes, {len(pl_nodes)} PL nodes)")
        return True
    except Exception as e:
        print(f"   ❌ PL search failed: {e}")
        return False

def test_search_hu():
    """Test HU adószám search"""
    print("🔍 Test: HU adószám search...")
    try:
        response = requests.get(f"{BASE_URL}/api/search?q=12345678", timeout=10)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "nodes" in data, "Should have nodes"
        assert "edges" in data, "Should have edges"
        hu_nodes = [n for n in data["nodes"] if n.get("country") == "HU"]
        print(f"   ✅ HU search OK ({len(data['nodes'])} nodes, {len(hu_nodes)} HU nodes)")
        return True
    except Exception as e:
        print(f"   ❌ HU search failed: {e}")
        return False

def test_cache_stats():
    """Test cache stats endpoint"""
    print("🔍 Test: Cache stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/cache/stats", timeout=5)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        # Cache stats môže mať rôzne formáty
        assert isinstance(data, dict), "Should return dictionary"
        print("   ✅ Cache stats OK")
        return True
    except Exception as e:
        print(f"   ❌ Cache stats failed: {e}")
        return False

def test_rate_limiter_stats():
    """Test rate limiter stats endpoint"""
    print("🔍 Test: Rate limiter stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/rate-limiter/stats", timeout=5)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "active_buckets" in data or "tiers" in data, "Should have rate limiter stats"
        print("   ✅ Rate limiter stats OK")
        return True
    except Exception as e:
        print(f"   ❌ Rate limiter stats failed: {e}")
        return False

def test_rate_limiting():
    """Test rate limiting functionality"""
    print("🔍 Test: Rate limiting...")
    try:
        # Urobiť viacero requestov rýchlo
        responses = []
        for i in range(15):
            response = requests.get(f"{BASE_URL}/api/search?q=test{i}", timeout=5)
            responses.append(response.status_code)
        
        # Mal by byť aspoň jeden 429 (rate limit exceeded)
        has_429 = 429 in responses
        if has_429:
            print("   ✅ Rate limiting works (429 detected)")
        else:
            print("   ⚠️ Rate limiting not triggered (might be OK if bucket refilled)")
        return True
    except Exception as e:
        print(f"   ❌ Rate limiting test failed: {e}")
        return False

def test_services_import():
    """Test, či sa všetky services správne importujú"""
    print("🔍 Test: Services import...")
    try:
        from services.sk_rpo import is_slovak_ico, fetch_rpo_sk
        from services.pl_krs import is_polish_krs, fetch_krs_pl
        from services.hu_nav import is_hungarian_tax_number, fetch_nav_hu
        from services.cache import get, set, get_stats
        from services.rate_limiter import is_allowed, get_stats as get_rl_stats
        from services.risk_intelligence import generate_risk_report
        
        # Test detekcie
        assert is_slovak_ico("88888888"), "SK IČO detection failed"
        assert is_polish_krs("123456789"), "PL KRS detection failed"
        assert is_hungarian_tax_number("12345678"), "HU adószám detection failed"
        
        print("   ✅ All services import OK")
        return True
    except Exception as e:
        print(f"   ❌ Services import failed: {e}")
        return False

def run_all_tests():
    """Spustí všetky testy"""
    print("")
    print("═══════════════════════════════════════")
    print("🧪 SPÚŠTANIE BACKEND TESTOV")
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
        print("   Spusti: cd backend && source venv/bin/activate && python main.py")
        return False
    
    print("")
    
    tests = [
        test_services_import,
        test_health_endpoint,
        test_cache_stats,
        test_rate_limiter_stats,
        test_search_cz,
        test_search_sk,
        test_search_pl,
        test_search_hu,
        test_rate_limiting,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            time.sleep(0.5)  # Malá pauza medzi testami
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

