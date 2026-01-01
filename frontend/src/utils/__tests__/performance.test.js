import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { debounce, throttle, PerformanceMonitor } from '../performance';

describe('Performance utilities', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('debounce', () => {
    it('delays function execution', () => {
      const mockFn = vi.fn();
      const debouncedFn = debounce(mockFn, 100);

      debouncedFn();
      expect(mockFn).not.toHaveBeenCalled();

      vi.advanceTimersByTime(100);
      expect(mockFn).toHaveBeenCalledTimes(1);
    });

    it('cancels previous calls when called multiple times', () => {
      const mockFn = vi.fn();
      const debouncedFn = debounce(mockFn, 100);

      debouncedFn();
      debouncedFn();
      debouncedFn();

      vi.advanceTimersByTime(100);
      expect(mockFn).toHaveBeenCalledTimes(1);
    });

    it('passes arguments correctly', () => {
      const mockFn = vi.fn();
      const debouncedFn = debounce(mockFn, 100);

      debouncedFn('arg1', 'arg2');
      vi.advanceTimersByTime(100);

      expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
    });
  });

  describe('throttle', () => {
    it('limits function execution frequency', () => {
      const mockFn = vi.fn();
      const throttledFn = throttle(mockFn, 100);

      throttledFn();
      expect(mockFn).toHaveBeenCalledTimes(1);

      throttledFn();
      throttledFn();
      expect(mockFn).toHaveBeenCalledTimes(1);

      vi.advanceTimersByTime(100);
      throttledFn();
      expect(mockFn).toHaveBeenCalledTimes(2);
    });
  });

  describe('PerformanceMonitor', () => {
    it('tracks performance metrics', () => {
      const monitor = new PerformanceMonitor();
      const measure = monitor.startMeasure('test');

      measure.end();
      const metrics = monitor.getMetrics();

      expect(metrics).toHaveLength(1);
      expect(metrics[0].name).toBe('test');
      expect(metrics[0].duration).toBeGreaterThanOrEqual(0);
    });

    it('tracks multiple metrics', () => {
      const monitor = new PerformanceMonitor();
      
      const measure1 = monitor.startMeasure('test1');
      measure1.end();
      
      const measure2 = monitor.startMeasure('test2');
      measure2.end();

      const metrics = monitor.getMetrics();
      expect(metrics).toHaveLength(2);
      expect(metrics[0].name).toBe('test1');
      expect(metrics[1].name).toBe('test2');
    });
  });
});

