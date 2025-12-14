<x-app-layout>
    <x-slot name="title">IČO ATLAS 5.0 - Domov</x-slot>
    
    <!-- Hero Section with Curved Background -->
    <div class="relative h-[35vh] bg-gradient-tatra overflow-hidden">
        <!-- Animated Background Pattern -->
        <div class="absolute inset-0 opacity-10">
            <div class="absolute top-10 left-10 w-32 h-32 border-2 border-white rounded-full animate-pulse-slow"></div>
            <div class="absolute bottom-10 right-10 w-24 h-24 border-2 border-white rounded-full animate-pulse-slow" style="animation-delay: 1s;"></div>
        </div>
        
        <!-- Curved Bottom -->
        <div class="absolute -bottom-1 left-0 right-0 h-12 bg-porcelain-white dark:bg-matte-black rounded-t-[3rem]"></div>
        
        <!-- Hero Content -->
        <div class="relative px-6 pt-8 pb-16 text-white">
            <div class="flex items-center justify-between mb-8">
                <div>
                    <h1 class="text-3xl font-display font-bold mb-1">Vitajte</h1>
                    <p class="text-white/80 text-sm">{{ auth()->user()->name ?? 'Hosť' }}</p>
                </div>
                <div class="flex items-center space-x-2">
                    <div class="w-12 h-12 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center">
                        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                        </svg>
                        <span class="absolute top-0 right-0 w-3 h-3 bg-slovak-crimson rounded-full border-2 border-tatra-navy"></span>
                    </div>
                </div>
            </div>
            
            <!-- Quick Stats Widget -->
            <x-glass-card variant="sm" padding="sm" class="text-tatra-navy dark:text-porcelain-100">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-xs text-tatra-400 dark:text-porcelain-400 mb-1">API Kredit</p>
                        <p class="text-2xl font-bold">2,847</p>
                    </div>
                    <div class="text-right">
                        <p class="text-xs text-tatra-400 dark:text-porcelain-400 mb-1">Využitie dnes</p>
                        <div class="flex items-center space-x-2">
                            <div class="w-16 h-2 bg-tatra-100 dark:bg-matte-700 rounded-full overflow-hidden">
                                <div class="h-full bg-slovak-crimson rounded-full" style="width: 68%"></div>
                            </div>
                            <span class="text-sm font-semibold">68%</span>
                        </div>
                    </div>
                </div>
            </x-glass-card>
        </div>
    </div>
    
    <!-- Main Content -->
    <div class="px-6 py-6 space-y-6">
        
        <!-- Search Bar -->
        <div x-data="{ focused: false }">
            <x-input-group 
                name="search" 
                placeholder="Hľadať IČO, názov, adresu..."
                icon="search"
                @focus="focused = true"
                @blur="focused = false"
            />
            
            <!-- Quick Search Suggestions (shown when focused) -->
            <div 
                x-show="focused"
                x-transition:enter="transition ease-out duration-200"
                x-transition:enter-start="opacity-0 translate-y-2"
                x-transition:enter-end="opacity-100 translate-y-0"
                x-transition:leave="transition ease-in duration-150"
                x-transition:leave-start="opacity-100"
                x-transition:leave-end="opacity-0"
                class="mt-2"
                style="display: none;"
            >
                <x-glass-card variant="sm" padding="sm">
                    <p class="text-xs text-tatra-400 dark:text-porcelain-400 mb-2">Často vyhľadávané</p>
                    <div class="space-y-1">
                        @foreach(['Bratislava', 's.r.o.', 'IT služby'] as $suggestion)
                            <button class="w-full text-left px-3 py-2 text-sm text-tatra-navy dark:text-porcelain-100 hover:bg-tatra-navy/5 dark:hover:bg-white/5 rounded-xl transition-colors">
                                {{ $suggestion }}
                            </button>
                        @endforeach
                    </div>
                </x-glass-card>
            </div>
        </div>
        
        <!-- Feature Cards -->
        <div>
            <h2 class="text-lg font-display font-bold text-tatra-navy dark:text-porcelain-100 mb-4">Hlavné funkcie</h2>
            
            <!-- Horizontal Scrolling Cards -->
            <div class="flex space-x-4 overflow-x-auto pb-2 -mx-6 px-6 scrollbar-hide">
                
                <!-- Data Card -->
                <x-glass-card clickable class="flex-shrink-0 w-64" padding="default">
                    <div class="flex items-start justify-between mb-4">
                        <div class="w-12 h-12 bg-gradient-crimson rounded-2xl flex items-center justify-center">
                            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                        </div>
                        <span class="badge badge-success">Aktívne</span>
                    </div>
                    <h3 class="text-xl font-bold text-tatra-navy dark:text-porcelain-100 mb-2">Dátová báza</h3>
                    <p class="text-sm text-tatra-400 dark:text-porcelain-400">Prístup k 250,000+ slovenským firmám</p>
                </x-glass-card>
                
                <!-- API Card -->
                <x-glass-card clickable class="flex-shrink-0 w-64" padding="default">
                    <div class="flex items-start justify-between mb-4">
                        <div class="w-12 h-12 bg-gradient-tatra rounded-2xl flex items-center justify-center">
                            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                        </div>
                        <span class="badge badge-info">Pro</span>
                    </div>
                    <h3 class="text-xl font-bold text-tatra-navy dark:text-porcelain-100 mb-2">API Access</h3>
                    <p class="text-sm text-tatra-400 dark:text-porcelain-400">REST API s real-time dátami</p>
                </x-glass-card>
                
                <!-- Pricing Card -->
                <x-glass-card clickable class="flex-shrink-0 w-64" padding="default">
                    <div class="flex items-start justify-between mb-4">
                        <div class="w-12 h-12 bg-gradient-to-br from-slovak-crimson to-tatra-navy rounded-2xl flex items-center justify-center">
                            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <span class="badge badge-primary">Nové</span>
                    </div>
                    <h3 class="text-xl font-bold text-tatra-navy dark:text-porcelain-100 mb-2">Cenníky</h3>
                    <p class="text-sm text-tatra-400 dark:text-porcelain-400">Flexibilné balíčky od 9.99€</p>
                </x-glass-card>
                
            </div>
        </div>
        
        <!-- Recent Activity -->
        <div>
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-lg font-display font-bold text-tatra-navy dark:text-porcelain-100">Nedávna aktivita</h2>
                <button class="text-sm text-slovak-crimson font-semibold">Všetko</button>
            </div>
            
            <x-glass-card padding="none">
                <div class="divide-y divide-tatra-100 dark:divide-matte-700">
                    @foreach([
                        ['name' => 'Tech Solutions s.r.o.', 'ico' => '12345678', 'time' => 'pred 5 min'],
                        ['name' => 'Slovenská Inovačná a.s.', 'ico' => '87654321', 'time' => 'pred 1 hod'],
                        ['name' => 'Digital Agency SK', 'ico' => '11223344', 'time' => 'pred 3 hod'],
                    ] as $activity)
                        <div class="px-6 py-4 hover:bg-tatra-navy/5 dark:hover:bg-white/5 transition-colors cursor-pointer">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-3">
                                    <div class="w-10 h-10 bg-gradient-tatra rounded-xl flex items-center justify-center text-white font-bold text-sm">
                                        {{ substr($activity['name'], 0, 1) }}
                                    </div>
                                    <div>
                                        <p class="text-sm font-semibold text-tatra-navy dark:text-porcelain-100">{{ $activity['name'] }}</p>
                                        <p class="text-xs text-tatra-400 dark:text-porcelain-400">IČO: {{ $activity['ico'] }}</p>
                                    </div>
                                </div>
                                <p class="text-xs text-tatra-400 dark:text-porcelain-400">{{ $activity['time'] }}</p>
                            </div>
                        </div>
                    @endforeach
                </div>
            </x-glass-card>
        </div>
        
        <!-- CTA Section -->
        <div class="pt-4">
            <x-primary-button fullWidth size="lg">
                <span class="flex items-center justify-center">
                    <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    Začať vyhľadávanie
                </span>
            </x-primary-button>
        </div>
        
    </div>
    
    <x-slot name="scripts">
        <script>
            // Hide scrollbar for horizontal scroll
            const style = document.createElement('style');
            style.textContent = '.scrollbar-hide::-webkit-scrollbar { display: none; } .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }';
            document.head.appendChild(style);
        </script>
    </x-slot>
    
</x-app-layout>
