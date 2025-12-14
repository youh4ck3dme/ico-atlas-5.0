<x-app-layout>
    <x-slot name="title">IČO ATLAS 5.0 - Vyhľadávanie</x-slot>
    
    <div class="px-6 py-6" x-data="{
        query: '',
        results: [],
        loading: false,
        searching: false,
        
        async search() {
            if (this.query.length < 2) {
                this.results = [];
                this.searching = false;
                return;
            }
            
            this.loading = true;
            this.searching = true;
            
            // Simulate API call
            setTimeout(() => {
                // Mock results
                if (this.query.length > 2) {
                    this.results = [
                        { name: 'Tech Solutions s.r.o.', ico: '12345678', city: 'Bratislava', status: 'active' },
                        { name: 'Slovak Innovation a.s.', ico: '87654321', city: 'Košice', status: 'active' },
                        { name: 'Digital Agency SK', ico: '11223344', city: 'Žilina', status: 'active' },
                    ].filter(r => 
                        r.name.toLowerCase().includes(this.query.toLowerCase()) ||
                        r.ico.includes(this.query)
                    );
                } else {
                    this.results = [];
                }
                this.loading = false;
            }, 300);
        }
    }">
        
        <!-- Header -->
        <div class="mb-6">
            <h1 class="text-2xl font-display font-bold text-tatra-navy dark:text-porcelain-100 mb-2">
                Vyhľadávanie firiem
            </h1>
            <p class="text-sm text-tatra-400 dark:text-porcelain-400">
                Zadajte IČO, názov spoločnosti alebo adresu
            </p>
        </div>
        
        <!-- Search Input with Live Results -->
        <div class="relative mb-6">
            <div class="relative">
                <input 
                    type="text"
                    x-model="query"
                    @input.debounce.300ms="search()"
                    placeholder="Hľadať..."
                    class="input-glass pl-12 pr-12"
                />
                
                <!-- Search Icon -->
                <div class="absolute left-4 top-1/2 -translate-y-1/2 text-tatra-300 dark:text-porcelain-400">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                </div>
                
                <!-- Loading Spinner -->
                <div 
                    x-show="loading" 
                    class="absolute right-4 top-1/2 -translate-y-1/2"
                    style="display: none;"
                >
                    <svg class="animate-spin w-5 h-5 text-slovak-crimson" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                </div>
                
                <!-- Clear Button -->
                <button 
                    x-show="query.length > 0"
                    @click="query = ''; results = []; searching = false"
                    class="absolute right-4 top-1/2 -translate-y-1/2 text-tatra-400 dark:text-porcelain-400 hover:text-tatra-navy dark:hover:text-porcelain-100 transition-colors"
                    style="display: none;"
                >
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            
            <!-- Autocomplete Dropdown -->
            <div 
                x-show="searching && results.length > 0"
                x-transition:enter="transition ease-out duration-200"
                x-transition:enter-start="opacity-0 translate-y-2"
                x-transition:enter-end="opacity-100 translate-y-0"
                x-transition:leave="transition ease-in duration-150"
                x-transition:leave-start="opacity-100"
                x-transition:leave-end="opacity-0"
                class="absolute top-full mt-2 left-0 right-0 z-10"
                style="display: none;"
            >
                <x-glass-card padding="none" class="max-h-96 overflow-y-auto">
                    <template x-for="(result, index) in results" :key="index">
                        <div 
                            class="px-6 py-4 hover:bg-tatra-navy/5 dark:hover:bg-white/5 transition-colors cursor-pointer border-b border-tatra-100 dark:border-matte-700 last:border-b-0"
                            @click="window.location.href = '/company/' + result.ico"
                        >
                            <div class="flex items-start justify-between">
                                <div class="flex-1">
                                    <h3 class="text-sm font-semibold text-tatra-navy dark:text-porcelain-100 mb-1" x-text="result.name"></h3>
                                    <div class="flex items-center space-x-3 text-xs text-tatra-400 dark:text-porcelain-400">
                                        <span class="flex items-center">
                                            <svg class="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                                            </svg>
                                            IČO: <span x-text="result.ico"></span>
                                        </span>
                                        <span class="flex items-center">
                                            <svg class="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                            </svg>
                                            <span x-text="result.city"></span>
                                        </span>
                                    </div>
                                </div>
                                <span 
                                    class="badge badge-success ml-4"
                                    x-show="result.status === 'active'"
                                >
                                    Aktívna
                                </span>
                            </div>
                        </div>
                    </template>
                </x-glass-card>
            </div>
        </div>
        
        <!-- Quick Filters -->
        <div class="mb-6">
            <p class="text-sm text-tatra-400 dark:text-porcelain-400 mb-3">Rýchle filtre</p>
            <div class="flex flex-wrap gap-2">
                @foreach(['Všetky', 's.r.o.', 'a.s.', 'Bratislava', 'Košice', 'IT sektor'] as $filter)
                    <button class="px-4 py-2 bg-white/50 dark:bg-matte-700/50 backdrop-blur-md border border-white/30 dark:border-white/20 text-sm text-tatra-navy dark:text-porcelain-100 rounded-full hover:bg-slovak-crimson hover:text-white hover:border-slovak-crimson transition-all duration-200 active:scale-95">
                        {{ $filter }}
                    </button>
                @endforeach
            </div>
        </div>
        
        <!-- Empty State (shown when no search) -->
        <div 
            x-show="!searching"
            x-transition:enter="transition ease-out duration-300"
            x-transition:enter-start="opacity-0 scale-95"
            x-transition:enter-end="opacity-100 scale-100"
        >
            <x-glass-card padding="lg" class="text-center">
                <!-- Illustration -->
                <div class="mb-6 flex justify-center">
                    <div class="relative">
                        <div class="w-32 h-32 bg-gradient-tatra rounded-full flex items-center justify-center">
                            <svg class="w-16 h-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                        </div>
                        <div class="absolute -top-2 -right-2 w-8 h-8 bg-slovak-crimson rounded-full flex items-center justify-center animate-pulse">
                            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                            </svg>
                        </div>
                    </div>
                </div>
                
                <h3 class="text-xl font-display font-bold text-tatra-navy dark:text-porcelain-100 mb-2">
                    Začnite vyhľadávať
                </h3>
                <p class="text-sm text-tatra-400 dark:text-porcelain-400 mb-6 max-w-sm mx-auto">
                    Zadajte aspoň 2 znaky pre zobrazenie výsledkov z našej databázy 250,000+ slovenských firiem
                </p>
                
                <!-- Popular Searches -->
                <div class="text-left max-w-sm mx-auto">
                    <p class="text-xs text-tatra-400 dark:text-porcelain-400 mb-2">Populárne vyhľadávania:</p>
                    <div class="space-y-2">
                        @foreach(['Eset', 'Slovnaft', 'Orange Slovensko'] as $popular)
                            <button 
                                class="w-full text-left px-4 py-3 bg-tatra-navy/5 dark:bg-white/5 hover:bg-tatra-navy/10 dark:hover:bg-white/10 rounded-xl transition-colors flex items-center justify-between group"
                                @click="query = '{{ $popular }}'; search()"
                            >
                                <span class="text-sm text-tatra-navy dark:text-porcelain-100">{{ $popular }}</span>
                                <svg class="w-4 h-4 text-tatra-400 dark:text-porcelain-400 group-hover:text-slovak-crimson transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                                </svg>
                            </button>
                        @endforeach
                    </div>
                </div>
            </x-glass-card>
        </div>
        
        <!-- No Results State -->
        <div 
            x-show="searching && results.length === 0 && !loading"
            x-transition:enter="transition ease-out duration-300"
            x-transition:enter-start="opacity-0 scale-95"
            x-transition:enter-end="opacity-100 scale-100"
            style="display: none;"
        >
            <x-glass-card padding="lg" class="text-center">
                <div class="mb-4 flex justify-center">
                    <div class="w-20 h-20 bg-tatra-navy/10 dark:bg-white/10 rounded-full flex items-center justify-center">
                        <svg class="w-10 h-10 text-tatra-400 dark:text-porcelain-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                </div>
                <h3 class="text-lg font-bold text-tatra-navy dark:text-porcelain-100 mb-2">
                    Nenašli sme žiadnu zhodu
                </h3>
                <p class="text-sm text-tatra-400 dark:text-porcelain-400 mb-4">
                    Skúste zmeniť vyhľadávací výraz alebo použite rýchle filtre
                </p>
                <x-primary-button variant="secondary" @click="query = ''; results = []; searching = false">
                    Vymazať hľadanie
                </x-primary-button>
            </x-glass-card>
        </div>
        
        <!-- Skeleton Loader (shown when loading) -->
        <div 
            x-show="loading && query.length > 0"
            class="space-y-3"
            style="display: none;"
        >
            @for($i = 0; $i < 3; $i++)
                <x-glass-card padding="default">
                    <div class="flex items-start space-x-4">
                        <div class="skeleton w-12 h-12 rounded-xl"></div>
                        <div class="flex-1 space-y-2">
                            <div class="skeleton h-4 w-3/4 rounded-lg"></div>
                            <div class="skeleton h-3 w-1/2 rounded-lg"></div>
                        </div>
                    </div>
                </x-glass-card>
            @endfor
        </div>
        
    </div>
    
</x-app-layout>
