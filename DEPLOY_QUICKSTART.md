# 🚀 Quick Start – GitHub + Deployment

## 1️⃣ GitHub Upload (5 minút)

### Krok 1: Pridať súbory do Git

```bash
cd ico-atlas-5.0

# Skontrolovať status
git status

# Pridať všetky súbory
git add .

# Vytvoriť commit
git commit -m "feat: Complete IČO ATLAS 5.0 implementation"
```

### Krok 2: Vytvoriť GitHub Repository

**Možnosť A: Cez GitHub Web UI**
1. Choď na https://github.com/new
2. Repository name: `ico-atlas-5.0`
3. **NEOZAČÍNAJ** s README
4. Klikni "Create repository"

**Možnosť B: Cez GitHub CLI**
```bash
gh repo create ico-atlas-5.0 --public --source=. --remote=origin --push
```

**Možnosť C: Manuálne**
```bash
git remote add origin https://github.com/TVOJE_USERNAME/ico-atlas-5.0.git
git branch -M main
git push -u origin main
```

---

## 2️⃣ Deployment na Railway (Odporúčané)

### Prečo Railway?
- ✅ Bezplatný tier
- ✅ Výborná podpora pre Laravel
- ✅ Automatický deployment z GitHubu
- ✅ Jednoduché environment variables

### Krok 1: Vytvoriť Railway Account

1. Choď na https://railway.app
2. Klikni "Login with GitHub"
3. Autorizuj Railway prístup

### Krok 2: Deploy z GitHub

1. V Railway dashboard klikni "New Project"
2. Vyber "Deploy from GitHub repo"
3. Vyber `ico-atlas-5.0` repository
4. Railway automaticky detekuje Laravel a začne build

### Krok 3: Environment Variables

V Railway dashboard → Settings → Variables pridaj:

```
APP_ENV=production
APP_KEY=base64:... (vygeneruj cez: php artisan key:generate --show)
APP_DEBUG=false
APP_URL=https://your-app.railway.app
ICOATLAS_ORSR_STUB=true
ICOATLAS_CACHE_TTL_HOURS=12
ICOATLAS_HTTP_TIMEOUT=10
```

### Krok 4: Custom Domain (voliteľné)

1. V Railway → Settings → Networking
2. Pridaj custom domain
3. Railway automaticky nastaví SSL

---

## 3️⃣ Deployment na Vercel (Experimentálne)

⚠️ **Poznámka:** Vercel má obmedzenú podporu pre PHP/Laravel. Odporúčam Railway namiesto toho.

### Ak chceš skúsiť:

```bash
# Inštalovať Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd ico-atlas-5.0
vercel
```

**Problémy s Vercel:**
- PHP runtime je obmedzený
- Laravel potrebuje tradičný server
- Možné problémy s storage a cache

---

## 4️⃣ Alternatívy

### Render.com
1. https://render.com
2. "New Web Service"
3. Pripoj GitHub repo
4. Build Command: `cd ico-atlas && composer install && npm install && npm run build`
5. Start Command: `cd ico-atlas && php artisan serve --host=0.0.0.0 --port=$PORT`

### Fly.io
1. https://fly.io
2. `fly launch`
3. Automaticky vytvorí Dockerfile

### DigitalOcean App Platform
1. https://www.digitalocean.com/products/app-platform
2. "Create App" → "GitHub"
3. Vyber repo a branch
4. Automaticky detekuje Laravel

---

## ✅ Deployment Checklist

### Pred deploymentom:
- [ ] `git add .` a `git commit`
- [ ] `php artisan test` – všetky testy prechádzajú
- [ ] `npm run build` – frontend zbuildovaný
- [ ] `.env` obsahuje správne hodnoty
- [ ] `APP_KEY` je vygenerovaný

### Po deploymente:
- [ ] Skontrolovať API: `curl https://your-app.com/api/company/search?ico=52374220`
- [ ] Skontrolovať logy
- [ ] Overiť, že cache funguje
- [ ] Testovať rate limiting

---

## 🔗 Užitočné odkazy

- **Railway**: https://railway.app
- **Render**: https://render.com
- **GitHub**: https://github.com
- **Vercel**: https://vercel.com

---

**Odporúčanie:** Použi **Railway** pre najjednoduchší a najspoľahlivejší deployment! 🚂

