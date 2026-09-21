# Prompt: Vyčistenie projektu a inštalácia balíčkov/extensionov

## Úloha
Vyčisti projekt od duplicít, doinštaluj správne balíčky a VS Code extensiony, a over, že všetko funguje správne.

## Krok 1: Vyčistenie duplicít

### 1.1 Python cache súbory
- Nájdi a vymaž všetky `__pycache__` adresáre v projekte
- Nájdi a vymaž všetky `.pyc`, `.pyo`, `.pyd` súbory
- Skontroluj, či `.gitignore` správne ignoruje tieto súbory

### 1.2 Node.js cache a build súbory
- Skontroluj, či `frontend/node_modules` je v `.gitignore`
- Skontroluj, či `frontend/dist` je v `.gitignore`
- Vymaž `frontend/.vite` cache ak existuje
- Vymaž `frontend/.cache` ak existuje

### 1.3 Duplicitné dokumenty
- Skontroluj `docs/` adresár na duplicitné alebo zastarané dokumenty
- Identifikuj dokumenty, ktoré sú duplicitné alebo už nie sú potrebné
- Navrhni, ktoré dokumenty možno zmazať alebo zlúčiť

### 1.4 Backup súbory
- Skontroluj `backups/` adresár
- Identifikuj staré backup súbory, ktoré možno zmazať (ponechaj len najnovšie)

### 1.5 Log súbory
- Skontroluj `logs/` adresáre
- Vymaž staré log súbory (ponechaj len aktuálne ak sú potrebné)
- Over, či `.gitignore` ignoruje log súbory

## Krok 2: Python balíčky (Backend)

### 2.1 Kontrola requirements.txt
- Skontroluj `backend/requirements.txt`
- Over, či všetky závislosti sú správne špecifikované s verziami
- Identifikuj chýbajúce alebo zastarané balíčky

### 2.2 Inštalácia Python balíčkov
- Aktivuj `backend/venv` virtuálne prostredie
- Spusti `pip install --upgrade pip`
- Spusti `pip install -r backend/requirements.txt`
- Over, či všetky balíčky sa nainštalovali bez chýb
- Spusti `pip list` a over verzie nainštalovaných balíčkov

### 2.3 Kontrola importov
- Skontroluj, či všetky importy v Python súboroch sú správne
- Identifikuj chýbajúce alebo nepotrebné importy
- Oprav akékoľvek problémy s importmi

## Krok 3: Node.js balíčky (Frontend)

### 3.1 Kontrola package.json
- Skontroluj `frontend/package.json`
- Over, či všetky závislosti sú správne špecifikované
- Identifikuj chýbajúce alebo zastarané balíčky
- Skontroluj, či `prop-types` je správne nainštalovaný (bol problém s ESM/CommonJS)

### 3.2 Inštalácia Node.js balíčkov
- Prejdi do `frontend/` adresára
- Spusti `npm install` alebo `npm ci` (pre čistú inštaláciu)
- Over, či všetky balíčky sa nainštalovali bez chýb
- Spusti `npm list` a over verzie nainštalovaných balíčkov

### 3.3 Kontrola závislostí
- Spusti `npm audit` a oprav akékoľvek bezpečnostné problémy
- Spusti `npm outdated` a identifikuj zastarané balíčky (voliteľné upgrade)

## Krok 4: VS Code Extensiony

### 4.1 Kontrola .vscode/extensions.json
- Skontroluj, či `.vscode/extensions.json` obsahuje všetky potrebné extensiony:
  - Python: `ms-python.python`, `ms-python.vscode-pylance`
  - Formátovanie: `ms-python.black-formatter`, `ms-python.isort`, `charliermarsh.ruff`
  - Frontend: `dbaeumer.vscode-eslint`, `esbenp.prettier-vscode`, `bradlc.vscode-tailwindcss`
  - Testovanie: `hbenl.vscode-test-explorer`, `littlefoxteam.vscode-python-test-adapter`
  - Ostatné: `usernamehw.errorlens`, `eamodio.gitlens`, `gruntfuggly.todo-tree`

### 4.2 Inštalácia extensionov
- Skontroluj, ktoré extensiony sú už nainštalované
- Navrhni inštaláciu chýbajúcich extensionov
- Over, či všetky extensiony sú kompatibilné s aktuálnou verziou VS Code/Cursor

## Krok 5: Overenie funkčnosti

### 5.1 Backend testy
- Spusti `python3 tests/test_backend_api.py` a over, či všetky testy prechádzajú
- Spusti `python3 tests/test_new_features.py` a over, či všetky testy prechádzajú
- Spusti `python3 tests/test_performance.py` a over, či všetky testy prechádzajú

### 5.2 Frontend testy
- Spusti `cd frontend && npm test` a over, či všetky testy prechádzajú
- Spusti `cd frontend && npm run build` a over, či build prechádza bez chýb

### 5.3 Linter kontrola
- Spusti Python linter (ruff/pylint) a oprav akékoľvek problémy
- Spusti ESLint pre frontend a oprav akékoľvek problémy

### 5.4 Import kontrola
- Over, či všetky importy fungujú správne
- Identifikuj a oprav akékoľvek problémy s importmi

## Krok 6: Finálna kontrola

### 6.1 Git status
- Spusti `git status` a over, či nie sú žiadne neočakávané zmeny
- Skontroluj, či `.gitignore` správne ignoruje všetky cache a build súbory

### 6.2 Dokumentácia
- Aktualizuj `README.md` ak sú potrebné zmeny v inštalácii
- Aktualizuj `docs/DEVELOPER_GUIDE.md` ak sú potrebné zmeny

### 6.3 Súhrn
- Vytvor súhrn všetkých vykonaných zmien
- Vytvor zoznam všetkých nainštalovaných balíčkov a extensionov
- Identifikuj akékoľvek známe problémy alebo obmedzenia

## Očakávaný výsledok

Po dokončení by mal projekt:
- ✅ Byť vyčistený od všetkých duplicít a cache súborov
- ✅ Mať všetky Python balíčky správne nainštalované v `backend/venv`
- ✅ Mať všetky Node.js balíčky správne nainštalované v `frontend/node_modules`
- ✅ Mať všetky VS Code extensiony odporúčané v `.vscode/extensions.json`
- ✅ Prechádzať všetky testy bez chýb
- ✅ Mať čistý git status (len zmeny v `.gitignore` ak boli potrebné)

## Poznámky

- **Python venv**: Uisti sa, že používaš správne virtuálne prostredie (`backend/venv`)
- **Node.js verzia**: Over, či používaš kompatibilnú verziu Node.js (odporúčané: Node.js 18+)
- **VS Code/Cursor**: Over, či máš najnovšiu verziu editora
- **Backup**: Pred vyčistením vytvor backup dôležitých súborov ak je to potrebné

