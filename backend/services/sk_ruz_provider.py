"""
RUZ Provider - Register účtovných závierok
Získava finančné dáta a účtovné závierky pre slovenské firmy
Implementácia podľa IČO ATLAS specifikácie
"""

import re
import time
import warnings
from typing import Dict, List, Optional

import requests
from services.proxy_rotation import get_proxy, mark_proxy_success, mark_proxy_failed

try:
    from bs4 import BeautifulSoup  # type: ignore[reportMissingModuleSource]
except ImportError:
    BeautifulSoup = None  # Fallback ak nie je nainštalovaný


class RuzProvider:
    """
    Provider pre získavanie účtovných závierok z RUZ.

    API Flow:
    1. API Request: https://www.registeruz.sk/cruz-public/api/uctovne-zavierky?ico={ico}
    2. Fallback: HTML Scraping ak API nie je dostupné
    """

    MAX_RETRIES = 2
    RETRY_DELAY = 1
    BASE_URL = "https://www.registeruz.sk"
    API_URL = f"{BASE_URL}/cruz-public/api/uctovne-zavierky"
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
                "Accept": "application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "sk-SK,sk;q=0.9,en;q=0.8",
            }
        )

    def lookup_financial_statements(
        self, ico: str, year: Optional[int] = None
    ) -> Optional[List[Dict]]:
        """
        Získa účtovné závierky pre firmu.

        Args:
            ico: 8-miestne slovenské IČO
            year: Rok závierky (ak None, vráti všetky roky)

        Returns:
            List s účtovnými závierkami alebo None
        """
        if self.STUB_MODE:
            return self._stub_financial_statements(ico, year)

        ico_normalized = self._normalize_ico(ico)
        if not ico_normalized:
            return None

        try:
            # 1. Skúsiť API
            api_data = self._fetch_from_api(ico_normalized, year)
            if api_data:
                return api_data

            # 2. Fallback: HTML Scraping
            print("⚠️ RUZ API nedostupné, používam HTML scraping...")
            html_data = self._fetch_from_html(ico_normalized, year)
            return html_data

        except Exception as e:
            print(f"❌ Chyba pri RUZ lookup: {e}")
            return None

    def _normalize_ico(self, ico: str) -> Optional[str]:
        """Normalizuje IČO - extrahuje len číslice a overí, že má 8 miest."""
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

    def _fetch_from_api(
        self, ico: str, year: Optional[int] = None
    ) -> Optional[List[Dict]]:
        """
        Získa dáta z RUZ API.

        Args:
            ico: 8-miestne IČO
            year: Rok (voliteľné)

        Returns:
            List s účtovnými závierkami alebo None
        """
        params = {"ico": ico}
        if year:
            params["year"] = str(year)  # Konvertovať na string pre URL parametre

        response = self._make_request_with_retry(self.API_URL, params=params)

        if not response or response.status_code != 200:
            return None

        try:
            data = response.json()
            return self._parse_api_response(data)
        except (ValueError, KeyError) as e:
            print(f"⚠️ Chyba pri parsovaní API odpovede: {e}")
            return None

    def _parse_api_response(self, data: Dict) -> List[Dict]:
        """
        Parsuje JSON odpoveď z RUZ API.

        Args:
            data: JSON odpoveď z API

        Returns:
            List s účtovnými závierkami
        """
        statements = []

        # Štruktúra: { "dic": "...", "icDph": "...", "uctovneZavierky": [...] }
        uctovne_zavierky = data.get("uctovneZavierky", [])

        for zavierka in uctovne_zavierky:
            # Normalizovať číselné hodnoty (čiarky → bodky, odstrániť medzery)
            obrat = self._normalize_number(zavierka.get("obrat", "0"))
            zisk = self._normalize_number(zavierka.get("zisk", "0"))

            statements.append(
                {
                    "year": zavierka.get("rok"),
                    "revenue": obrat,  # Obrat = tržby
                    "profit": zisk,
                    "dic": data.get("dic"),
                    "ic_dph": data.get("icDph"),
                }
            )

        # Zoradiť podľa roka (najnovšie prvé)
        statements.sort(key=lambda x: x.get("year", 0), reverse=True)

        return statements

    def _normalize_number(self, value: str) -> float:
        """
        Normalizuje číselnú hodnotu (čiarky → bodky, odstrániť medzery).

        Args:
            value: Formátovaný reťazec (napr. "1 000,00")

        Returns:
            Float hodnota
        """
        if not value:
            return 0.0

        # Odstrániť medzery
        value = value.replace(" ", "")
        # Nahradiť čiarku bodkou (slovenský formát)
        value = value.replace(",", ".")

        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def _fetch_from_html(
        self, ico: str, year: Optional[int] = None
    ) -> Optional[List[Dict]]:
        """
        Získa dáta z RUZ cez HTML scraping (fallback).

        Args:
            ico: 8-miestne IČO
            year: Rok (voliteľné)

        Returns:
            List s účtovnými závierkami alebo None
        """
        try:
            # 1. Vyhľadávanie
            search_url = f"{self.BASE_URL}/hladaj_subjekt.asp"
            search_response = self._make_request_with_retry(
                search_url, params={"ICO": ico}
            )

            if not search_response or search_response.status_code != 200:
                return None

            # 2. Extrahovať detail link
            detail_path = self._extract_detail_path(search_response.text)
            if not detail_path:
                return None

            # 3. Detail request
            detail_url = f"{self.BASE_URL}/{detail_path.lstrip('/')}"
            detail_response = self._make_request_with_retry(detail_url)

            if not detail_response or detail_response.status_code != 200:
                return None

            # 4. Parse HTML
            return self._parse_html(detail_response.text, year)

        except Exception as e:
            print(f"❌ Chyba pri HTML scraping: {e}")
            return None

    def _extract_detail_path(self, html: str) -> Optional[str]:
        """
        Extrahuje link na detail z HTML search výsledku.

        Hľadá: href obsahuje subjekt_detail.asp a ID=

        Args:
            html: HTML obsah search stránky

        Returns:
            Detail path alebo None
        """
        # Hľadať href obsahujúci subjekt_detail.asp a ID=
        pattern = r'href=["\']([^"\']*subjekt_detail\.asp[^"\']*ID=[^"\']+)["\']'
        match = re.search(pattern, html, re.IGNORECASE)

        if match:
            detail_path = match.group(1)
            # Odstrániť HTML entity
            detail_path = detail_path.replace("&amp;", "&")
            return detail_path

        return None

    def _parse_html(
        self, html: str, year: Optional[int] = None
    ) -> Optional[List[Dict]]:
        """
        Parsuje HTML detail stránky pomocou BeautifulSoup.

        Args:
            html: HTML obsah detail stránky
            year: Rok (voliteľné, pre filtrovanie)

        Returns:
            List s účtovnými závierkami alebo None
        """
        if not BeautifulSoup:
            print("⚠️ BeautifulSoup nie je nainštalovaný, HTML parsing nie je dostupný")
            return None

        try:
            soup = BeautifulSoup(html, "html.parser")
            if soup is None:
                return None

            # Extrahovať DIČ a IČ DPH
            dic = None
            ic_dph = None

            # Hľadať DIČ
            dic_elem = soup.find(string=re.compile(r"DI[ČC][:\s]+", re.IGNORECASE))
            if dic_elem:
                parent = dic_elem.find_parent()
                if parent:
                    value_elem = parent.find_next_sibling()
                    if value_elem:
                        dic_text = value_elem.get_text(strip=True)
                        dic = re.sub(r"\D+", "", dic_text)

            # Hľadať IČ DPH
            ic_dph_elem = soup.find(
                string=re.compile(r"IČ[O\s]*DPH[:\s]+", re.IGNORECASE)
            )
            if ic_dph_elem:
                parent = ic_dph_elem.find_parent()
                if parent:
                    value_elem = parent.find_next_sibling()
                    if value_elem:
                        ic_dph_text = value_elem.get_text(strip=True)
                        ic_dph_digits = re.sub(r"\D+", "", ic_dph_text)
                        if ic_dph_digits:
                            ic_dph = f"SK{ic_dph_digits}"

            # Hľadať tabuľku s účtovnými závierkami
            # Trieda: uctovne-zavierky alebo podobná
            table = soup.find("table", class_=re.compile(r"uctovne", re.IGNORECASE))
            if not table:
                # Skúsiť nájsť tabuľku obsahujúcu "Rok", "Obrat", "Zisk"
                tables = soup.find_all("table")
                for t in tables:
                    if "Rok" in t.get_text() and "Obrat" in t.get_text():
                        table = t
                        break

            if not table:
                return None

            # Skontrolovať, či table má metódu find_all (nie je NavigableString)
            if not hasattr(table, "find_all"):
                return None

            statements = []

            # Parsovať riadky tabuľky
            # Type ignore: table je Tag (nie NavigableString) kvôli hasattr check vyššie
            rows = table.find_all("tr")[1:]  # type: ignore[attr-defined]  # Preskočiť hlavičku

            for row in rows:
                cells = row.find_all(["td", "th"])  # type: ignore[attr-defined]
                if len(cells) < 3:
                    continue

                try:
                    rok = int(cells[0].get_text(strip=True))
                    obrat_text = cells[1].get_text(strip=True)
                    zisk_text = cells[2].get_text(strip=True)

                    # Filtrovať podľa roka ak je zadaný
                    if year and rok != year:
                        continue

                    obrat = self._normalize_number(obrat_text)
                    zisk = self._normalize_number(zisk_text)

                    statements.append(
                        {
                            "year": rok,
                            "revenue": obrat,
                            "profit": zisk,
                            "dic": dic,
                            "ic_dph": ic_dph,
                        }
                    )
                except (ValueError, IndexError):
                    continue

            # Zoradiť podľa roka (najnovšie prvé)
            statements.sort(key=lambda x: x.get("year", 0), reverse=True)

            return statements if statements else None

        except Exception as e:
            print(f"❌ Chyba pri parsovaní HTML: {e}")
            return None

    def get_financial_indicators(
        self, ico: str, year: Optional[int] = None
    ) -> Optional[Dict]:
        """
        Získa finančné ukazovatele pre firmu (najnovšia závierka).

        Args:
            ico: 8-miestne slovenské IČO
            year: Rok (ak None, vráti najnovšie)

        Returns:
            Dict s finančnými ukazovateľmi alebo None
        """
        statements = self.lookup_financial_statements(ico, year)

        if not statements:
            return None

        # Vziať najnovšiu závierku (prvý v zozname, už zoradené)
        latest = statements[0] if statements else None

        if not latest:
            return None

        return {
            "year": latest.get("year"),
            "revenue": latest.get("revenue", 0.0),
            "profit": latest.get("profit", 0.0),
            "dic": latest.get("dic"),
            "ic_dph": latest.get("ic_dph"),
        }

    def _stub_financial_statements(
        self, ico: str, year: Optional[int] = None
    ) -> Optional[List[Dict]]:
        """
        Stub mode - vracia testovacie dáta.

        Args:
            ico: IČO
            year: Rok (voliteľné)

        Returns:
            Testovacie dáta alebo None
        """
        if ico == "52374220":
            statements = [
                {
                    "year": 2023,
                    "revenue": 2000000.0,
                    "profit": 50000.0,
                    "dic": "2023456789",
                    "ic_dph": "SK2023456789",
                },
                {
                    "year": 2022,
                    "revenue": 1500000.0,
                    "profit": 30000.0,
                    "dic": "2023456789",
                    "ic_dph": "SK2023456789",
                },
            ]

            if year:
                statements = [s for s in statements if s["year"] == year]

            return statements

        return None


# Singleton instance
_ruz_provider = None


def get_ruz_provider() -> RuzProvider:
    """Vráti singleton inštanciu RuzProvider."""
    global _ruz_provider
    if _ruz_provider is None:
        _ruz_provider = RuzProvider()
    return _ruz_provider
