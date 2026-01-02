import subprocess
import sys
import os

def run_test_script(script_name):
    print(f"\n🚀 Running {script_name}...")
    try:
        # Use the venv python if available
        python_exe = os.path.join('backend', 'venv', 'Scripts', 'python.exe')
        if not os.path.exists(python_exe):
            python_exe = sys.executable
            
        result = subprocess.run([python_exe, script_name], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {script_name} passed!")
            return True
        else:
            print(f"❌ {script_name} failed!")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def main():
    print("=========================================")
    print("   ILUMINATI SYSTEM - UNIFIED TEST SUITE ")
    print("=========================================")
    
    tests = [
        "verify_fallback.py",
        "test_hybrid_cache.py",
        "test_real_ico.py",
        "tests/test_graph_standalone.py"
    ]
    
    results = {}
    for test in tests:
        if os.path.exists(test):
            results[test] = run_test_script(test)
        else:
            print(f"⚠️  Test script {test} not found, skipping.")
    
    print("\n" + "="*41)
    print("               TEST SUMMARY              ")
    print("="*41)
    all_passed = True
    for test, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{test:<25} : {status}")
        if not passed:
            all_passed = False
            
    if all_passed:
        print("\n✨ ALL CORE SYSTEMS ARE FUNCTIONAL")
    else:
        print("\n⚠️  SOME SYSTEMS NEED ATTENTION")
        sys.exit(1)

if __name__ == "__main__":
    main()
