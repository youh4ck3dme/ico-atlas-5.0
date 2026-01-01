# 🇸🇰 IČO ATLAS 5.0 - IMPLEMENTATION GUIDE

## 🎯 PHASE 1 & 2 COMPLETE ✅

### What's Included:

**1. Configuration Files:**
- ✅ `tailwind.config.js` - Slovak Enterprise Luxury color palette
- ✅ `resources/css/app.css` - Custom glassmorphism utilities
- ✅ `resources/js/app.js` - Alpine.js + utilities
- ✅ `resources/js/bootstrap.js` - Axios configuration
- ✅ `public/manifest.json` - PWA manifest
- ✅ `public/service-worker.js` - Offline functionality

**2. Blade Components:**
- ✅ `x-app-layout` - Main application wrapper
- ✅ `x-glass-card` - Glassmorphic cards (variants: sm, default, lg)
- ✅ `x-primary-button` - Slovak Crimson buttons with glow
- ✅ `x-input-group` - Floating label inputs
- ✅ `x-bottom-nav` - Glassmorphic navigation dock

**3. View Templates:**
- ✅ `welcome.blade.php` - Landing page with Hero section
- ✅ `search.blade.php` - Search interface with autocomplete
- ✅ `dashboard.blade.php` - Dashboard with widgets & charts

---

## 📦 INSTALLATION

### Step 1: Copy Files to Your Laravel Project

```bash
# Copy configuration
cp tailwind.config.js YOUR_PROJECT/

# Copy resources
cp -r resources/css YOUR_PROJECT/resources/
cp -r resources/js YOUR_PROJECT/resources/
cp -r resources/views/components YOUR_PROJECT/resources/views/
cp -r resources/views/*.blade.php YOUR_PROJECT/resources/views/

# Copy public files
cp -r public/manifest.json YOUR_PROJECT/public/
cp -r public/service-worker.js YOUR_PROJECT/public/
```

### Step 2: Install Dependencies

```bash
cd YOUR_PROJECT

# Install NPM packages
npm install alpinejs@^3.13.3
npm install @tailwindcss/forms

# Install Composer packages (if needed)
composer require laravel/ui
```

### Step 3: Build Assets

```bash
# Development
npm run dev

# Production
npm run build
```

### Step 4: Configure Routes

Add these routes to `routes/web.php`:

```php
Route::get('/', function () {
    return view('welcome');
})->name('home');

Route::get('/search', function () {
    return view('search');
})->name('search');

Route::get('/dashboard', function () {
    return view('dashboard');
})->name('dashboard');

Route::get('/profile', function () {
    return view('profile');
})->name('profile');
```

---

## 🎨 COLOR PALETTE

```
Tatra Navy:    #0B1E3D (Primary brand color)
Slovak Crimson: #DC143C (Accent color)
Porcelain White: #F8F9FA (Light background)
Matte Black:    #050505 (Dark background)
```

---

## 🧩 COMPONENT USAGE

### App Layout
```blade
<x-app-layout>
    <x-slot name="title">Page Title</x-slot>
    
    <!-- Your content -->
    
    <x-slot name="scripts">
        <script>
            // Custom scripts
        </script>
    </x-slot>
</x-app-layout>
```

### Glass Card
```blade
<x-glass-card>Content</x-glass-card>
<x-glass-card variant="sm" padding="lg">Content</x-glass-card>
<x-glass-card hover clickable>Clickable card</x-glass-card>
```

### Buttons
```blade
<x-primary-button>Click Me</x-primary-button>
<x-primary-button variant="secondary" size="lg">Secondary</x-primary-button>
<x-primary-button :loading="true">Loading...</x-primary-button>
```

### Input
```blade
<x-input-group 
    name="search" 
    label="Vyhľadať" 
    icon="search"
    :required="true"
/>
```

---

## 📱 PWA SETUP

### 1. Add to HTML `<head>`:
```html
<link rel="manifest" href="/manifest.json">
<link rel="apple-touch-icon" href="/images/icon-192x192.png">
<meta name="theme-color" content="#0B1E3D">
```

### 2. Generate Icons
Create icons in `/public/images/`:
- icon-72x72.png
- icon-96x96.png
- icon-128x128.png
- icon-144x144.png
- icon-152x152.png
- icon-192x192.png
- icon-384x384.png
- icon-512x512.png

Use tool: https://realfavicongenerator.net/

---

## 🌓 DARK MODE

Automatically handled by Alpine.js in `x-app-layout`.

Manual toggle:
```javascript
window.toggleDarkMode();
```

Check state:
```javascript
document.documentElement.classList.contains('dark');
```

---

## 🔔 NOTIFICATIONS

```javascript
// Show toast
window.showToast('Message', 'success');
window.showToast('Error', 'error');
window.showToast('Info', 'info');
```

---

## 🎯 UTILITY CLASSES

### Glassmorphism
```html
<div class="glass-card">Standard glass</div>
<div class="glass-card-sm">Small glass</div>
<div class="glass-card-lg">Large glass</div>
```

### Gradients
```html
<div class="bg-gradient-tatra">Tatra gradient</div>
<div class="bg-gradient-crimson">Crimson gradient</div>
<div class="bg-gradient-mesh">Mesh background</div>
```

### Animations
```html
<div class="animate-fade-in">Fade</div>
<div class="animate-slide-up">Slide</div>
<div class="animate-scale-in">Scale</div>
```

---

## 🚀 PRODUCTION DEPLOYMENT

```bash
# Build assets
npm run build

# Optimize Laravel
php artisan optimize
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Set permissions
chmod -R 755 storage bootstrap/cache
```

---

## 📊 PROJECT STRUCTURE

```
ico-atlas-5.0/
├── tailwind.config.js          # Slovak Enterprise palette
├── resources/
│   ├── css/
│   │   └── app.css             # Tailwind + utilities
│   ├── js/
│   │   ├── app.js              # Alpine.js initialization
│   │   └── bootstrap.js        # Axios config
│   └── views/
│       ├── components/
│       │   ├── app-layout.blade.php
│       │   ├── glass-card.blade.php
│       │   ├── primary-button.blade.php
│       │   ├── input-group.blade.php
│       │   └── bottom-nav.blade.php
│       ├── welcome.blade.php
│       ├── search.blade.php
│       └── dashboard.blade.php
└── public/
    ├── manifest.json           # PWA manifest
    └── service-worker.js       # Offline support
```

---

## ✨ KEY FEATURES IMPLEMENTED

✅ Mobile-first responsive design  
✅ Glassmorphism UI with Slovak colors  
✅ Dark mode support  
✅ PWA ready (offline, installable)  
✅ Alpine.js interactivity  
✅ Toast notifications  
✅ Skeleton loaders  
✅ Smooth animations  
✅ Floating navigation dock  
✅ Autocomplete search  
✅ Dashboard widgets  

---

## 🎓 NEXT STEPS

### Phase 3 (API Integration):
1. Create API routes for company lookup
2. Integrate with Slovak business register
3. Add authentication (Laravel Sanctum)
4. Implement data caching

### Phase 4 (Advanced Features):
1. Real-time notifications
2. Export to CSV/PDF
3. Advanced filtering
4. Company comparison
5. Favorites system

---

## 📖 DOCUMENTATION

Full component documentation and examples are in each `.blade.php` file.

For Tailwind utilities, see `resources/css/app.css`.

---

## 🐛 TROUBLESHOOTING

**Issue**: Styles not loading  
**Fix**: Run `npm run build` and clear browser cache

**Issue**: Alpine.js not working  
**Fix**: Check `resources/js/app.js` is imported in layout

**Issue**: Icons not showing  
**Fix**: Install `blade-ui-kit/blade-icons` or use inline SVGs

---

## 📞 SUPPORT

For questions or issues, check:
- Laravel Docs: https://laravel.com/docs
- Tailwind Docs: https://tailwindcss.com
- Alpine.js Docs: https://alpinejs.dev

---

**Built with 💙❤️ for Slovak Enterprise**

IČO ATLAS 5.0 © 2024
