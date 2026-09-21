/**
 * Performance utilities pre ILUMINATI SYSTEM
 */

/**
 * Debounce function - oneskorenie volania funkcie
 */
export function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function - obmedzenie frekvencie volania
 */
export function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * Lazy load image
 */
export function lazyLoadImage(src, placeholder = '/placeholder.svg') {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
}

/**
 * Virtual scrolling helper
 */
export function getVisibleItems(items, containerHeight, itemHeight, scrollTop) {
  const start = Math.floor(scrollTop / itemHeight);
  const end = Math.min(
    start + Math.ceil(containerHeight / itemHeight) + 1,
    items.length
  );
  return {
    start,
    end,
    visibleItems: items.slice(start, end),
    offsetY: start * itemHeight
  };
}

/**
 * Performance monitor
 */
export class PerformanceMonitor {
  constructor() {
    this.metrics = [];
  }

  startMeasure(name) {
    const start = performance.now();
    return {
      end: () => {
        const duration = performance.now() - start;
        this.metrics.push({ name, duration, timestamp: Date.now() });
        return duration;
      }
    };
  }

  getMetrics() {
    return this.metrics;
  }

  getAverage(name) {
    const filtered = this.metrics.filter(m => m.name === name);
    if (filtered.length === 0) return 0;
    const sum = filtered.reduce((acc, m) => acc + m.duration, 0);
    return sum / filtered.length;
  }

  clear() {
    this.metrics = [];
  }
}

// Global instance
export const performanceMonitor = new PerformanceMonitor();

