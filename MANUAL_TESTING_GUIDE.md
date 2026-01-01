# 🧪 Manuálne Testovanie - Návod

**Dátum:** December 20, 2024  
**Verzia:** 5.0

---

## 🌐 URL Adresy

- **Frontend:** http://localhost:8009
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/api/docs
- **Health Check:** http://localhost:8000/api/health
- **ReDoc:** http://localhost:8000/api/redoc

---

## 📋 Testovacie IČO

### Slovensko (SK)
- **52374220** - Tavira, s.r.o. (reálne IČO)
- **88888888** - Test IČO

### Česko (CZ)
- **27074358** - Test IČO
- **12345678** - Test IČO

### Poľsko (PL)
- **123456789** - Test KRS
- **0000001234** - Test NIP

### Maďarsko (HU)
- **12345678** - Test Adószám
- **87654321** - Test Adószám

---

## 🎯 Testovacie Scenáre

### 1. Frontend Testy

#### A. Základné Vyhľadávanie
1. Otvoriť: http://localhost:8009
2. Zadať IČO: `52374220`
3. Kliknúť "Search"
4. **Očakávaný výsledok:**
   - Graf s firmou
   - Detail panel s informáciami
   - Risk score

#### B. Export Funkcie
1. Po vyhľadaní IČO
2. Kliknúť na export tlačidlá:
   - **CSV** - Stiahne CSV súbor
   - **JSON** - Stiahne JSON súbor
   - **PDF** - Stiahne PDF súbor
   - **Excel** - Stiahne Excel súbor (iba Pro/Enterprise)

#### C. Advanced Filters
1. Rozbaliť "Advanced Filters"
2. Nastaviť:
   - Country: SK
   - Min Risk Score: 0
   - Max Risk Score: 100
3. Kliknúť "Apply Filters"

#### D. Favorites System (iba prihlásený)
1. Prihlásiť sa
2. Vyhľadať firmu
3. Kliknúť "Add to Favorites"
4. Prejsť na Dashboard
5. Skontrolovať, či je firma v favorites

#### E. Analytics Dashboard (iba Enterprise)
1. Prihlásiť sa ako Enterprise user
2. Prejsť na `/analytics`
3. Skontrolovať grafy:
   - Search Trends
   - Risk Distribution
   - User Activity
   - API Usage

---

### 2. Backend API Testy

#### A. Health Check
```bash
curl http://localhost:8000/api/health
```

**Očakávaný výsledok:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-20T...",
  "cache": {...},
  "features": {
    "cz_ares": true,
    "sk_rpo": true,
    "pl_krs": true,
    "hu_nav": true,
    "risk_intelligence": true,
    "cache": true,
    "database": true
  }
}
```

#### B. Search Endpoint
```bash
# SK IČO
curl 'http://localhost:8000/api/search?q=52374220'

# CZ IČO
curl 'http://localhost:8000/api/search?q=27074358'

# Textové vyhľadávanie
curl 'http://localhost:8000/api/search?q=Tavira'
```

**Očakávaný výsledok:**
```json
{
  "nodes": [...],
  "edges": [...]
}
```

#### C. Cache Stats
```bash
curl http://localhost:8000/api/cache/stats
```

#### D. Database Stats
```bash
curl http://localhost:8000/api/database/stats
```

#### E. Swagger UI
1. Otvoriť: http://localhost:8000/api/docs
2. Rozbaliť endpointy
3. Kliknúť "Try it out"
4. Zadať parametre
5. Kliknúť "Execute"

---

### 3. Nové Funkcie Testy

#### A. Excel Export
```bash
# Vyžaduje autentifikáciu
curl -X POST http://localhost:8000/api/export/excel \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nodes": [...], "edges": [...]}'
```

#### B. Batch Export
```bash
curl -X POST http://localhost:8000/api/export/batch-excel \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"company_data": {...}, "risk_score": 75}]'
```

#### C. Redis Cache (ak je nainštalovaný)
```bash
# Skontrolovať Redis stats v cache stats
curl http://localhost:8000/api/cache/stats
```

**Očakávaný výsledok:**
```json
{
  "redis_enabled": true,
  "redis": {
    "total_keys": 10,
    "used_memory_mb": 0.5
  },
  "in_memory": {...}
}
```

---

### 4. Authentication Testy

#### A. Registrácia
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User"
  }'
```

#### B. Prihlásenie
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123"
```

#### C. Protected Endpoint
```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 5. Docker Testy (ak používaš Docker)

#### A. Spustenie
```bash
docker-compose up -d
```

#### B. Logy
```bash
# Všetky logy
docker-compose logs -f

# Len backend
docker-compose logs -f backend

# Len frontend
docker-compose logs -f frontend
```

#### C. Zastavenie
```bash
docker-compose down
```

---

## 🔍 Kontrola Chýb

### Backend Chyby
```bash
# Skontrolovať logy
tail -f logs/backend.log

# Alebo ak používaš Docker
docker-compose logs -f backend
```

### Frontend Chyby
```bash
# Skontrolovať logy
tail -f logs/frontend.log

# Alebo otvoriť Developer Tools v prehliadači (F12)
```

### Database Chyby
```bash
# Skontrolovať database connection
curl http://localhost:8000/api/database/stats
```

---

## 📊 Checklist Testovania

### Základné Funkcie
- [ ] Health check funguje
- [ ] Frontend sa načíta
- [ ] Vyhľadávanie SK IČO funguje
- [ ] Vyhľadávanie CZ IČO funguje
- [ ] Graf sa zobrazuje správne
- [ ] Detail panel zobrazuje správne dáta

### Export Funkcie
- [ ] CSV export funguje
- [ ] JSON export funguje
- [ ] PDF export funguje
- [ ] Excel export funguje (iba Pro/Enterprise)

### Nové Funkcie
- [ ] Excel Export endpoint funguje
- [ ] Batch Export endpoint funguje
- [ ] Redis Cache funguje (ak je nainštalovaný)
- [ ] Analytics Dashboard funguje (iba Enterprise)
- [ ] Favorites System funguje

### API Endpoints
- [ ] `/api/health` - OK
- [ ] `/api/search` - OK
- [ ] `/api/cache/stats` - OK
- [ ] `/api/database/stats` - OK
- [ ] `/api/export/excel` - OK (iba Pro/Enterprise)
- [ ] `/api/export/batch-excel` - OK (iba Enterprise)

---

## 🐛 Známe Problémy

### Backend nebeží
```bash
# Skontrolovať, či port 8000 nie je obsadený
lsof -ti:8000

# Skontrolovať logy
tail -f logs/backend.log
```

### Frontend nebeží
```bash
# Skontrolovať, či port 3000 nie je obsadený
lsof -ti:8009

# Skontrolovať logy
tail -f logs/frontend.log
```

### Database Connection Error
```bash
# Skontrolovať, či PostgreSQL beží
# Skontrolovať DATABASE_URL v .env
```

---

## 📝 Poznámky

- **Excel Export** vyžaduje Pro alebo Enterprise účet
- **Batch Export** vyžaduje Enterprise účet
- **Redis Cache** je voliteľný - systém funguje aj bez neho
- **Analytics Dashboard** je dostupný iba pre Enterprise používateľov

---

**Status:** ✅ Pripravené na testovanie  
**Posledná aktualizácia:** December 20, 2024

