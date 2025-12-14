import './bootstrap';
import Alpine from 'alpinejs';

// Initialize Alpine.js
window.Alpine = Alpine;

// Global Alpine stores
Alpine.store('toast', {
    items: [],
    
    show(message, type = 'info', duration = 3000) {
        const id = Date.now();
        this.items.push({ id, message, type });
        
        setTimeout(() => {
            this.items = this.items.filter(item => item.id !== id);
        }, duration);
    },
    
    success(message) {
        this.show(message, 'success');
    },
    
    error(message) {
        this.show(message, 'error');
    },
    
    info(message) {
        this.show(message, 'info');
    }
});

// Global Alpine data
Alpine.data('search', () => ({
    query: '',
    results: [],
    loading: false,
    
    async search() {
        if (this.query.length < 2) {
            this.results = [];
            return;
        }
        
        this.loading = true;
        
        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(this.query)}`);
            const data = await response.json();
            this.results = data.results || [];
        } catch (error) {
            console.error('Search error:', error);
            Alpine.store('toast').error('Chyba pri vyhľadávaní');
        } finally {
            this.loading = false;
        }
    }
}));

// Start Alpine
Alpine.start();

// PWA Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Toast notification helper
window.showToast = (message, type = 'info') => {
    window.dispatchEvent(new CustomEvent('toast', {
        detail: { 
            id: Date.now(), 
            message, 
            type 
        }
    }));
};

// Utility: Format number as Slovak currency
window.formatCurrency = (amount) => {
    return new Intl.NumberFormat('sk-SK', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
};

// Utility: Format date in Slovak
window.formatDate = (date, options = {}) => {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    return new Intl.DateTimeFormat('sk-SK', { ...defaultOptions, ...options }).format(new Date(date));
};

// Debounce utility
window.debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Smooth scroll to element
window.scrollToElement = (elementId) => {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
};

// Copy to clipboard with feedback
window.copyToClipboard = async (text) => {
    try {
        await navigator.clipboard.writeText(text);
        window.showToast('Skopírované do schránky', 'success');
    } catch (err) {
        window.showToast('Nepodarilo sa skopírovať', 'error');
    }
};

// Detect dark mode preference
window.initDarkMode = () => {
    const darkMode = localStorage.getItem('darkMode');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (darkMode === 'true' || (darkMode === null && prefersDark)) {
        document.documentElement.classList.add('dark');
        return true;
    }
    return false;
};

// Toggle dark mode
window.toggleDarkMode = () => {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', isDark);
    return isDark;
};

// Initialize dark mode on page load
document.addEventListener('DOMContentLoaded', () => {
    window.initDarkMode();
});

// Handle network status
window.addEventListener('online', () => {
    window.showToast('Pripojenie obnovené', 'success');
});

window.addEventListener('offline', () => {
    window.showToast('Odpojené od internetu', 'error');
});

// Add haptic feedback for mobile (if available)
window.haptic = (type = 'impact') => {
    if ('vibrate' in navigator) {
        const patterns = {
            impact: [10],
            notification: [10, 50, 10],
            selection: [5]
        };
        navigator.vibrate(patterns[type] || [10]);
    }
};

console.log('🎨 IČO ATLAS 5.0 initialized - Slovak Enterprise Luxury');
