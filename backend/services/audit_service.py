"""
Audit Service - Full Firma Data Check
Poskytuje hĺbkový 360° audit firiem.
"""
import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from datetime import datetime

from services.sk_orsr_provider import OrsrProvider
from services.sk_region_resolver import resolve_region

class AuditService:
    """
    Služba pre komplexný audit firiem (Full Firma Data Check).
    Agreguje dáta z verejných registrov, dlhových zoznamov a analyzuje riziká.
    """

    def __init__(self):
        self.orsr_provider = OrsrProvider()
        # Zoznam známych virtuálnych sídiel (vzorka)
        self.virtual_addresses = [
            "napájadlá 7", "karpatské námestie 10", "klincová 37", 
            "kopčianska 10", "mýtna 15", "p.o.box", "pobox", "virtualne",
            "m. r. štefánika", "námestie snp", "gorkého"
        ]

    def perform_deep_audit(self, ico: str) -> Dict:
        """
        Vykoná kompletný 360° audit pre zadané IČO.
        """
        audit_report = {
            "ico": ico,
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "identity": {},
            "debts": [],
            "address_analysis": {},
            "officers": [],
            "risk_score": 0,
            "alerts": []
        }

        # 1. Identita (ORSR Data)
        # Použijeme existujúci provider alebo fallback scraping ak treba viac detailov
        company_data = self.orsr_provider.lookup_by_ico(ico)
        if not company_data:
            # Fallback pre CZ alebo ak ORSR zlyhá - zatiaľ jednoduchý return
            # V budúcnosti tu môžeme pridať ARES fallback
            audit_report["summary"]["status"] = "NENÁJDENÁ"
            audit_report["risk_score"] = 0 # Neznáma
            audit_report["alerts"].append({"level": "warning", "message": "Firma nebola nájdená v registroch."})
            return audit_report

        audit_report["identity"] = company_data
        
        # 2. Analýza statusu
        status = company_data.get("status", "Aktívna")
        if any(s in status.lower() for s in ["likvid", "konkurz", "výmaz", "zrušen"]):
             audit_report["alerts"].append({"level": "critical", "message": f"Firma je v stave: {status}"})
             audit_report["risk_score"] += 7

        # 3. Analýza sídla
        address = company_data.get("address", "")
        is_virtual = any(va.lower() in address.lower() for va in self.virtual_addresses)
        audit_report["address_analysis"] = {
            "raw_address": address,
            "is_virtual_suspect": is_virtual,
            "region": resolve_region(company_data.get("postal_code", ""))
        }
        if is_virtual:
            audit_report["alerts"].append({"level": "high", "message": "Sídlo na adrese hromadného poskytovateľa virtuálnych adries."})
            audit_report["risk_score"] += 3

        # 4. Dlhová analýza (Simulácia / Heuristika)
        # Reálna implementácia by scrapovala socpoist.sk/union.sk/vszp.sk
        # Tu použijeme logiku na základe skúseností (pre demo IČO 51200678) alebo placeholder
        debts = self._check_debts(ico)
        audit_report["debts"] = debts
        if debts:
            debt_count = len(debts)
            audit_report["alerts"].append({"level": "critical", "message": f"Nájdené záznamy v {debt_count} dlhových registroch."})
            audit_report["risk_score"] += 5

        # 5. Konatelia a história
        officers = company_data.get("executives", [])
        audit_report["officers"] = [{"name": name, "risk": "low"} for name in officers]
        # Jednoduchá heuristika pre podozrivé mená (napr. z minulých auditov)
        for officer in audit_report["officers"]:
             # Placeholder logic -> v reále by sme lustrovali osobu
             pass

        # 6. Finálne Trust Score (0-10)
        # Base 1 (Low risk)
        final_score = 1 + audit_report["risk_score"]
        if final_score > 10: final_score = 10
        audit_report["trust_score"] = final_score
        
        # Preklad skóre
        if final_score >= 8: verdict = "KRITICKÉ RIZIKO"
        elif final_score >= 5: verdict = "ZVÝŠENÉ RIZIKO"
        else: verdict = "NÍZKE RIZIKO"
        
        audit_report["summary"]["verdict"] = verdict
        
        return audit_report

    def _check_debts(self, ico: str) -> List[Dict]:
        """
        Simulovaná kontrola dlhov pre účely MVP.
        V produkcii by tu boli requesty na API poisťovní.
        """
        debts = []
        # Hardcoded známe dlžnícke IČO pre demo účely (aby funkcionalita bola viditeľná)
        if ico == "51200678": 
            debts.append({"source": "Sociálna poisťovňa", "status": "DLŽNÍK", "amount": "Vysoká suma"})
            debts.append({"source": "VšZP", "status": "ZÁZNAM", "amount": "Nedoplatok"})
            debts.append({"source": "Union", "status": "ZÁZNAM", "amount": "Nedoplatok"})
        
        return debts

audit_service = AuditService()
