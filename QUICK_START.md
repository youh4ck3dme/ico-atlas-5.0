# 🚀 ILUMINATI SYSTEM - Quick Start

## ✅ Problémy vyriešené

- ✅ Port 8000 uvoľnený
- ✅ Backend server spustený
- ✅ Start/Stop skripty vytvorené

## 📋 Spustenie

### Automatický spôsob (odporúčané)

```bash
./start.sh
```

Toto spustí oba servery (backend + frontend) automaticky.

### Manuálny spôsob

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 🛑 Zastavenie

```bash
./stop.sh
```

Alebo manuálne:
```bash
pkill -f 'python.*main.py'
pkill -f 'vite'
```

## 🌐 URL adresy

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

## 🧪 Testovanie

### Testovacie IČO:

- **SK:** `88888888` (testovacie simulované dáta)
- **CZ:** `27074358` (Agrofert - reálne ARES API)
- **PL:** `0000123456` (9-10 miestne KRS - fallback dáta)

### Príklad použitia:

1. Otvorte http://localhost:5173
2. Zadajte IČO (napr. `88888888`)
3. Kliknite "Overiť subjekt"
4. Zobrazí sa graf s risk analýzou

## ⚠️ Riešenie problémov

### Port 8000 už obsadený:
```bash
./stop.sh
# alebo
pkill -f 'python.*main.py'
lsof -ti:8000 | xargs kill -9
```

### Port 5173 už obsadený:
```bash
pkill -f 'vite'
lsof -ti:5173 | xargs kill -9
```

### Backend sa nespustí:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend sa nespustí:
```bash
cd frontend
npm install
npm run dev
```

## 📊 Funkcie

✅ **Podporované krajiny:**
- 🇨🇿 Česká republika (ARES)
- 🇸🇰 Slovensko (RPO)
- 🇵🇱 Poľsko (KRS)

✅ **Risk Intelligence:**
- White Horse Detector
- Detekcia karuselových štruktúr
- Detekcia virtuálnych sídel
- Vylepšený risk scoring

✅ **Export:**
- CSV
- PDF
- JSON

---

*Posledná aktualizácia: December 2024*

