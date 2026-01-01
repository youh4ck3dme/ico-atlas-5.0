#!/usr/bin/env python3
"""
🧪 Production Testing Script - ILUMINATI SYSTEM
Testuje všetky V4 krajiny s reálnym IČO
"""

import json
import sys
import time
from datetime import datetime
from typing import Dict, Optional

import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

# Testovacie IČO
TEST_ICOS = {
    "SK": {
        "ico": "52374220",
        "name": "Tavira, s.r.o.",
        "description": "Reálne slovenské IČO",
    },
    "CZ": {
        "ico": "27074358",
        "name": "Agrofert, a.s.",
        "description": "Reálne české IČO",
    },
    "PL": {
        "ico": "0000123456",
        "name": "Test KRS",
        "description": "Testovacie poľské KRS",
    },
    "HU": {
        "ico": "12345678",
        "name": "Test Adószám",
        "description": "Testovacie maďarské adószám",
    },
}


def print_header(text: str):
    """Vytlačí hlavičku sekcie"""
    print("\n" + "=" * 60)
    print(f"📋 {text}")
    print("=" * 60)


def print_success(text: str):
    """Vytlačí úspešnú správu"""
    print(f"✅ {text}")


def print_error(text: str):
    """Vytlačí chybovú správu"""
    print(f"❌ {text}")


def print_warning(text: str):
    """Vytlačí varovnú správu"""
    print(f"⚠️  {text}")


def test_health_check() -> bool:
    """Test 1: Health Check"""
    print_header("Test 1: Health Check")
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        duration = (time.time() - start_time) * 1000

        if response.status_code == 200:
            print_success(f"Health check: OK ({duration:.0f}ms)")
            data = response.json()
            print(f"   Status: {data.get('status', 'N/A')}")
            return True
        else:
            print_error(f"Health check: FAILED (HTTP {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Backend nie je spustený!")
        print(
            "   Spusti backend: cd backend && source venv/bin/activate && python main.py"
        )
        return False
    except Exception as e:
        print_error(f"Health check: ERROR - {e}")
        return False


def test_country_search(country: str, test_data: Dict) -> Dict:
    """Test search pre konkrétnu krajinu"""
    ico = test_data["ico"]
    name = test_data["name"]
    description = test_data["description"]

    print(f"\nTesting {country}: {ico} ({name})")
    print(f"   {description}")

    try:
        start_time = time.time()
        response = requests.get(
            f"{BASE_URL}/api/search", params={"q": ico}, timeout=TIMEOUT
        )
        duration = (time.time() - start_time) * 1000
        http_code = response.status_code

        if http_code == 200:
            data = response.json()
            nodes = data.get("nodes", [])
            edges = data.get("edges", [])

            if len(nodes) > 0:
                print_success(f"{country} search: OK ({duration:.0f}ms)")
                print(f"   Nodes: {len(nodes)}, Edges: {len(edges)}")

                # Zobraziť prvý node
                if nodes:
                    first_node = nodes[0]
                    print(
                        f"   First node: {first_node.get('name', 'N/A')} ({first_node.get('country', 'N/A')})"
                    )

                return {
                    "success": True,
                    "duration": duration,
                    "nodes": len(nodes),
                    "edges": len(edges),
                }
            else:
                print_warning(
                    f"{country} search: Response OK but no nodes found ({duration:.0f}ms)"
                )
                return {
                    "success": False,
                    "duration": duration,
                    "nodes": 0,
                    "edges": 0,
                    "error": "No nodes in response",
                }
        else:
            print_warning(f"{country} search: HTTP {http_code} ({duration:.0f}ms)")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'N/A')}")
            except:
                print(f"   Response: {response.text[:100]}")

            return {"success": False, "duration": duration, "http_code": http_code}
    except requests.exceptions.Timeout:
        print_error(f"{country} search: TIMEOUT (> {TIMEOUT}s)")
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        print_error(f"{country} search: ERROR - {e}")
        return {"success": False, "error": str(e)}


def test_error_handling() -> bool:
    """Test 6: Error Handling"""
    print_header("Test 6: Error Handling")
    print("Testing invalid IČO: 99999999")

    try:
        start_time = time.time()
        response = requests.get(
            f"{BASE_URL}/api/search", params={"q": "99999999"}, timeout=TIMEOUT
        )
        duration = (time.time() - start_time) * 1000

        if response.status_code in [200, 404, 400]:
            print_success(
                f"Error handling: OK (HTTP {response.status_code}, {duration:.0f}ms)"
            )
            try:
                data = response.json()
                if "error" in data or "detail" in data:
                    print(
                        f"   Error message: {data.get('error') or data.get('detail', 'N/A')}"
                    )
            except:
                pass
            return True
        else:
            print_warning(f"Error handling: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error handling: ERROR - {e}")
        return False


def test_cache_performance() -> Dict:
    """Test 7: Performance (Cache Test)"""
    print_header("Test 7: Performance (Cache Test)")
    print("Testing cache with repeated request: 52374220")

    ico = "52374220"

    # Prvé volanie
    print("First request:")
    try:
        start_time = time.time()
        response1 = requests.get(
            f"{BASE_URL}/api/search", params={"q": ico}, timeout=TIMEOUT
        )
        duration1 = (time.time() - start_time) * 1000
        http_code1 = response1.status_code

        if http_code1 == 200:
            print(f"   Duration: {duration1:.0f}ms")
        else:
            print_warning(f"   First request failed: HTTP {http_code1}")
            return {"success": False}
    except Exception as e:
        print_error(f"   First request error: {e}")
        return {"success": False}

    # Počkaj 1 sekundu
    time.sleep(1)

    # Druhé volanie (malo by byť z cache)
    print("Second request (should be cached):")
    try:
        start_time = time.time()
        response2 = requests.get(
            f"{BASE_URL}/api/search", params={"q": ico}, timeout=TIMEOUT
        )
        duration2 = (time.time() - start_time) * 1000
        http_code2 = response2.status_code

        if http_code2 == 200:
            print(f"   Duration: {duration2:.0f}ms")
            speedup = duration1 - duration2
            if duration2 < duration1:
                print_success(f"Cache test: OK ({speedup:.0f}ms faster)")
                return {
                    "success": True,
                    "first": duration1,
                    "second": duration2,
                    "speedup": speedup,
                }
            else:
                print_warning("Cache test: Both requests similar speed")
                return {"success": False, "first": duration1, "second": duration2}
        else:
            print_warning(f"   Second request failed: HTTP {http_code2}")
            return {"success": False}
    except Exception as e:
        print_error(f"   Second request error: {e}")
        return {"success": False}


def test_metrics() -> bool:
    """Test 8: API Metrics"""
    print_header("Test 8: API Metrics")

    try:
        response = requests.get(f"{BASE_URL}/api/metrics", timeout=5)
        if response.status_code == 200:
            print_success("Metrics endpoint: OK")
            data = response.json()
            print(f"   Total requests: {data.get('total_requests', 'N/A')}")
            print(f"   Cache hits: {data.get('cache_hits', 'N/A')}")
            print(f"   Cache misses: {data.get('cache_misses', 'N/A')}")
            return True
        else:
            print_warning(f"Metrics endpoint: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_warning(f"Metrics endpoint: Not available - {e}")
        return False


def main():
    """Hlavná testovacia funkcia"""
    print("\n" + "=" * 60)
    print("🧪 ILUMINATI SYSTEM - Production Testing")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        "health": False,
        "countries": {},
        "error_handling": False,
        "cache": {},
        "metrics": False,
    }

    # Test 1: Health Check
    results["health"] = test_health_check()
    if not results["health"]:
        print("\n❌ Backend nie je dostupný! Spusti backend server.")
        sys.exit(1)

    # Testy 2-5: V4 krajiny
    print_header("Tests 2-5: V4 Countries")
    for country, test_data in TEST_ICOS.items():
        results["countries"][country] = test_country_search(country, test_data)

    # Test 6: Error Handling
    results["error_handling"] = test_error_handling()

    # Test 7: Cache Performance
    results["cache"] = test_cache_performance()

    # Test 8: Metrics
    results["metrics"] = test_metrics()

    # Summary
    print_header("Test Summary")

    total_tests = 1 + len(TEST_ICOS) + 3  # health + countries + error + cache + metrics
    passed_tests = 0

    if results["health"]:
        passed_tests += 1
    print(f"Health check: {'✅' if results['health'] else '❌'}")

    print("\nCountries:")
    for country, result in results["countries"].items():
        if result.get("success"):
            passed_tests += 1
        status = "✅" if result.get("success") else "❌"
        duration = result.get("duration", 0)
        print(f"  {country}: {status} ({duration:.0f}ms)")

    if results["error_handling"]:
        passed_tests += 1
    print(f"Error handling: {'✅' if results['error_handling'] else '❌'}")

    if results["cache"].get("success"):
        passed_tests += 1
    print(f"Cache test: {'✅' if results['cache'].get('success') else '❌'}")

    if results["metrics"]:
        passed_tests += 1
    print(f"Metrics: {'✅' if results['metrics'] else '❌'}")

    print(f"\n📊 Results: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print_success("All tests passed! 🎉")
        return 0
    elif passed_tests >= total_tests * 0.7:
        print_warning(f"Most tests passed ({passed_tests}/{total_tests})")
        return 0
    else:
        print_error(f"Many tests failed ({passed_tests}/{total_tests})")
        return 1


if __name__ == "__main__":
    sys.exit(main())
