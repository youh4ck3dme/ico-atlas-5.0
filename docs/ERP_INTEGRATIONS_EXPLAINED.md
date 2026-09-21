# 🔌 ERP Integrácie - Vysvetlenie

## Čo je ERP systém?

**ERP (Enterprise Resource Planning)** = Systém na riadenie podnikových zdrojov

ERP systémy sú softvéry, ktoré firmy používajú na správu:
- **Financie** (účtovníctvo, faktúry, platby)
- **Zásoby** (tovar, sklady)
- **Zákazníci** (CRM, objednávky)
- **Dodávatelia** (nákupy, faktúry)
- **Zamestnanci** (mzdy, dochádzka)

### Najpoužívanejšie ERP systémy v regióne V4:

1. **SAP** 🇩🇪
   - Najväčší ERP systém na svete
   - Používajú ho veľké korporácie
   - Veľmi komplexný a drahý

2. **Pohoda** 🇸🇰
   - Slovenský ERP systém
   - Veľmi populárny na Slovensku
   - Používajú ho stredné a väčšie firmy

3. **Money S3** 🇨🇿
   - Český ERP systém
   - Populárny v Českej republike
   - Podobný Pohode

---

## Prečo ERP integrácie pre ILUMINATI SYSTEM?

### Aktuálna situácia:
ILUMINATI SYSTEM získava dáta z **verejných registrov** (RPO, ARES, KRS):
- ✅ IČO, názov firmy
- ✅ Adresa, právna forma
- ✅ Konatelia, spoločníci
- ✅ Základné finančné údaje (ak sú verejné)

### Problém:
**Verejné registre neobsahujú všetko!**

Chýbajúce informácie:
- ❌ Skutočné obraty (len ak sú verejné)
- ❌ Aktuálne záväzky voči dodávateľom
- ❌ Platenie faktúr (včas/neskoro)
- ❌ Finančná zdravot firmy v reálnom čase
- ❌ Históriu transakcií

### Riešenie: ERP integrácia

Ak by ILUMINATI SYSTEM mal prístup k ERP dátam firmy, mohol by:

1. **Automaticky kontrolovať platobnú disciplínu**
   - Ktoré faktúry platí včas?
   - Ktoré faktúry má po splatnosti?
   - Ako dlho trvá platba?

2. **Analyzovať finančnú zdravot v reálnom čase**
   - Aktuálne záväzky
   - Pohľávky
   - Cash flow

3. **Detekovať riziká skôr**
   - Firma má veľa po splatnosti faktúr? → ⚠️ Riziko
   - Firma neplatí dodávateľom? → ⚠️ Riziko
   - Pokles obratov? → ⚠️ Riziko

---

## Ako by to fungovalo v praxi?

### Scenár 1: Firma chce overiť dodávateľa

**Bez ERP integrácie:**
```
1. Používateľ zadá IČO dodávateľa
2. ILUMINATI zobrazí:
   - Základné údaje z registra
   - Risk score (na základe verejných dát)
   - "⚠️ Môže byť riziko" (ale nevieme prečo)
```

**S ERP integráciou:**
```
1. Používateľ zadá IČO dodávateľa
2. ILUMINATI automaticky:
   - Načíta dáta z verejných registrov
   - Pripojí sa k ERP systému používateľa
   - Skontroluje históriu platieb tejto firme
3. Zobrazí:
   - "✅ Táto firma platí vždy včas (30 dní)"
   - "✅ Nikdy nemala problém s platbami"
   - "✅ Risk score: NÍZKY"
```

### Scenár 2: Automatické varovania

**S ERP integráciou:**
```
ILUMINATI môže automaticky:
- Sledovať všetkých dodávateľov v ERP
- Ak sa zhorší risk score dodávateľa → poslať webhook
- "⚠️ Váš dodávateľ XYZ má teraz vysoký risk score!"
```

---

## Technická implementácia

### 1. SAP Connector
```python
# backend/services/erp/sap_connector.py

def connect_to_sap(credentials):
    """
    Pripojenie k SAP systému cez SAP API
    """
    # SAP má REST API alebo SOAP API
    # Potrebujeme:
    # - Server URL
    # - Username/Password
    # - Company code
    pass

def get_supplier_payment_history(supplier_ico):
    """
    Získa históriu platieb pre dodávateľa
    """
    # Query SAP databázu
    # Vráti: faktúry, dátumy, sumy, stav platieb
    pass
```

### 2. Pohoda Connector
```python
# backend/services/erp/pohoda_connector.py

def connect_to_pohoda(api_key, company_id):
    """
    Pripojenie k Pohoda API
    """
    # Pohoda má REST API
    # Potrebujeme API key a Company ID
    pass

def get_invoices(supplier_ico):
    """
    Získa faktúry od dodávateľa
    """
    # API call: GET /api/invoices?supplier_ico=...
    pass
```

### 3. Money S3 Connector
```python
# backend/services/erp/money_s3_connector.py

def connect_to_money_s3(credentials):
    """
    Pripojenie k Money S3 API
    """
    # Podobné ako Pohoda
    pass
```

---

## Frontend - ERP Integration Hub

```jsx
// frontend/src/pages/ErpIntegrations.jsx

// Používateľ môže:
1. Pripojiť svoj ERP systém (SAP/Pohoda/Money S3)
2. Nastaviť synchronizáciu (každý deň/každý týždeň)
3. Vidieť status synchronizácie
4. Zobraziť logy synchronizácií
```

---

## Bezpečnosť a súkromie

⚠️ **Kritické otázky:**

1. **GDPR compliance**
   - Používateľ musí súhlasiť
   - Dáta musia byť šifrované
   - Používateľ môže kedykoľvek odpojiť ERP

2. **Autentifikácia**
   - ERP credentials sa ukladajú šifrované
   - Používame OAuth2 alebo API keys
   - Nikdy neukladáme priamo heslo

3. **Prístup k dátam**
   - ILUMINATI má prístup len na čítanie
   - Nikdy nemení dáta v ERP
   - Synchronizácia je jednosmerná (ERP → ILUMINATI)

---

## Prečo je to "pending"?

### Dôvody:

1. **Komplexnosť**
   - Každý ERP má iné API
   - Rôzne autentifikačné metódy
   - Rôzne dátové formáty

2. **Bezpečnosť**
   - Potrebujeme robustné šifrovanie
   - GDPR compliance
   - Audit logy

3. **Priorita**
   - Najprv sme dokončili základné features
   - ERP integrácie sú "nice to have" pre Enterprise klientov
   - Nie je kritické pre MVP

4. **Partnerstvá**
   - Možno potrebujeme partnerstvo s ERP poskytovateľmi
   - SAP môže vyžadovať špeciálnu licenciu
   - Pohoda/Money S3 môžu mať obmedzenia API

---

## Odhad implementácie

### Čas: 2-3 mesiace

**Fáza 1 (2 týždne):**
- Research ERP API dokumentácie
- Prototyp pre 1 ERP (Pohoda - najjednoduchšie)

**Fáza 2 (1 mesiac):**
- Backend connector pre Pohoda
- Frontend UI pre pripojenie
- Testovanie s reálnymi dátami

**Fáza 3 (1 mesiac):**
- Money S3 connector
- SAP connector (základný)
- Dokumentácia

**Fáza 4 (2 týždne):**
- Bezpečnostné audit
- GDPR compliance
- Production deployment

---

## Zhrnutie

**ERP integrácie = Spojenie ILUMINATI SYSTEM s ERP systémom firmy**

**Výhody:**
- ✅ Presnejšie risk scoring
- ✅ Automatické varovania
- ✅ Reálne finančné dáta
- ✅ Hodnota pre Enterprise klientov

**Výzvy:**
- ⚠️ Komplexnosť implementácie
- ⚠️ Bezpečnosť a GDPR
- ⚠️ Partnerstvá s ERP poskytovateľmi

**Status:** Pending (nie je kritické pre MVP, ale je to silná Enterprise feature)

---

*Posledná aktualizácia: December 20, 2024*

