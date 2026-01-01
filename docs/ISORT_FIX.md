# Fix: isort Extension Incompatibility with Python 3.14

## Problém

isort extension (`ms-python.isort`) nie je kompatibilný s Python 3.14 kvôli zmene v `ast` module:

```
ImportError: cannot import name 'Str' from 'ast'
```

## Riešenie

Odstránený `ms-python.isort` z odporúčaných extensionov a nahradený `ruff`, ktorý:
- ✅ Je kompatibilný s Python 3.14
- ✅ Automaticky formátuje importy (funkcia isort)
- ✅ Je rýchlejší a modernější
- ✅ Už je v odporúčaných extensionoch

## Zmeny

1. **`.vscode/extensions.json`**:
   - Odstránený `"ms-python.isort"` z recommendations
   - Pridaný do `unwantedRecommendations`

2. **`.vscode/settings.json`**:
   - Odstránený `isort.interpreter` setting

## Alternatíva

Ak potrebuješ isort, môžeš:
1. Použiť Python 3.11 alebo 3.12 namiesto 3.14
2. Použiť ruff namiesto isort (odporúčané)
3. Spustiť isort manuálne z príkazového riadku

## Ruff konfigurácia

Ruff automaticky formátuje importy. Konfigurácia je v `pyproject.toml` alebo `.ruff.toml`:

```toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["I"]  # Import sorting
```

## Reštart

Po zmene je potrebné reštartovať Cursor/VS Code, aby sa zmeny prejavili.

