"""
Slovensko - ORSR Provider (Live Scraping)
Hybridný model: Cache → DB → Live Scraping
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any

import requests
from bs4 import BeautifulSoup

from services.cache import get, get_cache_key
from services.cache import set as cache_set
from services.database import CompanyCache, get_db_session
from services.proxy_rotation import get_proxy, mark_proxy_success, mark_proxy_failed


class OrsrProvider:
    """
    Provider pre získavanie dát z ORSR.sk cez live scraping.
    Používa hybridný model: Cache → DB → Live Scraping
    """

    CACHE_TTL = timedelta(hours=12)  # Cache na 12 hodín
    DB_REFRESH_DAYS = 7  # Auto-refresh po 7 dňoch

    def __init__(self):
        self.session = requests.Session()
        # SSL overovanie pre ORSR už funguje korektne
        self.session.verify = True

    def lookup_by_ico(self, ico: str, force_refresh: bool = False) -> Optional[Dict]:
        """
        Vyhľadá firmu podľa IČO s hybridným modelom.

        Vrstvy:
        1. Cache (Redis/File) - najrýchlejšie
        2. DB - ak cache expirovala
        3. Live Scraping - ak DB je stará alebo neexistuje

        Args:
            ico: 8-miestne slovenské IČO
            force_refresh: Vynútiť nový scraping

        Returns:
            Dict s dátami firmy alebo None
        """
        # 1. Cache vrstva (najrýchlejšia)
        if not force_refresh:
            cache_key = get_cache_key(f"orsr_sk_{ico}")
            cached_data = get(cache_key)
            if cached_data:
                print(f"✅ Cache hit pre IČO {ico}")
                return cached_data

        # 2. DB vrstva
        # 2. DB vrstva
        try:
            with get_db_session() as db:
                if db:
                    company = (
                        db.query(CompanyCache)
                        .filter(
                            CompanyCache.identifier == ico, CompanyCache.country == "SK"
                        )
                        .first()
                    )

                    if company:
                        # Kontrola, či je DB záznam aktuálny
                        days_old = (datetime.utcnow() - company.last_synced_at).days

                        if days_old < self.DB_REFRESH_DAYS and not force_refresh:
                            print(f"✅ DB hit pre IČO {ico} (staré {days_old} dní)")
                            data = (
                                company.company_data or company.data
                            )  # Fallback na legacy field
                            # Uložiť do cache
                            cache_set(cache_key, data, ttl=self.CACHE_TTL)
                            return data
                        else:
                            print(
                                f"⚠️ DB záznam starý ({days_old} dní), spúšťam live scraping..."
                            )
        except Exception as e:
            print(f"⚠️ Chyba pri čítaní z DB (ORSR): {e}")

        # 3. Live Scraping (najpomalšie, ale najaktuálnejšie)
        print(f"🔄 Live scraping pre IČO {ico}...")
        live_data = self._scrape_orsr(ico)

        if live_data:
            # Uložiť do cache
            try:
                cache_set(cache_key, live_data, ttl=self.CACHE_TTL)
            except Exception as e:
                print(f"⚠️ Failed to cache data: {e}")

            # Uložiť do DB
            try:
                with get_db_session() as db:
                    if db:
                        company = (
                            db.query(CompanyCache)
                            .filter(
                                CompanyCache.identifier == ico, CompanyCache.country == "SK"
                            )
                            .first()
                        )

                        if company:
                            # Aktualizovať existujúci záznam
                            company.company_data = live_data
                            company.data = live_data  # Legacy field
                            company.company_name = live_data.get("name")
                            company.risk_score = live_data.get("risk_score")
                            company.last_synced_at = datetime.utcnow()
                            company.updated_at = datetime.utcnow()
                        else:
                            # Vytvoriť nový záznam
                            company = CompanyCache(
                                identifier=ico,
                                country="SK",
                                company_data=live_data,
                                data=live_data,  # Legacy field
                                company_name=live_data.get("name"),
                                risk_score=live_data.get("risk_score"),
                                last_synced_at=datetime.utcnow(),
                            )
                            db.add(company)

                        db.commit()
                        print(f"✅ Dáta uložené do DB pre IČO {ico}")
            except Exception as db_err:
                print(f"⚠️ Nepodarilo sa uložiť dáta do DB: {db_err}")

            return live_data

        return None

    def _scrape_orsr(self, ico: str) -> Optional[Dict]:
        """
        Vykoná live scraping z ORSR.sk.

        Args:
            ico: 8-miestne slovenské IČO

        Returns:
            Dict s normalizovanými dátami alebo None
        """
        try:
            # 1. Vyhľadávanie podľa IČO - Použiť správny endpoint hladaj_ico.asp
            search_url = f"https://www.orsr.sk/hladaj_ico.asp?ICO={ico}&SID=0"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            proxy = get_proxy()
            if proxy:
                self.session.proxies = proxy
                print(f"🌐 Používa sa proxy: {proxy.get('http') or proxy.get('https')}")

            try:
                response = self.session.get(search_url, headers=headers, timeout=30)
                if proxy: mark_proxy_success(proxy)
            except Exception as e:
                if proxy: mark_proxy_failed(proxy)
                print(f"⚠️ ORSR search error: {e}")
                return None

            response.encoding = 'windows-1250'
            
            if response.status_code != 200:
                print(f"❌ ORSR search failed: {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, "html.parser")

            # 2. Nájsť link na detail výpisu
            # Hľadáme link s title="Aktuálny výpis" aby sme ignorovali jazykové prepínače
            detail_link = soup.find("a", attrs={"title": "Aktuálny výpis"})
            
            if not detail_link:
                # Fallback: hľadať link v tabuľke výsledkov (ak title chýba)
                # Ignorujeme lan=en
                links = soup.find_all("a", href=lambda x: x and "vypis.asp?ID=" in x)
                for link in links:
                    href = link.get("href", "")
                    if "lan=en" not in href and "Aktuálny" in link.get_text():
                        detail_link = link
                        break

            if not detail_link:
                print(f"⚠️ IČO {ico} sa nenašlo v ORSR (link nenájdený)")
                return None

            href = detail_link["href"]
            # Construct full URL - href môže byť relatívny (och, orsr má niekedy 'vypis.asp' bez /)
            # ORSR links are usually "vypis.asp?ID=..."
            if href.startswith("/"):
                detail_url = f"https://www.orsr.sk{href}"
            else:
                detail_url = f"https://www.orsr.sk/{href}"
            
            # Remove encoding params if any (keep pure link)
            if "&amp;" in detail_url:
                detail_url = detail_url.replace("&amp;", "&")

            # 3. Stiahnuť detail výpisu
            detail_response = self.session.get(detail_url, headers=headers, timeout=30)
            detail_response.encoding = 'windows-1250'
            
            # DEBUG: Save HTML to file
            try:
                with open("debug_orsr_output.html", "w", encoding="utf-8") as f:
                    f.write(detail_response.text)
                print("DEBUG: Saved HTML to debug_orsr_output.html")
            except Exception as e:
                print(f"DEBUG: Failed to save HTML: {e}")

            print(f"DEBUG: Downloaded detail_url {detail_url}, Status: {detail_response.status_code}, Length: {len(detail_response.text)}")
            if detail_response.status_code != 200:
                print(f"❌ ORSR detail failed: {detail_response.status_code}")
                return None

            detail_soup = BeautifulSoup(detail_response.text, "html.parser")

            # 4. Parsovať HTML a extrahovať dáta
            data = self._parse_orsr_html(detail_soup, ico)
            
            if not data.get("name"):
                print(f"❌ Parsovanie zlyhalo - meno nenájdené pre IČO {ico}")
                # Analyze why name wasn't found - dumping structure
                print("HTML Structure check:")
                print(f"HTML PREVIEW: {detail_soup.prettify()[:2000]}")
                tds = detail_soup.find_all("td")
                matching_tds = [td for td in tds if "Obchodné meno" in td.get_text()]
                print(f"Found {len(matching_tds)} tds with 'Obchodné meno'")
                for td in matching_tds:
                    print(f"TD Content: '{td.get_text(strip=True)}'")
                    sibling = td.find_next_sibling("td")
                    if sibling:
                        print(f"Sibling Content: '{sibling.get_text(strip=True)}'")
                    else:
                        print("No sibling found")
            else:
                print(f"✅ Scraping úspešný: {data.get('name')}")

            return data if data.get("name") else None

        except Exception as e:
            print(f"❌ Chyba pri scraping ORSR: {e}")
            return None

    def _parse_orsr_html(self, soup: BeautifulSoup, ico: str) -> Dict:
        """
        Parsuje HTML z ORSR výpisu a extrahuje dáta.
        """
        data = {
            "ico": ico,
            "country": "SK",
            "name": None,
            "legal_form": None,
            "address": None,
            "postal_code": None,
            "city": None,
            "region": None,
            "district": None,
            "executives": [],
            "shareholders": [],
            "founded": None,
            "status": "Aktívna",
            "dic": None,
            "ic_dph": None,
        }

        # Helper to clean text
        def clean_text(text):
            if not text: return ""
            # Remove (od: ...) and whitespace
            text = re.sub(r"\s*\(od:.*?\)", "", text)
            return text.strip()

        # ---------------------------
        # PEOPLE PARSER (ORSR vypis.asp DOM-aware)
        # ---------------------------
        STOP_PERSON = {
            "predstavenstvo",
            "štatutárny orgán",
            "spoločníci",
            "akcionári",
            "holandské kráľovstvo",
            "česká republika",
            "slovenská republika",
            "rakúska republika",
            "nemecká spolková republika",
            "maďarsko",
            "čierna hora",
        }

        def _norm(s: str) -> str:
            return re.sub(r"\s+", " ", (s or "").strip()).lower()

        def _is_stop_person(s: str) -> bool:
            return _norm(s) in STOP_PERSON

        def _unique_keep_order(seq):
            seen = set()
            out = []
            for x in seq:
                x = clean_text(x)
                if x and x not in seen:
                    seen.add(x)
                    out.append(x)
            return out

        def _looks_like_address(line: str) -> bool:
            l = _norm(line)
            if not l:
                return False
            # digits, postal codes, typical address tokens
            if re.search(r"\d", line):
                return True
            if any(tok in l for tok in ["ul.", "ulica", "č.", "cislo", "číslo", "nám", "cesta", "str.", "/", "psc", "psč"]):
                return True
            # city+postcode pattern "Viedeň 1030" contains digits -> already handled
            return False

        def _looks_like_role(line: str) -> bool:
            l = _norm(line).lstrip("-").strip()
            if not l:
                return False
            # common roles in ORSR
            role_tokens = [
                "predseda", "člen", "clen", "konateľ", "konatel", "prokurista",
                "predstavenstva", "dozornej rady", "správca", "likvidátor", "likvidator"
            ]
            return any(tok in l for tok in role_tokens)

        def _parse_people_from_names_td(names_td: BeautifulSoup, mode: str):
            """
            mode: 'executives' | 'shareholders'
            Prefer anchor boundaries: <a class="lnm">NAME</a>
            """
            people = []

            anchors = names_td.find_all("a", class_="lnm")
            if anchors:
                for a in anchors:
                    name = clean_text(a.get_text(" ", strip=True))
                    if not name or _is_stop_person(name):
                        continue

                    p = {"name": name}
                    role = None
                    since = None
                    until = None
                    birth_date = None
                    residence_parts = []

                    # gather sibling spans until next anchor
                    for sib in a.next_siblings:
                        # stop at next person
                        if getattr(sib, "name", None) == "a" and "lnm" in (sib.get("class") or []):
                            break

                        if getattr(sib, "name", None) != "span":
                            continue

                        t = clean_text(sib.get_text(" ", strip=True))
                        if not t:
                            continue

                        tl = _norm(t)

                        # ignore obvious noise
                        if _is_stop_person(t):
                            continue

                        # structured label lines
                        if tl.startswith("vznik funkcie:"):
                            since = clean_text(t.split(":", 1)[1])
                            continue
                        if tl.startswith("zánik funkcie:") or tl.startswith("zanik funkcie:"):
                            until = clean_text(t.split(":", 1)[1])
                            continue
                        if tl.startswith("dátum narodenia:") or tl.startswith("datum narodenia:"):
                            birth_date = clean_text(t.split(":", 1)[1])
                            continue

                        # owners section has financial lines - ignore
                        if mode == "shareholders":
                            if tl.startswith("vklad:") or tl.startswith("splatené:") or tl.startswith("splatene:") or "osoba je" in tl:
                                continue

                        # role line often begins with "-"
                        if t.strip().startswith("-") or _looks_like_role(t):
                            if not role:
                                role = clean_text(t.lstrip("-").strip())
                            continue

                        # address lines
                        if _looks_like_address(t) or residence_parts:
                            residence_parts.append(t)
                            continue

                        # anything else -> ignore

                    if role:
                        p["role"] = role
                    if since:
                        p["since"] = since
                    if until:
                        p["until"] = until
                    if birth_date:
                        p["birth_date"] = birth_date
                    if residence_parts:
                        p["residence_address"] = " / ".join(residence_parts)

                    people.append(p)

                # dedupe by (name, role) keep order
                seen = set()
                out = []
                for p in people:
                    k = (_norm(p.get("name", "")), _norm(p.get("role", "")))
                    if k[0] and k not in seen:
                        seen.add(k)
                        out.append(p)
                return out

            # Fallback (no anchors): use get_text lines with strong heuristics
            txt = names_td.get_text(separator="\n", strip=True)
            lines = [clean_text(x) for x in (txt or "").split("\n")]
            lines = [x for x in lines if x]

            cur = None
            for line in lines:
                l = _norm(line)
                if _is_stop_person(line):
                    continue
                if l.startswith("vznik funkcie:") or l.startswith("zánik funkcie:") or l.startswith("dátum narodenia:"):
                    if cur:
                        key = l.split(":", 1)[0]
                        val = clean_text(line.split(":", 1)[1])
                        if "vznik" in key:
                            cur["since"] = val
                        elif "zánik" in key or "zanik" in key:
                            cur["until"] = val
                        else:
                            cur["birth_date"] = val
                    continue

                # start a person ONLY if line looks like name:
                # require 2+ words and no digits and not role and not address
                looks_name = (not re.search(r"\d", line)) and (len(line.split()) >= 2) and (not _looks_like_role(line))
                if looks_name:
                    if cur:
                        people.append(cur)
                    cur = {"name": line}
                    continue

                if cur:
                    if (line.strip().startswith("-") or _looks_like_role(line)) and not cur.get("role"):
                        cur["role"] = clean_text(line.lstrip("-").strip())
                    elif _looks_like_address(line) or cur.get("residence_address"):
                        cur["residence_address"] = (cur.get("residence_address", "") + " / " + line).strip(" /")

            if cur:
                people.append(cur)

            # final filter: remove any that accidentally are places
            people = [p for p in people if p.get("name") and not _is_stop_person(p["name"])]
            return people

        # Helper to find value next to label
        def get_value(label_pattern):
            # Find all TDs
            tds = soup.find_all("td")
            for td in tds:
                if td.get_text() and label_pattern in td.get_text():
                    sibling = td.find_next_sibling("td")
                    if sibling:
                        return clean_text(sibling.get_text(separator=" ", strip=True))
            return None

        # 1. Názov firmy
        data["name"] = get_value("Obchodné meno:")
        
        # 2. Právna forma
        data["legal_form"] = get_value("Právna forma:")
        
        # 3. Sídlo (Adresa)
        raw_address = get_value("Sídlo:")
        if raw_address:
            data["address"] = raw_address
            # Parse postal code and city
            postal_match = re.search(r"\b\d{3}\s?\d{2}\b", raw_address)
            if postal_match:
                data["postal_code"] = postal_match.group().replace(" ", "")
                # City is usually after postal code or at the end
                parts = raw_address.split(postal_match.group())
                if len(parts) > 1:
                    data["city"] = parts[1].strip().strip(",").strip()
                elif "," in raw_address:
                     data["city"] = raw_address.split(",")[-1].strip()

        # 4. Štatutárny orgán (Konatelia / Predstavenstvo)
        stat_tds = [td for td in soup.find_all("td") if "Štatutárny orgán:" in td.get_text()]
        if stat_tds:
            stat_td = stat_tds[0]
            names_td = stat_td.find_next_sibling("td")
            if names_td:
                people = _parse_people_from_names_td(names_td, mode="executives")
                data["executive_people"] = people  # structured (optional)
                data["executives"] = _unique_keep_order([p["name"] for p in people if p.get("name")])

        # 5. Spoločníci (Owners)
        spol_tds = [td for td in soup.find_all("td") if "Spoločníci:" in td.get_text() or "Akcionár" in td.get_text()]
        if spol_tds:
            spol_td = spol_tds[0]
            names_td = spol_td.find_next_sibling("td")
            if names_td:
                people = _parse_people_from_names_td(names_td, mode="shareholders")
                data["shareholder_people"] = people  # structured (optional)
                data["shareholders"] = _unique_keep_order([p["name"] for p in people if p.get("name")])

        # 6. Deň zápisu
        data["founded"] = get_value("Deň zápisu:")

        # Status check
        if "likvidácia" in str(soup).lower() or "konkurz" in str(soup).lower():
            data["status"] = "Likvidácia/Konkurz"

        # stable dedupe already done above (do NOT use set() here)


        
        # Obohatenie o geolokáciu (Kraj, Okres z PSČ)
        if data.get("postal_code"):
            try:
                from services.sk_region_resolver import enrich_address_with_region
                region_data = enrich_address_with_region(data.get("address", ""), data["postal_code"])
                data["region"] = region_data.get("region")
                data["district"] = region_data.get("district")
            except: pass

        # Obohatenie o DIČ/IČ DPH - Temporarily disabled for debugging speed
        # if not data.get("dic") and not data.get("ic_dph"):
             # print(f"🔍 Hľadám DIČ/IČ DPH pre IČO {ico}...")
             # ... (zrsr logic disabled)

        # Obohatenie o finančné ukazovatele z RUZ - Temporarily disabled for debugging speed
        # try:
             # ... (ruz logic disabled)
        # except Exception as e:
             # print(f"⚠️ RUZ obohatenie zlyhalo: {e}")

        return data


# Singleton instance
_orsr_provider = None


def get_orsr_provider() -> OrsrProvider:
    """Vráti singleton inštanciu OrsrProvider."""
    global _orsr_provider
    if _orsr_provider is None:
        _orsr_provider = OrsrProvider()
    return _orsr_provider
