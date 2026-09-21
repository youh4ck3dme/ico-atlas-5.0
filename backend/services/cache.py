"""
Hybrid Cache Service pre ILUMINATI SYSTEM.
Implementuje dvojúrovňovú cache:
L1: In-memory (vysoká rýchlosť, krátka expirácia)
L2: Redis (perzistencia, dlhšia expirácia)
"""

import hashlib
import json
import logging
import random
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

# Import Redis cache (ak je dostupný)
try:
    from services.redis_cache import (
        get_redis_client,
        redis_get,
        redis_set,
        redis_delete,
    )
    REDIS_AVAILABLE = True
except (ImportError, Exception):
    REDIS_AVAILABLE = False
    redis_get = redis_set = redis_delete = None

class TieredCache:
    def __init__(self, default_ttl_hours: int = 24, l1_ttl_minutes: int = 60, l1_max_size: int = 1000):
        self._l1_cache: OrderedDict[str, Tuple[Any, datetime]] = OrderedDict()
        self._l1_max_size = l1_max_size
        self._default_ttl = timedelta(hours=default_ttl_hours)
        self._l1_ttl = timedelta(minutes=l1_ttl_minutes)
        self._redis_enabled = REDIS_AVAILABLE
        self._jitter_range = (0.9, 1.1)  # 10% jitter
        
    def _is_redis_active(self) -> bool:
        """Dynamicky kontroluje stav Redis klienta."""
        if not self._redis_enabled:
            return False
        return get_redis_client() is not None

    def get_cache_key(self, query: str, source: str = "default") -> str:
        """Generuje MD5 hash ako kľúč."""
        key_string = f"{source}:{query}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """
        Získa hodnotu z cache (L1 -> L2).
        """
        now = datetime.now()

        # 1. Skúsiť L1 (Memory)
        if key in self._l1_cache:
            value, expiry = self._l1_cache[key]
            if now < expiry:
                # Move to end (most recently used)
                self._l1_cache.move_to_end(key)
                return value
            else:
                del self._l1_cache[key]

        # 2. Skúsiť L2 (Redis)
        if self._is_redis_active():
            value = redis_get(key)
            if value is not None:
                # Refresh L1 pri načítaní z L2
                self._l1_cache[key] = (value, now + self._l1_ttl)
                return value

        return None

    def set(self, key: str, value: Any, ttl: Optional[timedelta] = None) -> None:
        """
        Uloží hodnotu do cache (L1 aj L2).
        """
        if ttl is None:
            ttl = self._default_ttl

        now = datetime.now()
        
        # Uložiť do L1 (Memory) - s LRU limitom
        if key in self._l1_cache:
            self._l1_cache.move_to_end(key)
        
        l1_expiry = now + min(ttl, self._l1_ttl)
        self._l1_cache[key] = (value, l1_expiry)
        
        # Evict oldest if over limit
        if len(self._l1_cache) > self._l1_max_size:
            self._l1_cache.popitem(last=False)

        # Uložiť do L2 (Redis) s jitterom
        if self._is_redis_active():
            # Apply jitter to TTL for Redis to prevent stampedes
            jitter = random.uniform(*self._jitter_range)
            jittered_ttl_seconds = int(ttl.total_seconds() * jitter)
            redis_set(key, value, jittered_ttl_seconds)

    def delete(self, key: str) -> None:
        """Vymaže kľúč z oboch úrovní."""
        if key in self._l1_cache:
            del self._l1_cache[key]
            
        if self._is_redis_active():
            redis_delete(key)

    def clear(self) -> None:
        """Vyčistí celú lokálnu cache."""
        self._l1_cache = {}

    def get_stats(self) -> Dict:
        """Vráti štatistiky hybridnej cache."""
        now = datetime.now()
        
        # Cleanup expirovaných v L1 pri volaní stats
        keys_to_del = [k for k, (_, exp) in self._l1_cache.items() if now > exp]
        for k in keys_to_del:
            del self._l1_cache[k]

        stats = {
            "mode": "tiered",
            "l1_items": len(self._l1_cache),
            "redis_available": REDIS_AVAILABLE,
            "redis_active": self._is_redis_active(),
        }

        if stats["redis_active"]:
            try:
                from services.redis_cache import redis_get_stats
                stats["l2_stats"] = redis_get_stats()
            except Exception as e:
                stats["l2_stats"] = {"error": str(e)}

        return stats

# Singleton instancia pre celú aplikáciu
_instance = TieredCache()

# Exporty funkcií pre zachovanie spätnej kompatibility
def get(key: str) -> Optional[Any]: return _instance.get(key)
def get_cache(key: str) -> Optional[Any]: return _instance.get(key)
def set(key: str, value: Any, ttl: Optional[timedelta] = None) -> None: _instance.set(key, value, ttl)
def set_cache(key: str, value: Any, ttl: Optional[timedelta] = None) -> None: _instance.set(key, value, ttl)
def delete(key: str) -> None: _instance.delete(key)
def clear() -> None: _instance.clear()
def get_stats() -> Dict: return _instance.get_stats()
def get_cache_key(query: str, source: str = "default") -> str: return _instance.get_cache_key(query, source)
