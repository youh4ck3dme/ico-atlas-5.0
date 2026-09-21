"""
Testy pre RUZ Provider
Overuje API a HTML parsing
"""

from unittest.mock import Mock, patch

import pytest

from backend.services.sk_ruz_provider import RuzProvider


class TestRuzProvider:
    """Testy pre RUZ Provider"""

    def test_api_response_parsing(self):
        """Test parsovania API JSON odpovede"""
        provider = RuzProvider()
        provider.STUB_MODE = False

        # Príklad JSON odpovede z dokumentácie
        api_response = {
            "dic": "2099999999",
            "icDph": "SK2099999999",
            "uctovneZavierky": [
                {"rok": 2022, "obrat": "1 000,00", "zisk": "500,00"},
                {"rok": 2023, "obrat": "2 000,00", "zisk": "1 000,00"},
            ],
        }

        statements = provider._parse_api_response(api_response)

        assert statements is not None
        assert len(statements) == 2

        # Najnovšia závierka (2023) by mala byť prvá
        assert statements[0]["year"] == 2023
        assert statements[0]["revenue"] == 2000.0
        assert statements[0]["profit"] == 1000.0
        assert statements[0]["dic"] == "2099999999"
        assert statements[0]["ic_dph"] == "SK2099999999"

        # Staršia závierka (2022)
        assert statements[1]["year"] == 2022
        assert statements[1]["revenue"] == 1000.0
        assert statements[1]["profit"] == 500.0

    def test_normalize_number(self):
        """Test normalizácie číselných hodnôt"""
        provider = RuzProvider()

        # Slovenský formát (čiarky, medzery)
        assert provider._normalize_number("1 000,00") == 1000.0
        assert provider._normalize_number("2 500,50") == 2500.5
        assert provider._normalize_number("500,00") == 500.0

        # Prázdne alebo neplatné
        assert provider._normalize_number("") == 0.0
        assert provider._normalize_number("N/A") == 0.0

    def test_stub_mode(self):
        """Test stub mode pre IČO 52374220"""
        provider = RuzProvider()
        provider.STUB_MODE = True

        statements = provider.lookup_financial_statements("52374220")

        assert statements is not None
        assert len(statements) == 2
        assert statements[0]["year"] == 2023
        assert statements[0]["revenue"] == 2000000.0

    def test_get_financial_indicators(self):
        """Test získania finančných ukazovateľov"""
        provider = RuzProvider()
        provider.STUB_MODE = True

        indicators = provider.get_financial_indicators("52374220")

        assert indicators is not None
        assert indicators["year"] == 2023
        assert indicators["revenue"] == 2000000.0
        assert indicators["profit"] == 50000.0
        assert indicators["dic"] == "2023456789"

    def test_normalize_ico(self):
        """Test normalizácie IČO"""
        provider = RuzProvider()

        assert provider._normalize_ico("12345678") == "12345678"
        assert provider._normalize_ico("12 345 678") == "12345678"
        assert provider._normalize_ico("12345") is None
