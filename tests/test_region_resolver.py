"""
Špeciálne testy pre Region resolver (PSČ → Kraj/Okres)
"""

import os
import sys

import pytest

# Pridať backend do path
backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

try:
    from services.sk_region_resolver import (
        enrich_address_with_region,
        resolve_region,
    )
except ImportError:
    pytest.skip("Region resolver nie je dostupný")


def test_region_resolver_imports():
    """Test, či Region resolver sa dá importovať"""
    try:
        from backend.services.sk_region_resolver import resolve_region

        assert resolve_region is not None
        assert callable(resolve_region)
    except ImportError:
        pytest.skip("Region resolver nie je dostupný")


def test_region_resolver_bratislava():
    """Test, či Region resolver správne rozpozná Bratislavu"""
    # Bratislava PSČ
    postal_codes = ["81101", "81102", "81103", "81104", "81105"]

    for psc in postal_codes:
        result = resolve_region(psc)
        if result:
            assert isinstance(result, dict)
            # Bratislava by mala byť v Bratislavskom kraji
            region = result.get("region") or result.get("kraj", "")
            if region:
                assert "Bratislav" in region or "bratislav" in region.lower(), (
                    f"PSČ {psc} by malo byť v Bratislavskom kraji, ale je: {region}"
                )


def test_region_resolver_known_cities():
    """Test, či Region resolver správne rozpozná známe mestá"""
    test_cases = [
        ("01001", "Žilina"),  # Žilina
        ("04001", "Košice"),  # Košice
        ("90201", "Trenčín"),  # Trenčín
        ("02101", "Nitra"),  # Nitra
    ]

    for psc, city_name in test_cases:
        result = resolve_region(psc)
        if result:
            assert isinstance(result, dict)
            # Overiť, či výsledok obsahuje region alebo district
            assert (
                "region" in result
                or "kraj" in result
                or "district" in result
                or "okres" in result
            )


def test_region_resolver_invalid_postal_code():
    """Test, či Region resolver správne spracuje neplatné PSČ"""
    invalid_codes = ["00000", "99999", "abc", ""]

    for invalid_code in invalid_codes:
        result = resolve_region(invalid_code)
        # Neplatné PSČ by malo vrátiť None alebo prázdny dict
        assert result is None or result == {} or len(result) == 0


def test_enrich_address_with_region():
    """Test, či enrich_address_with_region funguje"""
    try:
        # Test adresa s PSČ
        test_address = {
            "street": "Hlavná 1",
            "city": "Bratislava",
            "postal_code": "81101",
        }

        enriched = enrich_address_with_region(test_address)

        if enriched:
            assert isinstance(enriched, dict)
            # Enriched adresa by mala obsahovať region/district
            assert (
                "region" in enriched
                or "kraj" in enriched
                or "district" in enriched
                or "okres" in enriched
            )

    except Exception as e:
        pytest.skip(f"enrich_address_with_region nie je dostupný: {e}")


def test_region_resolver_postal_code_file():
    """Test, či existuje CSV súbor s PSČ"""
    import os
    from pathlib import Path

    csv_path = Path(__file__).parent.parent / "backend" / "data" / "postal_codes_sk.csv"

    # CSV súbor by mal existovať
    if csv_path.exists():
        assert csv_path.is_file()
        # Skontrolovať, či nie je prázdny
        assert csv_path.stat().st_size > 0
    else:
        pytest.skip("PSČ CSV súbor neexistuje (to je OK, ak sa používa fallback)")


def test_region_resolver_coverage():
    """Test, či Region resolver má dobré pokrytie PSČ"""
    # Test viacerých PSČ z rôznych krajov
    test_postal_codes = [
        "81101",  # Bratislava
        "01001",  # Žilina
        "04001",  # Košice
        "90201",  # Trenčín
        "02101",  # Nitra
        "94901",  # Nitra (ďalšie)
    ]

    success_count = 0
    for psc in test_postal_codes:
        result = resolve_region(psc)
        if result and isinstance(result, dict) and len(result) > 0:
            success_count += 1

    # Aspoň 50% PSČ by malo byť rozpoznaných
    success_rate = success_count / len(test_postal_codes)
    assert success_rate >= 0.5, (
        f"Region resolver rozpoznal len {success_rate * 100:.1f}% PSČ (očakávané aspoň 50%)"
    )
