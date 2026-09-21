"""
Performance optimization utilities pre backend
"""

import time
import functools
from typing import Callable
from collections import defaultdict
import asyncio


def timing_decorator(func: Callable) -> Callable:
    """Decorator pre meranie času vykonania funkcie"""
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start
            print(f"⏱️ {func.__name__} trvalo {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start
            print(f"❌ {func.__name__} zlyhalo po {duration:.3f}s: {e}")
            raise
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start
            print(f"⏱️ {func.__name__} trvalo {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start
            print(f"❌ {func.__name__} zlyhalo po {duration:.3f}s: {e}")
            raise
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


def cache_result(ttl: int = 3600):
    """
    Decorator pre caching výsledkov funkcie s TTL.
    
    Args:
        ttl: Time to live v sekundách
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        cache_times = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Vytvoriť cache key
            key = str(args) + str(sorted(kwargs.items()))
            
            # Skontrolovať cache
            if key in cache:
                cache_time = cache_times.get(key, 0)
                if time.time() - cache_time < ttl:
                    return cache[key]
            
            # Vypočítať výsledok
            result = func(*args, **kwargs)
            
            # Uložiť do cache
            cache[key] = result
            cache_times[key] = time.time()
            
            return result
        
        # Cleanup expired cache
        def cleanup():
            current_time = time.time()
            expired_keys = [
                k for k, t in cache_times.items()
                if current_time - t >= ttl
            ]
            for k in expired_keys:
                cache.pop(k, None)
                cache_times.pop(k, None)
        
        wrapper.cleanup = cleanup
        wrapper.clear_cache = lambda: (cache.clear(), cache_times.clear())
        
        return wrapper
    return decorator


def batch_requests(batch_size: int = 10, delay: float = 0.1):
    """
    Decorator pre batch processing requestov.
    
    Args:
        batch_size: Počet requestov v batchi
        delay: Oneskořenie medzi batchmi v sekundách
    """
    def decorator(func: Callable) -> Callable:
        # Each queued item: (args, kwargs, future)
        queue = []
        processing = False
        
        async def process_queue():
            nonlocal processing
            if processing or len(queue) == 0:
                return
            
            processing = True
            try:
                while len(queue) > 0:
                    batch = queue[:batch_size]
                    queue[:] = queue[batch_size:]
                    
                    # Spracovať batch
                    results = await asyncio.gather(
                        *(func(*args, **kwargs) for args, kwargs, _future in batch),
                        return_exceptions=True,
                    )
                    
                    # Vrátiť výsledky
                    for (_args, _kwargs, future), result in zip(batch, results):
                        if future.done():
                            continue
                        if isinstance(result, Exception):
                            future.set_exception(result)
                        else:
                            future.set_result(result)
                    
                    # Delay medzi batchmi
                    if len(queue) > 0:
                        await asyncio.sleep(delay)
            finally:
                processing = False
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Ensure the Future is bound to the currently running loop
            loop = asyncio.get_running_loop()
            future = loop.create_future()
            queue.append((args, kwargs, future))
            
            # Spustiť processing ak nie je aktívny
            if not processing:
                asyncio.create_task(process_queue())
            
            return await future
        
        return wrapper
    return decorator


class ConnectionPool:
    """Connection pool pre HTTP requests"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.semaphore = asyncio.Semaphore(max_connections)
        self.stats = defaultdict(int)
    
    async def acquire(self):
        """Získať connection z poolu"""
        await self.semaphore.acquire()
        self.stats['acquired'] += 1
    
    def release(self):
        """Uvoľniť connection"""
        self.semaphore.release()
        self.stats['released'] += 1
    
    async def __aenter__(self):
        await self.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.release()
    
    def get_stats(self):
        return dict(self.stats)


# Global connection pool
_connection_pool = ConnectionPool(max_connections=10)


def get_connection_pool() -> ConnectionPool:
    """Získať globálny connection pool"""
    return _connection_pool
