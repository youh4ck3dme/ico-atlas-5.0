"""
RegionResolver - Geolokácia z PSČ
Mapping PSČ → Kraj/Okres pre Slovensko
Načítava dáta z CSV súboru alebo používa fallback mapping
"""

import csv
import os
from typing import Dict, Optional

# Cesta k CSV súboru
_POSTAL_CODE_CSV = os.path.join(
    os.path.dirname(__file__), "..", "data", "postal_codes_sk.csv"
)

# Fallback mapping (ak CSV nie je dostupný)
_FALLBACK_POSTAL_CODE_REGIONS: Dict[str, Dict[str, str]] = {
    # Bratislavský kraj
    "81101": {"kraj": "Bratislavský", "okres": "Bratislava I"},
    "81102": {"kraj": "Bratislavský", "okres": "Bratislava I"},
    "81103": {"kraj": "Bratislavský", "okres": "Bratislava I"},
    "81104": {"kraj": "Bratislavský", "okres": "Bratislava I"},
    "81105": {"kraj": "Bratislavský", "okres": "Bratislava I"},
    "81106": {"kraj": "Bratislavský", "okres": "Bratislava I"},
    "81107": {"kraj": "Bratislavský", "okres": "Bratislava I"},
    "81108": {"kraj": "Bratislavský", "okres": "Bratislava I"},
    "81109": {"kraj": "Bratislavský", "okres": "Bratislava I"},
    "82101": {"kraj": "Bratislavský", "okres": "Bratislava II"},
    "82102": {"kraj": "Bratislavský", "okres": "Bratislava II"},
    "82103": {"kraj": "Bratislavský", "okres": "Bratislava II"},
    "82104": {"kraj": "Bratislavský", "okres": "Bratislava II"},
    "82105": {"kraj": "Bratislavský", "okres": "Bratislava II"},
    "83101": {"kraj": "Bratislavský", "okres": "Bratislava III"},
    "83102": {"kraj": "Bratislavský", "okres": "Bratislava III"},
    "83103": {"kraj": "Bratislavský", "okres": "Bratislava III"},
    "83104": {"kraj": "Bratislavský", "okres": "Bratislava III"},
    "83105": {"kraj": "Bratislavský", "okres": "Bratislava III"},
    "84101": {"kraj": "Bratislavský", "okres": "Bratislava IV"},
    "84102": {"kraj": "Bratislavský", "okres": "Bratislava IV"},
    "84103": {"kraj": "Bratislavský", "okres": "Bratislava IV"},
    "84104": {"kraj": "Bratislavský", "okres": "Bratislava IV"},
    "84105": {"kraj": "Bratislavský", "okres": "Bratislava IV"},
    "85101": {"kraj": "Bratislavský", "okres": "Bratislava V"},
    "85102": {"kraj": "Bratislavský", "okres": "Bratislava V"},
    "85103": {"kraj": "Bratislavský", "okres": "Bratislava V"},
    "85104": {"kraj": "Bratislavský", "okres": "Bratislava V"},
    "85105": {"kraj": "Bratislavský", "okres": "Bratislava V"},
    # Trnavský kraj
    "91701": {"kraj": "Trnavský", "okres": "Trnava"},
    "91702": {"kraj": "Trnavský", "okres": "Trnava"},
    # Trenčiansky kraj
    "91101": {"kraj": "Trenčiansky", "okres": "Trenčín"},
    # Žilinský kraj
    "01001": {"kraj": "Žilinský", "okres": "Žilina"},
    "01002": {"kraj": "Žilinský", "okres": "Žilina"},
    # Banskobystrický kraj
    "97401": {"kraj": "Banskobystrický", "okres": "Banská Bystrica"},
    # Košický kraj
    "04001": {"kraj": "Košický", "okres": "Košice I"},
    "04002": {"kraj": "Košický", "okres": "Košice I"},
    "04011": {"kraj": "Košický", "okres": "Košice II"},
    "04012": {"kraj": "Košický", "okres": "Košice II"},
    "04013": {"kraj": "Košický", "okres": "Košice II"},
    "04022": {"kraj": "Košický", "okres": "Košice III"},
    "04023": {"kraj": "Košický", "okres": "Košice III"},
    # Prešovský kraj
    "08001": {"kraj": "Prešovský", "okres": "Prešov"},
    # Nitriansky kraj
    "94901": {"kraj": "Nitriansky", "okres": "Nitra"},
}


def _load_postal_codes_from_csv() -> Dict[str, Dict[str, str]]:
    """
    Načíta mapping PSČ → Kraj/Okres z CSV súboru.

    Returns:
        Dict s mappingom alebo fallback mapping ak CSV nie je dostupný
    """
    mapping = {}

    if not os.path.exists(_POSTAL_CODE_CSV):
        print(f"⚠️ CSV súbor {_POSTAL_CODE_CSV} neexistuje, používam fallback mapping")
        return _FALLBACK_POSTAL_CODE_REGIONS

    try:
        with open(_POSTAL_CODE_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Detekovať názvy stĺpcov (podporovať rôzne formáty)
            fieldnames = reader.fieldnames or []

            # Nájsť správne stĺpce
            postal_col = None
            kraj_col = None
            okres_col = None

            for field in fieldnames:
                field_lower = field.lower()
                if (
                    "postal" in field_lower
                    or "psc" in field_lower
                    or "code" in field_lower
                ):
                    postal_col = field
                if "kraj" in field_lower or "region" in field_lower:
                    kraj_col = field
                if "okres" in field_lower or "district" in field_lower:
                    okres_col = field

            if not postal_col:
                print(f"⚠️ CSV neobsahuje stĺpec pre PSČ, používam fallback mapping")
                return _FALLBACK_POSTAL_CODE_REGIONS

            for row in reader:
                postal_code = row.get(postal_col, "").strip()
                if postal_code:
                    # Normalizovať PSČ (odstrániť medzery)
                    postal_code = postal_code.replace(" ", "").replace("-", "")

                    kraj = row.get(kraj_col or "kraj", "").strip() if kraj_col else ""
                    okres = (
                        row.get(okres_col or "okres", "").strip() if okres_col else ""
                    )

                    # Normalizovať názvy (odstrániť "kraj" ak je súčasťou názvu)
                    if kraj and kraj.endswith(" kraj"):
                        kraj = kraj[:-5].strip()

                    mapping[postal_code] = {
                        "kraj": kraj,
                        "okres": okres,
                    }

        if mapping:
            print(f"✅ Načítaných {len(mapping)} PSČ z CSV")
            return mapping
        else:
            print(f"⚠️ CSV je prázdny, používam fallback mapping")
            return _FALLBACK_POSTAL_CODE_REGIONS

    except Exception as e:
        print(f"❌ Chyba pri načítaní CSV: {e}, používam fallback mapping")
        return _FALLBACK_POSTAL_CODE_REGIONS


# Načítať mapping pri importe
_POSTAL_CODE_REGIONS = _load_postal_codes_from_csv()


def resolve_region(postal_code: str) -> Optional[Dict[str, str]]:
    """
    Vyrieši kraj a okres z PSČ.

    Args:
        postal_code: PSČ (môže byť s medzerou alebo bez)

    Returns:
        Dict s 'kraj' a 'okres' alebo None ak sa nenašlo
    """
    if not postal_code:
        return None

    # Normalizovať PSČ (odstrániť medzery)
    postal_clean = postal_code.replace(" ", "").strip()

    # Skúsiť presné zhodu
    if postal_clean in _POSTAL_CODE_REGIONS:
        return _POSTAL_CODE_REGIONS[postal_clean].copy()

    # Skúsiť prvých 5 číslic (pre PSČ typu "811 01")
    if len(postal_clean) >= 5:
        postal_5 = postal_clean[:5]
        if postal_5 in _POSTAL_CODE_REGIONS:
            return _POSTAL_CODE_REGIONS[postal_5].copy()

    # Skúsiť prvých 3 číslice (pre okres)
    if len(postal_clean) >= 3:
        postal_3 = postal_clean[:3]
        # Nájsť najbližší match
        for code, region in _POSTAL_CODE_REGIONS.items():
            if code.startswith(postal_3):
                return region.copy()

    return None


def enrich_address_with_region(
    address: str, postal_code: Optional[str] = None
) -> Dict[str, Optional[str]]:
    """
    Obohati adresu o kraj a okres z PSČ.

    Args:
        address: Textová adresa
        postal_code: PSČ (ak nie je v adrese)

    Returns:
        Dict s 'address', 'postal_code', 'city', 'region', 'district'
    """
    # Extrahovať PSČ z adresy ak nie je poskytnuté
    if not postal_code and address:
        import re

        postal_match = re.search(r"\b\d{5}\b", address)
        if postal_match:
            postal_code = postal_match.group()

    result = {
        "address": address,
        "postal_code": postal_code,
        "city": None,
        "region": None,
        "district": None,
    }

    if postal_code:
        region_data = resolve_region(postal_code)
        if region_data:
            result["region"] = region_data.get("kraj")
            result["district"] = region_data.get("okres")

    # Extrahovať mesto z adresy (posledné slovo pred PSČ alebo po PSČ)
    if address:
        import re

        # Odstrániť PSČ a extrahovať mesto
        address_clean = re.sub(r"\b\d{5}\b", "", address)
        parts = [p.strip() for p in address_clean.split(",") if p.strip()]
        if parts:
            result["city"] = parts[-1] if parts else None

    return result
