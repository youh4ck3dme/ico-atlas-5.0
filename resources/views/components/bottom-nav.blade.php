@props([
    'currentRoute' => null,
])

@php
    $current = $currentRoute ?? request()->route()->getName();
    
    $navItems = [
        [
            'route' => 'home',
            'label' => 'Domov',
            'icon' => 'home',
        ],
        [
            'route' => 'search',
            'label' => 'Hľadať',
            'icon' => 'search',
        ],
        [
            'route' => 'dashboard',
            'label' => 'Dashboard',
            'icon' => 'layout-dashboard',
        ],
        [
            'route' => 'profile',
            'label' => 'Profil',
            'icon' => 'user',
        ],
    ];
@endphp

<nav class="fixed bottom-0 left-0 right-0 safe-bottom z-40">
    <div class="mobile-frame px-4 pb-4">
        <!-- Glass Dock Container -->
        <div class="glass-card-lg">
            <div class="flex items-center justify-around p-2">
                
                @foreach($navItems as $item)
                    @php
                        $isActive = $current === $item['route'];
                        $activeClasses = $isActive 
                            ? 'text-slovak-crimson bg-slovak-crimson/10' 
                            : 'text-tatra-400 dark:text-porcelain-400 hover:text-tatra-navy dark:hover:text-porcelain-100';
                    @endphp
                    
                    <a 
                        href="{{ route($item['route']) }}"
                        class="flex flex-col items-center justify-center space-y-1 px-4 py-2 rounded-2xl transition-all duration-300 {{ $activeClasses }} active:scale-95"
                        aria-label="{{ $item['label'] }}"
                        x-data="{ pressed: false }"
                        @mousedown="pressed = true"
                        @mouseup="pressed = false"
                        @mouseleave="pressed = false"
                    >
                        <!-- Icon Container with Ripple Effect -->
                        <div class="relative">
                            <!-- Active Indicator -->
                            @if($isActive)
                                <div class="absolute -top-1 -right-1 w-2 h-2 bg-slovak-crimson rounded-full animate-pulse"></div>
                            @endif
                            
                            <!-- Icon -->
                            <x-lucide-icon 
                                :name="$item['icon']" 
                                class="w-6 h-6 transition-transform duration-200"
                                :class="{ 'scale-110': pressed }"
                                x-bind:class="{ 'scale-110': pressed }"
                            />
                        </div>
                        
                        <!-- Label -->
                        <span class="text-xs font-medium tracking-tight">
                            {{ $item['label'] }}
                        </span>
                        
                        <!-- Active Underline -->
                        @if($isActive)
                            <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-1 h-1 bg-slovak-crimson rounded-full"></div>
                        @endif
                    </a>
                @endforeach
                
            </div>
        </div>
        
        <!-- iPhone Home Indicator -->
        <div class="flex justify-center mt-2">
            <div class="w-32 h-1 bg-tatra-navy/20 dark:bg-porcelain-100/20 rounded-full"></div>
        </div>
    </div>
</nav>

{{-- Lucide Icon Component (Fallback if not using Blade UI Kit) --}}
@unless(class_exists('BladeUI\Icons\BladeIconsServiceProvider'))
    {{-- Simple SVG Icons --}}
    @php
        $icons = [
            'home' => '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />',
            'search' => '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />',
            'layout-dashboard' => '<rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" />',
            'user' => '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />',
        ];
    @endphp
    
    @push('scripts')
    <script>
        // Simple icon component replacement
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('[data-icon]').forEach(el => {
                const iconName = el.getAttribute('data-icon');
                const iconPath = @json($icons)[iconName];
                if (iconPath) {
                    el.innerHTML = iconPath;
                }
            });
        });
    </script>
    @endpush
@endunless
