<x-app-layout>
    <x-slot name="title">IČO ATLAS 5.0 - Dashboard</x-slot>
    
    <div class="px-6 py-6 space-y-6">
        
        <!-- Header with Stats -->
        <div>
            <div class="flex items-center justify-between mb-6">
                <div>
                    <h1 class="text-2xl font-display font-bold text-tatra-navy dark:text-porcelain-100">Dashboard</h1>
                    <p class="text-sm text-tatra-400 dark:text-porcelain-400 mt-1">
                        Prehľad vašej aktivity
                    </p>
                </div>
                <button class="w-10 h-10 bg-white/50 dark:bg-matte-700/50 backdrop-blur-md border border-white/30 dark:border-white/20 rounded-xl flex items-center justify-center hover:bg-white/70 dark:hover:bg-matte-700/70 transition-colors">
                    <svg class="w-5 h-5 text-tatra-navy dark:text-porcelain-100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                    </svg>
                </button>
            </div>
            
            <!-- Stats Grid -->
            <div class="grid grid-cols-2 gap-4">
                <!-- API Calls Widget -->
                <x-glass-card padding="default">
                    <div class="flex items-center justify-between mb-3">
                        <div class="w-10 h-10 bg-gradient-crimson rounded-xl flex items-center justify-center">
                            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                        </div>
                        <span class="text-xs text-slovak-crimson font-semibold">+12%</span>
                    </div>
                    <p class="text-xs text-tatra-400 dark:text-porcelain-400 mb-1">API Volania</p>
                    <p class="text-2xl font-bold text-tatra-navy dark:text-porcelain-100">2,847</p>
                </x-glass-card>
                
                <!-- Credits Widget -->
                <x-glass-card padding="default">
                    <div class="flex items-center justify-between mb-3">
                        <div class="w-10 h-10 bg-gradient-tatra rounded-xl flex items-center justify-center">
                            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <span class="text-xs text-green-500 font-semibold">Aktívne</span>
                    </div>
                    <p class="text-xs text-tatra-400 dark:text-porcelain-400 mb-1">Zostatky</p>
                    <p class="text-2xl font-bold text-tatra-navy dark:text-porcelain-100">847</p>
                </x-glass-card>
            </div>
        </div>
        
        <!-- Usage Chart -->
        <div>
            <h2 class="text-lg font-display font-bold text-tatra-navy dark:text-porcelain-100 mb-4">Využitie API</h2>
            
            <x-glass-card padding="lg">
                <!-- Circular Progress -->
                <div class="flex items-center justify-center mb-6" x-data="{ progress: 68 }">
                    <div class="relative">
                        <!-- Background Circle -->
                        <svg class="w-40 h-40 transform -rotate-90">
                            <circle cx="80" cy="80" r="70" fill="none" class="stroke-tatra-100 dark:stroke-matte-700" stroke-width="12"></circle>
                            <!-- Progress Circle -->
                            <circle 
                                cx="80" 
                                cy="80" 
                                r="70" 
                                fill="none" 
                                class="stroke-slovak-crimson transition-all duration-1000" 
                                stroke-width="12"
                                :stroke-dasharray="`${progress * 4.4} 440`"
                                stroke-linecap="round"
                            ></circle>
                        </svg>
                        <!-- Center Text -->
                        <div class="absolute inset-0 flex flex-col items-center justify-center">
                            <p class="text-4xl font-bold text-tatra-navy dark:text-porcelain-100" x-text="progress + '%'"></p>
                            <p class="text-xs text-tatra-400 dark:text-porcelain-400">Mesačný limit</p>
                        </div>
                    </div>
                </div>
                
                <!-- Stats Breakdown -->
                <div class="grid grid-cols-3 gap-4 pt-4 border-t border-tatra-100 dark:border-matte-700">
                    <div class="text-center">
                        <p class="text-xs text-tatra-400 dark:text-porcelain-400 mb-1">Použité</p>
                        <p class="text-lg font-bold text-tatra-navy dark:text-porcelain-100">6,800</p>
                    </div>
                    <div class="text-center">
                        <p class="text-xs text-tatra-400 dark:text-porcelain-400 mb-1">Zostáva</p>
                        <p class="text-lg font-bold text-tatra-navy dark:text-porcelain-100">3,200</p>
                    </div>
                    <div class="text-center">
                        <p class="text-xs text-tatra-400 dark:text-porcelain-400 mb-1">Limit</p>
                        <p class="text-lg font-bold text-tatra-navy dark:text-porcelain-100">10,000</p>
                    </div>
                </div>
            </x-glass-card>
        </div>
        
        <!-- Activity Timeline -->
        <div>
            <h2 class="text-lg font-display font-bold text-tatra-navy dark:text-porcelain-100 mb-4">Aktivita</h2>
            
            <x-glass-card padding="none">
                <div class="divide-y divide-tatra-100 dark:divide-matte-700">
                    @foreach([
                        ['action' => 'API Request', 'details' => 'GET /api/company/12345678', 'time' => 'pred 2 min', 'status' => 'success'],
                        ['action' => 'Vyhľadávanie', 'details' => 'Query: "Bratislava s.r.o."', 'time' => 'pred 15 min', 'status' => 'success'],
                        ['action' => 'Export dát', 'details' => 'CSV export 150 záznamov', 'time' => 'pred 1 hod', 'status' => 'success'],
                        ['action' => 'API Request', 'details' => 'GET /api/search?q=tech', 'time' => 'pred 2 hod', 'status' => 'error'],
                    ] as $activity)
                        <div class="px-6 py-4 hover:bg-tatra-navy/5 dark:hover:bg-white/5 transition-colors">
                            <div class="flex items-start space-x-3">
                                <!-- Status Icon -->
                                <div class="flex-shrink-0 mt-1">
                                    @if($activity['status'] === 'success')
                                        <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                                    @else
                                        <div class="w-2 h-2 bg-slovak-crimson rounded-full"></div>
                                    @endif
                                </div>
                                
                                <!-- Content -->
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm font-semibold text-tatra-navy dark:text-porcelain-100 mb-1">
                                        {{ $activity['action'] }}
                                    </p>
                                    <p class="text-xs text-tatra-400 dark:text-porcelain-400 truncate">
                                        {{ $activity['details'] }}
                                    </p>
                                </div>
                                
                                <!-- Time -->
                                <p class="text-xs text-tatra-400 dark:text-porcelain-400 flex-shrink-0">
                                    {{ $activity['time'] }}
                                </p>
                            </div>
                        </div>
                    @endforeach
                </div>
                
                <!-- View All Button -->
                <div class="px-6 py-4 border-t border-tatra-100 dark:border-matte-700">
                    <button class="w-full text-center text-sm text-slovak-crimson font-semibold hover:underline">
                        Zobraziť všetko
                    </button>
                </div>
            </x-glass-card>
        </div>
        
        <!-- Quick Actions -->
        <div>
            <h2 class="text-lg font-display font-bold text-tatra-navy dark:text-porcelain-100 mb-4">Rýchle akcie</h2>
            
            <div class="grid grid-cols-2 gap-4">
                <x-glass-card clickable padding="default">
                    <div class="text-center">
                        <div class="w-12 h-12 bg-gradient-crimson rounded-2xl flex items-center justify-center mx-auto mb-3">
                            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                            </svg>
                        </div>
                        <p class="text-sm font-semibold text-tatra-navy dark:text-porcelain-100">Export</p>
                        <p class="text-xs text-tatra-400 dark:text-porcelain-400 mt-1">Stiahnuť dáta</p>
                    </div>
                </x-glass-card>
                
                <x-glass-card clickable padding="default">
                    <div class="text-center">
                        <div class="w-12 h-12 bg-gradient-tatra rounded-2xl flex items-center justify-center mx-auto mb-3">
                            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        </div>
                        <p class="text-sm font-semibold text-tatra-navy dark:text-porcelain-100">Reporty</p>
                        <p class="text-xs text-tatra-400 dark:text-porcelain-400 mt-1">Generovať</p>
                    </div>
                </x-glass-card>
            </div>
        </div>
        
        <!-- Upgrade CTA -->
        <x-glass-card padding="lg" class="bg-gradient-crimson text-white border-0">
            <div class="text-center">
                <div class="w-16 h-16 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                    </svg>
                </div>
                <h3 class="text-xl font-bold mb-2">Upgradujte na Pro</h3>
                <p class="text-white/80 text-sm mb-6">
                    Získajte neobmedzený prístup a pokročilé funkcie
                </p>
                <button class="w-full px-6 py-3 bg-white text-slovak-crimson font-semibold rounded-full hover:bg-white/90 transition-all duration-200 active:scale-95">
                    Zistiť viac
                </button>
            </div>
        </x-glass-card>
        
    </div>
    
</x-app-layout>
