import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

import pytest
from unittest.mock import MagicMock, patch
from services.audit_service import AuditService

@pytest.fixture
def mock_orsr_provider():
    with patch("services.audit_service.OrsrProvider") as MockProvider:
        provider_instance = MockProvider.return_value
        yield provider_instance

@pytest.fixture
def audit_service(mock_orsr_provider):
    return AuditService()

def test_audit_company_not_found(audit_service, mock_orsr_provider):
    """Test when company is not found in ORSR"""
    mock_orsr_provider.lookup_by_ico.return_value = None
    
    result = audit_service.perform_deep_audit("00000000")
    
    assert result["summary"]["status"] == "NENÁJDENÁ"
    assert result["risk_score"] == 0
    assert len(result["alerts"]) > 0

def test_audit_high_risk_company(audit_service, mock_orsr_provider):
    """Test company with virtual address and debts (simulated via IČO)"""
    mock_data = {
        "name": "Risky Business s.r.o.",
        "address": "Napájadlá 7, Košice",
        "status": "Aktívna",
        "postal_code": "04001",
        "executives": ["Ján Risk"]
    }
    mock_orsr_provider.lookup_by_ico.return_value = mock_data
    
    # 51200678 triggers hardcoded debt simulation
    result = audit_service.perform_deep_audit("51200678")
    
    # Check Virtual Address Detection
    assert result["address_analysis"]["is_virtual_suspect"] is True
    
    # Check Debt Detection (based on simulation for this IČO)
    assert len(result["debts"]) > 0
    
    # Check Scores
    assert result["risk_score"] >= 8 # 3 (virtual) + 5 (debts)
    assert result["summary"]["verdict"] == "KRITICKÉ RIZIKO" or result["summary"]["verdict"] == "ZVÝŠENÉ RIZIKO"

def test_audit_low_risk_company(audit_service, mock_orsr_provider):
    """Test standard company without risks"""
    mock_data = {
        "name": "Safe Company a.s.",
        "address": "Priemyselná 1, Žilina",
        "status": "Aktívna",
        "postal_code": "01001",
        "executives": ["Peter Safe"]
    }
    mock_orsr_provider.lookup_by_ico.return_value = mock_data
    
    result = audit_service.perform_deep_audit("12345678")
    
    assert result["address_analysis"]["is_virtual_suspect"] is False
    assert len(result["debts"]) == 0
    assert result["risk_score"] < 5
    assert result["summary"]["verdict"] == "NÍZKE RIZIKO"

def test_audit_liquidated_company(audit_service, mock_orsr_provider):
    """Test company in liquidation"""
    mock_data = {
        "name": "Old Company s.r.o.",
        "address": "Mierová 5, Bratislava",
        "status": "V likvidácii",
        "postal_code": "81101",
        "executives": []
    }
    mock_orsr_provider.lookup_by_ico.return_value = mock_data
    
    result = audit_service.perform_deep_audit("87654321")
    
    # Should have high risk due to status
    assert result["risk_score"] >= 7
    assert any("likvid" in a["message"].lower() for a in result["alerts"])
