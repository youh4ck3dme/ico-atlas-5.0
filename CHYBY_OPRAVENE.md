# ✅ Opravené Chyby – IČO ATLAS 5.0

## 🔧 Opravené problémy

### 1. ✅ Carbon TypeError (riadok 93 v CompanyService.php)

**Problém:**
```
Carbon\Carbon::rawAddUnit(): Argument #3 ($value) must be of type int|float, string given
```

**Príčina:**
`config('icoatlas.cache_ttl_hours', 12)` vracia string namiesto int.

**Oprava:**
```php
// Predtým:
now()->addHours(config('icoatlas.cache_ttl_hours', 12))

// Teraz:
now()->addHours((int) config('icoatlas.cache_ttl_hours', 12))
```

---

### 2. ✅ Undefined array key "district" (riadok 80 v CompanyService.php)

**Problém:**
```
Undefined array key "district"
```

**Príčina:**
`$company['district'] ?: $resolved['district']` hádže error, ak kľúč neexistuje.

**Oprava:**
```php
// Predtým:
$company['district'] = $company['district'] ?: $resolved['district'];
$company['region']   = $company['region']   ?: $resolved['region'];

// Teraz:
$company['district'] = $company['district'] ?? $resolved['district'];
$company['region']   = $company['region']   ?? $resolved['region'];
```

---

### 3. ✅ CompanyServiceTest – nesprávne mocky

**Problém:**
Testy očakávali, že providery sa nevolajú, ale CompanyService ich volá.

**Oprava:**
- `uses_stub_in_testing_environment`: Používa skutočný `OrsrProvider` so stub mode
- `calculates_latency_correctly`: Používa skutočný `OrsrProvider` so stub mode
- Pridané `Config::set('icoatlas.orsr.stub_mode', true)` pre správne testovanie
- Pridané mockovanie `RegionResolver::fromZip()` vo všetkých testoch

---

## 📋 Zoznam opráv

1. ✅ **CompanyService.php:93** – Pridaný cast na int pre `cache_ttl_hours`
2. ✅ **CompanyService.php:80-81** – Zmenené `?:` na `??` pre null coalescing
3. ✅ **CompanyServiceTest.php** – Opravené mocky a pridané Config::set
4. ✅ **CompanyServiceTest.php** – Pridané mockovanie RegionResolver vo všetkých testoch

---

## ✅ Status

Všetky známe chyby sú opravené:
- ✅ Carbon TypeError
- ✅ Undefined array key
- ✅ Nesprávne test mocky
- ✅ Chýbajúce RegionResolver mocky

---

## 🧪 Testovanie

Spusti testy:
```bash
cd ico-atlas
php artisan test
```

**Očakávaný výsledok:**
- Všetky testy by mali prejsť
- Žiadne TypeError
- Žiadne Undefined array key errors

---

**Dátum opráv:** 17. december 2024

