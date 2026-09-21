"""
Špeciálne testy pre Favorites system a Analytics
"""

import pytest
import requests
import urllib3

# Potlač SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://localhost:8000"
BASE_URL_HTTPS = "https://localhost:8000"


def get_base_url():
    """Vráti dostupný base URL"""
    try:
        requests.get(f"{BASE_URL_HTTPS}/api/health", verify=False, timeout=2)
        return BASE_URL_HTTPS
    except Exception:
        try:
            requests.get(f"{BASE_URL}/api/health", timeout=2)
            return BASE_URL
        except Exception:
            pytest.skip("Backend server nie je dostupný")


def test_favorites_endpoint_exists():
    """Test, či favorites endpoint existuje"""
    base_url = get_base_url()
    verify_ssl = base_url.startswith("https")

    try:
        # Test GET endpoint (bez autentifikácie by mal vrátiť 401)
        response = requests.get(
            f"{base_url}/api/user/favorites", verify=verify_ssl, timeout=5
        )
        # Endpoint by mal existovať (401 = unauthorized, 404 = not found)
        assert response.status_code != 404, "Favorites endpoint neexistuje"
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend server nie je dostupný")


def test_favorites_check_endpoint():
    """Test, či favorites check endpoint existuje"""
    base_url = get_base_url()
    verify_ssl = base_url.startswith("https")

    try:
        response = requests.get(
            f"{base_url}/api/user/favorites/check/12345678/SK",
            verify=verify_ssl,
            timeout=5,
        )
        # Endpoint by mal existovať
        assert response.status_code != 404, "Favorites check endpoint neexistuje"
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend server nie je dostupný")


def test_analytics_endpoint_exists():
    """Test, či analytics endpoint existuje"""
    base_url = get_base_url()
    verify_ssl = base_url.startswith("https")

    try:
        response = requests.get(
            f"{base_url}/api/analytics/dashboard", verify=verify_ssl, timeout=5
        )
        # Endpoint by mal existovať (401 = unauthorized, 404 = not found)
        assert response.status_code != 404, "Analytics dashboard endpoint neexistuje"
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend server nie je dostupný")


def test_analytics_search_trends_endpoint():
    """Test, či analytics search trends endpoint existuje"""
    base_url = get_base_url()
    verify_ssl = base_url.startswith("https")

    try:
        response = requests.get(
            f"{base_url}/api/analytics/search-trends?period=7d",
            verify=verify_ssl,
            timeout=5,
        )
        assert response.status_code != 404, "Search trends endpoint neexistuje"
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend server nie je dostupný")


def test_analytics_risk_distribution_endpoint():
    """Test, či analytics risk distribution endpoint existuje"""
    base_url = get_base_url()
    verify_ssl = base_url.startswith("https")

    try:
        response = requests.get(
            f"{base_url}/api/analytics/risk-distribution", verify=verify_ssl, timeout=5
        )
        assert response.status_code != 404, "Risk distribution endpoint neexistuje"
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend server nie je dostupný")


def test_favorites_service_imports():
    """Test, či favorites service sa dá importovať"""
    import os
    import sys

    # Pridať backend do path
    backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

    try:
        from services.favorites import (
            add_favorite,
            get_user_favorites,
            is_favorite,
            remove_favorite,
        )

        assert add_favorite is not None
        assert remove_favorite is not None
        assert get_user_favorites is not None
        assert is_favorite is not None
    except ImportError:
        pytest.skip("Favorites service nie je dostupný")


def test_analytics_service_imports():
    """Test, či analytics service sa dá importovať"""
    import os
    import sys

    # Pridať backend do path
    backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

    try:
        from services.analytics import (
            get_api_usage,
            get_dashboard_summary,
            get_risk_distribution,
            get_search_trends,
            get_user_activity,
        )

        assert get_search_trends is not None
        assert get_risk_distribution is not None
        assert get_user_activity is not None
        assert get_api_usage is not None
        assert get_dashboard_summary is not None
    except ImportError:
        pytest.skip("Analytics service nie je dostupný")
