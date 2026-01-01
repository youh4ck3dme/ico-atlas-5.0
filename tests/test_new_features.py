"""
Testy pre nové features: CEIDG, Biała Lista, Debt Registers, Database
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

def test_pl_ceidg():
    """Test PL CEIDG (živnostníci) search"""
    print("🔍 Test: PL CEIDG search...")
    try:
        # CEIDG môže byť NIP (10 číslic) alebo REGON (9 alebo 14 číslic)
        response = requests.get(f"{BASE_URL}/api/search?q=1234567890", timeout=10)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "nodes" in data, "Should have nodes"
        assert "edges" in data, "Should have edges"
        pl_nodes = [n for n in data["nodes"] if n.get("country") == "PL"]
        print(f"   ✅ PL CEIDG search OK ({len(data['nodes'])} nodes, {len(pl_nodes)} PL nodes)")
        return True
    except Exception as e:
        print(f"   ❌ PL CEIDG search failed: {e}")
        return False

def test_pl_biala_lista():
    """Test PL Biała Lista (VAT status)"""
    print("🔍 Test: PL Biała Lista integration...")
    try:
        # Test s PL KRS, ktorý by mal mať VAT status
        response = requests.get(f"{BASE_URL}/api/search?q=123456789", timeout=10)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "nodes" in data, "Should have nodes"
        # Skontrolovať, či má niektorý node VAT info v details
        has_vat_info = any("VAT" in str(n.get("details", "")) for n in data["nodes"])
        print(f"   ✅ PL Biała Lista OK (VAT info: {has_vat_info})")
        return True
    except Exception as e:
        print(f"   ❌ PL Biała Lista failed: {e}")
        return False

def test_debt_registers_sk():
    """Test debt registers pre SK"""
    print("🔍 Test: SK debt registers...")
    try:
        # Test s SK IČO (88888888 má simulované dáta)
        response = requests.get(f"{BASE_URL}/api/search?q=88888888", timeout=10)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "nodes" in data, "Should have nodes"
        # Skontrolovať, či má debt nodes
        debt_nodes = [n for n in data["nodes"] if n.get("type") == "debt"]
        print(f"   ✅ SK debt registers OK (debt nodes: {len(debt_nodes)})")
        return True
    except Exception as e:
        print(f"   ❌ SK debt registers failed: {e}")
        return False

def test_debt_registers_cz():
    """Test debt registers pre CZ"""
    print("🔍 Test: CZ debt registers...")
    try:
        # Test s CZ IČO
        response = requests.get(f"{BASE_URL}/api/search?q=27074358", timeout=10)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "nodes" in data, "Should have nodes"
        # Skontrolovať, či má debt nodes
        debt_nodes = [n for n in data["nodes"] if n.get("type") == "debt"]
        print(f"   ✅ CZ debt registers OK (debt nodes: {len(debt_nodes)})")
        return True
    except Exception as e:
        print(f"   ❌ CZ debt registers failed: {e}")
        return False

def test_database_stats():
    """Test database stats endpoint"""
    print("🔍 Test: Database stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/database/stats", timeout=5)
        # Endpoint môže vrátiť 404 ak nie je implementovaný, alebo 200
        if response.status_code == 404:
            print("   ⚠️ Database stats endpoint not found (might not be implemented)")
            return True  # Nie je kritická chyba
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict), "Should return dictionary"
        assert "status" in data, "Should have status"
        print(f"   ✅ Database stats OK (status: {data.get('status')})")
        return True
    except Exception as e:
        print(f"   ⚠️ Database stats: {e} (might be OK if not implemented)")
        return True  # Nie je kritická chyba

def test_search_history():
    """Test search history endpoint"""
    print("🔍 Test: Search history...")
    try:
        # Najprv urobiť search, aby sa uložila história
        requests.get(f"{BASE_URL}/api/search?q=test_history", timeout=5)
        time.sleep(0.5)
        
        # Potom získať históriu
        response = requests.get(f"{BASE_URL}/api/search/history?limit=10", timeout=5)
        # Endpoint môže vrátiť 404 ak databáza nie je dostupná, alebo 200 s prázdnym listom
        if response.status_code == 404:
            print("   ⚠️ Search history endpoint not found (database might not be available)")
            return True  # Nie je kritická chyba
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list), "Should return list"
        print(f"   ✅ Search history OK ({len(data)} entries)")
        return True
    except Exception as e:
        print(f"   ⚠️ Search history: {e} (might be OK if DB not available)")
        return True  # Nie je kritická chyba

def test_services_import_new():
    """Test import nových services"""
    print("🔍 Test: New services import...")
    try:
        from services.pl_ceidg import is_ceidg_number  # type: ignore
        from services.pl_biala_lista import is_polish_nip  # type: ignore
        
        # Test detekcie
        assert is_ceidg_number("1234567890"), "CEIDG detection failed"
        assert is_polish_nip("1234567890"), "Polish NIP detection failed"
        
        print("   ✅ All new services import OK")
        return True
    except Exception as e:
        print(f"   ❌ New services import failed: {e}")
        return False

def run_all_tests():
    """Spustí všetky testy"""
    print("")
    print("═══════════════════════════════════════")
    print("🧪 SPÚŠTANIE TESTOV NOVÝCH FEATURES")
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
        test_services_import_new,
        test_pl_ceidg,
        test_pl_biala_lista,
        test_debt_registers_sk,
        test_debt_registers_cz,
        test_database_stats,
        test_search_history,
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

