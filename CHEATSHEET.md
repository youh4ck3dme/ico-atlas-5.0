# 📋 IČO ATLAS 5.0 - COMPONENT CHEATSHEET

## 🎨 COLORS

```
Tatra Navy:      #0B1E3D    bg-tatra-navy    text-tatra-navy
Slovak Crimson:  #DC143C    bg-slovak-crimson    text-slovak-crimson
Porcelain:       #F8F9FA    bg-porcelain-white   text-porcelain-white
Matte Black:     #050505    bg-matte-black       text-matte-black
```

---

## 🧩 BLADE COMPONENTS

### App Layout
```blade
<x-app-layout>
    <x-slot name="title">Title</x-slot>
    Content here
</x-app-layout>
```

### Glass Card
```blade
<!-- Basic -->
<x-glass-card>Content</x-glass-card>

<!-- Small variant -->
<x-glass-card variant="sm">Content</x-glass-card>

<!-- Large variant -->
<x-glass-card variant="lg">Content</x-glass-card>

<!-- No padding -->
<x-glass-card padding="none">Content</x-glass-card>

<!-- Clickable with hover -->
<x-glass-card hover clickable>Click me</x-glass-card>
```

### Buttons
```blade
<!-- Primary (Slovak Crimson) -->
<x-primary-button>Click</x-primary-button>

<!-- Secondary (Glass) -->
<x-primary-button variant="secondary">Click</x-primary-button>

<!-- Ghost -->
<x-primary-button variant="ghost">Click</x-primary-button>

<!-- Sizes -->
<x-primary-button size="sm">Small</x-primary-button>
<x-primary-button size="lg">Large</x-primary-button>

<!-- Full width -->
<x-primary-button fullWidth>Full Width</x-primary-button>

<!-- Loading state -->
<x-primary-button :loading="true">Loading</x-primary-button>

<!-- Disabled -->
<x-primary-button :disabled="true">Disabled</x-primary-button>
```

### Input Group
```blade
<!-- Basic -->
<x-input-group name="email" label="Email" />

<!-- With icon -->
<x-input-group name="search" icon="search" placeholder="Hľadať..." />

<!-- Required -->
<x-input-group name="name" label="Meno" :required="true" />

<!-- With error -->
<x-input-group name="email" error="Neplatný email" />

<!-- Password -->
<x-input-group name="password" type="password" label="Heslo" icon="lock" />
```

### Bottom Navigation
```blade
<!-- Auto-detect current route -->
<x-bottom-nav />

<!-- Manual current route -->
<x-bottom-nav currentRoute="search" />
```

---

## 🎨 UTILITY CLASSES

### Glassmorphism
```html
<div class="glass-card">Standard glass card</div>
<div class="glass-card-sm">Small glass card</div>
<div class="glass-card-lg">Large glass card</div>
<div class="glass-blur-xl">Extra blur backdrop</div>
```

### Buttons (CSS Classes)
```html
<button class="btn-primary">Primary</button>
<button class="btn-secondary">Secondary</button>
<button class="btn-ghost">Ghost</button>
```

### Inputs
```html
<input type="text" class="input-glass" />
```

### Badges
```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-info">Info</span>
```

### Gradients
```html
<div class="bg-gradient-tatra">Tatra gradient</div>
<div class="bg-gradient-crimson">Crimson gradient</div>
<div class="bg-gradient-mesh">Mesh background</div>
```

### Text Gradients
```html
<h1 class="text-gradient-crimson">Crimson gradient text</h1>
<h1 class="text-gradient-tatra">Tatra gradient text</h1>
```

### Animations
```html
<div class="animate-fade-in">Fade in</div>
<div class="animate-slide-up">Slide up</div>
<div class="animate-slide-down">Slide down</div>
<div class="animate-scale-in">Scale in</div>
<div class="animate-pulse-slow">Slow pulse</div>
<div class="animate-shimmer">Shimmer</div>
```

### Skeleton Loaders
```html
<div class="skeleton h-4 w-full rounded-lg"></div>
<div class="skeleton h-20 w-20 rounded-xl"></div>
```

---

## 🌓 DARK MODE

### HTML
```html
<div class="text-tatra-navy dark:text-porcelain-100">
    Auto dark mode text
</div>
```

### Alpine.js
```html
<div x-data="{ darkMode: false }" :class="darkMode ? 'dark' : ''">
    <button @click="darkMode = !darkMode">Toggle</button>
</div>
```

### JavaScript
```javascript
// Toggle dark mode
window.toggleDarkMode();

// Check if dark mode
document.documentElement.classList.contains('dark');
```

---

## 📱 ALPINE.JS PATTERNS

### Show/Hide
```html
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    <div x-show="open">Content</div>
</div>
```

### Transitions
```html
<div 
    x-show="open"
    x-transition:enter="transition ease-out duration-300"
    x-transition:enter-start="opacity-0 scale-95"
    x-transition:enter-end="opacity-100 scale-100"
>
    Content
</div>
```

### Search with Debounce
```html
<input 
    x-data="{ query: '' }"
    x-model="query"
    @input.debounce.300ms="search()"
    type="text"
/>
```

---

## 🔔 NOTIFICATIONS

### Show Toast
```javascript
window.showToast('Message here', 'success');
window.showToast('Error message', 'error');
window.showToast('Info message', 'info');
```

### Toast Types
- `success` - Green checkmark
- `error` - Red X
- `info` - Blue info

---

## 🛠️ UTILITY FUNCTIONS

### Format Currency
```javascript
window.formatCurrency(9.99);
// Output: "9,99 €"
```

### Format Date
```javascript
window.formatDate(new Date());
// Output: "14. december 2024"
```

### Copy to Clipboard
```javascript
window.copyToClipboard('Text to copy');
// Shows success toast
```

### Debounce
```javascript
const debouncedSearch = window.debounce(() => {
    console.log('Search');
}, 300);
```

### Haptic Feedback
```javascript
window.haptic('impact');      // Single vibration
window.haptic('notification'); // Double vibration
window.haptic('selection');   // Light vibration
```

---

## 🎯 COMMON LAYOUTS

### Hero Section
```blade
<div class="h-[35vh] bg-gradient-tatra">
    <div class="px-6 py-8 text-white">
        <h1 class="text-3xl font-bold">Title</h1>
        <p class="text-white/80">Subtitle</p>
    </div>
</div>
```

### Card Grid
```blade
<div class="grid grid-cols-2 gap-4 p-6">
    <x-glass-card clickable>Card 1</x-glass-card>
    <x-glass-card clickable>Card 2</x-glass-card>
</div>
```

### List with Dividers
```blade
<x-glass-card padding="none">
    <div class="divide-y divide-tatra-100 dark:divide-matte-700">
        <div class="px-6 py-4">Item 1</div>
        <div class="px-6 py-4">Item 2</div>
    </div>
</x-glass-card>
```

### Stats Widget
```blade
<x-glass-card>
    <p class="text-xs text-tatra-400 mb-1">Label</p>
    <p class="text-2xl font-bold text-tatra-navy">2,847</p>
</x-glass-card>
```

---

## 🚀 QUICK RECIPES

### Loading State
```html
<div class="skeleton h-20 w-full rounded-xl"></div>
```

### Empty State
```html
<x-glass-card padding="lg" class="text-center">
    <div class="w-20 h-20 bg-tatra-navy/10 rounded-full mx-auto mb-4 flex items-center justify-center">
        <svg class="w-10 h-10 text-tatra-400">...</svg>
    </div>
    <h3 class="text-lg font-bold mb-2">No results</h3>
    <p class="text-sm text-tatra-400">Try adjusting filters</p>
</x-glass-card>
```

### Notification Badge
```html
<div class="relative">
    <svg class="w-6 h-6">...</svg>
    <span class="absolute -top-1 -right-1 w-4 h-4 bg-slovak-crimson rounded-full text-xs text-white flex items-center justify-center">
        3
    </span>
</div>
```

---

**Slovak Enterprise Luxury** 💙❤️

Quick Reference for IČO ATLAS 5.0
