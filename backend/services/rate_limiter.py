"""
Rate Limiting Service pre ILUMINATI SYSTEM
Implementuje Token Bucket algoritmus
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from collections import defaultdict
import time

# Token Bucket pre každého klienta
_buckets: Dict[str, Dict] = defaultdict(lambda: {
    'tokens': 10,  # Počiatočný počet tokenov
    'last_refill': datetime.now(),
    'capacity': 10,  # Maximálna kapacita
    'refill_rate': 1.0,  # Tokenov za sekundu
})

# Konfigurácia pre rôzne tiery
TIER_CONFIGS = {
    'free': {
        'capacity': 10,
        'refill_rate': 0.5,  # 0.5 tokenu za sekundu = 30 requestov za minútu
    },
    'pro': {
        'capacity': 50,
        'refill_rate': 2.0,  # 2 tokeny za sekundu = 120 requestov za minútu
    },
    'enterprise': {
        'capacity': 200,
        'refill_rate': 10.0,  # 10 tokenov za sekundu = 600 requestov za minútu
    },
}

# Default tier
DEFAULT_TIER = 'free'


def refill_tokens(client_id: str, tier: str = DEFAULT_TIER) -> None:
    """
    Doplní tokeny do bucketu podľa refill rate.
    """
    if client_id not in _buckets:
        config = TIER_CONFIGS.get(tier, TIER_CONFIGS[DEFAULT_TIER])
        _buckets[client_id] = {
            'tokens': config['capacity'],
            'last_refill': datetime.now(),
            'capacity': config['capacity'],
            'refill_rate': config['refill_rate'],
        }
        return
    
    bucket = _buckets[client_id]
    now = datetime.now()
    elapsed = (now - bucket['last_refill']).total_seconds()
    
    # Vypočítať koľko tokenov pridať
    tokens_to_add = elapsed * bucket['refill_rate']
    
    # Pridať tokeny (max do capacity)
    bucket['tokens'] = min(bucket['capacity'], bucket['tokens'] + tokens_to_add)
    bucket['last_refill'] = now


def is_allowed(client_id: str, tokens_required: int = 1, tier: str = DEFAULT_TIER) -> tuple[bool, Optional[Dict]]:
    """
    Skontroluje, či má klient dostatok tokenov.
    
    Args:
        client_id: Identifikátor klienta (IP, API key, atď.)
        tokens_required: Počet tokenov potrebných pre request
        tier: Tier klienta (free/pro/enterprise)
        
    Returns:
        Tuple (is_allowed, info_dict)
        info_dict obsahuje: allowed, remaining, reset_after
    """
    refill_tokens(client_id, tier)
    bucket = _buckets[client_id]
    
    if bucket['tokens'] >= tokens_required:
        bucket['tokens'] -= tokens_required
        return True, {
            'allowed': True,
            'remaining': int(bucket['tokens']),
            'reset_after': int((bucket['capacity'] - bucket['tokens']) / bucket['refill_rate']),
        }
    else:
        return False, {
            'allowed': False,
            'remaining': int(bucket['tokens']),
            'reset_after': int((bucket['capacity'] - bucket['tokens']) / bucket['refill_rate']),
            'retry_after': int((tokens_required - bucket['tokens']) / bucket['refill_rate']),
        }


def get_client_id(request) -> str:
    """
    Extrahuje client_id z FastAPI requestu.
    Používa IP adresu alebo API key header.
    """
    # Skúsiť API key header
    api_key = request.headers.get('X-API-Key')
    if api_key:
        return f"api_key:{api_key}"
    
    # Inak použiť IP adresu
    client_ip = request.client.host if request.client else 'unknown'
    return f"ip:{client_ip}"


def get_stats() -> Dict:
    """
    Vráti štatistiky rate limitera.
    """
    return {
        'active_buckets': len(_buckets),
        'tiers': TIER_CONFIGS,
        'default_tier': DEFAULT_TIER,
    }


def reset_bucket(client_id: str) -> None:
    """
    Resetuje bucket pre klienta (pre testing alebo admin).
    """
    if client_id in _buckets:
        del _buckets[client_id]


def cleanup_old_buckets(max_age_hours: int = 24) -> int:
    """
    Vymaže staré buckety (neaktívne viac ako max_age_hours).
    Vráti počet vymazaných bucketov.
    """
    now = datetime.now()
    to_delete = []
    
    for client_id, bucket in _buckets.items():
        age = (now - bucket['last_refill']).total_seconds() / 3600
        if age > max_age_hours:
            to_delete.append(client_id)
    
    for client_id in to_delete:
        del _buckets[client_id]
    
    return len(to_delete)

