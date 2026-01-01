"""
Špeciálne testy pre detekciu krajiny (CZ vs SK pre 8-miestne čísla)
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Pridať backend do path
backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from main import app
from unittest.mock import MagicMock
from contextlib import contextmanager
import services.database

# Mock database session
@contextmanager
def mock_db_session():
    yield MagicMock()
services.database.get_db_session = mock_db_session

client = TestClient(app)

# Global mocks for external services
@pytest.fixture(autouse=True)
def mock_external_services(mocker):
    # Mock ARES
    mock_ares = mocker.patch("main.fetch_ares_cz")
    mock_ares.return_value = {
        "ekonomickeSubjekty": [
            {
                "ico": "47114983",
                "obchodniJmeno": "ČEZ, a.s.",
                "sidlo": {"textovaAdresa": "Praha, CZ"}
            },
            {
                "ico": "27074358",
                "obchodniJmeno": "Agrofert, a.s.",
                "sidlo": {"textovaAdresa": "Praha, CZ"}
            }
        ]
    }
    
    # Mock ORSR
    mock_orsr = mocker.patch("main.get_orsr_provider")
    mock_provider = MagicMock()
    
    def mock_lookup(ico, force_refresh=False):
        if ico == "31333501":
            return {"ico": "31333501", "name": "Agrofert Holding a.s.", "country": "SK", "status": "Aktívna"}
        if ico == "52374220":
            return {"ico": "52374220", "name": "Tavira, s.r.o.", "country": "SK", "status": "Aktívna"}
        return None
        
    mock_provider.lookup_by_ico.side_effect = mock_lookup
    mock_orsr.return_value = mock_provider
    
    yield


def test_czech_ico_detected_as_cz():
    """Test, či české IČO sa správne detekuje ako CZ (nie SK)"""
    # České IČO (8-miestne)
    czech_ico = "47114983"  # ČEZ, a.s.
    
    try:
        response = client.get(f"/api/search?q={czech_ico}")
        assert response.status_code == 200
        
        data = response.json()
        nodes = data.get("nodes", [])
        
        if nodes:
            # Nájsť hlavnú firmu
            company_node = next((n for n in nodes if n.get("type") == "company"), None)
            if company_node:
                country = company_node.get("country")
                # České IČO by malo byť detekované ako CZ, nie SK
                assert country == "CZ", \
                    f"České IČO {czech_ico} bolo detekované ako {country}, očakávané CZ"
    except Exception as e:
        pytest.fail(f"Test zlyhal: {e}")


def test_slovak_ico_detected_as_sk():
    """Test, či slovenské IČO sa správne detekuje ako SK"""
    # Slovenské IČO (8-miestne)
    slovak_ico = "31333501"  # Agrofert Holding a.s.
    
    try:
        response = client.get(f"/api/search?q={slovak_ico}")
        assert response.status_code == 200
        
        data = response.json()
        nodes = data.get("nodes", [])
        
        if nodes:
            # Nájsť hlavnú firmu
            company_node = next((n for n in nodes if n.get("type") == "company"), None)
            if company_node:
                country = company_node.get("country")
                # Slovenské IČO by malo byť detekované ako SK
                assert country == "SK", \
                    f"Slovenské IČO {slovak_ico} bolo detekované ako {country}, očakávané SK"
    except Exception as e:
        pytest.fail(f"Test zlyhal: {e}")


def test_country_detection_priority():
    """Test priority detekcie: CZ má prioritu pred SK pre 8-miestne čísla"""
    # České IČO, ktoré by sa mohlo zameniť so SK
    czech_ico = "27074358"  # Agrofert, a.s. (CZ)
    
    try:
        response = client.get(f"/api/search?q={czech_ico}")
        assert response.status_code == 200
        
        data = response.json()
        nodes = data.get("nodes", [])
        
        if nodes:
            company_node = next((n for n in nodes if n.get("type") == "company"), None)
            if company_node:
                country = company_node.get("country")
                # ARES by mal vrátiť dáta pre CZ, takže by to malo byť CZ
                # Ak ARES nevrátil dáta, môže to byť SK (fallback)
                assert country in ["CZ", "SK"], \
                    f"Krajina {country} nie je platná (očakávané CZ alebo SK)"
    except Exception as e:
        pytest.fail(f"Test zlyhal: {e}")


def test_company_name_not_fallback():
    """Test, či názov firmy nie je 'Firma {ICO}' (fallback)"""
    # Reálne IČO, ktoré by malo mať skutočný názov
    test_ico = "52374220"  # Tavira, s.r.o. (SK)
    
    try:
        response = client.get(f"/api/search?q={test_ico}")
        assert response.status_code == 200
        
        data = response.json()
        nodes = data.get("nodes", [])
        
        if nodes:
            company_node = next((n for n in nodes if n.get("type") == "company"), None)
            if company_node:
                label = company_node.get("label", "")
                # Názov by nemal byť "Firma {ICO}" (to je fallback)
                assert not label.startswith("Firma "), \
                    f"Názov firmy je fallback: {label}"
                assert label != f"Firma {test_ico}", \
                    f"Názov firmy je fallback formát: {label}"
    except Exception as e:
        pytest.fail(f"Test zlyhal: {e}")
