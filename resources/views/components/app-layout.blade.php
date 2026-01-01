<!DOCTYPE html>
<html lang="sk" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="theme-color" content="#0B1E3D">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    
    <title>{{ $title ?? 'IČO ATLAS 5.0' }}</title>
    
    <!-- PWA Meta -->
    <link rel="manifest" href="/manifest.json">
    <link rel="apple-touch-icon" href="/icon-192.png">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    @vite(['resources/css/app.css', 'resources/js/app.js'])
    
    {{ $head ?? '' }}
</head>
<body class="overflow-x-hidden" x-data="{ darkMode: false }" :class="darkMode ? 'dark' : ''">
    
    <!-- Background Canvas -->
    <div class="fixed inset-0 -z-10 bg-porcelain-white dark:bg-matte-black bg-gradient-mesh">
        <!-- Animated Gradient Orbs -->
        <div class="absolute top-0 right-0 w-96 h-96 bg-slovak-crimson/5 dark:bg-slovak-crimson/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div class="absolute bottom-0 left-0 w-96 h-96 bg-tatra-navy/5 dark:bg-tatra-navy/20 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 1s;"></div>
    </div>
    
    <!-- Mobile Frame Container -->
    <div class="mobile-frame relative">
        
        <!-- Status Bar (iOS Style) -->
        <div class="safe-top sticky top-0 z-50 px-6 py-3 bg-white/50 dark:bg-matte-900/50 backdrop-blur-xl border-b border-white/10">
            <div class="flex items-center justify-between text-xs">
                <div class="flex items-center space-x-2">
                    <span class="text-tatra-navy dark:text-porcelain-100 font-semibold">
                        {{ now()->format('H:i') }}
                    </span>
                </div>
                <div class="flex items-center space-x-1">
                    <!-- Dark Mode Toggle -->
                    <button 
                        @click="darkMode = !darkMode" 
                        class="p-2 rounded-lg hover:bg-tatra-navy/5 dark:hover:bg-white/5 transition-colors"
                        aria-label="Toggle dark mode"
                    >
                        <svg x-show="!darkMode" class="w-4 h-4 text-tatra-navy" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                        </svg>
                        <svg x-show="darkMode" class="w-4 h-4 text-porcelain-100" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="display: none;">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                    </button>
                    
                    <!-- Signal Indicators -->
                    <div class="flex items-center space-x-1 px-2">
                        <div class="w-1 h-2 bg-tatra-navy dark:bg-porcelain-100 rounded-full"></div>
                        <div class="w-1 h-3 bg-tatra-navy dark:bg-porcelain-100 rounded-full"></div>
                        <div class="w-1 h-4 bg-tatra-navy dark:bg-porcelain-100 rounded-full"></div>
                        <div class="w-1 h-5 bg-tatra-navy dark:bg-porcelain-100 rounded-full"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Main Content Area -->
        <main class="min-h-screen pb-24">
            {{ $slot }}
        </main>
        
        <!-- Bottom Navigation -->
        <x-bottom-nav />
        
    </div>
    
    <!-- Toast Container -->
    <div 
        id="toast-container" 
        class="fixed top-20 right-4 left-4 md:left-auto md:w-96 z-50 space-y-2"
        x-data="{ toasts: [] }"
        @toast.window="toasts.push($event.detail); setTimeout(() => toasts.shift(), 3000)"
    >
        <template x-for="toast in toasts" :key="toast.id">
            <div 
                x-show="true"
                x-transition:enter="transition ease-out duration-300"
                x-transition:enter-start="opacity-0 translate-y-2"
                x-transition:enter-end="opacity-100 translate-y-0"
                x-transition:leave="transition ease-in duration-200"
                x-transition:leave-start="opacity-100"
                x-transition:leave-end="opacity-0"
                class="glass-card-sm p-4 flex items-start space-x-3 animate-slide-down"
            >
                <div 
                    class="flex-shrink-0 w-2 h-2 mt-1.5 rounded-full"
                    :class="{
                        'bg-slovak-crimson': toast.type === 'error',
                        'bg-green-500': toast.type === 'success',
                        'bg-tatra-navy': toast.type === 'info'
                    }"
                ></div>
                <p class="text-sm text-tatra-navy dark:text-porcelain-100" x-text="toast.message"></p>
            </div>
        </template>
    </div>
    
    {{ $scripts ?? '' }}
    
</body>
</html>
