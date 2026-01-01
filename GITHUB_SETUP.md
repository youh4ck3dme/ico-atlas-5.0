# 📦 GitHub Setup – IČO ATLAS 5.0

## Rýchly štart

### 1. Skontrolovať Git status

```bash
cd ico-atlas-5.0
git status
```

### 2. Pridať všetky súbory

```bash
git add .
```

### 3. Vytvoriť commit

```bash
git commit -m "feat: Complete IČO ATLAS 5.0 implementation

- Backend API with ORSR/ZRSR/RÚZ providers
- Frontend with Alpine.js and Tailwind CSS
- 12-field API contract
- Region resolution (PSČ → okres/kraj)
- Comprehensive test suite
- PWA support
- Documentation"
```

### 4. Vytvoriť GitHub Repository

#### Možnosť A: Cez GitHub Web UI

1. Choď na https://github.com/new
2. Repository name: `ico-atlas-5.0`
3. Description: `🇸🇰 Advanced company lookup PWA for Slovakia - IČO ATLAS 5.0`
4. Public / Private (podľa preferencie)
5. **NEOZAČÍNAJ** s README, .gitignore alebo licenciou
6. Klikni "Create repository"

#### Možnosť B: Cez GitHub CLI

```bash
# Ak máš nainštalovaný GitHub CLI
gh repo create ico-atlas-5.0 \
  --public \
  --description "🇸🇰 Advanced company lookup PWA for Slovakia - IČO ATLAS 5.0" \
  --source=. \
  --remote=origin \
  --push
```

#### Možnosť C: Manuálne

```bash
# Pridaj remote (nahraď TVOJE_USERNAME)
git remote add origin https://github.com/TVOJE_USERNAME/ico-atlas-5.0.git

# Push na GitHub
git branch -M main
git push -u origin main
```

### 5. Overenie

```bash
git remote -v
git log --oneline -5
```

---

## 📝 GitHub Repository Settings

### Topics (tags)

Pridaj tieto topics v GitHub UI:
- `laravel`
- `php`
- `slovakia`
- `company-lookup`
- `pwa`
- `api`
- `tailwindcss`
- `alpinejs`

### Description

```
🇸🇰 Advanced company lookup PWA for Slovakia. Real-time data from ORSR, ZRSR, and RÚZ. 12-field company profile with district and region resolution.
```

### Website (ak máš deployment)

```
https://ico-atlas-5-0.railway.app
```

---

## 🔄 Ďalšie Commity

### Po zmene kódu:

```bash
git add .
git commit -m "feat: Add new feature"  # alebo "fix: Fix bug"
git push
```

### Commit message konvencie:

- `feat:` - nová funkcionalita
- `fix:` - oprava chyby
- `docs:` - zmena v dokumentácii
- `test:` - pridané/upravené testy
- `refactor:` - refaktoring kódu
- `chore:` - údržba (dependencies, config)

---

## ✅ Hotovo!

Tvoj projekt je teraz na GitHube! 🎉

**Next steps:**
1. Pridaj collaborators (ak potrebuješ)
2. Nastav GitHub Actions pre CI/CD (voliteľné)
3. Vytvor Issues pre tracking úloh
4. Pridaj GitHub Pages pre dokumentáciu (voliteľné)
