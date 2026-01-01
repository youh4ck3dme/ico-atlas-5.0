"""
Metrics & Monitoring service
Zbieranie metrík pre monitoring a analytics
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import time


class MetricsCollector:
    """
    Zbieranie metrík pre monitoring.
    """
    
    def __init__(self):
        self._counters: Dict[str, int] = defaultdict(int)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = defaultdict(list)
        self._timers: Dict[str, List[float]] = defaultdict(list)
        self._events: List[Dict] = []
        self._max_events = 1000  # Max počet eventov v pamäti
        
    def increment(self, metric_name: str, value: int = 1, tags: Optional[Dict] = None):
        """Zvýši counter"""
        key = self._build_key(metric_name, tags)
        self._counters[key] += value
    
    def decrement(self, metric_name: str, value: int = 1, tags: Optional[Dict] = None):
        """Zníži counter"""
        key = self._build_key(metric_name, tags)
        self._counters[key] -= value
    
    def gauge(self, metric_name: str, value: float, tags: Optional[Dict] = None):
        """Nastaví gauge hodnotu"""
        key = self._build_key(metric_name, tags)
        self._gauges[key] = value
    
    def histogram(self, metric_name: str, value: float, tags: Optional[Dict] = None):
        """Pridá hodnotu do histogramu"""
        key = self._build_key(metric_name, tags)
        self._histograms[key].append(value)
        # Limitovať veľkosť histogramu
        if len(self._histograms[key]) > 1000:
            self._histograms[key] = self._histograms[key][-1000:]
    
    def timer(self, metric_name: str, duration: float, tags: Optional[Dict] = None):
        """Pridá čas do timeru"""
        key = self._build_key(metric_name, tags)
        self._timers[key].append(duration)
        # Limitovať veľkosť timerov
        if len(self._timers[key]) > 1000:
            self._timers[key] = self._timers[key][-1000:]
    
    def record_event(self, event_type: str, data: Optional[Dict] = None):
        """Zaznamená event"""
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        self._events.append(event)
        # Limitovať počet eventov
        if len(self._events) > self._max_events:
            self._events = self._events[-self._max_events:]
    
    def _build_key(self, metric_name: str, tags: Optional[Dict]) -> str:
        """Vytvorí kľúč pre metric s tags"""
        if not tags:
            return metric_name
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{metric_name}[{tag_str}]"
    
    def get_metrics(self) -> Dict:
        """Vráti všetky metríky"""
        return {
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
            "histograms": {
                k: {
                    "count": len(v),
                    "min": min(v) if v else 0,
                    "max": max(v) if v else 0,
                    "avg": sum(v) / len(v) if v else 0,
                    "p95": self._percentile(v, 95) if v else 0,
                    "p99": self._percentile(v, 99) if v else 0
                }
                for k, v in self._histograms.items()
            },
            "timers": {
                k: {
                    "count": len(v),
                    "min": min(v) if v else 0,
                    "max": max(v) if v else 0,
                    "avg": sum(v) / len(v) if v else 0,
                    "p95": self._percentile(v, 95) if v else 0,
                    "p99": self._percentile(v, 99) if v else 0
                }
                for k, v in self._timers.items()
            },
            "events_count": len(self._events),
            "recent_events": self._events[-10:]  # Posledných 10 eventov
        }
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Vypočíta percentil"""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def reset(self):
        """Resetuje všetky metríky"""
        self._counters.clear()
        self._gauges.clear()
        self._histograms.clear()
        self._timers.clear()
        self._events.clear()


# Globálna inštancia
_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    """Získa globálnu inštanciu metrics collectoru"""
    return _metrics


def increment(metric_name: str, value: int = 1, tags: Optional[Dict] = None):
    """Zvýši counter"""
    _metrics.increment(metric_name, value, tags)


def gauge(metric_name: str, value: float, tags: Optional[Dict] = None):
    """Nastaví gauge"""
    _metrics.gauge(metric_name, value, tags)


def timer(metric_name: str, duration: float, tags: Optional[Dict] = None):
    """Pridá čas do timeru"""
    _metrics.timer(metric_name, duration, tags)


def record_event(event_type: str, data: Optional[Dict] = None):
    """Zaznamená event"""
    _metrics.record_event(event_type, data)


class TimerContext:
    """Context manager pre meranie času"""
    
    def __init__(self, metric_name: str, tags: Optional[Dict] = None):
        self.metric_name = metric_name
        self.tags = tags
        self.start_time: Optional[float] = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            timer(self.metric_name, duration, self.tags)

