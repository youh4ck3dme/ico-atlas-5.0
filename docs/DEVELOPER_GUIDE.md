# 👨‍💻 ILUMINATI SYSTEM - Developer Guide

Kompletný návod pre vývojárov pracujúcich na ILUMINATI SYSTEM projekte.

## 📋 Obsah

1. [Architektúra](#architektúra)
2. [Setup vývojového prostredia](#setup-vývojového-prostredia)
3. [Štruktúra projektu](#štruktúra-projektu)
4. [Backend vývoj](#backend-vývoj)
5. [Frontend vývoj](#frontend-vývoj)
6. [Testovanie](#testovanie)
7. [API integrácie](#api-integrácie)
8. [Best practices](#best-practices)
9. [Debugging](#debugging)

## 🏗️ Architektúra

### Vysoká úroveň

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Frontend  │ ──────> │   Backend   │ ──────> │  External   │
│   (React)   │  HTTP   │  (FastAPI)  │  HTTP   │     APIs    │
└─────────────┘         └─────────────┘         └─────────────┘
                              │
                              ▼
                        ┌─────────────┐
                        │  PostgreSQL  │
                        │  Database    │
                        └─────────────┘
```

### Komponenty

**Frontend:**
- React 18 s Vite
- Tailwind CSS pre styling
- React Router pre navigáciu
- react-force-graph-2d pre vizualizáciu grafu
- Service Worker pre PWA funkcionalitu

**Backend:**
- FastAPI framework
- SQLAlchemy pre databázu
- Modulárne služby (services/)
- Circuit Breaker pattern
- Rate limiting (Token Bucket)
- Proxy rotation pre externé API

**Databáza:**
- PostgreSQL pre históriu, cache a analytics
- In-memory cache pre rýchle odpovede

## 🛠️ Setup vývojového prostredia

### Predpoklady

- **Python:** 3.10+ (odporúčané 3.11)
- **Node.js:** 18+ (odporúčané 20+)
- **PostgreSQL:** 14+ (voliteľné pre lokálny vývoj)
- **Git:** Pre verzionovanie

### Krok 1: Klonovanie repozitára

```bash
git clone <repository-url>
cd DIMITRI-CHECKER
```

### Krok 2: Backend setup

```bash
cd backend

# Vytvorenie virtual environment
python3 -m venv venv

# Aktivácia (macOS/Linux)
source venv/bin/activate

# Aktivácia (Windows)
# venv\Scripts\activate

# Inštalácia závislostí
pip install -r requirements.txt

# Setup databázy (voliteľné)
./setup_database.sh
```

### Krok 3: Frontend setup

```bash
cd frontend

# Inštalácia závislostí
npm install

# Spustenie dev servera
npm run dev
```

### Krok 4: Environment premenné

Vytvorte `.env` súbor v `backend/`:

```env
# Databáza
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/iluminati_db

# Proxy (voliteľné)
PROXY_LIST=http://proxy1.com:8080,http://proxy2.com:8080

# API Keys (ak potrebné)
ARES_API_KEY=your_key_here
RPO_API_KEY=your_key_here
```

## 📁 Štruktúra projektu

```
DIMITRI-CHECKER/
├── backend/
│   ├── main.py                 # FastAPI aplikácia
│   ├── requirements.txt        # Python závislosti
│   ├── services/               # Modulárne služby
│   │   ├── sk_rpo.py          # Slovensko RPO integrácia
│   │   ├── cz_ares.py         # Česko ARES integrácia
│   │   ├── pl_krs.py          # Poľsko KRS integrácia
│   │   ├── hu_nav.py          # Maďarsko NAV integrácia
│   │   ├── cache.py           # Cache služba
│   │   ├── rate_limiter.py    # Rate limiting
│   │   ├── circuit_breaker.py # Circuit Breaker
│   │   ├── proxy_rotation.py  # Proxy rotation
│   │   ├── metrics.py         # Metríky
│   │   ├── performance.py     # Performance utilities
│   │   ├── risk_intelligence.py # Risk scoring
│   │   └── database.py        # PostgreSQL služba
│   └── venv/                  # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── main.jsx           # Entry point
│   │   ├── App.jsx            # Router
│   │   ├── pages/             # Stránky
│   │   ├── components/        # React komponenty
│   │   ├── hooks/             # Custom hooks
│   │   └── utils/             # Utility funkcie
│   ├── public/                # Statické súbory
│   └── package.json           # Node.js závislosti
├── tests/                     # Testy
│   ├── test_backend_api.py
│   ├── test_new_features.py
│   ├── test_performance.py
│   └── test_proxy_rotation.py
├── docs/                      # Dokumentácia
└── run_tests.sh              # Test script
```

## 🔧 Backend vývoj

### Pridanie novej krajiny

1. Vytvorte nový súbor v `backend/services/` (napr. `at_firmenbuch.py`)
2. Implementujte funkcie:
   - `fetch_<country>_<register>(identifier)` - získanie dát
   - `parse_<country>_<register>_data(data)` - parsovanie
   - `calculate_<country>_risk_score(data)` - risk scoring
   - `is_<country>_<identifier>(query)` - validácia

3. Importujte do `main.py` a pridajte do `search_company` endpointu

**Príklad:**

```python
# backend/services/at_firmenbuch.py
def fetch_firmenbuch_at(fnr: str) -> Optional[Dict]:
    """Získa dáta z rakúskeho Firmenbuch"""
    # Implementácia...
    pass

def is_austrian_fnr(query: str) -> bool:
    """Validuje rakúsky FNR"""
    return bool(re.match(r'^\d{6}[A-Z]$', query))
```

### Pridanie novej služby

1. Vytvorte súbor v `backend/services/`
2. Implementujte triedu/funkcie
3. Exportujte hlavné funkcie
4. Importujte do `main.py` podľa potreby

### API endpointy

Všetky endpointy sú v `main.py`:

- `GET /api/search` - Hlavné vyhľadávanie
- `GET /api/health` - Health check
- `GET /api/cache/stats` - Cache štatistiky
- `GET /api/metrics` - Metríky
- `GET /api/proxy/stats` - Proxy štatistiky

**Pridanie nového endpointu:**

```python
@app.get("/api/new-endpoint")
async def new_endpoint():
    """Popis endpointu"""
    return {"status": "ok"}
```

## 🎨 Frontend vývoj

### Pridanie novej stránky

1. Vytvorte komponentu v `frontend/src/pages/`
2. Pridajte route do `App.jsx`:

```jsx
import NewPage from './pages/NewPage';

// V App.jsx
<Route path="/new-page" element={<NewPage />} />
```

### Pridanie novej komponenty

1. Vytvorte súbor v `frontend/src/components/`
2. Exportujte komponentu
3. Importujte kde potrebné

**Príklad:**

```jsx
// frontend/src/components/NewComponent.jsx
import React from 'react';

export default function NewComponent({ prop1, prop2 }) {
  return (
    <div className="new-component">
      {/* Komponenta */}
    </div>
  );
}
```

### Styling

Používame **Tailwind CSS**. Utility-first prístup:

```jsx
<div className="bg-blue-500 text-white p-4 rounded-lg">
  Content
</div>
```

### State management

Pre jednoduché state používame React hooks (`useState`, `useEffect`). Pre komplexnejší state zvážte Context API alebo Zustand.

## 🧪 Testovanie

### Spustenie testov

```bash
# Všetky testy
./run_tests.sh

# Len backend testy
python3 tests/test_backend_api.py

# Len performance testy
python3 tests/test_performance.py
```

### Pridanie nového testu

1. Vytvorte test súbor v `tests/` alebo pridajte do existujúceho
2. Použite `unittest` alebo jednoduché assert testy

**Príklad:**

```python
def test_new_feature():
    """Test novej funkcionality"""
    result = new_function("input")
    assert result == "expected_output"
```

### Test coverage

Cieľ: **100% coverage** pre kritické služby.

## 🔌 API integrácie

### Pridanie novej API integrácie

1. Vytvorte službu v `backend/services/`
2. Použite `make_request_with_proxy()` pre HTTP volania
3. Implementujte error handling a fallback
4. Pridajte cache pre optimalizáciu

**Príklad:**

```python
from services.proxy_rotation import make_request_with_proxy
from services.cache import get, set, get_cache_key

def fetch_new_api(identifier: str):
    cache_key = get_cache_key(identifier, "new_api")
    cached = get(cache_key)
    if cached:
        return cached
    
    url = f"https://api.example.com/{identifier}"
    response = make_request_with_proxy(url)
    
    if response and response.status_code == 200:
        data = response.json()
        set(cache_key, data)
        return data
    
    return None
```

## ✅ Best practices

### Backend

- **Modulárnosť:** Každá služba v samostatnom súbore
- **Error handling:** Vždy používajte try/except
- **Logging:** Používajte `print()` pre debug, `log_error()` pre chyby
- **Type hints:** Vždy pridajte type hints
- **Docstrings:** Dokumentujte funkcie a triedy

### Frontend

- **Komponenty:** Malé, znovupoužiteľné komponenty
- **Performance:** Používajte `React.memo`, `useMemo`, `useCallback`
- **Accessibility:** Pridajte ARIA atribúty
- **SEO:** Meta tagy v `index.html`

### Git

- **Commits:** Popisné commit messages
- **Branches:** Feature branches pre nové funkcie
- **Code review:** Vždy review pred merge

## 🐛 Debugging

### Backend debugging

```python
# Pridajte debug printy
print(f"🔍 Debug: {variable}")

# Použite Python debugger
import pdb; pdb.set_trace()

# Skontrolujte logy
tail -f logs/app.log
```

### Frontend debugging

```javascript
// Console logy
console.log('Debug:', variable);

// React DevTools
// Nainštalujte React DevTools extension

// Network tab
// Skontrolujte API volania v DevTools
```

### Časté problémy

**Backend sa nespustí:**
- Skontrolujte, či je venv aktivovaný
- Skontrolujte, či sú nainštalované závislosti
- Skontrolujte port 8000 (nie je obsadený)

**Frontend sa nespustí:**
- Skontrolujte Node.js verziu
- Vymažte `node_modules` a `npm install` znova
- Skontrolujte port 5173

**API volania zlyhávajú:**
- Skontrolujte CORS nastavenia
- Skontrolujte network tab v DevTools
- Skontrolujte backend logy

## 📚 Ďalšie zdroje

- [FastAPI dokumentácia](https://fastapi.tiangolo.com/)
- [React dokumentácia](https://react.dev/)
- [Tailwind CSS dokumentácia](https://tailwindcss.com/)
- [PostgreSQL dokumentácia](https://www.postgresql.org/docs/)

---

*Posledná aktualizácia: December 2024*

