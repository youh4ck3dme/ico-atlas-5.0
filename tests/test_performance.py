"""
Testy pre performance optimalizácie
"""

import sys
import os
import time
import asyncio

# Pridať backend do path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.performance import (  # type: ignore
    timing_decorator,
    cache_result,
    batch_requests,
    get_connection_pool,
    ConnectionPool
)


def test_timing_decorator():
    """Test timing decorator"""
    @timing_decorator
    def test_func(x):
        time.sleep(0.01)
        return x * 2
    
    result = test_func(5)
    assert result == 10, "Timing decorator should not modify function result"


def test_timing_decorator_async():
    """Test timing decorator on async functions (should preserve results/exceptions)."""
    @timing_decorator
    async def async_func(x):
        await asyncio.sleep(0.01)
        return x + 1

    @timing_decorator
    async def async_fail():
        await asyncio.sleep(0.01)
        raise ValueError("boom")

    async def run_test():
        assert await async_func(1) == 2
        try:
            await async_fail()
            assert False, "Expected ValueError from decorated async function"
        except ValueError as e:
            assert str(e) == "boom"

    asyncio.run(run_test())


def test_cache_result():
    """Test cache decorator"""
    call_count = [0]
    
    @cache_result(ttl=60)
    def expensive_function(x):
        call_count[0] += 1
        return x * 2
    
    # Prvé volanie - malo by sa vypočítať
    result1 = expensive_function(5)
    assert result1 == 10, "First call should compute result"
    assert call_count[0] == 1, "Function should be called once"
    
    # Druhé volanie - malo by použiť cache
    result2 = expensive_function(5)
    assert result2 == 10, "Second call should return cached result"
    assert call_count[0] == 1, "Function should not be called again (cached)"
    
    # Rôzne argumenty - malo by sa vypočítať znova
    result3 = expensive_function(10)
    assert result3 == 20, "Different args should compute new result"
    assert call_count[0] == 2, "Function should be called for different args"


def test_cache_result_ttl_expiration_and_clear_cache():
    """Cache should recompute after TTL expiration; clear_cache should reset state."""
    call_count = [0]

    @cache_result(ttl=0.05)
    def f(x):
        call_count[0] += 1
        return x * 3

    assert f(2) == 6
    assert f(2) == 6
    assert call_count[0] == 1, "Should be cached within TTL"

    time.sleep(0.06)
    assert f(2) == 6
    assert call_count[0] == 2, "Should recompute after TTL expiration"

    # clear_cache should force recompute even within TTL
    f.clear_cache()
    assert f(2) == 6
    assert call_count[0] == 3


def test_cache_cleanup():
    """Test cache cleanup"""
    @cache_result(ttl=1)
    def test_func(x):
        return x * 2
    
    result1 = test_func(5)
    assert result1 == 10
    
    # Počkaj, kým cache expiruje
    time.sleep(1.1)
    
    # Cleanup
    test_func.cleanup()
    
    # Nové volanie by malo vypočítať znova
    result2 = test_func(5)
    assert result2 == 10


def test_connection_pool():
    """Test connection pool"""
    pool = ConnectionPool(max_connections=3)
    
    assert pool.max_connections == 3, "Pool should have max 3 connections"
    
    stats = pool.get_stats()
    assert isinstance(stats, dict), "Pool should return stats as dict"
    
    # Test, že pool funguje
    async def test_async():
        async with pool:
            # Connection acquired
            pass
        # Connection released
    
    asyncio.run(test_async())
    
    # Po použití by mali byť štatistiky
    stats_after = pool.get_stats()
    assert isinstance(stats_after, dict), "Pool should track stats"


def test_connection_pool_context_manager():
    """Test connection pool as context manager"""
    pool = get_connection_pool()
    
    async def test_async():
        async with pool:
            # Connection acquired
            pass
        # Connection released
    
    # Test async context manager
    asyncio.run(test_async())


def test_batch_requests():
    """Test batch processing decorator"""
    call_count = [0]
    
    @batch_requests(batch_size=2, delay=0.1)
    async def async_function(x):
        call_count[0] += 1
        return x * 2
    
    async def run_test():
        # Spustiť niekoľko requestov
        tasks = [async_function(i) for i in range(5)]
        results = await asyncio.gather(*tasks)
        
        # Všetky výsledky by mali byť správne
        for i, result in enumerate(results):
            assert result == i * 2, f"Result {i} should be {i * 2}"
    
    asyncio.run(run_test())


def test_batch_requests_limits_concurrency_and_respects_delay():
    """batch_requests should process at most batch_size concurrently and delay between batches."""
    batch_size = 2
    delay = 0.15

    active = 0
    max_active = 0
    start_times = {}
    end_times = {}

    @batch_requests(batch_size=batch_size, delay=delay)
    async def work(x):
        nonlocal active, max_active
        start_times[x] = time.monotonic()
        active += 1
        max_active = max(max_active, active)
        await asyncio.sleep(0.05)
        active -= 1
        end_times[x] = time.monotonic()
        return x

    async def run_test():
        tasks = [asyncio.create_task(work(i)) for i in range(5)]
        results = await asyncio.gather(*tasks)
        assert results == [0, 1, 2, 3, 4]

        # "Batches" are sequential in this decorator; ensure we never exceed batch_size.
        assert max_active <= batch_size, f"max_active={max_active} exceeded batch_size={batch_size}"

        # Timing check (non-flaky): item 2 should not start until after batch 0-1 completes + delay.
        batch1_end = max(end_times[0], end_times[1])
        assert start_times[2] >= batch1_end + delay - 0.06, (
            f"Expected delay between batches. start_times[2]={start_times[2]:.3f}, "
            f"batch1_end={batch1_end:.3f}, delay={delay}"
        )

        # Same for item 4 (third batch) relative to completion of items 2-3.
        batch2_end = max(end_times[2], end_times[3])
        assert start_times[4] >= batch2_end + delay - 0.06, (
            f"Expected delay between batches. start_times[4]={start_times[4]:.3f}, "
            f"batch2_end={batch2_end:.3f}, delay={delay}"
        )

    asyncio.run(run_test())


def test_batch_requests_propagates_exceptions_per_call():
    """If one call raises, only that call should fail; others should still resolve."""
    @batch_requests(batch_size=3, delay=0.01)
    async def maybe_fail(x):
        await asyncio.sleep(0.01)
        if x in (2, 5):
            raise ValueError(f"bad:{x}")
        return x * 10

    async def run_test():
        tasks = [asyncio.create_task(maybe_fail(i)) for i in range(6)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        assert results[0] == 0
        assert results[1] == 10
        assert isinstance(results[2], ValueError) and str(results[2]) == "bad:2"
        assert results[3] == 30
        assert results[4] == 40
        assert isinstance(results[5], ValueError) and str(results[5]) == "bad:5"

        # Validate that awaiting the failing call raises (not returned as a value).
        try:
            await maybe_fail(2)
            assert False, "Expected ValueError to be raised for x=2"
        except ValueError as e:
            assert str(e) == "bad:2"

    asyncio.run(run_test())


def test_performance_improvement():
    """Test, že cache skutočne zlepšuje výkon"""
    call_count = [0]
    
    @cache_result(ttl=60)
    def slow_function(x):
        call_count[0] += 1
        time.sleep(0.05)  # Simulácia pomalého výpočtu
        return x * 2
    
    # Prvé volanie - pomalé
    start1 = time.time()
    result1 = slow_function(5)
    time1 = time.time() - start1
    
    # Druhé volanie - rýchle (z cache)
    start2 = time.time()
    result2 = slow_function(5)
    time2 = time.time() - start2
    
    assert result1 == result2 == 10, "Results should be the same"
    assert call_count[0] == 1, "Function should be called only once"
    assert time2 < time1, "Cached call should be faster"


if __name__ == "__main__":
    print("🧪 Testing performance optimizations...")
    print()
    
    tests = [
        ("Timing decorator", test_timing_decorator),
        ("Cache result", test_cache_result),
        ("Cache cleanup", test_cache_cleanup),
        ("Connection pool", test_connection_pool),
        ("Connection pool context", test_connection_pool_context_manager),
        ("Batch requests", test_batch_requests),
        ("Performance improvement", test_performance_improvement),
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
