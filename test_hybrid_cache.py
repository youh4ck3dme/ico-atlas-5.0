import sys
import os
import time
from datetime import timedelta

# Pridať backend do path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.cache import TieredCache

def test_lru_eviction():
    print("\n--- Testing L1 LRU Eviction ---")
    # L1 max size = 5 for testing
    cache = TieredCache(l1_max_size=5)
    
    # Fill cache
    for i in range(5):
        cache.set(f"key_{i}", f"value_{i}")
    
    print(f"Cache size: {len(cache._l1_cache)}")
    assert len(cache._l1_cache) == 5
    
    # Access key_0 to make it most recent
    cache.get("key_0")
    
    # Add one more key (should evict key_1, since key_0 was recently accessed)
    cache.set("key_5", "value_5")
    
    print(f"Cache size after one more: {len(cache._l1_cache)}")
    assert len(cache._l1_cache) == 5
    
    assert cache.get("key_1") is None
    assert cache.get("key_0") == "value_0"
    assert cache.get("key_5") == "value_5"
    print("✅ LRU Eviction passed")

def test_ttl_jitter():
    print("\n--- Testing TTL Jitter (MOCKED REDIS) ---")
    import unittest.mock as mock
    
    with mock.patch('services.cache.REDIS_AVAILABLE', True):
        with mock.patch('services.cache.redis_set') as mock_set:
            cache = TieredCache()
            cache._redis_enabled = True
            
            with mock.patch.object(cache, '_is_redis_active', return_value=True):
                ttls = []
                for _ in range(10):
                    cache.set("jitter_test", "val", ttl=timedelta(seconds=100))
                    # Capture the TTL passed to redis_set
                    args, kwargs = mock_set.call_args
                    ttls.append(args[2])
                
                print(f"Generated TTLs: {ttls}")
                unique_ttls = set(ttls)
                print(f"Unique TTLs: {len(unique_ttls)}")
                
                # With jitter, we expect some variance
                assert len(unique_ttls) > 1
                for ttl in ttls:
                    assert 90 <= ttl <= 110
                
                print("✅ TTL Jitter passed")

if __name__ == "__main__":
    try:
        test_lru_eviction()
        test_ttl_jitter()
        print("\n✨ All Hybrid Cache tests passed!")
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
