# ⚡ IČO ATLAS 5.0 - QUICK START

## 🚀 Get Running in 5 Minutes

### 1️⃣ Copy Files (30 seconds)

```bash
# Navigate to your Laravel project
cd YOUR_LARAVEL_PROJECT

# Copy all files from ico-atlas-5.0 folder
cp -r ico-atlas-5.0/tailwind.config.js .
cp -r ico-atlas-5.0/resources/* resources/
cp -r ico-atlas-5.0/public/* public/
```

### 2️⃣ Install Dependencies (2 minutes)

```bash
npm install alpinejs@^3.13.3 @tailwindcss/forms
```

### 3️⃣ Build Assets (1 minute)

```bash
npm run dev
```

### 4️⃣ Add Routes (30 seconds)

In `routes/web.php`:

```php
Route::get('/', fn() => view('welcome'))->name('home');
Route::get('/search', fn() => view('search'))->name('search');
Route::get('/dashboard', fn() => view('dashboard'))->name('dashboard');
Route::get('/profile', fn() => view('profile'))->name('profile');
```

### 5️⃣ Done! 🎉

Visit: `http://localhost:8000`

---

## 🎨 First Component (10 seconds)

```blade
<x-app-layout>
    <div class="p-6">
        <x-glass-card>
            <h1 class="text-2xl font-bold">Hello Slovakia! 🇸🇰</h1>
        </x-glass-card>
    </div>
</x-app-layout>
```

---

## 🔥 Common Patterns

### Search Page
```blade
<x-app-layout>
    <div class="p-6">
        <x-input-group name="search" icon="search" placeholder="Hľadať..." />
    </div>
</x-app-layout>
```

### Card Grid
```blade
<div class="grid grid-cols-2 gap-4 p-6">
    <x-glass-card clickable>
        <p class="font-bold">Card 1</p>
    </x-glass-card>
    <x-glass-card clickable>
        <p class="font-bold">Card 2</p>
    </x-glass-card>
</div>
```

### CTA Button
```blade
<x-primary-button fullWidth size="lg">
    Začať hneď
</x-primary-button>
```

---

## 🎯 Color Classes

```html
<!-- Backgrounds -->
<div class="bg-tatra-navy">Dark blue</div>
<div class="bg-slovak-crimson">Red accent</div>

<!-- Text -->
<p class="text-tatra-navy">Navy text</p>
<p class="text-slovak-crimson">Crimson text</p>

<!-- Gradients -->
<div class="bg-gradient-tatra">Gradient</div>
```

---

## 💡 Pro Tips

**Dark Mode:**
```javascript
window.toggleDarkMode();
```

**Show Toast:**
```javascript
window.showToast('Success!', 'success');
```

**Format Currency:**
```javascript
window.formatCurrency(9.99); // "9,99 €"
```

---

## 🐛 Quick Fixes

**Styles not working?**
```bash
npm run build
```

**Alpine not working?**
Check `@vite(['resources/js/app.js'])` in layout

**Icons missing?**
Use inline SVGs from welcome.blade.php examples

---

## 📚 Full Documentation

See `INSTALLATION.md` for complete guide.

---

**Slovak Enterprise Luxury** 💙❤️
