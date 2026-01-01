"""
Redis Cache Service pre ILUMINATI SYSTEM
Migrácia z in-memory cache na Redis pre lepšiu škálovateľnosť
"""

import json
import logging
import os
from typing import Any, Optional

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    import logging
    logging.getLogger("iluminati").warning("Redis library not found. Install it with 'pip install redis'")
    REDIS_AVAILABLE = False
    redis = None

# Redis konfigurácia
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_URL = os.getenv("REDIS_URL", None)

# Redis client (singleton)
_redis_client: Optional[Any] = None
_redis_initialized = False


def get_redis_client():
    """Získa Redis client (singleton pattern)"""
    global _redis_client, _redis_initialized
    
    if not REDIS_AVAILABLE:
        return None
    
    if _redis_client is None and not _redis_initialized:
        _redis_initialized = True
        try:
            if REDIS_URL:
                _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
            else:
                _redis_client = redis.Redis(
                    host=REDIS_HOST,
                    port=REDIS_PORT,
                    db=REDIS_DB,
                    password=REDIS_PASSWORD,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2,
                )
            # Test connection
            _redis_client.ping()
            logging.getLogger("iluminati").info(f"✅ Redis cache pripojený na {REDIS_HOST}:{REDIS_PORT}")
        except Exception as e:
            logging.getLogger("iluminati").warning(f"⚠️ Redis nie je dostupný na {REDIS_HOST}:{REDIS_PORT}: {e}")
            logging.getLogger("iluminati").info("   Používa sa in-memory cache fallback (L1)")
            _redis_client = None
    
    return _redis_client


def redis_get(key: str) -> Optional[Any]:
    """
    Získa hodnotu z Redis cache.
    
    Args:
        key: Cache kľúč
        
    Returns:
        Hodnota alebo None ak neexistuje
    """
    client = get_redis_client()
    if not client:
        return None
    
    try:
        value = client.get(key)
        if value is None:
            return None
        
        # Pokúsiť sa deserializovať JSON
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    except Exception as e:
        print(f"⚠️ Redis get error: {e}")
        return None


def redis_set(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Uloží hodnotu do Redis cache.
    
    Args:
        key: Cache kľúč
        value: Hodnota na uloženie
        ttl: Time to live v sekundách (default: 1 hodina)
        
    Returns:
        True ak úspešné, False inak
    """
    client = get_redis_client()
    if not client:
        return False
    
    try:
        # Serializovať JSON ak je to dict/list
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        
        client.setex(key, ttl, value)
        return True
    except Exception as e:
        print(f"⚠️ Redis set error: {e}")
        return False


def redis_delete(key: str) -> bool:
    """
    Vymaže kľúč z Redis cache.
    
    Args:
        key: Cache kľúč
        
    Returns:
        True ak úspešné, False inak
    """
    client = get_redis_client()
    if not client:
        return False
    
    try:
        client.delete(key)
        return True
    except Exception as e:
        print(f"⚠️ Redis delete error: {e}")
        return False


def redis_exists(key: str) -> bool:
    """
    Skontroluje, či kľúč existuje v Redis cache.
    
    Args:
        key: Cache kľúč
        
    Returns:
        True ak existuje, False inak
    """
    client = get_redis_client()
    if not client:
        return False
    
    try:
        return bool(client.exists(key))
    except Exception as e:
        print(f"⚠️ Redis exists error: {e}")
        return False


def redis_clear_pattern(pattern: str) -> int:
    """
    Vymaže všetky kľúče zodpovedajúce patternu.
    
    Args:
        pattern: Redis pattern (napr. "icoatlas:*")
        
    Returns:
        Počet vymazaných kľúčov
    """
    client = get_redis_client()
    if not client:
        return 0
    
    try:
        keys = client.keys(pattern)
        if keys:
            return client.delete(*keys)
        return 0
    except Exception as e:
        print(f"⚠️ Redis clear pattern error: {e}")
        return 0


def redis_get_stats() -> dict:
    """
    Získa štatistiky Redis cache.
    
    Returns:
        Dict so štatistikami
    """
    client = get_redis_client()
    if not client:
        return {
            "available": False,
            "connected": False,
            "total_keys": 0,
            "memory_used": 0,
        }
    
    try:
        info = client.info()
        keys = client.dbsize()
        
        return {
            "available": True,
            "connected": True,
            "total_keys": keys,
            "memory_used": info.get("used_memory_human", "0B"),
            "memory_used_bytes": info.get("used_memory", 0),
            "hits": info.get("keyspace_hits", 0),
            "misses": info.get("keyspace_misses", 0),
            "hit_rate": (
                info.get("keyspace_hits", 0) / 
                (info.get("keyspace_hits", 0) + info.get("keyspace_misses", 1))
            ) * 100,
        }
    except Exception as e:
        print(f"⚠️ Redis stats error: {e}")
        return {
            "available": True,
            "connected": False,
            "error": str(e),
        }

