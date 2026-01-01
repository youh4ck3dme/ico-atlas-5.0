"""
ZRSR Provider - Živnostenský register SR
Získava DIČ/IČ DPH pre slovenské firmy
Implementácia podľa IČO ATLAS specifikácie
"""

import re
import time
import warnings
from typing import Dict, Optional

import requests
from services.proxy_rotation import get_proxy, mark_proxy_success, mark_proxy_failed


class ZrsrProvider:
    """
    Provider pre získavanie DIČ/IČ DPH z Živnostenského registra SR.

    Scraping Flow:
    1. Search Request: https://www.zrsr.sk/hladaj_subjekt.asp?ICO={ICO}
    2. Extract Detail Link: subjekt_detail.asp?ID=...
    3. Detail Request: https://www.zrsr.sk/{detail_path}
    4. Parse HTML pomocou regexov
    """

    MAX_RETRIES = 2
    RETRY_DELAY = 1
    BASE_URL = "https://www.zrsr.sk"
    STUB_MODE = False  # Pre testovanie môže byť True

    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        # Potlač SSL warnings
        try:
            import urllib3

            urllib3.disable_warnings()
        except ImportError:
            warnings.filterwarnings("ignore", message="Unverified HTTPS request")

        # User-Agent pre lepšiu kompatibilitu
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "sk-SK,sk;q=0.9,en;q=0.8",
            }
        )

    def lookup_dic_ic_dph(
        self, ico: str, company_name: Optional[str] = None
    ) -> Optional[Dict[str, str]]:
        """
        Získa DIČ a IČ DPH pre firmu.

        Args:
            ico: 8-miestne slovenské IČO
            company_name: Názov firmy (voliteľné, pre lepšie vyhľadávanie)

        Returns:
            Dict s 'dic' a 'ic_dph' alebo None
        """
        if self.STUB_MODE:
            return self._stub_company(ico)

        ico_normalized = self._normalize_ico(ico)
        if not ico_normalized:
            return None

        try:
            # 1. Search Request
            search_url = f"{self.BASE_URL}/hladaj_subjekt.asp"
            search_response = self._make_request_with_retry(
                search_url, params={"ICO": ico_normalized}
            )

            if not search_response or search_response.status_code != 200:
                print(
                    f"⚠️ ZRSR search failed: {search_response.status_code if search_response else 'No response'}"
                )
                return None

            # 2. Extract Detail Link
            detail_path = self._extract_detail_path(search_response.text)
            if not detail_path:
                print(f"⚠️ ZRSR detail link not found for IČO {ico_normalized}")
                return None

            # 3. Detail Request
            detail_url = f"{self.BASE_URL}/{detail_path.lstrip('/')}"
            detail_response = self._make_request_with_retry(detail_url)

            if not detail_response or detail_response.status_code != 200:
                print(
                    f"⚠️ ZRSR detail failed: {detail_response.status_code if detail_response else 'No response'}"
                )
                return None

            # 4. Parse HTML
            parsed_data = self._parse_detail_html(detail_response.text, ico_normalized)

            if parsed_data:
                print(f"✅ ZRSR data found for IČO {ico_normalized}: {parsed_data}")

            return parsed_data

        except Exception as e:
            print(f"❌ Chyba pri ZRSR lookup: {e}")
            return None

    def _normalize_ico(self, ico: str) -> Optional[str]:
        """
        Normalizuje IČO - extrahuje len číslice a overí, že má 8 miest.

        Args:
            ico: IČO (môže obsahovať medzery)

        Returns:
            Normalizované IČO (8 číslic) alebo None
        """
        digits = re.sub(r"\D+", "", ico)
        return digits if len(digits) == 8 else None

    def _make_request_with_retry(
        self, url: str, params: Optional[Dict] = None, max_retries: Optional[int] = None
    ) -> Optional[requests.Response]:
        """
        Vykoná HTTP request s retry mechanizmom.

        Args:
            url: URL pre request
            params: Query parametre
            max_retries: Maximálny počet pokusov (default: MAX_RETRIES)

        Returns:
            Response alebo None pri chybe
        """
        if max_retries is None:
            max_retries = self.MAX_RETRIES

        for attempt in range(max_retries + 1):
            proxy = get_proxy()
            if proxy:
                self.session.proxies = proxy
                
            try:
                response = self.session.get(url, params=params, timeout=10)
                if proxy:
                    mark_proxy_success(proxy)
                if response.status_code == 200:
                    return response
                elif response.status_code == 404:
                    return None  # Neexistuje, netreba retry
                else:
                    if attempt < max_retries:
                        time.sleep(self.RETRY_DELAY)
                        continue
                    return response
            except requests.exceptions.RequestException as e:
                if proxy:
                    mark_proxy_failed(proxy)
                if attempt < max_retries:
                    print(
                        f"⚠️ Request failed (attempt {attempt + 1}/{max_retries + 1}): {e}"
                    )
                    time.sleep(self.RETRY_DELAY)
                    continue
                print(f"❌ Request failed after {max_retries + 1} attempts: {e}")
                return None

        return None

    def _extract_detail_path(self, html: str) -> Optional[str]:
        """
        Extrahuje link na detail z HTML search výsledku.

        Hľadá: href="subjekt_detail.asp?ID=..."

        Args:
            html: HTML obsah search stránky

        Returns:
            Detail path alebo None
        """
        # Hľadať href="subjekt_detail.asp?ID=..."
        pattern = r'href=["\']([^"\']*subjekt_detail\.asp\?ID=[^"\']+)["\']'
        match = re.search(pattern, html, re.IGNORECASE)

        if match:
            # HTML decode (ak je potrebné)
            detail_path = match.group(1)
            # Odstrániť HTML entity
            detail_path = detail_path.replace("&amp;", "&")
            return detail_path

        return None

    def _parse_detail_html(
        self, html: str, expected_ico: str
    ) -> Optional[Dict[str, str]]:
        """
        Parsuje HTML detail stránky pomocou regexov.

        Používa kombináciu plaintext + regex pre robustnosť.

        Args:
            html: HTML obsah detail stránky
            expected_ico: Očakávané IČO (pre validáciu)

        Returns:
            Dict s dátami alebo None
        """
        # Zjednodušenie: pre regexy často stačí plaintext
        # Odstrániť HTML tagy
        text = re.sub(r"<[^>]+>", " ", html)
        # Normalizovať whitespace
        text = re.sub(r"\s+", " ", text)

        result = {
            "dic": None,
            "ic_dph": None,
            "name": None,
            "ico": expected_ico,
            "address": None,
            "status": None,
            "establishment_date": None,
        }

        # 1. Obchodné meno (vylepšený regex s lookahead fixom)
        # Pattern: (?:Obchodné\s+meno|Názov)[:\s]+(.+?)(?:\s*[;,]|\s*(?:IČO|Sídlo|DIČ|IČ DPH|Stav|Dátum)|$)
        name_pattern = r"(?:Obchodné\s+meno|Názov)[:\s]+(.+?)(?:\s*[;,]|\s*(?:IČO|Sídlo|DIČ|IČ\s*DPH|Stav|Dátum)|$)"
        name_match = re.search(name_pattern, text, re.IGNORECASE | re.UNICODE)
        if name_match:
            result["name"] = name_match.group(1).strip()

        # 2. DIČ
        # Pattern: DI[ČC][:\s]+([\d\s]{8,})
        dic_pattern = r"DI[ČC][:\s]+([\d\s]{8,})"
        dic_match = re.search(dic_pattern, text, re.IGNORECASE | re.UNICODE)
        if dic_match:
            # Odstrániť všetko okrem číslic
            dic_digits = re.sub(r"\D+", "", dic_match.group(1))
            if len(dic_digits) >= 8:
                result["dic"] = dic_digits

        # 3. IČ DPH
        # Pattern: IČ[O\s]*DPH[:\s]+(?:SK)?([\d\s]{8,})
        ic_dph_pattern = r"IČ[O\s]*DPH[:\s]+(?:SK)?([\d\s]{8,})"
        ic_dph_match = re.search(ic_dph_pattern, text, re.IGNORECASE | re.UNICODE)
        if ic_dph_match:
            # Odstrániť všetko okrem číslic
            ic_dph_digits = re.sub(r"\D+", "", ic_dph_match.group(1))
            if len(ic_dph_digits) >= 8:
                result["ic_dph"] = f"SK{ic_dph_digits}"

        # 4. Sídlo / Adresa (vylepšený regex s lookahead fixom)
        # Pattern: (?:Sídlo|Adresa)[:\s]+(.+?)(?:\s*(?:Dátum|Stav|IČO|DIČ|IČ DPH)|$)
        address_pattern = (
            r"(?:Sídlo|Adresa)[:\s]+(.+?)(?:\s*(?:Dátum|Stav|IČO|DIČ|IČ\s*DPH)|$)"
        )
        address_match = re.search(address_pattern, text, re.IGNORECASE | re.UNICODE)
        if address_match:
            result["address"] = address_match.group(1).strip()

        # 5. Dátum vzniku
        # Pattern: (?:Dátum\s+vzniku|Vznik)[:\s]+(\d{1,2}[./]\d{1,2}[./]\d{4})
        date_pattern = r"(?:Dátum\s+vzniku|Vznik)[:\s]+(\d{1,2}[./]\d{1,2}[./]\d{4})"
        date_match = re.search(date_pattern, text, re.IGNORECASE | re.UNICODE)
        if date_match:
            result["establishment_date"] = date_match.group(1).strip()

        # 6. Stav (vylepšený regex)
        # Pattern: (?:Stav|Status)[:\s]+(.+?)(?:\s*[;,]|\s*$)
        status_pattern = r"(?:Stav|Status)[:\s]+(.+?)(?:\s*[;,]|\s*$)"
        status_match = re.search(status_pattern, text, re.IGNORECASE | re.UNICODE)
        if status_match:
            status = status_match.group(1).strip()
            # Normalizovať stav
            if "aktív" in status.lower():
                result["status"] = "Aktívna"
            else:
                result["status"] = status

        # 7. IČO (pre validáciu)
        # Pattern: IČO[:\s]+([\d\s]{8,})
        ico_pattern = r"IČO[:\s]+([\d\s]{8,})"
        ico_match = re.search(ico_pattern, text, re.IGNORECASE | re.UNICODE)
        if ico_match:
            ico_digits = re.sub(r"\D+", "", ico_match.group(1))
            if len(ico_digits) == 8:
                result["ico"] = ico_digits

        # Validácia: ak nemáme ani meno, parsovanie zlyhalo
        if not result["name"]:
            return None

        # Vrátiť len relevantné polia (dic, ic_dph) pre obohatenie
        # Zabezpečiť, že všetky hodnoty sú stringy (nie None)
        return {
            "dic": result.get("dic") or "",
            "ic_dph": result.get("ic_dph") or "",
            # Voliteľne aj ďalšie dáta
            "name": result.get("name") or "",
            "address": result.get("address") or "",
            "status": result.get("status") or "",
        }

    def _stub_company(self, ico: str) -> Optional[Dict[str, str]]:
        """
        Stub mode - vracia testovacie dáta.

        Args:
            ico: IČO

        Returns:
            Testovacie dáta alebo None
        """
        if ico == "52374220":
            return {
                "name": "DEMO Živnostník",
                "dic": "2023456789",
                "ic_dph": "SK2023456789",
                "status": "Aktívna",
            }
        return None


# Singleton instance
_zrsr_provider = None


def get_zrsr_provider() -> ZrsrProvider:
    """Vráti singleton inštanciu ZrsrProvider."""
    global _zrsr_provider
    if _zrsr_provider is None:
        _zrsr_provider = ZrsrProvider()
    return _zrsr_provider
