"""
Dlhové registre - Finančná správa SK/CZ
Kontrola dlhov voči daňovým úradom
"""

import requests
from typing import Dict, Optional
from datetime import datetime, timedelta
import re

# Cache pre dlhové registry
_debt_cache = {}
_cache_ttl = timedelta(hours=12)  # Kratší TTL pre dlhy (častejšie sa menia)


def search_debt_registers(identifier: str, country: str) -> Optional[Dict]:
    """
    Vyhľadá dlhy voči Finančnej správe.
    
    Args:
        identifier: IČO alebo daňové číslo
        country: "SK" alebo "CZ"
        
    Returns:
        Dict s informáciami o dlhoch alebo None
    """
    if country not in ["SK", "CZ"]:
        return None
    
    # Kontrola cache
    cache_key = f"debt_{country}_{identifier}"
    if cache_key in _debt_cache:
        cached_data, cached_time = _debt_cache[cache_key]
        if datetime.now() - cached_time < _cache_ttl:
            print(f"✅ Cache hit pre dlhové registry {country} {identifier}")
            return cached_data
    
    try:
        if country == "SK":
            return _search_sk_debt(identifier)
        elif country == "CZ":
            return _search_cz_debt(identifier)
    except Exception as e:
        print(f"⚠️ Chyba pri vyhľadávaní dlhov ({country}): {e}")
        return _generate_fallback_debt_data(identifier, country)


def _search_sk_debt(ico: str) -> Optional[Dict]:
    """
    Vyhľadá dlhy voči Finančnej správe SR.
    
    Poznámka: V reálnom nasadení by sme použili oficiálny API
    alebo web scraping z https://www.financnasprava.sk/
    """
    # Validácia IČO (8 miest)
    if not ico or len(ico) != 8 or not ico.isdigit():
        return None
    
    try:
        # Simulácia API volania
        # V produkcii: requests.get(f"https://api.financnasprava.sk/debt/{ico}")
        
        # Fallback pre MVP - simulácia
        has_debt = int(ico[-1]) % 4 == 0  # 25% šanca že má dlh
        
        if has_debt:
            total_debt = int(ico[-3:]) * 100  # Simulovaný dlh
            debt_data = {
                "has_debt": True,
                "total_debt": total_debt,
                "currency": "EUR",
                "debt_items": [
                    {
                        "type": "DPH",
                        "amount": total_debt * 0.6,
                        "due_date": "2024-12-31"
                    },
                    {
                        "type": "Daň z príjmu",
                        "amount": total_debt * 0.4,
                        "due_date": "2024-12-31"
                    }
                ],
                "last_updated": datetime.now().isoformat()
            }
        else:
            debt_data = {
                "has_debt": False,
                "total_debt": 0,
                "currency": "EUR",
                "debt_items": [],
                "last_updated": datetime.now().isoformat()
            }
        
        result = {
            "country": "SK",
            "identifier": ico,
            "data": debt_data,
            "risk_score": 8 if has_debt else 0
        }
        
        _debt_cache[f"debt_SK_{ico}"] = (result, datetime.now())
        return result
        
    except Exception as e:
        print(f"⚠️ Chyba pri SK dlhovom registri: {e}")
        return None


def _search_cz_debt(ico: str) -> Optional[Dict]:
    """
    Vyhľadá dlhy voči Finančnej správe ČR.
    
    Poznámka: V reálnom nasadení by sme použili oficiálny API
    alebo web scraping z https://www.financnisprava.cz/
    """
    # Validácia IČO (8 alebo 9 miest)
    if not ico or len(ico) not in [8, 9] or not ico.isdigit():
        return None
    
    try:
        # Simulácia API volania
        # V produkcii: requests.get(f"https://api.financnisprava.cz/debt/{ico}")
        
        # Fallback pre MVP - simulácia
        has_debt = int(ico[-1]) % 4 == 0  # 25% šanca že má dlh
        
        if has_debt:
            total_debt = int(ico[-3:]) * 100  # Simulovaný dlh
            debt_data = {
                "has_debt": True,
                "total_debt": total_debt,
                "currency": "CZK",
                "debt_items": [
                    {
                        "type": "DPH",
                        "amount": total_debt * 0.6,
                        "due_date": "2024-12-31"
                    },
                    {
                        "type": "Daň z příjmu",
                        "amount": total_debt * 0.4,
                        "due_date": "2024-12-31"
                    }
                ],
                "last_updated": datetime.now().isoformat()
            }
        else:
            debt_data = {
                "has_debt": False,
                "total_debt": 0,
                "currency": "CZK",
                "debt_items": [],
                "last_updated": datetime.now().isoformat()
            }
        
        result = {
            "country": "CZ",
            "identifier": ico,
            "data": debt_data,
            "risk_score": 8 if has_debt else 0
        }
        
        _debt_cache[f"debt_CZ_{ico}"] = (result, datetime.now())
        return result
        
    except Exception as e:
        print(f"⚠️ Chyba pri CZ dlhovom registri: {e}")
        return None


def _generate_fallback_debt_data(identifier: str, country: str) -> Dict:
    """Generuje fallback dáta pre dlhové registry"""
    return {
        "country": country,
        "identifier": identifier,
        "data": {
            "has_debt": False,
            "total_debt": 0,
            "currency": "EUR" if country == "SK" else "CZK",
            "debt_items": [],
            "last_updated": datetime.now().isoformat()
        },
        "risk_score": 0
    }


def has_debt(identifier: str, country: str) -> bool:
    """
    Jednoduchá kontrola, či má firma dlh.
    
    Returns:
        True ak má dlh, False inak
    """
    debt_result = search_debt_registers(identifier, country)
    if not debt_result:
        return False
    
    return debt_result.get("data", {}).get("has_debt", False)

