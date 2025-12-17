# 🚀 IČO ATLAS 5.0 – Deployment Guide

## 📦 GitHub Setup

### 1. Inicializácia Git (ak ešte nie je)

```bash
cd ico-atlas-5.0
git init
git add .
git commit -m "Initial commit: IČO ATLAS 5.0 - Complete implementation"
```

### 2. Vytvorenie GitHub Repository

#### Cez GitHub Web UI:
1. Choď na https://github.com/new
2. Vytvor nový repository (napr. `ico-atlas-5.0`)
3. **NEOZAČÍNAJ** s README, .gitignore alebo licenciou (už máme)

#### Cez GitHub CLI (ak máš nainštalovaný):
```bash
gh repo create ico-atlas-5.0 --public --source=. --remote=origin --push
```

#### Alebo manuálne:
```bash
# Pridaj remote
git remote add origin https://github.com/TVOJE_USERNAME/ico-atlas-5.0.git

# Push na GitHub
git branch -M main
git push -u origin main
```

### 3. GitHub Actions (CI/CD) - Voliteľné

Vytvor `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: '8.2'
        extensions: mbstring, xml, curl, sqlite
    
    - name: Install Dependencies
      run: |
        cd ico-atlas
        composer install --prefer-dist --no-progress
        npm ci
    
    - name: Run Tests
      run: |
        cd ico-atlas
        php artisan test
```

---

## ☁️ Vercel Deployment

### ⚠️ Dôležité poznámky

**Vercel má obmedzenú podporu pre PHP/Laravel aplikácie:**
- Vercel primárne podporuje serverless funkcie
- Laravel aplikácie vyžadujú tradičný server (PHP-FPM + Nginx)
- **Odporúčané alternatívy:**
  - **Railway** (https://railway.app) – výborná podpora pre Laravel
  - **Render** (https://render.com) – bezplatný tier pre Laravel
  - **Fly.io** (https://fly.io) – Docker-based deployment
  - **DigitalOcean App Platform** – jednoduchý deployment

### Ak chceš skúsiť Vercel (experimentálne):

#### 1. Inštalácia Vercel CLI

```bash
npm i -g vercel
```

#### 2. Login do Vercel

```bash
vercel login
```

#### 3. Deployment

```bash
cd ico-atlas-5.0
vercel
```

#### 4. Environment Variables

V Vercel dashboard pridaj:
```
APP_ENV=production
APP_KEY=base64:... (vygeneruj cez php artisan key:generate)
APP_DEBUG=false
ICOATLAS_ORSR_STUB=true
ICOATLAS_CACHE_TTL_HOURS=12
ICOATLAS_HTTP_TIMEOUT=10
```

---

## 🌐 Odporúčané: Railway Deployment

### 1. Vytvor Railway Account

1. Choď na https://railway.app
2. Prihlás sa cez GitHub
3. Klikni "New Project" → "Deploy from GitHub repo"

### 2. Railway Configuration

#### `railway.json` (vytvor v root):

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd ico-atlas && php artisan serve --host=0.0.0.0 --port=$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### Environment Variables v Railway:

```
APP_ENV=production
APP_KEY=base64:... (vygeneruj)
APP_DEBUG=false
APP_URL=https://your-app.railway.app
ICOATLAS_ORSR_STUB=true
ICOATLAS_CACHE_TTL_HOURS=12
ICOATLAS_HTTP_TIMEOUT=10
```

### 3. Build Commands

Railway automaticky detekuje Laravel a spustí:
- `composer install`
- `php artisan migrate --force` (ak máš databázu)
- `npm install && npm run build`

---

## 🐳 Docker Deployment (Univerzálne)

### 1. Vytvor `Dockerfile` v root:

```dockerfile
FROM php:8.2-fpm

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    nginx

# Install PHP extensions
RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www

# Copy application
COPY . /var/www

# Install dependencies
RUN cd ico-atlas && composer install --optimize-autoloader --no-dev
RUN cd ico-atlas && npm install && npm run build

# Set permissions
RUN chown -R www-data:www-data /var/www
RUN chmod -R 755 /var/www/storage

# Nginx config
COPY docker/nginx.conf /etc/nginx/sites-available/default

EXPOSE 80

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
```

### 2. Vytvor `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:80"
    environment:
      - APP_ENV=production
      - APP_DEBUG=false
    volumes:
      - ./ico-atlas/storage:/var/www/ico-atlas/storage
```

---

## 📋 Deployment Checklist

### Pred deploymentom:

- [ ] Všetky testy prechádzajú: `php artisan test`
- [ ] `.env` je správne nastavený
- [ ] `APP_KEY` je vygenerovaný: `php artisan key:generate`
- [ ] Frontend je zbuildovaný: `npm run build`
- [ ] Config cache: `php artisan config:cache`
- [ ] Route cache: `php artisan route:cache`
- [ ] `.gitignore` obsahuje `.env`

### Po deploymente:

- [ ] Skontrolovať, že API funguje: `curl https://your-app.com/api/company/search?ico=52374220`
- [ ] Skontrolovať logy pre chyby
- [ ] Overiť, že cache funguje
- [ ] Testovať rate limiting

---

## 🔗 Užitočné odkazy

- **Railway**: https://railway.app
- **Render**: https://render.com
- **Fly.io**: https://fly.io
- **DigitalOcean**: https://www.digitalocean.com/products/app-platform
- **Laravel Deployment**: https://laravel.com/docs/deployment

---

**Poznámka:** Pre produkčný deployment odporúčam **Railway** alebo **Render** namiesto Vercel, pretože majú lepšiu podporu pre PHP/Laravel aplikácie.

