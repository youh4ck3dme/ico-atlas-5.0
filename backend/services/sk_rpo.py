"""
Slovensko.Digital Ekosystém - RPO (Register právnych osôb) integrácia
API dokumentácia: https://ekosystem.slovensko.digital/api-docs
"""

from datetime import datetime, timedelta
from typing import Dict, Optional

import requests

# Cache pre RPO odpovede (in-memory, neskôr Redis)
_rpo_cache = {}
_cache_ttl = timedelta(hours=24)  # 24 hodín TTL


def fetch_rpo_sk(ico: str) -> Optional[Dict]:
    """
    Získa dáta z RPO cez Slovensko.Digital Ekosystém API.

    Args:
        ico: 8-miestne slovenské IČO

    Returns:
        Dict s dátami firmy alebo None pri chybe
    """
    # Kontrola cache
    cache_key = f"rpo_sk_{ico}"
    if cache_key in _rpo_cache:
        cached_data, cached_time = _rpo_cache[cache_key]
        if datetime.now() - cached_time < _cache_ttl:
            print(f"✅ Cache hit pre IČO {ico}")
            return cached_data

    # Validácia IČO (8 miest)
    if not ico or len(ico) != 8 or not ico.isdigit():
        return None

    try:
        # Slovensko.Digital Ekosystém RPO API
        # Poznámka: V reálnom nasadení by sme použili oficiálny API endpoint
        # Pre MVP simulujeme odpoveď alebo používame verejné API

        # Alternatíva 1: Priamy RPO API (ak je dostupný)
        url = f"https://rpo.slovensko.digital/api/subject/{ico}"

        # Alternatíva 2: Finančná správa SR API (ak je dostupný)
        # url = f"https://www.financnasprava.sk/api/subject/{ico}"

        headers = {"Accept": "application/json", "User-Agent": "ILUMINATI-SYSTEM/1.0"}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            # Uložiť do cache
            _rpo_cache[cache_key] = (data, datetime.now())
            return data
        elif response.status_code == 404:
            print(f"⚠️ IČO {ico} sa nenašlo v RPO")
            return None
        else:
            print(f"⚠️ RPO API chyba: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Chyba pri volaní RPO API: {e}")
        # Nevrátiť fallback dáta - necháme ORSR provider, aby sa pokúsil o live scraping
        return None
    except Exception as e:
        print(f"❌ Neočakávaná chyba: {e}")
        return None


def _generate_fallback_sk_data(ico: str) -> Dict:
    """
    Generuje fallback dáta pre slovenské IČO (ak API nie je dostupné).
    V produkcii by toto nemalo byť použité.
    """
    return {
        "ico": ico,
        "name": f"Slovenská Spoločnosť {ico} s.r.o.",
        "legal_form": "s.r.o.",
        "status": "Aktívna",
        "address": {
            "street": "Hlavná ulica 1",
            "city": "Bratislava",
            "postal_code": "811 01",
            "country": "SK",
        },
        "founded": "2020-01-15",
        "note": "Fallback dáta - API nedostupné",
    }


def parse_rpo_data(rpo_data: Dict, ico: str) -> Dict:
    """
    Parsuje dáta z RPO do jednotnej schémy.

    Returns:
        Dict s normalizovanými dátami
    """
    if not rpo_data:
        return {}

    # Normalizácia dát do jednotnej schémy
    normalized = {
        "ico": rpo_data.get("ico", ico),
        "name": rpo_data.get("name") or rpo_data.get("obchodneMeno", "Neznáma firma"),
        "legal_form": rpo_data.get("legal_form")
        or rpo_data.get("pravnaForma", "s.r.o."),
        "status": rpo_data.get("status") or rpo_data.get("stav", "Aktívna"),
        "country": "SK",
        "address": _parse_address(rpo_data.get("address", {})),
        "founded": rpo_data.get("founded") or rpo_data.get("datumVzniku"),
        "executives": rpo_data.get("executives", []),  # Konatelia
        "shareholders": rpo_data.get("shareholders", []),  # Spoločníci
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

    return ", ".join(parts) if parts else "Adresa neuvedená"


def calculate_sk_risk_score(company_data: Dict) -> int:
    """
    Vypočíta risk score pre slovenskú firmu.

    Faktory:
    - Status (likvidácia, konkurz = vysoké riziko)
    - Počet konateľov (biely kôň detektor)
    - Adresa (virtual seat = stredné riziko)
    - Vek firmy (nové firmy = vyššie riziko)
    """
    score = 0

    # Status
    status = company_data.get("status", "").lower()
    if "likvidácia" in status or "konkurz" in status:
        score += 7
    elif "zrušená" in status:
        score += 5

    # Biely kôň detektor (konatelia)
    executives = company_data.get("executives", [])
    if len(executives) > 10:  # Viac ako 10 firiem
        score += 6
    elif len(executives) > 5:
        score += 3

    # Virtual seat (adresa s viacerými firmami)
    address = company_data.get("address", "")
    if isinstance(address, str) and ("virtual" in address.lower() or "52" in address):
        score += 3

    # Vek firmy (ak je nová)
    founded = company_data.get("founded")
    if founded:
        try:
            founded_date = datetime.strptime(founded, "%Y-%m-%d")
            age_years = (datetime.now() - founded_date).days / 365
            if age_years < 1:  # Menej ako rok
                score += 2
        except (ValueError, TypeError):
            pass

    return min(score, 10)  # Max 10


def is_slovak_ico(query: str) -> bool:
    """Kontroluje, či je query slovenské IČO (8 miest, len čísla)."""
    import re

    return bool(re.match(r"^\d{8}$", query.strip()))


def get_cache_stats() -> Dict:
    """Vráti štatistiky cache."""
    return {
        "cached_items": len(_rpo_cache),
        "cache_ttl_hours": _cache_ttl.total_seconds() / 3600,
    }


def clear_cache():
    """Vyčistí cache (pre testovanie)."""
    global _rpo_cache
    _rpo_cache = {}
