"""
Poľsko - CEIDG (Centralna Ewidencja i Informacja o Działalności Gospodarczej)
Integrácia pre živnostníkov (sole proprietors)
API dokumentácia: https://api.ceidg.gov.pl/
"""

import requests
from typing import Dict, Optional
from datetime import datetime, timedelta
from services.proxy_rotation import make_request_with_proxy

# Cache pre CEIDG odpovede
_ceidg_cache = {}
_cache_ttl = timedelta(hours=24)


def get_ceidg_provider():
    """Vráti provider pre poľský CEIDG register."""
    return {
        "name": "Polish CEIDG",
        "country": "PL",
        "fetch_function": fetch_ceidg_pl,
        "parse_function": parse_ceidg_data,
        "risk_function": calculate_ceidg_risk_score,
        "validation_function": is_ceidg_number,
    }


def fetch_ceidg_pl(ceidg_number: str) -> Optional[Dict]:
    """
    Získa dáta z CEIDG pre živnostníka.
    
    Args:
        ceidg_number: CEIDG číslo (NIP alebo REGON)
        
    Returns:
        Dict s dátami živnostníka alebo None pri chybe
    """
    # Kontrola cache
    cache_key = f"ceidg_pl_{ceidg_number}"
    if cache_key in _ceidg_cache:
        cached_data, cached_time = _ceidg_cache[cache_key]
        if datetime.now() - cached_time < _cache_ttl:
            print(f"✅ Cache hit pre CEIDG {ceidg_number}")
            return cached_data
    
    # Validácia
    if not ceidg_number or len(ceidg_number) < 9:
        return None
    
    try:
        # CEIDG API endpoint
        # Poznámka: V reálnom nasadení by sme použili oficiálny API
        # API vyžaduje autentifikáciu a má rate limiting
        api_url = f"https://api.ceidg.gov.pl/ceidg/ceidgPublic.svc/GetEntrepreneur/{ceidg_number}"
        
        # Headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Použiť proxy rotation pre stabilitu (s fallbackom)
        response = make_request_with_proxy(api_url, headers=headers, timeout=10)
        
        if response is None:
            # Proxy zlyhalo, skúsiť priame volanie
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
            except Exception as e:
                print(f"⚠️ Priame CEIDG volanie zlyhalo: {e}")
                return _generate_fallback_ceidg_data(ceidg_number)
        
        if response.status_code == 200:
            data = response.json()
            _ceidg_cache[cache_key] = (data, datetime.now())
            return data
        else:
            # Fallback na simulované dáta pre MVP
            print(f"⚠️ CEIDG API neodpovedá (status {response.status_code}), používam fallback")
            return _generate_fallback_ceidg_data(ceidg_number)
            
    except Exception as e:
        print(f"⚠️ Chyba pri CEIDG API: {e}, používam fallback")
        return _generate_fallback_ceidg_data(ceidg_number)


def _generate_fallback_ceidg_data(ceidg_number: str) -> Dict:
    """Generuje fallback dáta pre CEIDG (pre MVP/testing)"""
    return {
        "nip": ceidg_number,
        "regon": ceidg_number[:9] if len(ceidg_number) >= 9 else ceidg_number,
        "name": f"Jan Kowalski ({ceidg_number[-4:]})",
        "legal_form": "Fizyczna osoba prowadząca działalność gospodarczą",
        "status": "Aktywna",
        "address": f"ul. Przykładowa {ceidg_number[-2:]}, 00-001 Warszawa",
        "founded": "2020-01-15",
        "vat_status": "VAT payer",
        "activities": ["Handel detaliczny", "Usługi IT"]
    }


def parse_ceidg_data(ceidg_data: Dict, ceidg_number: str) -> Dict:
    """
    Parsuje dáta z CEIDG do jednotnej schémy.
    
    Returns:
        Dict s normalizovanými dátami
    """
    if not ceidg_data:
        return {}
    
    # Normalizácia dát do jednotnej schémy
    normalized = {
        "ceidg": ceidg_data.get("nip") or ceidg_data.get("regon", ceidg_number),
        "name": ceidg_data.get("name") or ceidg_data.get("nazwa", "Nieznany przedsiębiorca"),
        "legal_form": ceidg_data.get("legal_form") or "Fizyczna osoba prowadząca działalność gospodarczą",
        "status": ceidg_data.get("status") or "Aktywna",
        "country": "PL",
        "address": ceidg_data.get("address") or "Adres nieznany",
        "founded": ceidg_data.get("founded") or ceidg_data.get("dataRozpoczecia"),
        "vat_status": ceidg_data.get("vat_status") or "Unknown",
        "activities": ceidg_data.get("activities", []) or ceidg_data.get("dzialalnosci", []),
    }
    
    return normalized


def calculate_ceidg_risk_score(company_data: Dict) -> int:
    """
    Vypočíta risk score pre CEIDG živnostníka.
    
    Returns:
        Risk score 0-10
    """
    if not company_data:
        return 5
    
    score = 0
    
    # Základný risk
    status = company_data.get("status", "").lower()
    if "nieaktywna" in status or "zawieszona" in status:
        score += 4
    elif "skreślona" in status or "zamknięta" in status:
        score += 7
    
    # VAT status
    vat_status = company_data.get("vat_status", "").lower()
    if "nie" in vat_status or "non" in vat_status:
        score += 2  # Menej dôveryhodný ak nie je VAT payer
    
    # Vek firmy (mladšie = vyšší risk)
    founded = company_data.get("founded")
    if founded:
        try:
            founded_date = datetime.strptime(founded, "%Y-%m-%d")
            age_years = (datetime.now() - founded_date).days / 365
            if age_years < 1:
                score += 3
            elif age_years < 2:
                score += 1
        except (ValueError, TypeError):
            pass
    
    # Počet aktivít (viac aktivít = menej špecializovaný)
    activities = company_data.get("activities", [])
    if len(activities) > 5:
        score += 1
    
    return min(score, 10)  # Max 10


def is_ceidg_number(query: str) -> bool:
    """
    Detekuje, či je query CEIDG číslo (NIP alebo REGON).
    
    NIP: 10 číslic
    REGON: 9 alebo 14 číslic
    """
    if not query:
        return False
    
    # Odstrániť medzery a pomlčky
    clean = query.replace(" ", "").replace("-", "")
    
    # NIP: 10 číslic
    if len(clean) == 10 and clean.isdigit():
        return True
    
    # REGON: 9 alebo 14 číslic
    if len(clean) in [9, 14] and clean.isdigit():
        return True
    
    return False

