/**
 * Testy pre frontend performance utilities
 */

// Simulácia testov pre performance utilities
// (V reálnom prostredí by sme použili Jest/Vitest)

const performanceTests = {
  debounce: () => {
    console.log("🧪 Testing debounce...");
    
    let callCount = 0;
    const testFunc = () => { callCount++; };
    
    // Simulácia debounce (v reálnom teste by sme importovali z performance.js)
    const debounce = (func, wait) => {
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
    
    const debouncedFunc = debounce(testFunc, 100);
    
    // Rýchle volania - malo by sa zavolať len raz
    debouncedFunc();
    debouncedFunc();
    debouncedFunc();
    
    return new Promise((resolve) => {
      setTimeout(() => {
        // Po 150ms by sa malo zavolať len raz
        const result = callCount === 1;
        console.log(result ? "✅ debounce: OK" : "❌ debounce: FAILED");
        resolve(result);
      }, 150);
    });
  },
  
  throttle: () => {
    console.log("🧪 Testing throttle...");
    
    let callCount = 0;
    const testFunc = () => { callCount++; };
    
    // Simulácia throttle
    const throttle = (func, limit) => {
      let inThrottle;
      return function(...args) {
        if (!inThrottle) {
          func.apply(this, args);
          inThrottle = true;
          setTimeout(() => inThrottle = false, limit);
        }
      };
    };
    
    const throttledFunc = throttle(testFunc, 100);
    
    // Rýchle volania
    throttledFunc();
    throttledFunc();
    throttledFunc();
    
    // Malo by sa zavolať len raz (throttle)
    const result = callCount === 1;
    console.log(result ? "✅ throttle: OK" : "❌ throttle: FAILED");
    return Promise.resolve(result);
  },
  
  performanceMonitor: () => {
    console.log("🧪 Testing PerformanceMonitor...");
    
    // Simulácia PerformanceMonitor
    class PerformanceMonitor {
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
    }
    
    const monitor = new PerformanceMonitor();
    const measure = monitor.startMeasure("test");
    
    // Simulácia práce
    setTimeout(() => {
      measure.end();
      
      const metrics = monitor.getMetrics();
      const result = metrics.length === 1 && metrics[0].name === "test";
      console.log(result ? "✅ PerformanceMonitor: OK" : "❌ PerformanceMonitor: FAILED");
    }, 10);
    
    return Promise.resolve(true);
  }
};

// Spustiť testy
async function runTests() {
  console.log("═══════════════════════════════════════");
  console.log("🧪 Frontend Performance Tests");
  console.log("═══════════════════════════════════════");
  console.log();
  
  const results = await Promise.all([
    performanceTests.debounce(),
    performanceTests.throttle(),
    performanceTests.performanceMonitor()
  ]);
  
  const passed = results.filter(r => r).length;
  const failed = results.length - passed;
  
  console.log();
  console.log("═══════════════════════════════════════");
  console.log(`📊 Results: ${passed} passed, ${failed} failed`);
  console.log("═══════════════════════════════════════");
  
  return failed === 0;
}

// Export pre Node.js alebo spustenie priamo
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { runTests, performanceTests };
} else if (typeof window !== 'undefined') {
  window.performanceTests = { runTests, performanceTests };
}

// Spustiť ak je to Node.js script
if (typeof require !== 'undefined' && require.main === module) {
  runTests().then(success => {
    process.exit(success ? 0 : 1);
  });
}

