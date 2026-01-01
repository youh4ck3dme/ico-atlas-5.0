# 📘 ILUMINATI SYSTEM - Enterprise Business Intelligence Platform

**Verzia:** 5.0 (Enterprise Edition)  
**Status:** ~95% dokončené | **Test Coverage:** 85%  
**Posledná aktualizácia:** December 2024

## Vízia Produktu

Cieľ: Poskytnúť malým a stredným podnikom (SME) v regióne V4 nástroj podnikovej rozviedky (Business Intelligence), ktorý bol doteraz dostupný len bankám a veľkým korporáciám.

**USP:** Agregácia dát zo 4 krajín do jedného grafu v reálnom čase. Na rozdiel od konkurencie, ktorá často ponúka len statické výpisy, ILUMINATE SYSTEM odhaľuje skryté vzťahy naprieč hranicami na jedno kliknutie.

## Technická Architektúra

### Frontend
- **Technológia:** React 18 (Vite) + Tailwind CSS
- **Vizualizácia:** react-force-graph-2d pre interaktívne grafy
- **State Management:** React Context (AuthContext)
- **Performance:** Code splitting, memoization, lazy loading

### Backend
- **Technológia:** Python 3.10+ s FastAPI
- **Integrácie:** 
  - 🇸🇰 SK: RPO (Slovensko.Digital)
  - 🇨🇿 CZ: ARES (Finančná správa)
  - 🇵🇱 PL: KRS + CEIDG + Biała Lista
  - 🇭🇺 HU: NAV Online
- **Database:** PostgreSQL pre históriu, cache a analytics
- **Architektúra:** Modulárny monolit pripravený na mikroservisy
- **Payment:** Stripe integration pre subscriptions

## Inštalácia a Spustenie

### Predpoklady
- Python 3.10+ s pip
- Node.js 18+ s npm
- Git
- Docker & Docker Compose (voliteľné, pre containerizované spustenie)
- PostgreSQL (ak nepoužívate Docker)
- Redis (voliteľné, pre distributed caching)

### Krok 1: Backend Setup

```bash
cd backend

# Vytvorenie izolovaného prostredia
python -m venv venv

# Aktivácia prostredia
# Mac/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Inštalácia závislostí
pip install -r requirements.txt

# Spustenie vývojového servera
python main.py
```

Backend bude dostupný na `http://localhost:8000`.  
API dokumentácia: `http://localhost:8000/docs`

### Krok 2: Frontend Setup

```bash
cd frontend

# Inštalácia balíčkov
npm install

# Spustenie vývojového servera
npm run dev
```

Frontend bude dostupný na `http://localhost:5173`

### Krok 3: Testovanie

1. Otvorte prehliadač na `http://localhost:5173`
2. Do vyhľadávacieho poľa zadajte názov firmy (napr. "Agrofert")
3. Skontrolujte konzolu prehliadača (F12) a terminál backendu, či prebehla komunikácia

## Štruktúra Projektu

```
DIMITRI-CHECKER/
├── backend/
│   ├── main.py            # ILUMINATE SYSTEM Engine (FastAPI)
│   ├── requirements.txt   # Python závislosti
│   ├── pyrightconfig.json # Python linter konfigurácia
│   └── venv/             # Python virtual environment
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   ├── dist/             # Production build
│   ├── node_modules/     # Node.js závislosti
│   └── src/
│       ├── main.jsx
│       ├── index.css
│       ├── App.jsx        # Router a hlavná aplikácia
│       ├── components/
│       │   ├── Footer.jsx      # Footer s linkmi na právne dokumenty
│       │   ├── Layout.jsx      # Layout wrapper s footerom
│       │   └── Disclaimer.jsx  # Disclaimer komponenta
│       └── pages/
│           ├── HomePage.jsx              # Hlavná stránka s vyhľadávaním
│           ├── TermsOfService.jsx        # VOP
│           ├── PrivacyPolicy.jsx        # GDPR zásady
│           ├── Disclaimer.jsx           # Vyhlásenie o zodpovednosti
│           ├── CookiePolicy.jsx         # Cookie Policy
│           └── DataProcessingAgreement.jsx  # DPA pre B2B
├── docs/                 # Dokumentácia
│   ├── README.md
│   ├── DESIGN_UPGRADE_PROMPT.md
│   ├── SERVER_STATUS.md
│   ├── TEST_ICO_GUIDE.md
│   └── TEST_REPORT.md
├── logs/                 # Log súbory
├── .vscode/              # VS Code konfigurácia
├── test_basic.py         # Základné testy
├── .gitignore
└── README.md
```

## Funkcionalita MVP

✅ **Implementované:**
- Frontend: Funkčný React UI s vyhľadávacím poľom a základným zobrazením výsledkov
- Backend: FastAPI server bežiaci lokálne
- Integrácia: Konektor pre český register ARES
- Vizualizácia: SVG graf s uzlami (firmy, osoby, adresy) a hranami (vzťahy)
- CORS: Zabezpečená komunikácia Frontend <-> Backend
- **Routing:** React Router pre navigáciu medzi stránkami
- **Právne dokumenty:** Kompletné stránky pre VOP, Privacy Policy, Disclaimer, Cookie Policy, DPA
- **Footer:** Footer s linkmi na všetky právne dokumenty dostupný na každej stránke
- **Disclaimer:** Automatické zobrazenie disclaimeru pod každým grafom
- **Authentication:** Login/Register s JWT tokens
- **User Dashboard:** Tier management, search history, usage statistics, favorite companies
- **Payment Integration:** Stripe checkout pre subscription upgrades
- **Enterprise Features:** API Keys Management, Webhooks Delivery System, ERP Integrations, Analytics Dashboard
- **Performance:** React.memo, useCallback, useMemo, code splitting
- **Offline Support:** Service Worker, PWA capabilities

## Roadmapa

### Fáza 1: MVP ✅ DOKONČENÉ
- [x] Frontend: Funkčný React UI
- [x] Backend: FastAPI server
- [x] Integrácia: ARES (CZ)
- [x] Lokálne prepojenie: CORS, porty
- [x] Právne dokumenty: VOP, Privacy Policy, Disclaimer, Cookie Policy, DPA
- [x] Footer s linkmi na dokumenty
- [x] Disclaimer pod grafom

### Fáza 2: Persistence & Graph ✅ DOKONČENÉ
- [x] Databáza: PostgreSQL
- [x] SK Integrácia: RPO cez Ekosystém Slovensko.Digital
- [x] PL Integrácia: KRS + CEIDG + Biała Lista
- [x] HU Integrácia: NAV Online
- [x] Vizualizácia: react-force-graph-2d

### Fáza 3: Risk Intelligence ✅ DOKONČENÉ
- [x] Dlhové registre: Finančná správa SK/CZ
- [x] Fraud Detection: White Horse Detector
- [x] Reporting: PDF reporty
- [x] Enhanced risk scoring algoritmus

### Fáza 4: Monetizácia a Škálovanie ✅ DOKONČENÉ
- [x] Platby: Stripe integrácia
- [x] Auth: Používateľské účty (JWT)
- [x] Subscription tiers: Free/Pro/Enterprise
- [x] User Dashboard
- [x] Rate limiting podľa tieru
- [x] Obľúbené firmy (Favorites) ✅ DOKONČENÉ

### Fáza 5: Enterprise Features ✅ DOKONČENÉ
- [x] API Keys Management (backend + frontend)
- [x] Webhooks Delivery System (backend + frontend)
- [x] User Dashboard s Enterprise features
- [x] HMAC SHA256 signatures pre webhooks
- [x] IP whitelisting pre API keys
- [x] ERP integrácie (SAP, Pohoda, Money S3) ✅ DOKONČENÉ
- [x] Analytics Dashboard (backend + frontend) ✅ DOKONČENÉ

## Bezpečnosť

- **Rate Limiting:** ✅ Token Bucket algoritmus implementovaný
- **GDPR:** ✅ Spracovávame výhradne verejne dostupné dáta + Consent management
- **Proxy Rotation:** ✅ Pre registre bez oficiálneho API
- **Authentication:** ✅ JWT-based authentication s bcrypt password hashing
- **API Security:** ✅ HMAC SHA256 signatures pre webhooks
- **Tier-based Access:** ✅ Enterprise features len pre Enterprise tier

## Právne dokumenty

Všetky právne dokumenty sú dostupné v aplikácii cez footer alebo priamo na:
- `/vop` - Všeobecné obchodné podmienky
- `/privacy` - Zásady ochrany osobných údajov (GDPR)
- `/disclaimer` - Vyhlásenie o odmietnutí zodpovednosti
- `/cookies` - Cookie Policy
- `/dpa` - Data Processing Agreement (pre B2B klientov)

**Dôležité:** Pred spustením produkcie nezabudnite:
1. Vyplniť kontaktné údaje (e-maily, adresy) v dokumentoch
2. Dodať IČO a názov s.r.o. do Privacy Policy a DPA
3. Skontrolovať dokumenty s právnikom
4. Implementovať checkbox pri registrácii (súhlas s VOP a Privacy Policy)

## Licencia

Tento projekt je vo vývoji. Všetky práva vyhradené.

## Changelog

### Verzia 5.0 (December 2024) - Enterprise Edition
- ✅ **Authentication & Monetization:** Kompletná implementácia (Login, Register, Dashboard, Stripe)
- ✅ **Enterprise Features:** API Keys Management a Webhooks Delivery System
- ✅ **V4 Integrations:** SK (RPO), CZ (ARES), PL (KRS + CEIDG + Biała Lista), HU (NAV)
- ✅ **Performance:** Frontend a backend optimalizácie (memoization, code splitting, connection pooling)
- ✅ **Security:** JWT authentication, HMAC signatures, rate limiting, tier-based access
- ✅ **Documentation:** Kompletná dokumentácia (Developer Guide, Deployment Guide, Architecture)

### Verzia 4.0 (November 2024)
- ✅ Risk Intelligence s dlhovými registrami
- ✅ PDF export reportov
- ✅ Circuit Breaker pattern
- ✅ Proxy rotation

### Verzia 3.0 (October 2024)
- ✅ PostgreSQL databáza
- ✅ Cross-border integrácie (V4)
- ✅ Force-directed graph vizualizácia

## Kontakt

Pre otázky a podporu kontaktujte vývojový tím.

