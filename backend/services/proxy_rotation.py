"""
Proxy rotation služba pre externé API volania.
Zabezpečuje stabilitu a obchádza rate limiting.
"""

import os
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class ProxyPool:
    """Pool proxy serverov s rotáciou a health checking"""

    def __init__(self, max_failures: int = 5, failure_cooldown_mins: int = 15):
        self.proxies: List[Dict[str, str]] = []
        self.current_index = 0
        self.failed_proxies: Dict[str, datetime] = {}
        self.permanently_failed: set[str] = set()  # Proxies that reached max_failures
        self.proxy_stats: Dict[str, Dict] = defaultdict(
            lambda: {"success": 0, "failed": 0, "last_used": None, "last_failed": None}
        )
        self.max_failures = max_failures
        self.failure_cooldown = timedelta(minutes=failure_cooldown_mins)

    def add_proxy(self, proxy_url: str, auth: Optional[Dict[str, str]] = None):
        """
        Pridať proxy do poolu.
        """
        proxy_config = {"http": proxy_url, "https": proxy_url}

        if auth:
            if "://" in proxy_url:
                protocol = proxy_url.split("://")[0]
                rest = proxy_url.split("://")[1]
                proxy_config["http"] = (
                    f"{protocol}://{auth['username']}:{auth['password']}@{rest}"
                )
                proxy_config["https"] = proxy_config["http"]

        self.proxies.append(proxy_config)
        print(f"✅ Proxy pridané: {proxy_url}")

    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """
        Získať ďalší dostupný proxy (round-robin s health checking).
        """
        if not self.proxies:
            return None

        # Skúsiť nájsť dostupný proxy
        attempts = 0
        total_proxies = len(self.proxies)

        while attempts < total_proxies:
            proxy = self.proxies[self.current_index]
            proxy_key = str(proxy)
            
            self.current_index = (self.current_index + 1) % total_proxies
            attempts += 1

            # 1. Skontrolovať permanentné zlyhanie
            if proxy_key in self.permanently_failed:
                continue

            # 2. Skontrolovať cooldown (dočasné zlyhanie)
            if proxy_key in self.failed_proxies:
                last_failed = self.failed_proxies[proxy_key]
                if datetime.now() - last_failed < self.failure_cooldown:
                    # Proxy je stále v cooldown, preskočiť
                    continue
                else:
                    # Cooldown vypršal, skúsime ho znova
                    del self.failed_proxies[proxy_key]

            # Proxy je dostupný
            self.proxy_stats[proxy_key]["last_used"] = datetime.now()
            return proxy

        # Ak sú všetky v cooldown, použite fallback na prvý (bez permanentne zlyhaných)
        for proxy in self.proxies:
            if str(proxy) not in self.permanently_failed:
                return proxy

        return None

    def mark_success(self, proxy: Dict[str, str]):
        """Označiť proxy ako úspešné"""
        proxy_key = str(proxy)
        self.proxy_stats[proxy_key]["success"] += 1
        
        # Reset zlyhaní pri úspechu (ak nebol permanentne vyradený)
        if proxy_key in self.failed_proxies:
            del self.failed_proxies[proxy_key]

    def mark_failed(self, proxy: Dict[str, str]):
        """Označiť proxy ako zlyhané"""
        proxy_key = str(proxy)
        now = datetime.now()
        
        self.proxy_stats[proxy_key]["failed"] += 1
        self.proxy_stats[proxy_key]["last_failed"] = now
        self.failed_proxies[proxy_key] = now
        
        # Kontrola limitu zlyhaní
        if self.proxy_stats[proxy_key]["failed"] >= self.max_failures:
            print(f"❌ Proxy {proxy_key} dosiahlo limit chýb a je permanentne vyradené.")
            self.permanently_failed.add(proxy_key)

    def get_stats(self) -> Dict:
        """Získať štatistiky proxy poolu"""
        return {
            "total_count": len(self.proxies),
            "healthy_count": len(self.proxies) - len(self.failed_proxies) - len(self.permanently_failed),
            "cooldown_count": len(self.failed_proxies),
            "excluded_count": len(self.permanently_failed),
            "proxy_details": dict(self.proxy_stats),
        }



# Globálny proxy pool
_proxy_pool = ProxyPool()


def init_proxy_pool(proxy_list: Optional[List[str]] = None):
    """
    Inicializovať proxy pool s proxy servermi.

    Args:
        proxy_list: Zoznam proxy URL (napr. ["http://proxy1.com:8080", "http://proxy2.com:8080"])

    Environment Variables:
        PROXY_LIST: Comma-separated list of proxy URLs (e.g., "http://proxy1.com:8080,http://proxy2.com:8080")
        PROXY_USERNAME: Username for proxy authentication (optional)
        PROXY_PASSWORD: Password for proxy authentication (optional)
    """
    global _proxy_pool

    if proxy_list:
        for proxy_url in proxy_list:
            _proxy_pool.add_proxy(proxy_url)
        print(f"✅ Proxy pool inicializovaný s {len(proxy_list)} proxy")
        return

    # Načítať z environment variables
    proxy_env = os.getenv("PROXY_LIST", "")
    if proxy_env:
        proxies = [p.strip() for p in proxy_env.split(",") if p.strip()]
        proxy_username = os.getenv("PROXY_USERNAME")
        proxy_password = os.getenv("PROXY_PASSWORD")

        auth = None
        if proxy_username and proxy_password:
            auth = {"username": proxy_username, "password": proxy_password}

        for proxy_url in proxies:
            if auth:
                _proxy_pool.add_proxy(proxy_url, auth=auth)
            else:
                _proxy_pool.add_proxy(proxy_url)

        print(
            f"✅ Proxy pool inicializovaný s {len(proxies)} proxy z environment variables"
        )
        return

    # Žiadne proxy - používajú sa priame API volania
    print("ℹ️ Proxy pool prázdny - používajú sa priame API volania")
    print("   💡 Tip: Nastav PROXY_LIST environment variable pre proxy rotation")
    print(
        "   💡 Príklad: export PROXY_LIST='http://proxy1.com:8080,http://proxy2.com:8080'"
    )


def get_proxy() -> Optional[Dict[str, str]]:
    """
    Získať ďalší proxy z poolu.

    Returns:
        Proxy config dict alebo None ak nie sú dostupné proxy
    """
    return _proxy_pool.get_next_proxy()


def mark_proxy_success(proxy: Dict[str, str]):
    """Označiť proxy ako úspešné"""
    _proxy_pool.mark_success(proxy)


def mark_proxy_failed(proxy: Dict[str, str]):
    """Označiť proxy ako zlyhané"""
    _proxy_pool.mark_failed(proxy)


def get_proxy_stats() -> Dict:
    """Získať štatistiky proxy poolu"""
    return _proxy_pool.get_stats()


def make_request_with_proxy(
    url: str,
    headers: Optional[Dict] = None,
    timeout: int = 10,
    max_retries: int = 3,
    use_proxy: bool = True,
):
    """
    Vykonať HTTP request s proxy rotation.

    Args:
        url: URL na volanie
        headers: HTTP headers
        timeout: Timeout v sekundách
        max_retries: Maximálny počet pokusov s rôznymi proxy
        use_proxy: Použiť proxy ak sú dostupné (default: True)

    Returns:
        Response object alebo None pri chybe
    """
    import requests

    if headers is None:
        headers = {}

    # Ak nie sú proxy alebo use_proxy=False, použiť priame volanie
    proxy = get_proxy() if use_proxy else None

    for attempt in range(max_retries):
        try:
            if proxy:
                response = requests.get(
                    url, headers=headers, proxies=proxy, timeout=timeout
                )
                mark_proxy_success(proxy)
                return response
            else:
                # Priame volanie bez proxy
                response = requests.get(url, headers=headers, timeout=timeout)
                return response

        except requests.exceptions.ProxyError as e:
            if proxy:
                mark_proxy_failed(proxy)
                print(f"⚠️ Proxy chyba: {e}, skúšam ďalší proxy...")
                proxy = get_proxy() if use_proxy else None
            else:
                print(f"⚠️ Request chyba: {e}")
                return None

        except requests.exceptions.RequestException as e:
            if proxy:
                mark_proxy_failed(proxy)
                proxy = get_proxy() if use_proxy else None
            print(f"⚠️ Request chyba: {e}")
            if attempt == max_retries - 1:
                return None

    return None
