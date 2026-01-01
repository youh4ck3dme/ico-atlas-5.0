# Verejné API pre firemné registre v okolí Slovenska (do 3000km)

Na základe analýzy krajín v okruhu 3000km od Slovenska som identifikoval nasledujúce verejné API pre firemné registre. Zahrnul som krajiny V4 + susedné krajiny s dostupnými verejnými API.

## 🇸🇰 **Slovensko** (RPO - Register právnych osôb)
**API:** Slovensko.Digital Ekosystém API  
**Endpoint:** `https://rpo.slovensko.digital/api/subject/{ico}`  
**Dokumentácia:** https://ekosystem.slovensko.digital/api-docs  
**Údaje:** Názov firmy, adresa, právna forma, stav, konatelia, spoločníci  
**Hodnota pre projekt:** ✅ Kritická - už implementovaná, ale potrebuje stabilizáciu  
**Cena:** Bezplatné, verejné API  
**Poznámka:** Vyžaduje možno API kľúč pre vyššie limity

## 🇨🇿 **Česko** (ARES - Administrativní registr ekonomických subjektů)
**API:** ARES REST API  
**Endpoint:** `https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat`  
**Dokumentácia:** https://ares.gov.cz/stranky/vyvojari  
**Údaje:** IČO, názov, adresa, právna forma, DPH status  
**Hodnota pre projekt:** ✅ Implementované a funkčné  
**Cena:** Bezplatné  
**Poznámka:** Obmedzenie na 5 výsledkov na vyhľadávanie

## 🇵🇱 **Poľsko** (KRS - Krajowy Rejestr Sądowy)
**API:** Ministerstwo Sprawiedliwości KRS API  
**Endpoint:** `https://api-krs.ms.gov.pl/api/krs/{krs_number}`  
**Dokumentácia:** https://api-krs.ms.gov.pl/  
**Údaje:** KRS číslo, názov, adresa, právna forma, zarząd (konatelia)  
**Hodnota pre projekt:** ✅ Čiastočne implementované, potrebuje dokončenie  
**Cena:** Bezplatné  
**Poznámka:** Podporuje aj CEIDG pre živnostníkov

## 🇭🇺 **Maďarsko** (NAV - Nemzeti Adó- és Vámhivatal)
**API:** NAV Online API  
**Endpoint:** `https://api.nav.gov.hu/api/taxpayer/{adoszam}`  
**Dokumentácia:** https://api.nav.gov.hu/  
**Údaje:** Adószám, názov, adresa, jogforma, igazgatók  
**Hodnota pre projekt:** ✅ Implementované s fallback dátami  
**Cena:** Bezplatné pre základné vyhľadávanie  
**Poznámka:** Vyššie limity vyžadujú registráciu

## 🇦🇹 **Rakúsko** (Firmenbuch - Obchodný register)
**API:** Bundesministerium für Justiz API  
**Endpoint:** `https://www.justiz.gv.at/api/firmenbuch/{fnr}`  
**Dokumentácia:** https://www.justiz.gv.at/api/  
**Údaje:** Firmenbuchnummer (FNR), názov, adresa, právna forma, Geschäftsführer  
**Hodnota pre projekt:** ⭐ Vysoká - rozšírenie na nemecky hovoriace krajiny  
**Cena:** Bezplatné  
**Poznámka:** Dostupné cez web scraping alebo oficiálne API

## 🇩🇪 **Nemecko** (Handelsregister - Obchodný register)
**API:** Bundesanzeiger API alebo krajinské registre  
**Endpoint:** Rôzne podľa krajiny (napr. `https://www.handelsregister.de/api/firma/{hrb}`)  
**Dokumentácia:** https://www.bundesanzeiger.de/  
**Údaje:** HRB/HRA číslo, názov, adresa, právna forma, Geschäftsführer  
**Hodnota pre projekt:** ⭐ Vysoká - najväčší trh v EÚ  
**Cena:** Bezplatné pre základné údaje  
**Poznámka:** Distribuované po krajinách, API limity

## 🇺🇦 **Ukrajina** (Deržavnyj rejestr - Štátny register)
**API:** YouControl API alebo OpenData  
**Endpoint:** `https://api.youcontrol.com.ua/v1/company/{edrpou}`  
**Dokumentácia:** https://youcontrol.com.ua/en/api/  
**Údaje:** EDRPOU kód, názov, adresa, právna forma, benefiční vlastníci  
**Hodnota pre projekt:** ⭐ Stredná - rozvojový trh s vysokým rizikom  
**Cena:** Freemium (1000 volaní/mesiac zadarmo)  
**Poznámka:** Vyžaduje API kľúč

## 🇷🇴 **Rumunsko** (ONRC - Oficiul Național al Registrului Comerțului)
**API:** Ministerul Justiției API  
**Endpoint:** `https://onrc.gov.ro/api/firma/{cui}`  
**Dokumentácia:** https://onrc.gov.ro/  
**Údaje:** CUI, názov, adresa, forma juridică, administratori  
**Hodnota pre projekt:** ⭐ Stredná - rastúci trh  
**Cena:** Bezplatné  
**Poznámka:** Obmedzené na základné údaje

## 🇷🇸 **Srbsko** (APR - Agencija za privredne registre)
**API:** Serbian Business Registers Agency API  
**Endpoint:** `https://aprs.org.rs/api/company/{maticni_broj}`  
**Dokumentácia:** https://aprs.org.rs/en/api  
**Údaje:** Matični broj, názov, adresa, pravna forma, direktori  
**Hodnota pre projekt:** ⭐ Stredná - Balkánsky trh  
**Cena:** Bezplatné pre základné vyhľadávanie  
**Poznámka:** Vyžaduje registráciu pre vyššie limity

## 🇭🇷 **Chorvátsko** (Sudski registri - Súdní registre)
**API:** Ministarstvo pravosuđa API  
**Endpoint:** `https://sudreg.pravosudje.hr/api/firma/{mbs}`  
**Dokumentácia:** https://sudreg.pravosudje.hr/  
**Údaje:** MBS, názov, adresa, pravna forma, članovi uprave  
**Hodnota pre projekt:** ⭐ Stredná - EÚ trh  
**Cena:** Bezplatné  
**Poznámka:** Distribuované po súdoch

## 🇸🇮 **Slovinsko** (AJPES - Agencija Republike Slovenije za javnopravne evidence in storitve)
**API:** AJPES API  
**Endpoint:** `https://api.ajpes.si/api/company/{maticna_stevilka}`  
**Dokumentácia:** https://api.ajpes.si/  
**Údaje:** Matična številka, názov, adresa, pravna oblika, direktorji  
**Hodnota pre projekt:** ⭐ Stredná - malý ale stabilný trh  
**Cena:** Bezplatné  
**Poznámka:** Vyžaduje API kľúč

## 🇮🇹 **Taliansko** (Registro Imprese)
**API:** Unioncamere API alebo InfoCamere  
**Endpoint:** `https://api.infocamere.it/company/{rea}`  
**Dokumentácia:** https://www.infocamere.it/  
**Údaje:** REA číslo, názov, adresa, forma giuridica, amministratori  
**Hodnota pre projekt:** ⭐ Stredná - veľký trh ale zložitá implementácia  
**Cena:** Freemium  
**Poznámka:** Distribuované po regiónoch

## 🇨🇭 **Švajčiarsko** (Zefix - Švajčiarsky obchodný register)
**API:** Eidgenössisches Amt für das Handelsregister API  
**Endpoint:** `https://api.zefix.ch/api/company/{ch_id}`  
**Dokumentácia:** https://www.zefix.ch/  
**Údaje:** CH-ID, názov, adresa, Rechtsform, Verwaltungsräte  
**Hodnota pre projekt:** ⭐ Stredná - kvalitné dáta ale vysoké náklady  
**Cena:** Platené API  
**Poznámka:** Vyžaduje komerčnú licenciu

## 📊 Hodnotenie a odporúčania

### **Najvyššia priorita (V4 krajiny):**
1. **Slovensko** - dokončiť stabilizáciu
2. **Poľsko** - dokončiť KRS + CEIDG
3. **Maďarsko** - dokončiť NAV integráciu

### **Rozšírenie (ďalšie 3-6 mesiacov):**
1. **Rakúsko** - podobný trh ako Nemecko
2. **Nemecko** - najväčší trh v EÚ
3. **Ukrajina** - rozvojový trh s vysokým rizikom

### **Technické poznámky:**
- Väčšina API je bezplatná pre základné vyhľadávanie
- Rate limiting je bežné (100-1000 volaní/deň)
- Niektoré vyžadujú API kľúče alebo registráciu
- GDPR compliance je kritická pre všetky EÚ krajiny
- Proxy rotation odporúčam pre stability

**Celkový počet identifikovaných API:** 12 krajín s verejnými firemnými registrami

---

## Implementačný stav

### ✅ Implementované (V4):
- 🇸🇰 Slovensko (RPO) - `backend/services/sk_rpo.py`
- 🇨🇿 Česká republika (ARES) - `backend/main.py`
- 🇵🇱 Poľsko (KRS) - `backend/services/pl_krs.py`
- 🇭🇺 Maďarsko (NAV) - `backend/services/hu_nav.py`

### ⏳ Plánované:
- 🇦🇹 Rakúsko (Firmenbuch)
- 🇩🇪 Nemecko (Handelsregister)
- 🇺🇦 Ukrajina (YouControl)
- 🇷🇴 Rumunsko (ONRC)
- 🇷🇸 Srbsko (APR)
- 🇭🇷 Chorvátsko (Sudski registri)
- 🇸🇮 Slovinsko (AJPES)
- 🇮🇹 Taliansko (Registro Imprese)
- 🇨🇭 Švajčiarsko (Zefix)

---

*Posledná aktualizácia: December 2024*

