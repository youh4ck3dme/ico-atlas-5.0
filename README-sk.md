# 🇸🇰 IČO ATLAS 5.0

> **Najpokročilejšia, vysokovýkonná PWA na vyhľadávanie firiem v slovenskej histórii.**

**Slovak Enterprise Luxury** - Fúzia slovenských národných farieb s ultra-prémiovou fintech estetikou.

![Status](https://img.shields.io/badge/Status-Phase%201%20%26%202%20Complete-success)
![Laravel](https://img.shields.io/badge/Laravel-11-red)
![Tailwind](https://img.shields.io/badge/Tailwind-3.4-blue)
![Alpine.js](https://img.shields.io/badge/Alpine.js-3.13-cyan)
![PWA](https://img.shields.io/badge/PWA-Ready-orange)

**📖 [English version](README.md)**

---

## 🚀 Rýchly štart

### 1. Kopírovanie súborov
```bash
cp -r ico-atlas-5.0/* YOUR_LARAVEL_PROJECT/
```

### 2. Inštalácia závislostí
```bash
npm install alpinejs@^3.13.3 @tailwindcss/forms
```

### 3. Stavba
```bash
npm run dev
```

### 4. Pridajte trasy
```php
Route::get('/', fn() => view('welcome'))->name('home');
Route::get('/search', fn() => view('search'))->name('search');
Route::get('/dashboard', fn() => view('dashboard'))->name('dashboard');
```

### 5. Hotovo! 🎉
Navštívte `http://localhost:8000`

**📖 Úplné nastavenie:** Pozri [INSTALLATION.md](INSTALLATION.md)  
**⚡ Stručný návod:** Pozri [QUICKSTART.md](QUICKSTART.md)

---

## 🧩 Komponenty

### `<x-app-layout>`
Hlavný obal aplikácie s mobilným rámom a tmavým režimom.

```blade
<x-app-layout>
    <x-slot name="title">Page Title</x-slot>
    Your content here
</x-app-layout>
```

### `<x-glass-card>`
Sklomorfná nádoba s variantmi.

```blade
<x-glass-card>Content</x-glass-card>
<x-glass-card variant="lg" hover clickable>Clickable</x-glass-card>
```

### `<x-primary-button>`
Slovak Crimson CTA so žiarivým efektom.

```blade
<x-primary-button>Click Me</x-primary-button>
<x-primary-button variant="secondary" fullWidth>Full Width</x-primary-button>
```

### `<x-input-group>`
Plávajúci vstupný štítok s ikonami.

```blade
<x-input-group name="search" icon="search" placeholder="Hľadať..." />
```

### `<x-bottom-nav>`
Plávajúci navigačný dok v štýle iOS.

```blade
<x-bottom-nav />
```

**📋 Úplný odkaz:** Pozri [CHEATSHEET.md](CHEATSHEET.md)

---

## 🎯 Prípady použitia

### Vstupná stránka
```blade
<x-app-layout>
    <div class="h-[35vh] bg-gradient-tatra">
        <div class="px-6 py-8 text-white">
            <h1 class="text-3xl font-bold">Vitajte</h1>
        </div>
    </div>
    
    <div class="p-6">
        <x-glass-card>
            <h2 class="text-xl font-bold mb-4">Funkcie</h2>
            <x-primary-button fullWidth>Začať</x-primary-button>
        </x-glass-card>
    </div>
</x-app-layout>
```

### Vyhľadávacie rozhranie
```blade
<x-app-layout>
    <div class="p-6">
        <x-input-group 
            name="search" 
            icon="search" 
            placeholder="Hľadať firmu..."
        />
        
        <x-glass-card class="mt-4">
            Results here
        </x-glass-card>
    </div>
</x-app-layout>
```

### Prístrojová doska
```blade
<x-app-layout>
    <div class="p-6 space-y-4">
        <div class="grid grid-cols-2 gap-4">
            <x-glass-card>Widget 1</x-glass-card>
            <x-glass-card>Widget 2</x-glass-card>
        </div>
    </div>
</x-app-layout>
```

---

## 🎨 Nástroje na úpravu farieb

```html
<!-- Backgrounds -->
<div class="bg-tatra-navy">Tatra Navy</div>
<div class="bg-slovak-crimson">Slovak Crimson</div>

<!-- Gradients -->
<div class="bg-gradient-tatra">Gradient</div>
<div class="text-gradient-crimson">Gradient Text</div>

<!-- Glass Effects -->
<div class="glass-card">Glass Card</div>
<div class="glass-blur-xl">Extra Blur</div>
```

---

## 🌓 Tmavý režim

Automatický tmavý režim s perzistenciou lokálneho úložiska.

```html
<!-- Toggle dark mode -->
<button @click="darkMode = !darkMode">Toggle</button>

<!-- Conditional classes -->
<div class="text-tatra-navy dark:text-porcelain-100">
    Text changes in dark mode
</div>
```

Rozhranie API JavaScriptu:
```javascript
window.toggleDarkMode();  // Toggle
window.initDarkMode();    // Initialize
```

---

## 🔔 Upozornenia

```javascript
// Show toasts
window.showToast('Success!', 'success');
window.showToast('Error occurred', 'error');
window.showToast('Info message', 'info');
```

---

## 🛠️ Nástroje

```javascript
// Format currency
window.formatCurrency(9.99);  // "9,99 €"

// Format date
window.formatDate(new Date());  // "14. december 2024"

// Copy to clipboard
window.copyToClipboard('text');  // Shows toast

// Haptic feedback (mobile)
window.haptic('impact');
```

---

## 📱 Funkcie PWA

### Inštalateľné
- iOS: Pridať na domovskú obrazovku
- Android: Výzva na inštaláciu aplikácie
- Počítač: Inštalácia z prehliadača

### Offline podpora
Servisný pracovník ukladá aktíva do vyrovnávacej pamäte na použitie offline.

### Push notifikácie
Pripravené na webové push notifikácie.

---

## 📊 Technické špecifikácie

**Frontend:**
- Nástroj na zostavenie: Vite 5.0
- CSS framework: Tailwind CSS 3.4+
- JS Framework: Alpine.js 3.13
- Ikony: Lucide / Inline SVG

**Výkon:**
- Prvý náter: <1s
- Interaktívne: <2 s
- Balík: ~45KB gzipovaný

**Podpora prehliadačov:**
- Chrome 90+
- Safari 14+
- Firefox 88+
- Okraj 90+

---

## 🏆 Stav fázy

### ✅ Fáza 1 a 2 (Dokončená)
- [x] Dizajnový systém
- [x] Základné komponenty
- [x] Šablóny stránok
- [x] Nadácia PWA
- [x] Dokumentácia

### 🔮 Fáza 3 (odporúčaná)
- [ ] Integrácia API
- [ ] Autentifikácia
- [ ] Vyhľadávanie v reálnom čase
- [ ] Export údajov
- [ ] Pokročilé filtrovanie

---

## 📚 Dokumentácia

| Dokument | Účel |
|----------|---------|
| [INSTALLATION.md](INSTALLATION.md) | Kompletný sprievodca nastavením |
| [QUICKSTART.md](QUICKSTART.md) | 5-minútový rýchly štart |
| [CHEATSHEET.md](CHEATSHEET.md) | Referenčný kód komponentu |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Úplný prehľad projektu |

---

## 🎯 Najlepšie postupy

1. ✅ Vždy používajte `<x-app-layout>` ako obal
2. ✅ Uprednostňujem `glass-card` nádoby
3. ✅ Použi slovenské farby (Tatra Navy & Crimson)
4. ✅ Testujte v tmavom režime
5. ✅ Urobte to primárne pre mobilné zariadenia
6. ✅ Udržujte Alpine.js ľahký

---

## 🐛 Riešenie problémov

**Štýly nefungujú?**
```bash
npm run build
php artisan view:clear
```

**Alpine.js sa neinicializuje?**
Skontrolujte `@vite(['resources/js/app.js'])` rozloženie.

**Tmavý režim sa nezobrazuje?**
Uistite sa, `window.initDarkMode()` že sa spúšťa pri načítaní stránky.

---

## 🤝 Prispievanie

Toto je štartovacia sada pripravená na výrobu. Môžete si ju voľne prispôsobiť:

1. Aktualizovať farby v `tailwind.config.js`
2. Pridajte nové komponenty do `resources/views/components/`
3. Rozšíriť inžinierske siete v `resources/css/app.css`
4. Pridajte funkcie v `resources/js/app.js`

---

## 📝 Licencia

Proprietárne - IČO ATLAS 5.0 © 2024

---

## 🎓 Zdroje

- **Repozitár:** https://github.com/youh4ck3dme/ico-atlas-5.0
- **Laravel Docs:** https://laravel.com/docs
- **Tailwind CSS:** https://tailwindcss.com
- **Alpine.js:** https://alpinejs.dev
- **Vite:** https://vitejs.dev

---

## 🙏 Zásluhy

**Dizajnová inšpirácia:**
- Precedent (https://precedent.dev)
- Revolut (https://revolut.com)
- Apple (https://apple.com/sk)

**Tech Stack:**
- Laravel Framework
- Tailwind Labs
- Alpine.js Team

---

## 🚀 Ďalšie kroky

1. ✅ Preskúmajte dokumentáciu
2. ✅ Sledujte QUICKSTART.md
3. ✅ Prispôsobte komponenty
4. ✅ Vytvorte svoje funkcie
5. ✅ Nasadenie do výroby

---

<div align="center">

**Vybudované s 💙❤️ pre Slovensko**

*Slovak Enterprise Luxury - Kde sa tradícia stretáva s inováciou*

---

**IČO ATLAS 5.0** - Budúcnosť vyhľadávania firiem

🔷 **Tatra Navy** • ❤️ **Slovak Crimson** • ⚪ **Porcelain** • ⚫ **Matte**

</div>

