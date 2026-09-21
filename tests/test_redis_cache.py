"""
Špeciálne testy pre Redis cache funkcionalitu
"""

import os
import sys

import pytest

# Pridať backend do path
backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

import services.redis_cache as redis_cache

from unittest.mock import MagicMock, patch

# Mock Redis client for tests where Redis is not available
@pytest.fixture(autouse=True)
def mock_redis():
    with patch("services.redis_cache.get_redis_client") as mock_get:
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        
        # In-memory storage for mock
        storage = {}
        
        def mock_get_val(key):
            return storage.get(key)
            
        def mock_set_val(key, val, ex=None):
            storage[key] = val
            return True
            
        def mock_del_val(key):
            if key in storage:
                del storage[key]
                return 1
            return 0
            
        mock_client.get.side_effect = mock_get_val
        mock_client.setex.side_effect = lambda k, t, v: mock_set_val(k, v)
        mock_client.delete.side_effect = mock_del_val
        mock_client.exists.side_effect = lambda k: k in storage
        mock_get.return_value = mock_client
        yield mock_client


def test_redis_cache_imports():
    """Test, či Redis cache sa dá importovať"""
    assert redis_cache.get_redis_client is not None
    assert callable(redis_cache.get_redis_client)


def test_redis_client_initialization(mock_redis):
    """Test, či Redis klient sa inicializuje"""
    client = redis_cache.get_redis_client()
    assert client is not None
    assert client.ping() is True


def test_redis_get_set_delete(mock_redis):
    """Test základných Redis operácií (get, set, delete)"""
    # Test set
    test_key = "test_key_12345"
    test_value = {"test": "data", "number": 42}
    redis_cache.redis_set(test_key, test_value, ttl=60)

    # Test get
    retrieved = redis_cache.redis_get(test_key)
    assert retrieved is not None
    assert retrieved == test_value

    # Test delete
    redis_cache.redis_delete(test_key)
    deleted = redis_cache.redis_get(test_key)
    assert deleted is None


def test_redis_get_stats():
    """Test, či redis_get_stats vracia správne štatistiky"""
    stats = redis_cache.redis_get_stats()
    assert isinstance(stats, dict)
    assert "total_keys" in stats or "available" in stats


def test_redis_cache_integration():
    """Test, či cache.py používa Redis (cez mock)"""
    from services.cache import get, set, delete
    
    test_key = "test_cache_key_12345"
    test_value = {"test": "cache"}

    set(test_key, test_value)
    retrieved = get(test_key)

    assert retrieved is not None
    assert retrieved == test_value
    
    delete(test_key)
    assert get(test_key) is None


def test_redis_fallback_to_memory():
    """Test, či cache fallbackuje na in-memory (ak Redis mock vráti None)"""
    with patch("services.redis_cache.get_redis_client", return_value=None):
        from services.cache import get, set, delete
        
        test_key = "test_fallback_key_12345"
        test_value = {"test": "fallback"}

        set(test_key, test_value)
        retrieved = get(test_key)

        assert retrieved == test_value
        delete(test_key)
