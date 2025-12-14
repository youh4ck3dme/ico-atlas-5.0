@props([
    'variant' => 'default', // default, sm, lg
    'padding' => 'default', // none, sm, default, lg
    'hover' => false,
    'clickable' => false,
])

@php
    $baseClasses = 'transition-smooth';
    
    // Variant classes
    $variantClasses = match($variant) {
        'sm' => 'glass-card-sm',
        'lg' => 'glass-card-lg',
        default => 'glass-card',
    };
    
    // Padding classes
    $paddingClasses = match($padding) {
        'none' => '',
        'sm' => 'p-4',
        'lg' => 'p-8',
        default => 'p-6',
    };
    
    // Interactive states
    $interactiveClasses = '';
    if ($hover || $clickable) {
        $interactiveClasses = 'hover:shadow-glass-lg dark:hover:shadow-glass-dark-lg hover:-translate-y-1';
    }
    if ($clickable) {
        $interactiveClasses .= ' cursor-pointer active:scale-[0.98]';
    }
    
    $classes = trim("$baseClasses $variantClasses $paddingClasses $interactiveClasses");
@endphp

<div {{ $attributes->merge(['class' => $classes]) }}>
    {{ $slot }}
</div>
