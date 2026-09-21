# 🚀 IČO ATLAS 5.0 – GitHub & Deployment

## ✅ Čo bolo pripravené

1. ✅ **vercel.json** – Vercel konfigurácia (experimentálne)
2. ✅ **railway.json** – Railway konfigurácia (odporúčané)
3. ✅ **.vercelignore** – Vercel ignore súbory
4. ✅ **.github/workflows/tests.yml** – GitHub Actions CI/CD
5. ✅ **DEPLOYMENT.md** – Kompletný deployment guide
6. ✅ **GITHUB_SETUP.md** – GitHub setup inštrukcie
7. ✅ **DEPLOY_QUICKSTART.md** – Rýchly štart
8. ✅ **deploy.sh** – Deployment script

---

## 📦 GitHub Upload (5 minút)

### Rýchly spôsob:

```bash
cd ico-atlas-5.0

# 1. Pridať súbory
git add .

# 2. Commit
git commit -m "feat: Complete IČO ATLAS 5.0 implementation"

# 3. Vytvoriť repo na GitHub.com a potom:
git remote add origin https://github.com/TVOJE_USERNAME/ico-atlas-5.0.git
git branch -M main
git push -u origin main
```

**Alebo použij script:**
```bash
./deploy.sh
```

---

## ☁️ Deployment (Odporúčané: Railway)

### Railway (Najlepšia voľba pre Laravel)

1. **Vytvor účet:** https://railway.app → Login with GitHub
2. **New Project** → **Deploy from GitHub repo**
3. **Vyber** `ico-atlas-5.0`
4. **Pridaj Environment Variables:**
   ```
   APP_ENV=production
   APP_KEY=base64:... (vygeneruj: php artisan key:generate --show)
   APP_DEBUG=false
   ICOATLAS_ORSR_STUB=true
   ```
5. **Hotovo!** Railway automaticky deployne aplikáciu

### Vercel (Experimentálne)

⚠️ **Poznámka:** Vercel má obmedzenú podporu pre PHP/Laravel. Odporúčam Railway.

```bash
npm i -g vercel
vercel login
vercel
```

---

## 📋 Environment Variables

### Pre Railway/Vercel pridaj:

```env
APP_ENV=production
APP_KEY=base64:... (vygeneruj)
APP_DEBUG=false
APP_URL=https://your-app.railway.app
ICOATLAS_ORSR_STUB=true
ICOATLAS_CACHE_TTL_HOURS=12
ICOATLAS_HTTP_TIMEOUT=10
```

---

## ✅ Checklist

### Pred uploadom na GitHub:
- [ ] `git add .`
- [ ] `git commit -m "..." `
- [ ] Vytvoriť GitHub repo
- [ ] `git push`

### Pred deploymentom:
- [ ] `php artisan test` – všetky testy OK
- [ ] `npm run build` – frontend zbuildovaný
- [ ] `APP_KEY` vygenerovaný
- [ ] Environment variables pripravené

### Po deploymente:
- [ ] Testovať API: `curl https://your-app.com/api/company/search?ico=52374220`
- [ ] Skontrolovať logy
- [ ] Overiť cache

---

## 🔗 Dokumentácia

- **DEPLOYMENT.md** – Kompletný guide
- **GITHUB_SETUP.md** – GitHub inštrukcie
- **DEPLOY_QUICKSTART.md** – Rýchly štart

---

**Odporúčanie:** Použi **Railway** pre najjednoduchší deployment! 🚂

