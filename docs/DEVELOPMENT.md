# Development Guide

## React DevTools

### Čo to je?
React DevTools je rozšírenie pre prehliadač, ktoré umožňuje:
- Debug React komponentov
- Kontrolovať props a state
- Profilovať výkon
- Sledovať React component tree

### Ako nainštalovať

#### Chrome / Edge
1. Otvorte Chrome Web Store
2. Vyhľadajte "React Developer Tools"
3. Nainštalujte: https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi

#### Firefox
1. Otvorte Firefox Add-ons
2. Vyhľadajte "React Developer Tools"
3. Nainštalujte: https://addons.mozilla.org/en-US/firefox/addon/react-devtools/

#### Safari
- Odporúčame použiť Chrome alebo Firefox pre vývoj
- React DevTools pre Safari nie je oficiálne podporované

### Použitie

1. **Otvorte DevTools** (F12 alebo Cmd+Option+I)
2. **Nájdite záložku "Components"** - zobrazí React component tree
3. **Nájdite záložku "Profiler"** - pre profilovanie výkonu

### Výhody

- ✅ Lepšie debugovanie komponentov
- ✅ Profilovanie výkonu aplikácie
- ✅ Inspekcia props a state
- ✅ Sledovanie state changes v reálnom čase
- ✅ Identifikácia pomalých komponentov

### Varovanie v konzole

Ak vidíte varovanie:
```
Download the React DevTools for a better development experience
```

To je len informačné varovanie - aplikácia funguje normálne aj bez DevTools. DevTools sú voliteľné, ale odporúčané pre vývoj.

## Vite Dev Server

### Spustenie
```bash
cd frontend
npm run dev
```

### Hot Module Replacement (HMR)
- Automatické obnovenie pri zmene súborov
- Rýchlejšie development
- Zachováva state komponentov

### Troubleshooting

#### Cache problémy
```bash
cd frontend
rm -rf node_modules/.vite
npm run dev
```

#### Port už používaný
```bash
# Zmeň port v vite.config.js
server: {
  port: 5174
}
```

## Backend Development

### Spustenie
```bash
cd backend
source venv/bin/activate
python main.py
```

### API Dokumentácia
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Debugging
- Použite `print()` pre logging
- FastAPI automaticky zobrazuje chyby v response
- Skontrolujte konzolu pre backend logy

## Code Quality

### Linting
```bash
# Backend (Pyright)
# Automaticky v VS Code

# Frontend (ESLint - ak je nainštalovaný)
cd frontend
npm run lint
```

### Formatting
- Backend: Black alebo autopep8
- Frontend: Prettier (ak je nainštalovaný)

## Git Workflow

### Commit Messages
```
feat: Pridaná HU integrácia
fix: Opravený ForceGraph links
docs: Aktualizovaná dokumentácia
refactor: Refaktorizácia cache systému
```

### Branches
- `main` - produkčná verzia
- `develop` - development verzia
- `feature/*` - nové funkcie
- `fix/*` - opravy chýb

## Testing

### Backend Tests
```bash
cd backend
python test_basic.py
```

### Frontend Tests
```bash
cd frontend
npm test  # Ak je nastavený
```

### Manual Testing
1. Spusti oba servery (`./start.sh`)
2. Otvor http://localhost:5173
3. Testuj všetky funkcie
4. Skontroluj konzolu pre chyby

## Performance

### Frontend
- Build produkčnej verzie: `npm run build`
- Kontrola veľkosti bundle: `npm run build` (zobrazí veľkosti)
- Lazy loading pre routes (ak je implementovaný)

### Backend
- Cache pre API odpovede (24h TTL)
- Rate limiting (ak je implementovaný)
- Connection pooling (ak používa databázu)

## Deployment

### Frontend
```bash
cd frontend
npm run build
# Upload dist/ do web servera
```

### Backend
```bash
cd backend
# Použiť gunicorn alebo uvicorn pre produkciu
gunicorn main:app --workers 4 --bind 0.0.0.0:8000
```

## Useful Commands

```bash
# Spustenie oboch serverov
./start.sh

# Zastavenie serverov
./stop.sh

# Backend health check
curl http://localhost:8000/api/health

# Cache stats
curl http://localhost:8000/api/cache/stats

# Frontend build
cd frontend && npm run build
```

