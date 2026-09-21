# Inštrukcie: Odinštalovanie isort Extension

## Problém
isort extension (`ms-python.isort`) nie je kompatibilný s Python 3.14 a spôsobuje chyby.

## Riešenie: Odinštalovanie Extensionu

### Krok 1: Otvoriť Extensions Panel
1. Stlač `Cmd+Shift+X` (Mac) alebo `Ctrl+Shift+X` (Windows/Linux)
2. Alebo klikni na ikonu Extensions v sidebar

### Krok 2: Nájsť isort Extension
1. Vyhľadaj "isort" v search boxe
2. Nájdeš "isort" od Microsoft (`ms-python.isort`)

### Krok 3: Odinštalovať
1. Klikni na gear icon (⚙️) vedľa extensionu
2. Vyber "Uninstall"
3. Alebo klikni na "Uninstall" button

### Krok 4: Reštart Cursor
1. Stlač `Cmd+Q` (Mac) alebo `Ctrl+Q` (Windows/Linux) na ukončenie
2. Spusti Cursor znova

## Alternatíva: Použiť Ruff

Ruff extension (`charliermarsh.ruff`) už je nainštalovaný a funguje:
- ✅ Kompatibilný s Python 3.14
- ✅ Automaticky formátuje importy
- ✅ Rýchlejší ako isort

### Overenie Ruff
1. Otvor Python súbor
2. Stlač `Cmd+Shift+P` (Mac) alebo `Ctrl+Shift+P` (Windows/Linux)
3. Napíš "Format Document"
4. Ruff by mal formátovať súbor

## Workspace Settings

Workspace settings sú už nakonfigurované:
- `isort.enabled: false` - Zakazuje isort
- `ruff.enable: true` - Povoluje Ruff
- `ruff.organizeImports: true` - Ruff organizuje importy

## Po odinštalovaní

Po odinštalovaní isort extensionu:
- ✅ Chyby sa prestanú zobrazovať
- ✅ Ruff bude fungovať namiesto isort
- ✅ Importy budú automaticky formátované Ruffom

