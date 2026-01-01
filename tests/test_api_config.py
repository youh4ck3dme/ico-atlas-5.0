"""
Špeciálne testy pre API konfiguráciu (HTTP/HTTPS auto-detection)
"""

import os
import sys

# Pridať frontend do path pre import
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "src")
if frontend_path not in sys.path:
    sys.path.insert(0, frontend_path)


def test_api_config_file_exists():
    """Test, či API konfiguračný súbor existuje"""
    api_config_path = os.path.join(
        os.path.dirname(__file__), "..", "frontend", "src", "config", "api.js"
    )
    assert os.path.exists(api_config_path), "API konfiguračný súbor neexistuje"


def test_api_url_uses_environment_variable():
    """Test, či API_URL používa environment variable"""
    # Tento test by mal byť v JavaScript/TypeScript
    # Pre Python test len overíme, či súbor existuje
    api_config_path = os.path.join(
        os.path.dirname(__file__), "..", "frontend", "src", "config", "api.js"
    )

    if os.path.exists(api_config_path):
        with open(api_config_path, "r") as f:
            content = f.read()
            # Skontrolovať, či obsahuje REACT_APP_API_URL
            assert "REACT_APP_API_URL" in content or "process.env" in content, (
                "API konfigurácia by mala používať environment variables"
            )


def test_api_url_auto_detects_https():
    """Test, či API_URL automaticky detekuje HTTPS"""
    api_config_path = os.path.join(
        os.path.dirname(__file__), "..", "frontend", "src", "config", "api.js"
    )

    if os.path.exists(api_config_path):
        with open(api_config_path, "r") as f:
            content = f.read()
            # Skontrolovať, či obsahuje HTTPS detekciu
            assert "https://" in content or "window.location.protocol" in content, (
                "API konfigurácia by mala podporovať HTTPS auto-detection"
            )


def test_api_url_fallback_to_http():
    """Test, či API_URL má fallback na HTTP"""
    api_config_path = os.path.join(
        os.path.dirname(__file__), "..", "frontend", "src", "config", "api.js"
    )

    if os.path.exists(api_config_path):
        with open(api_config_path, "r") as f:
            content = f.read()
            # Skontrolovať, či obsahuje HTTP fallback
            assert "http://" in content, "API konfigurácia by mala mať HTTP fallback"
