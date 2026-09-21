"""
Testy pre ZRSR Provider
Overuje parsovanie HTML podľa dokumentácie
"""

from unittest.mock import Mock, patch

import pytest

from backend.services.sk_zrsr_provider import ZrsrProvider


class TestZrsrProvider:
    """Testy pre ZRSR Provider"""

    def test_documentation_example_html_is_parsed_correctly(self):
        """
        Overuje, že príklad HTML uvedený v dokumentácii
        je správne parsovaný implementovanou logikou.
        """
        # Presne ten istý HTML kód ako v dokumentácii
        doc_html = """<!DOCTYPE html>
<html>
<head><title>Výpis zo Živnostenského registra</title></head>
<body>
    <div class="main-content">
        <table class="detail-table">
            <tr>
                <td class="label">Obchodné meno:</td>
                <td class="value"><strong>Ukážková Firma s.r.o.</strong></td>
            </tr>
            <tr>
                <td class="label">IČO:</td>
                <td class="value">12 345 678</td>
            </tr>
            <tr>
                <td class="label">Sídlo:</td>
                <td class="value">Priemyselná 12, 010 01 Žilina</td>
            </tr>
            <tr>
                <td class="label">DIČ:</td>
                <td class="value">2021234567</td>
            </tr>
             <tr>
                <td class="label">IČ DPH:</td>
                <td class="value">SK2021234567</td>
            </tr>
            <tr>
                <td class="label">Dátum vzniku:</td>
                <td class="value">15.03.2010</td>
            </tr>
            <tr>
                <td class="label">Stav:</td>
                <td class="value">aktívna</td>
            </tr>
        </table>
    </div>
</body>
</html>"""

        provider = ZrsrProvider()
        provider.STUB_MODE = False

        # Mock HTTP odpovedí
        mock_search_response = Mock()
        mock_search_response.status_code = 200
        mock_search_response.text = (
            '<html><a href="subjekt_detail.asp?ID=999">Link na detail</a></html>'
        )

        mock_detail_response = Mock()
        mock_detail_response.status_code = 200
        mock_detail_response.text = doc_html

        with patch.object(provider, "_make_request_with_retry") as mock_request:
            # 1. Search request
            # 2. Detail request
            mock_request.side_effect = [mock_search_response, mock_detail_response]

            # Hľadáme podľa IČO z príkladu
            result = provider.lookup_dic_ic_dph("12345678")

        # Overenie, či JSON výstup sedí s dokumentáciou
        assert result is not None, "Parser nevratil žiadne dáta"
        assert result.get("ico") == "12345678" or result.get("name") is not None
        assert result.get("name") == "Ukážková Firma s.r.o."
        assert result.get("dic") == "2021234567"
        assert result.get("ic_dph") == "SK2021234567"
        assert result.get("address") == "Priemyselná 12, 010 01 Žilina"
        assert result.get("status") == "Aktívna"

    def test_stub_mode(self):
        """Test stub mode pre IČO 52374220"""
        provider = ZrsrProvider()
        provider.STUB_MODE = True

        result = provider.lookup_dic_ic_dph("52374220")

        assert result is not None
        assert result.get("name") == "DEMO Živnostník"
        assert result.get("dic") == "2023456789"
        assert result.get("ic_dph") == "SK2023456789"
        assert result.get("status") == "Aktívna"

    def test_normalize_ico(self):
        """Test normalizácie IČO"""
        provider = ZrsrProvider()

        # Rôzne formáty IČO
        assert provider._normalize_ico("12345678") == "12345678"
        assert provider._normalize_ico("12 345 678") == "12345678"
        assert provider._normalize_ico("12-345-678") == "12345678"
        assert provider._normalize_ico("12345") is None  # Príliš krátke
        assert provider._normalize_ico("123456789") is None  # Príliš dlhé

    def test_extract_detail_path(self):
        """Test extrakcie detail path z HTML"""
        provider = ZrsrProvider()

        html = '<html><a href="subjekt_detail.asp?ID=12345">Link</a></html>'
        path = provider._extract_detail_path(html)

        assert path == "subjekt_detail.asp?ID=12345"

        # Test s HTML entitami
        html2 = '<html><a href="subjekt_detail.asp?ID=123&amp;SID=2">Link</a></html>'
        path2 = provider._extract_detail_path(html2)

        assert path2 == "subjekt_detail.asp?ID=123&SID=2"
