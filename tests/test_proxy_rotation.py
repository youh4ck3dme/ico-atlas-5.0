"""
Testy pre proxy rotation službu
"""

import sys
import os
from unittest.mock import Mock, patch

# Pridať backend do path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.proxy_rotation import (  # type: ignore
    ProxyPool,
    init_proxy_pool,
    get_proxy,
    get_proxy_stats,
    make_request_with_proxy
)


def test_proxy_pool_add_proxy():
    """Test pridania proxy do poolu"""
    pool = ProxyPool()
    pool.add_proxy("http://proxy1.com:8080")
    
    assert len(pool.proxies) == 1, "Proxy by malo byť pridané"
    assert pool.proxies[0]["http"] == "http://proxy1.com:8080"


def test_proxy_pool_get_next():
    """Test získania ďalšieho proxy"""
    pool = ProxyPool()
    pool.add_proxy("http://proxy1.com:8080")
    pool.add_proxy("http://proxy2.com:8080")
    
    proxy1 = pool.get_next_proxy()
    proxy2 = pool.get_next_proxy()
    
    assert proxy1 is not None, "Proxy by malo byť dostupné"
    assert proxy2 is not None, "Druhé proxy by malo byť dostupné"
    assert proxy1 != proxy2 or len(pool.proxies) == 1, "Proxy by sa mali rotovať"


def test_proxy_pool_mark_success():
    """Test označenia proxy ako úspešné"""
    pool = ProxyPool()
    pool.add_proxy("http://proxy1.com:8080")
    
    proxy = pool.get_next_proxy()
    pool.mark_success(proxy)
    
    stats = pool.get_stats()
    assert stats['total_proxies'] == 1
    assert stats['available_proxies'] == 1


def test_proxy_pool_mark_failed():
    """Test označenia proxy ako zlyhané"""
    pool = ProxyPool()
    pool.add_proxy("http://proxy1.com:8080")
    
    proxy = pool.get_next_proxy()
    pool.mark_failed(proxy)
    
    stats = pool.get_stats()
    assert stats['failed_proxies'] == 1, "Proxy by malo byť označené ako zlyhané"


def test_proxy_pool_stats():
    """Test získania štatistík"""
    pool = ProxyPool()
    pool.add_proxy("http://proxy1.com:8080")
    
    stats = pool.get_stats()
    assert 'total_proxies' in stats
    assert 'available_proxies' in stats
    assert 'failed_proxies' in stats
    assert stats['total_proxies'] == 1


def test_init_proxy_pool():
    """Test inicializácie proxy poolu"""
    init_proxy_pool(["http://proxy1.com:8080", "http://proxy2.com:8080"])
    
    stats = get_proxy_stats()
    assert stats['total_proxies'] == 2, "Mali by byť 2 proxy"


def test_get_proxy():
    """Test získania proxy z globálneho poolu"""
    init_proxy_pool(["http://proxy1.com:8080"])
    
    proxy = get_proxy()
    assert proxy is not None, "Proxy by malo byť dostupné"


@patch('requests.get')
def test_make_request_with_proxy(mock_get):
    """Test HTTP requestu s proxy"""
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"test": "data"}
    mock_get.return_value = mock_response
    
    # Test bez proxy (proxy pool prázdny)
    init_proxy_pool([])
    response = make_request_with_proxy("http://example.com/api")
    
    assert response is not None, "Response by mal byť vrátený"
    assert mock_get.called, "requests.get by malo byť zavolané"


if __name__ == "__main__":
    print("🧪 Testing proxy rotation...")
    print()
    
    tests = [
        ("Add proxy", test_proxy_pool_add_proxy),
        ("Get next proxy", test_proxy_pool_get_next),
        ("Mark success", test_proxy_pool_mark_success),
        ("Mark failed", test_proxy_pool_mark_failed),
        ("Get stats", test_proxy_pool_stats),
        ("Init pool", test_init_proxy_pool),
        ("Get proxy", test_get_proxy),
        ("Make request", test_make_request_with_proxy),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name}")
            passed += 1
        except Exception as e:
            print(f"❌ {name}: {e}")
            failed += 1
    
    print()
    print("═══════════════════════════════════════")
    print(f"📊 Results: {passed} passed, {failed} failed")
    print("═══════════════════════════════════════")
    
    if failed > 0:
        sys.exit(1)

