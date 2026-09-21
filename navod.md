# 📖 Návod na Inštaláciu a Spustenie - ILUMINATI SYSTEM

**Verzia:** 5.0 Enterprise Edition  
**Dátum:** 2025-12-20

---

## 🚀 Rýchly Štart

### Krok 1: Rozbalenie projektu

```bash
# Ak máte ZIP súbor, rozbaliť ho:
unzip v4.zip -d iluminati-system
cd iluminati-system
```

### Krok 2: Backend Setup

```bash
# Prejsť do backend adresára
cd backend

# Vytvoriť Python virtual environment
python3 -m venv venv

# Aktivovať virtual environment
# Na macOS/Linux:
source venv/bin/activate
# Na Windows:
# venv\Scripts\activate

# Nainštalovať Python závislosti
pip install -r requirements.txt
```

### Krok 3: Frontend Setup

```bash
# Prejsť do frontend adresára
cd ../frontend

# Nainštalovať Node.js závislosti
npm install
```

### Krok 4: Databáza Setup

```bash
# Vytvoriť PostgreSQL databázu
# (Ak nemáte PostgreSQL, použite Docker - pozri nižšie)

# Vytvoriť .env súbor v root adresári projektu
cd ..
cp .env.example .env

# Upraviť .env súbor:
# DATABASE_URL=postgresql://user:password@localhost:5432/iluminati_db
```

### Krok 5: Spustenie

#### Možnosť A: Použiť start.sh skript (najjednoduchšie)

```bash
# V root adresári projektu
chmod +x start.sh
./start.sh
```

#### Možnosť B: Manuálne spustenie

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # macOS/Linux
# alebo: venv\Scripts\activate  # Windows
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Krok 6: Prístup k aplikácii

- **Frontend:** http://localhost:8009
- **Backend API:** http://localhost:8000
- **API Dokumentácia:** http://localhost:8000/api/docs

---

## 🐳 Docker Setup (Odporúčané)

Ak máte Docker nainštalovaný, môžete spustiť celý projekt jedným príkazom:

```bash
# Spustiť všetky služby (PostgreSQL, Redis, Backend, Frontend)
docker-compose up -d

# Zobraziť logy
docker-compose logs -f

# Zastaviť služby
docker-compose down
```

Docker automaticky:
- Vytvorí PostgreSQL databázu
- Spustí Redis cache
- Spustí Backend API
- Spustí Frontend aplikáciu

---

## 📋 Systémové Požiadavky

### Backend
- **Python:** 3.10 alebo vyššie
- **PostgreSQL:** 14 alebo vyššie
- **Redis:** 7 alebo vyššie (voliteľné, pre cache)

### Frontend
- **Node.js:** 18 alebo vyššie
- **npm:** 9 alebo vyššie

### Docker (voliteľné)
- **Docker Desktop:** Najnovšia verzia
- **Docker Compose:** v2 alebo vyššie

---

## 🔧 Konfigurácia

### Environment Variables (.env)

Vytvorte `.env` súbor v root adresári projektu:

```env
# Database
DATABASE_URL=postgresql://iluminati_user:iluminati_password@localhost:5432/iluminati_db

# Redis (voliteľné, pre cache)
REDIS_URL=redis://localhost:6379/0

# JWT Secret Key (ZMEŇTE V PRODUKCII!)
SECRET_KEY=your-secret-key-change-in-production

# Stripe (voliteľné, pre platby)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Frontend URL
FRONTEND_URL=http://localhost:8009

# Backend URL
BACKEND_URL=http://localhost:8000
```

### PostgreSQL Setup

```bash
# Vytvoriť databázu
createdb iluminati_db

# Alebo pomocou psql:
psql -U postgres
CREATE DATABASE iluminati_db;
CREATE USER iluminati_user WITH PASSWORD 'iluminati_password';
GRANT ALL PRIVILEGES ON DATABASE iluminati_db TO iluminati_user;
\q
```

---

## 🧪 Testovanie

### Backend testy

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Frontend testy

```bash
cd frontend
npm test
```

### Všetky testy naraz

```bash
# Backend
cd backend && source venv/bin/activate && pytest tests/ -v

# Frontend
cd frontend && npm test
```

---

## 🔐 SSL/HTTPS Setup (Voliteľné)

Ak chcete používať HTTPS:

```bash
# Vytvoriť SSL adresár
mkdir -p ssl

# Vygenerovať self-signed certifikát
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# Backend a Frontend automaticky detekujú SSL certifikáty
```

Pozri `docs/SSL_SETUP.md` pre detailné inštrukcie.

---

## 📊 Funkcie

### Implementované funkcie:

✅ **V4 Krajiny:**
- 🇸🇰 Slovensko (ORSR, ZRSR, RUZ)
- 🇨🇿 Česko (ARES)
- 🇵🇱 Poľsko (KRS)
- 🇭🇺 Maďarsko (NAV)

✅ **Enterprise Features:**
- Analytics Dashboard
- Favorites System
- Excel Export
- API Keys Management
- Webhooks
- ERP Integrations

✅ **Security:**
- JWT Authentication
- Rate Limiting
- Circuit Breaker
- CORS Protection

✅ **Performance:**
- Redis Cache
- Database Connection Pooling
- Request Batching

---

## 🆘 Riešenie Problémov

### Backend sa nespustí

**Problém:** `ModuleNotFoundError`
```bash
# Riešenie: Nainštalujte závislosti
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Problém:** `Connection refused` (PostgreSQL)
```bash
# Riešenie: Skontrolujte, či PostgreSQL beží
# macOS:
brew services start postgresql
# Linux:
sudo systemctl start postgresql
# Windows:
# Spustiť PostgreSQL službu v Services
```

**Problém:** `Port 8000 already in use`
```bash
# Riešenie: Zastaviť proces na porte 8000
# macOS/Linux:
lsof -ti:8000 | xargs kill -9
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend sa nespustí

**Problém:** `Port 8009 already in use`
```bash
# Riešenie: Zastaviť proces na porte 8009
lsof -ti:8009 | xargs kill -9
```

**Problém:** `npm install` zlyhá
```bash
# Riešenie: Vymazať cache a nainštalovať znova
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS chyby

**Problém:** `Access-Control-Allow-Origin` error
```bash
# Riešenie: Skontrolujte CORS origins v backend/main.py
# Pridajte svoj frontend URL do origins listu
```

### Databázové chyby

**Problém:** `relation does not exist`
```bash
# Riešenie: Spustiť migrácie
cd backend
source venv/bin/activate
python -m alembic upgrade head
# Alebo manuálne vytvoriť tabuľky (pozri docs/DATABASE_SETUP.md)
```

---

## 📚 Dokumentácia

### Hlavné dokumenty:
- **README.md** - Prehľad projektu
- **QUICK_START.md** - Rýchly štart
- **TEST_REPORT.md** - Test report
- **SPECIAL_TESTS_REPORT.md** - Špeciálne testy

### Detailná dokumentácia (docs/):
- **DEVELOPER_GUIDE.md** - Príručka pre vývojárov
- **PRODUCTION_TESTING_PLAN.md** - Plán testovania
- **DATABASE_SETUP.md** - Nastavenie databázy
- **SSL_SETUP.md** - SSL konfigurácia
- **DEPLOYMENT_GUIDE.md** - Nasadenie do produkcie

---

## 🎯 Testovanie s Reálnym IČO

### Slovensko (SK)
```
52374220 - Tavira, s.r.o.
31333501 - Agrofert Holding a.s.
```

### Česko (CZ)
```
27074358 - Agrofert, a.s.
47114983 - ČEZ, a.s.
```

### Poľsko (PL)
```
0000123456 - Test KRS
```

### Maďarsko (HU)
```
12345678 - Test Adószám
```

**Testovanie:**
1. Otvoriť http://localhost:8009
2. Zadať IČO do vyhľadávacieho poľa
3. Kliknúť "Overiť subjekt"
4. Skontrolovať výsledky

---

## 🔄 Aktualizácia projektu

```bash
# Ak máte Git:
git pull origin main

# Aktualizovať závislosti:
cd backend && source venv/bin/activate && pip install -r requirements.txt --upgrade
cd ../frontend && npm update
```

---

## 📞 Podpora

Pre viac informácií:
- Pozri `docs/` adresár
- Skontrolujte `README.md`
- Pozri `QUICK_START.md` pre rýchly štart

---

## ✅ Checklist pred spustením

- [ ] Python 3.10+ nainštalovaný
- [ ] Node.js 18+ nainštalovaný
- [ ] PostgreSQL beží
- [ ] Redis beží (voliteľné)
- [ ] Backend závislosti nainštalované (`pip install -r requirements.txt`)
- [ ] Frontend závislosti nainštalované (`npm install`)
- [ ] `.env` súbor vytvorený a nakonfigurovaný
- [ ] Databáza vytvorená
- [ ] Porty 8000 a 8009 sú voľné

---

**Úspešné testovanie! 🚀**

*Posledná aktualizácia: 2025-12-20*

