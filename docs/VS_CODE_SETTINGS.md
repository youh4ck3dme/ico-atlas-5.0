# ⚙️ VS Code Nastavenia - Vysvetlenie

## Čo robia oznámenia

### 1. "Running Code Actions and Formatters..."
**Čo to je:**
- Automatické akcie, ktoré sa spúšťajú pri uložení súboru (Ctrl+S / Cmd+S)
- Formátuje kód podľa nastavených pravidiel
- Organizuje importy (zoraďuje, odstraňuje nepoužité)

**Kedy sa spúšťa:**
- Pri každom uložení Python súboru (`.py`)

---

### 2. "Applying code action 'Ruff: Organize imports'"
**Čo to je:**
- **Ruff** je moderný Python linter/formatter
- Automaticky organizuje importy:
  - Zoraďuje ich podľa štandardu (stdlib, third-party, local)
  - Odstraňuje nepoužité importy
  - Zoskupuje podobné importy

**Príklad:**
```python
# Pred:
from services.sk_ruz_provider import get_ruz_provider
import requests
from typing import Dict
from datetime import datetime

# Po:
from datetime import datetime
from typing import Dict

import requests

from services.sk_ruz_provider import get_ruz_provider
```

---

## Ako to vypnúť alebo upraviť

### Možnosť 1: Vypnúť organizovanie importov (odporúčané)
```json
{
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": "never"  // Zmeniť z "explicit" na "never"
    }
  }
}
```

### Možnosť 2: Vypnúť všetko formátovanie pri uložení
```json
{
  "[python]": {
    "editor.formatOnSave": false,  // Vypnúť formátovanie
    "editor.codeActionsOnSave": {}  // Vypnúť akcie
  }
}
```

### Možnosť 3: Vypnúť len Ruff organizovanie importov
```json
{
  "ruff.organizeImports": false  // Vypnúť Ruff organizovanie
}
```

### Možnosť 4: Nechať zapnuté, ale bez oznámení
- Oznámenia sú len informačné, kód sa stále formátuje
- Môžeš ich ignorovať - neovplyvňujú funkčnosť

---

## Aktuálne nastavenia

V `.vscode/settings.json` máš:
```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,  // ✅ Formátuje pri uložení
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"  // ✅ Organizuje importy
    }
  },
  "ruff.enable": true,
  "ruff.organizeImports": true
}
```

---

## Odporúčanie

**Pre produkciu:** Nechať zapnuté ✅
- Udržiava kód konzistentný
- Automaticky odstraňuje nepoužité importy
- Zoraďuje importy podľa štandardu

**Ak ťa to ruší:** Vypnúť len oznámenia (možnosť 4)
- Kód sa stále formátuje
- Len nevidíš oznámenia

---

*Posledná aktualizácia: December 20, 2024*

