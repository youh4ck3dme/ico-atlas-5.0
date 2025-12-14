# 🚀 IČO ATLAS 5.0 - GitHub Setup Guide

## Option 1: Upload ZIP to GitHub (Najjednoduchšie)

### 1. Vytvor nový repozitár na GitHub
```
1. Idi na https://github.com/new
2. Repository name: ico-atlas-5.0
3. Description: Slovak Enterprise Luxury PWA
4. Public/Private: Vyber podľa potreby
5. Nezaškrtávaj "Initialize with README" (už máš README.md)
6. Klikni "Create repository"
```

### 2. Upload cez GitHub Web Interface
```
1. Stiahni si ico-atlas-5.0.zip
2. Rozbaľ ZIP
3. Na GitHub stránke repozitára klikni "uploading an existing file"
4. Pretiahnuť všetky súbory
5. Commit message: "Initial commit - Phase 1 & 2 complete"
6. Klikni "Commit changes"
```

---

## Option 2: Git Command Line (Pokročilé)

### 1. Rozbaľ ZIP a inicializuj Git
```bash
# Rozbaľ ZIP
unzip ico-atlas-5.0.zip
cd ico-atlas-5.0

# Inicializuj Git
git init
git add .
git commit -m "Initial commit - IČO ATLAS 5.0 - Phase 1 & 2 complete"
```

### 2. Pripoj k GitHub
```bash
# Vytvor repo na GitHub, potom:
git remote add origin https://github.com/TVOJ_USERNAME/ico-atlas-5.0.git
git branch -M main
git push -u origin main
```

---

## Option 3: GitHub Desktop (Najjednoduchšie pre začiatočníkov)

### 1. Nainštaluj GitHub Desktop
```
Stiahni z: https://desktop.github.com
```

### 2. Vytvor repozitár
```
1. File → New Repository
2. Name: ico-atlas-5.0
3. Description: Slovak Enterprise Luxury PWA
4. Vyber "ico-atlas-5.0" folder (rozbalený ZIP)
5. Klikni "Create Repository"
```

### 3. Publikuj na GitHub
```
1. Klikni "Publish repository"
2. Vyber Public/Private
3. Klikni "Publish Repository"
```

---

## 📝 Odporúčané README Badges

Pridaj do README.md (na začiatok):

```markdown
![Status](https://img.shields.io/badge/Status-Phase%201%20%26%202%20Complete-success)
![Laravel](https://img.shields.io/badge/Laravel-11-red)
![Tailwind](https://img.shields.io/badge/Tailwind-3.4-blue)
![Alpine.js](https://img.shields.io/badge/Alpine.js-3.13-cyan)
![PWA](https://img.shields.io/badge/PWA-Ready-orange)
```

---

## 🏷️ Odporúčané GitHub Topics

Pridaj tieto topics do repozitára:
```
laravel
tailwindcss
alpinejs
pwa
glassmorphism
slovak
blade-components
vite
dark-mode
mobile-first
```

---

## 📄 Odporúčaná .gitignore

Vytvor `.gitignore` súbor:

```gitignore
# Dependencies
/node_modules
/vendor

# Build
/public/hot
/public/storage
/public/build

# Environment
.env
.env.backup
.env.production

# IDE
.idea
.vscode
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Laravel
/storage/*.key
/storage/framework/cache/*
/storage/framework/sessions/*
/storage/framework/views/*
/storage/logs/*

# NPM
npm-debug.log
yarn-error.log
```

---

## 📋 GitHub Repository Settings

### 1. About Section
```
Description: 🇸🇰 Slovak Enterprise Luxury PWA - The most advanced company lookup PWA with glassmorphism UI
Website: (tvoj deployment URL)
Topics: laravel, tailwindcss, alpinejs, pwa, glassmorphism, slovak
```

### 2. Default Branch
```
Odporúčam: main (už sa nepoužíva "master")
```

### 3. Branch Protection (Optional)
```
Settings → Branches → Add rule
Branch name: main
☑ Require pull request reviews before merging
```

---

## 🌟 GitHub Actions (Optional - CI/CD)

Vytvor `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Build assets
      run: npm run build
      
    - name: Deploy
      run: echo "Deploy to your server"
```

---

## 📊 GitHub Project Board (Optional)

Vytvor project board pre Phase 3:

### Columns:
1. **To Do**
   - API integration
   - Authentication
   - Real-time search
   
2. **In Progress**
   
3. **Done**
   - Phase 1: Design system ✅
   - Phase 2: Components ✅

---

## 🔗 Užitočné Links

Po publikovaní na GitHub:

```
Repository: https://github.com/USERNAME/ico-atlas-5.0
Issues: https://github.com/USERNAME/ico-atlas-5.0/issues
Wiki: https://github.com/USERNAME/ico-atlas-5.0/wiki
Projects: https://github.com/USERNAME/ico-atlas-5.0/projects
```

---

## 🎯 First Commit Message Template

```
Initial commit - IČO ATLAS 5.0

🎨 Design System
- Slovak Enterprise Luxury color palette
- Glassmorphism UI components
- Dark mode support

🧩 Components (5)
- x-app-layout
- x-glass-card
- x-primary-button
- x-input-group
- x-bottom-nav

📄 Views (3)
- Landing page
- Search interface
- Dashboard

📱 PWA
- Manifest
- Service Worker
- Offline support

✨ Features
- Mobile-first design
- Alpine.js reactivity
- Tailwind CSS utilities
- Full documentation

Status: Phase 1 & 2 Complete ✅
```

---

## 🚀 Po Publikovaní

### 1. Zdieľaj!
```
Twitter: Práve som vytvoril IČO ATLAS 5.0 🇸🇰
LinkedIn: Nová Slovak Enterprise Luxury PWA
```

### 2. Pridaj Screenshot
```
Vytvor screenshots/ folder
Pridaj:
- landing-page.png
- search-interface.png
- dashboard.png
- dark-mode.png
```

### 3. Demo
```
Deploy na:
- Vercel
- Netlify
- GitHub Pages
```

---

**Happy coding! 🇸🇰💙❤️**
