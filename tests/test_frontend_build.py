"""
Test frontend build a základnej funkcionality
"""
import subprocess
import os
import sys

def test_frontend_build():
    """Test, či frontend build funguje"""
    print("🔍 Test: Frontend build...")
    try:
        frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
        result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("   ✅ Frontend build úspešný")
            return True
        else:
            print(f"   ❌ Frontend build zlyhal:")
            print(f"      {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Frontend build test failed: {e}")
        return False

def test_package_json():
    """Test, či package.json je validný"""
    print("🔍 Test: package.json...")
    try:
        import json
        frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
        package_path = os.path.join(frontend_dir, 'package.json')
        
        with open(package_path, 'r') as f:
            package = json.load(f)
        
        assert 'dependencies' in package, "Should have dependencies"
        assert 'react' in package['dependencies'], "Should have react"
        assert 'react-dom' in package['dependencies'], "Should have react-dom"
        
        print("   ✅ package.json OK")
        return True
    except Exception as e:
        print(f"   ❌ package.json test failed: {e}")
        return False

def test_vite_config():
    """Test, či vite.config.js existuje"""
    print("🔍 Test: vite.config.js...")
    try:
        frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
        vite_config = os.path.join(frontend_dir, 'vite.config.js')
        
        assert os.path.exists(vite_config), "vite.config.js should exist"
        
        with open(vite_config, 'r') as f:
            content = f.read()
            assert 'VitePWA' in content or 'react' in content, "Should have plugins"
        
        print("   ✅ vite.config.js OK")
        return True
    except Exception as e:
        print(f"   ❌ vite.config.js test failed: {e}")
        return False

def test_components_exist():
    """Test, či hlavné komponenty existujú"""
    print("🔍 Test: React komponenty...")
    try:
        frontend_src = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src')
        
        required_components = [
            'App.jsx',
            'pages/HomePageNew.jsx',
            'components/ForceGraph.jsx',
            'components/ErrorBoundary.jsx',
            'components/SEOHead.jsx',
        ]
        
        missing = []
        for comp in required_components:
            comp_path = os.path.join(frontend_src, comp)
            if not os.path.exists(comp_path):
                missing.append(comp)
        
        if missing:
            print(f"   ❌ Chýbajúce komponenty: {', '.join(missing)}")
            return False
        
        print(f"   ✅ Všetky komponenty existujú ({len(required_components)})")
        return True
    except Exception as e:
        print(f"   ❌ Components test failed: {e}")
        return False

def run_all_tests():
    """Spustí všetky frontend testy"""
    print("")
    print("═══════════════════════════════════════")
    print("🧪 SPÚŠTANIE FRONTEND TESTOV")
    print("═══════════════════════════════════════")
    print("")
    
    tests = [
        test_package_json,
        test_vite_config,
        test_components_exist,
        test_frontend_build,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
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
        print("🎉 VŠETKY FRONTEND TESTY ÚSPEŠNÉ!")
    else:
        print("⚠️ Niektoré testy zlyhali")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

