@props([
    'type' => 'button',
    'variant' => 'primary', // primary, secondary, ghost, danger
    'size' => 'default', // sm, default, lg
    'loading' => false,
    'disabled' => false,
    'icon' => null,
    'iconPosition' => 'left', // left, right
    'fullWidth' => false,
])

@php
    $baseClasses = 'inline-flex items-center justify-center font-semibold transition-smooth active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100';
    
    // Size classes
    $sizeClasses = match($size) {
        'sm' => 'px-4 py-2 text-sm rounded-full',
        'lg' => 'px-8 py-4 text-lg rounded-full',
        default => 'px-6 py-3 text-base rounded-full',
    };
    
    // Variant classes
    $variantClasses = match($variant) {
        'primary' => 'btn-primary',
        'secondary' => 'btn-secondary',
        'ghost' => 'btn-ghost',
        'danger' => 'px-6 py-3 bg-red-500 hover:bg-red-600 text-white shadow-lg hover:shadow-xl rounded-full',
        default => 'btn-primary',
    };
    
    // Full width
    $widthClass = $fullWidth ? 'w-full' : '';
    
    $classes = trim("$baseClasses $sizeClasses $variantClasses $widthClass");
    
    $isDisabled = $disabled || $loading;
@endphp

<button 
    type="{{ $type }}"
    {{ $attributes->merge(['class' => $classes]) }}
    @if($isDisabled) disabled @endif
    x-data="{ ripple: false }"
    @click="ripple = true; setTimeout(() => ripple = false, 600)"
>
    <!-- Loading Spinner -->
    @if($loading)
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
    @endif
    
    <!-- Icon Left -->
    @if($icon && $iconPosition === 'left' && !$loading)
        <x-icon :name="$icon" class="w-5 h-5 mr-2" />
    @endif
    
    <!-- Button Text -->
    <span>{{ $slot }}</span>
    
    <!-- Icon Right -->
    @if($icon && $iconPosition === 'right' && !$loading)
        <x-icon :name="$icon" class="w-5 h-5 ml-2" />
    @endif
    
    <!-- Ripple Effect -->
    <span 
        x-show="ripple"
        x-transition:enter="transition ease-out duration-300"
        x-transition:enter-start="opacity-0 scale-0"
        x-transition:enter-end="opacity-100 scale-100"
        x-transition:leave="transition ease-in duration-300"
        x-transition:leave-start="opacity-100 scale-100"
        x-transition:leave-end="opacity-0 scale-150"
        class="absolute inset-0 bg-white/20 rounded-full pointer-events-none"
        style="display: none;"
    ></span>
</button>
