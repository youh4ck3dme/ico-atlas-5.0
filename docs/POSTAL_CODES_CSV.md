# 📮 PSČ CSV - Inštrukcie

## Aktuálny stav

**Súbor:** `backend/data/postal_codes_sk.csv`

**Obsahuje:** ~40 základných PSČ (hlavné mestá a okresy)

**Status:** ⚠️ Potrebuje doplniť na ~1 800 položiek

---

## Formát CSV

```csv
postal_code,kraj,okres
81101,Bratislavský,Bratislava I
82101,Bratislavský,Bratislava II
04001,Košický,Košice I
```

**Stĺpce:**
- `postal_code` - PSČ (5 číslic, bez medzier)
- `kraj` - Názov kraja (bez "kraj" na konci)
- `okres` - Názov okresu

---

## Zdroje pre kompletný CSV

### 1. Národný katalóg otvorených dát (Odporúčané)
**URL:** https://data.gov.sk/dataset/psc

**Výhody:**
- Oficiálny zdroj
- Aktualizovaný každé 3 mesiace
- Licencia CC0 (voľne použiteľná)

**Ako stiahnuť:**
1. Otvoriť https://data.gov.sk/dataset/psc
2. Stiahnuť CSV súbor
3. Skontrolovať hlavičku (možno bude potrebné premenovať stĺpce)
4. Skopírovať do `backend/data/postal_codes_sk.csv`

---

### 2. Postcodezip.com
**URL:** https://www.postcodezip.com/slovakia/postal-codes.csv

**Výhody:**
- Rýchlo stiahnuteľné
- Jednoduchý formát

**Poznámka:** Obsahuje len ~404 položiek

---

### 3. GeoPostcodes
**URL:** https://www.geopostcodes.com/Slovakia

**Výhody:**
- Veľký dataset (13 445 položiek)
- Obsahuje regionálne informácie

**Poznámka:** Môže vyžadovať registráciu

---

## Ako pridať CSV do projektu

### Krok 1: Stiahnuť CSV
```bash
# Príklad: Stiahnuť z data.gov.sk
curl -o backend/data/postal_codes_sk.csv "URL_K_CSV_SUBORU"
```

### Krok 2: Skontrolovať formát
```bash
head -5 backend/data/postal_codes_sk.csv
```

**Očakávaný výstup:**
```
postal_code,kraj,okres
81101,Bratislavský,Bratislava I
82101,Bratislavský,Bratislava II
...
```

### Krok 3: Ak formát nevyhovuje, upraviť
```bash
# Príklad: Premenovať stĺpce
sed -i '1s/PSČ/postal_code/; 1s/Kraj/kraj/; 1s/Okres/okres/' backend/data/postal_codes_sk.csv
```

### Krok 4: Overiť načítanie
```python
from services.sk_region_resolver import resolve_region

# Test
result = resolve_region("81101")
print(result)  # {"kraj": "Bratislavský", "okres": "Bratislava I"}
```

---

## RegionResolver podporuje

✅ **Rôzne formáty CSV:**
- `postal_code,kraj,okres`
- `code,region,district`
- `PSČ,Kraj,Okres`

✅ **Automatická detekcia stĺpcov:**
- Hľadá stĺpec obsahujúci "postal", "psc", "code"
- Hľadá stĺpec obsahujúci "kraj", "region"
- Hľadá stĺpec obsahujúci "okres", "district"

✅ **Normalizácia:**
- Odstraňuje medzery z PSČ
- Odstraňuje " kraj" z názvu kraja
- Fallback mapping ak CSV nie je dostupný

---

## Testovanie

```bash
cd backend
source venv/bin/activate
python -c "from services.sk_region_resolver import resolve_region; print(resolve_region('81101'))"
```

**Očakávaný výstup:**
```
{'kraj': 'Bratislavský', 'okres': 'Bratislava I'}
```

---

## Poznámky

- **Fallback mapping:** Ak CSV nie je dostupný, používa sa základný fallback mapping (~40 PSČ)
- **Performance:** CSV sa načíta pri importe modulu (jednorazovo)
- **Aktualizácia:** CSV môžeš aktualizovať kedykoľvek - stačí reštartovať aplikáciu

---

*Posledná aktualizácia: December 20, 2024*

