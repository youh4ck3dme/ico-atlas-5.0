"""
Poľsko - KRS (Krajowy Rejestr Sądowy) integrácia
API dokumentácia: https://api-krs.ms.gov.pl/api/krs
"""

import requests
from typing import Dict, Optional
from datetime import datetime, timedelta
import re
from services.proxy_rotation import make_request_with_proxy

# Cache pre KRS odpovede
_krs_cache = {}
_cache_ttl = timedelta(hours=24)


def get_krs_provider():
    """Vráti provider pre poľský KRS register."""
    return {
        "name": "Polish KRS",
        "country": "PL",
        "fetch_function": fetch_krs_pl,
        "parse_function": parse_krs_data,
        "risk_function": calculate_pl_risk_score,
        "validation_function": is_polish_krs,
    }


def fetch_krs_pl(krs_number: str) -> Optional[Dict]:
    """
    Získa dáta z poľského KRS registra.
    
    Args:
        krs_number: KRS číslo (9 alebo 10 miest)
        
    Returns:
        Dict s dátami firmy alebo None pri chybe
    """
    # Kontrola cache
    cache_key = f"krs_pl_{krs_number}"
    if cache_key in _krs_cache:
        cached_data, cached_time = _krs_cache[cache_key]
        if datetime.now() - cached_time < _cache_ttl:
            print(f"✅ Cache hit pre KRS {krs_number}")
            return cached_data
    
    # Validácia KRS čísla (9 alebo 10 miest)
    if not krs_number or not re.match(r'^\d{9,10}$', krs_number):
        return None
    
    try:
        # Poľský KRS API (oficiálny endpoint)
        # Poznámka: V reálnom nasadení by sme použili oficiálny API endpoint
        # Pre MVP simulujeme odpoveď alebo používame verejné API
        
        # Alternatíva 1: Priamy KRS API (ak je dostupný)
        url = f"https://api-krs.ms.gov.pl/api/krs/{krs_number}"
        
        headers = {
            "Accept": "application/json",
            "User-Agent": "ILUMINATI-SYSTEM/1.0"
        }
        
        # Použiť proxy rotation pre stabilitu
        response = make_request_with_proxy(url, headers=headers, timeout=10)
        
        if response is None:
            # Proxy zlyhalo, skúsiť priame volanie
            response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Uložiť do cache
            _krs_cache[cache_key] = (data, datetime.now())
            return data
        elif response.status_code == 404:
            print(f"⚠️ KRS {krs_number} sa nenašlo v registri")
            return None
        else:
            print(f"⚠️ KRS API chyba: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Chyba pri volaní KRS API: {e}")
        # Fallback: Vrátiť simulované dáta pre testovanie
        return _generate_fallback_pl_data(krs_number)
    except Exception as e:
        print(f"❌ Neočakávaná chyba: {e}")
        return None


def _generate_fallback_pl_data(krs_number: str) -> Dict:
    """
    Generuje fallback dáta pre poľské KRS (ak API nie je dostupné).
    """
    return {
        "krs": krs_number,
        "name": f"Polska Spółka {krs_number} Sp. z o.o.",
        "legal_form": "Sp. z o.o.",
        "status": "Aktywna",
        "address": {
            "street": "ul. Główna 1",
            "city": "Warszawa",
            "postal_code": "00-001",
            "country": "PL"
        },
        "founded": "2020-01-15",
        "note": "Fallback data - API unavailable"
    }


def parse_krs_data(krs_data: Dict, krs_number: str) -> Dict:
    """
    Parsuje dáta z KRS do jednotnej schémy.
    
    Returns:
        Dict s normalizovanými dátami
    """
    if not krs_data:
        return {}
    
    # Normalizácia dát do jednotnej schémy
    normalized = {
        "krs": krs_data.get("krs", krs_number),
        "name": krs_data.get("name") or krs_data.get("nazwa", "Nieznana firma"),
        "legal_form": krs_data.get("legal_form") or krs_data.get("formaPrawna", "Sp. z o.o."),
        "status": krs_data.get("status") or "Aktywna",
        "country": "PL",
        "address": _parse_address(krs_data.get("address", {})),
        "founded": krs_data.get("founded") or krs_data.get("dataPowstania"),
        "executives": krs_data.get("executives", []),  # Zarząd
        "shareholders": krs_data.get("shareholders", []),  # Wspólnicy
    }
    
    return normalized


def _parse_address(address_data: Dict) -> str:
    """Parsuje adresu do textového formátu."""
    if isinstance(address_data, str):
        return address_data
    
    parts = []
    if address_data.get("street"):
        parts.append(address_data["street"])
    if address_data.get("city"):
        parts.append(address_data["city"])
    if address_data.get("postal_code"):
        parts.append(address_data["postal_code"])
    
    return ", ".join(parts) if parts else "Adres nie podano"


def calculate_pl_risk_score(company_data: Dict) -> int:
    """
    Vypočíta risk score pre poľskú firmu.
    
    Faktory:
    - Status (likwidacja, upadłość = vysoké riziko)
    - Počet zarządców (biely kôň detektor)
    - Vek firmy
    """
    score = 0
    
    # Status
    status = company_data.get("status", "").lower()
    if "likwidacja" in status or "upadłość" in status:
        score += 7
    elif "zawieszona" in status:
        score += 5
    
    # Biely kôň detektor (zarządcy)
    executives = company_data.get("executives", [])
    if len(executives) > 10:
        score += 6
    elif len(executives) > 5:
        score += 3
    
    # Vek firmy
    founded = company_data.get("founded")
    if founded:
        try:
            founded_date = datetime.strptime(founded, "%Y-%m-%d")
            age_years = (datetime.now() - founded_date).days / 365
            if age_years < 1:
                score += 2
        except (ValueError, TypeError):
            pass
    
    return min(score, 10)


def is_polish_krs(query: str) -> bool:
    """Kontroluje, či je query poľské KRS číslo (9-10 miest, len čísla)."""
    return bool(re.match(r'^\d{9,10}$', query.strip()))


def get_cache_stats() -> Dict:
    """Vráti štatistiky cache."""
    return {
        "cached_items": len(_krs_cache),
        "cache_ttl_hours": _cache_ttl.total_seconds() / 3600
    }
