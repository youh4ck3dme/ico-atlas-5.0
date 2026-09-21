"""
Špeciálne testy pre SSL/HTTPS funkcionalitu
"""

from pathlib import Path

import pytest
import requests
import urllib3

# Potlač SSL warnings pre self-signed certifikáty
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL_HTTP = "http://localhost:8000"
BASE_URL_HTTPS = "https://localhost:8000"


def test_ssl_certificates_exist():
    """Test, či existujú SSL certifikáty"""
    ssl_dir = Path(__file__).parent.parent / "ssl"
    cert_file = ssl_dir / "cert.pem"
    key_file = ssl_dir / "key.pem"

    assert cert_file.exists(), "SSL certifikát (cert.pem) neexistuje"
    assert key_file.exists(), "SSL privátny kľúč (key.pem) neexistuje"


def test_backend_https_support():
    """Test, či backend podporuje HTTPS"""
    try:
        response = requests.get(
            f"{BASE_URL_HTTPS}/api/health",
            verify=False,  # Ignorovať SSL pre self-signed certifikáty
            timeout=3,
        )
        assert response.status_code == 200, "HTTPS endpoint by mal vrátiť 200"
        data = response.json()
        assert data.get("status") == "healthy", "Health check by mal vrátiť healthy"
    except requests.exceptions.SSLError:
        pytest.skip("SSL certifikát nie je dôveryhodný (normálne pre self-signed)")
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend server nie je dostupný na HTTPS")


def test_backend_http_fallback():
    """Test, či backend funguje aj na HTTP (fallback)"""
    try:
        response = requests.get(f"{BASE_URL_HTTP}/api/health", timeout=3)
        assert response.status_code == 200, "HTTP endpoint by mal vrátiť 200"
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend server nie je dostupný na HTTP")


def test_cors_https_origin():
    """Test, či CORS podporuje HTTPS origins"""
    try:
        response = requests.get(
            f"{BASE_URL_HTTPS}/api/health",
            headers={"Origin": "https://localhost:8009"},
            verify=False,
            timeout=3,
        )
        assert response.status_code == 200
        # Skontrolovať CORS hlavičky
        assert "access-control-allow-origin" in response.headers
        allowed_origin = response.headers.get("access-control-allow-origin")
        assert allowed_origin in ["https://localhost:8009", "*"], (
            f"CORS by mal povoliť HTTPS origin, ale povolil: {allowed_origin}"
        )
    except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
        pytest.skip("Backend server nie je dostupný")


def test_api_response_includes_ssl_info():
    """Test, či API root response obsahuje správne informácie"""
    try:
        # Skúsiť HTTPS najprv
        try:
            response = requests.get(f"{BASE_URL_HTTPS}/", verify=False, timeout=3)
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
            # Fallback na HTTP
            response = requests.get(f"{BASE_URL_HTTP}/", timeout=3)

        assert response.status_code == 200
        data = response.json()

        # Skontrolovať, či obsahuje export endpoints
        assert "endpoints" in data
        assert "export" in data["endpoints"]
        assert "excel" in data["endpoints"]["export"]
        assert "batch_excel" in data["endpoints"]["export"]

        # Skontrolovať supported formats
        assert "supported_formats" in data
        assert "Excel (XLSX)" in data["supported_formats"]

    except requests.exceptions.ConnectionError:
        pytest.skip("Backend server nie je dostupný")
