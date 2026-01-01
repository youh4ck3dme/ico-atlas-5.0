# 🧪 IČO ATLAS 5.0 – Testing Guide

## Rýchly štart

### 1. Spustenie testov

```bash
cd ico-atlas
php artisan test
```

**Očakávaný výstup:**
```
PASS  Tests\Feature\Api\CompanyApiTest
✓ valid ico returns 200 with company data
✓ missing ico parameter returns 422
✓ invalid ico format returns 422
...

PASS  Tests\Unit\Services\CompanyServiceTest
✓ uses stub in testing environment
✓ returns cached flag on second call
...

PASS  Tests\Unit\RegionResolverTest
✓ returns nulls for empty zip
✓ resolves known bratislava zip
...
```

### 2. Testovanie API endpointu

#### Lokálne testovanie (ak beží server)

```bash
# Spustiť server (v novom termináli)
cd ico-atlas
php artisan serve

# V inom termináli otestovať API
curl -sS "http://127.0.0.1:8000/api/company/search?ico=52374220" | jq
```

**Očakávaný výstup:**
```json
{
  "data": {
    "ico": "52374220",
    "name": "DEMO s. r. o.",
    "dic": null,
    "ic_dph": null,
    "legal_form": "s. r. o.",
    "address": "Drieňová 1J",
    "city": "Bratislava",
    "zip": "82101",
    "district": "Bratislava II",
    "region": "Bratislavský kraj",
    "country": "SK",
    "source": "orsr"
  },
  "meta": {
    "cached": false,
    "latency_ms": 5
  }
}
```

#### Testovanie neplatného IČO

```bash
curl -sS "http://127.0.0.1:8000/api/company/search?ico=123" | jq
```

**Očakávaný výstup (422):**
```json
{
  "message": "The given data was invalid.",
  "errors": {
    "ico": [
      "IČO musí mať presne 8 číslic."
    ]
  }
}
```

#### Testovanie neznámeho IČO

```bash
curl -sS "http://127.0.0.1:8000/api/company/search?ico=99999999" | jq
```

**Očakávaný výstup (404):**
```json
{
  "message": "Company not found",
  "data": null,
  "meta": {
    "cached": false,
    "latency_ms": 3
  }
}
```

### 3. Prepnutie na reálnu ORSR integráciu

#### Krok 1: Upraviť `.env` súbor

```bash
cd ico-atlas
nano .env  # alebo vim, code, atď.
```

#### Krok 2: Pridať/upraviť nasledujúce premenné

```env
# ORSR integrácia
ICOATLAS_ORSR_STUB=false
ICOATLAS_ORSR_BASE_URL=https://www.orsr.sk
ICOATLAS_ORSR_SEARCH_URL=https://www.orsr.sk/hladaj_ico.asp

# Cache settings
ICOATLAS_CACHE_TTL_HOURS=12

# HTTP timeout
ICOATLAS_HTTP_TIMEOUT=10
```

#### Krok 3: Vymazať cache a otestovať

```bash
php artisan config:clear
php artisan cache:clear

# Otestovať s reálnym IČO
curl -sS "http://127.0.0.1:8000/api/company/search?ico=31333547" | jq
```

**Poznámka:** Reálna ORSR integrácia vyžaduje:
- Funkčné internetové pripojenie
- Prístup k ORSR webu
- Správne parsovanie HTML (môže byť potrebné upraviť `OrsrProvider::parseDetailHtml()`)

---

## Testovacie scenáre

### Unit testy

```bash
# Všetky unit testy
php artisan test --testsuite=Unit

# Konkrétny test
php artisan test tests/Unit/Services/CompanyServiceTest.php
```

### Feature testy

```bash
# Všetky feature testy
php artisan test --testsuite=Feature

# Konkrétny test
php artisan test tests/Feature/Api/CompanyApiTest.php
```

### Verbose output

```bash
php artisan test --verbose
```

---

## Troubleshooting

### Testy nefungujú

1. **Skontrolovať PHP verziu:**
   ```bash
   php -v  # Musí byť PHP 8.2+
   ```

2. **Skontrolovať závislosti:**
   ```bash
   composer install
   ```

3. **Vymazať cache:**
   ```bash
   php artisan config:clear
   php artisan cache:clear
   ```

### API vracia 500 error

1. **Skontrolovať logy:**
   ```bash
   tail -f storage/logs/icoatlas.log
   tail -f storage/logs/laravel.log
   ```

2. **Skontrolovať, či beží server:**
   ```bash
   php artisan serve
   ```

3. **Skontrolovať .env nastavenia:**
   ```bash
   php artisan config:show icoatlas
   ```

---

## Test coverage

Aktuálne pokrytie:
- ✅ API endpoint (validácia, error handling)
- ✅ CompanyService (caching, provider pipeline)
- ✅ RegionResolver (PSČ mapping)
- ⚠️ OrsrProvider (stub mode, real mode potrebuje testy)
- ⚠️ ZrsrProvider (skeleton, potrebuje implementáciu)
- ⚠️ RuzProvider (skeleton, potrebuje implementáciu)

---

**Posledná aktualizácia:** 17. december 2024

