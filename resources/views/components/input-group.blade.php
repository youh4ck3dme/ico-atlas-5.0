@props([
    'label' => null,
    'name' => null,
    'type' => 'text',
    'placeholder' => ' ',
    'value' => null,
    'error' => null,
    'icon' => null,
    'iconPosition' => 'left', // left, right
    'required' => false,
    'disabled' => false,
])

@php
    $inputId = $name ?? 'input-' . uniqid();
    $hasIcon = !empty($icon);
    
    $inputClasses = 'input-glass peer';
    if ($hasIcon && $iconPosition === 'left') {
        $inputClasses .= ' pl-12';
    }
    if ($hasIcon && $iconPosition === 'right') {
        $inputClasses .= ' pr-12';
    }
    if ($error) {
        $inputClasses .= ' !border-slovak-crimson !ring-slovak-crimson';
    }
@endphp

<div {{ $attributes->merge(['class' => 'relative']) }}>
    
    <!-- Icon Left -->
    @if($hasIcon && $iconPosition === 'left')
        <div class="absolute left-4 top-1/2 -translate-y-1/2 text-tatra-300 dark:text-porcelain-400 pointer-events-none peer-focus:text-tatra-navy dark:peer-focus:text-porcelain-100 transition-colors">
            <x-icon :name="$icon" class="w-5 h-5" />
        </div>
    @endif
    
    <!-- Input Field -->
    <input
        type="{{ $type }}"
        id="{{ $inputId }}"
        name="{{ $name }}"
        value="{{ old($name, $value) }}"
        placeholder="{{ $placeholder }}"
        {{ $attributes->except(['class', 'label', 'error']) }}
        @if($required) required @endif
        @if($disabled) disabled @endif
        class="{{ $inputClasses }}"
    />
    
    <!-- Icon Right -->
    @if($hasIcon && $iconPosition === 'right')
        <div class="absolute right-4 top-1/2 -translate-y-1/2 text-tatra-300 dark:text-porcelain-400 pointer-events-none peer-focus:text-tatra-navy dark:peer-focus:text-porcelain-100 transition-colors">
            <x-icon :name="$icon" class="w-5 h-5" />
        </div>
    @endif
    
    <!-- Floating Label -->
    @if($label)
        <label 
            for="{{ $inputId }}"
            class="absolute left-4 top-1/2 -translate-y-1/2 text-tatra-300 dark:text-porcelain-400 transition-all duration-200 pointer-events-none
                   peer-focus:top-2 peer-focus:text-xs peer-focus:text-tatra-navy dark:peer-focus:text-porcelain-100
                   peer-[:not(:placeholder-shown)]:top-2 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:text-tatra-navy dark:peer-[:not(:placeholder-shown)]:text-porcelain-100"
            @if($hasIcon && $iconPosition === 'left') style="left: 3rem;" @endif
        >
            {{ $label }}
            @if($required)
                <span class="text-slovak-crimson">*</span>
            @endif
        </label>
    @endif
    
    <!-- Error Message -->
    @if($error)
        <div class="flex items-start mt-2 text-sm text-slovak-crimson">
            <svg class="w-4 h-4 mr-1 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span>{{ $error }}</span>
        </div>
    @endif
    
    @error($name)
        <div class="flex items-start mt-2 text-sm text-slovak-crimson animate-slide-down">
            <svg class="w-4 h-4 mr-1 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span>{{ $message }}</span>
        </div>
    @enderror
    
</div>

{{-- Simple Icon Component (if not using Lucide/Blade UI Kit) --}}
@unless(class_exists('BladeUI\Icons\BladeIconsServiceProvider'))
    @php
        $iconSvgs = [
            'search' => '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>',
            'mail' => '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>',
            'lock' => '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>',
            'user' => '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>',
            'phone' => '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>',
        ];
    @endphp
@endunless
