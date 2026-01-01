#!/usr/bin/env python3
"""
Test script for real IČO values to see what data we get from the background
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000"
API_KEY = None  # Set if using API keys
TEST_USER = {
    "email": "test_automation@example.com",
    "password": "TestPassword123!",
    "full_name": "Test Automation User"
}

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_test(test_name):
    print(f"\n🧪 {test_name}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def print_data(title, data, indent=0):
    """Pretty print data structure"""
    spaces = "  " * indent
    print(f"\n{spaces}📋 {title}:")
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f"{spaces}  {key}:")
                print_data("", value, indent + 2)
            else:
                print(f"{spaces}  {key}: {value}")
    elif isinstance(data, list):
        print(f"{spaces}  Count: {len(data)}")
        for i, item in enumerate(data[:3]):  # Show first 3 items
            print(f"{spaces}  [{i}]: {item}")
        if len(data) > 3:
            print(f"{spaces}  ... and {len(data) - 3} more")
    else:
        print(f"{spaces}  {data}")

def get_auth_headers():
    """Register/Login test user and return auth headers"""
    print_info("Authenticating test user...")
    
    login_url = f"{BASE_URL}/api/auth/login"
    register_url = f"{BASE_URL}/api/auth/register"
    
    login_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }

    # 1. Try Login First
    try:
        print_info("Attempting login...")
        response = requests.post(login_url, data=login_data, timeout=30)
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print_success("Login successful")
            return {"Authorization": f"Bearer {token}"}
            
        print_info(f"Login failed ({response.status_code}), attempting registration...")
        
    except Exception as e:
        print_error(f"Login error: {e}")

    # 2. Try Register if Login failed
    try:
        requests.post(register_url, json=TEST_USER, timeout=5)
    except Exception as e:
        print_info(f"Registration skipped/failed: {e}")

    # 3. Retry Login
    try:
        response = requests.post(login_url, data=login_data, timeout=30)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print_success("Login successful after registration")
            return {"Authorization": f"Bearer {token}"}
        else:
            print_error(f"Authentication failed: {response.text}")
            return {}
    except Exception as e:
        print_error(f"Authentication error: {e}")
        return {}

def test_real_ico_search(headers, ico, country="SK"):
    """Test search with real IČO"""
    print_test(f"Testing Real IČO: {ico} ({country})")
    
    # Test the enhanced search endpoint
    url = f"{BASE_URL}/api/v2/search"
    payload = {
        "query": ico,
        "countries": [country],
        "include_related": True,
        "risk_threshold": 0,
        "limit": 10,
        "format": "detailed"
    }
    
    try:
        print_info(f"Sending request to: {url}")
        print_info(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Search successful for IČO {ico}")
            
            # Analyze the response structure
            search_data = data.get('data', {})
            companies = search_data.get('companies', [])
            
            print_info(f"Found {len(companies)} companies")
            
            if companies:
                # Show detailed structure of first company
                first_company = companies[0]
                print_data("First Company Structure", first_company)
                
                # Extract key fields
                print_data("Key Fields Analysis", {
                    "identifier": first_company.get('identifier'),
                    "name": first_company.get('name'),
                    "country": first_company.get('country'),
                    "address": first_company.get('address'),
                    "risk_score": first_company.get('risk_score'),
                    "legal_form": first_company.get('legal_form'),
                    "executives": first_company.get('executives'),
                    "shareholders": first_company.get('shareholders'),
                    "founded": first_company.get('founded'),
                    "status": first_company.get('status'),
                    "dic": first_company.get('dic'),
                    "ic_dph": first_company.get('ic_dph'),
                    "virtual_seat": first_company.get('virtual_seat'),
                    "source": first_company.get('source'),
                    "data_quality": first_company.get('data_quality'),
                    "related_companies": first_company.get('related_companies')
                })
                
                # Check for network data
                if 'graph_data' in search_data:
                    graph_data = search_data['graph_data']
                    print_data("Graph Data Structure", {
                        "nodes_count": len(graph_data.get('nodes', [])),
                        "edges_count": len(graph_data.get('edges', [])),
                        "node_types": [node.get('type') for node in graph_data.get('nodes', [])[:5]],
                        "edge_types": [edge.get('type') for edge in graph_data.get('edges', [])[:5]]
                    })
                
                return True
            else:
                print_info("No companies found in response")
                return False
        else:
            print_error(f"Search failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Search error: {e}")
        return False

def test_company_details(headers, ico, country="SK"):
    """Test company details endpoint"""
    print_test(f"Testing Company Details: {ico} ({country})")
    
    url = f"{BASE_URL}/api/v2/company/{country}/{ico}"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Company details retrieved for {ico}")
            
            company_data = data.get('data', {})
            print_data("Company Details Structure", company_data)
            
            return True
        else:
            print_error(f"Company details failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Company details error: {e}")
        return False

def test_background_data_extraction(headers):
    """Test what data we get from background extraction"""
    print_header("BACKGROUND DATA EXTRACTION ANALYSIS")
    
    # Test with known real IČO from Slovakia
    real_sk_icos = [
        "35855304",  # Agentúra Viky s.r.o. (from existing test data)
        "35906215",  # Agrofert Holding a.s. (from existing test data)
        "45406215",  # Slovenské elektrárne, a.s. (from existing test data)
    ]
    
    # Test with known real IČO from Czech Republic
    real_cz_icos = [
        "27074358",  # Agrofert Holding a.s. (CZ version)
    ]
    
    results = []
    
    print_info("Testing Slovak IČO values...")
    for ico in real_sk_icos:
        print_info(f"\n--- Testing IČO: {ico} (SK) ---")
        success = test_real_ico_search(headers, ico, "SK")
        details_success = test_company_details(headers, ico, "SK")
        results.append({
            "ico": ico,
            "country": "SK",
            "search_success": success,
            "details_success": details_success
        })
    
    print_info("Testing Czech IČO values...")
    for ico in real_cz_icos:
        print_info(f"\n--- Testing IČO: {ico} (CZ) ---")
        success = test_real_ico_search(headers, ico, "CZ")
        details_success = test_company_details(headers, ico, "CZ")
        results.append({
            "ico": ico,
            "country": "CZ",
            "search_success": success,
            "details_success": details_success
        })
    
    # Summary
    print_header("TEST RESULTS SUMMARY")
    for result in results:
        status = "✅ SUCCESS" if result['search_success'] and result['details_success'] else "❌ FAILED"
        print(f"{status} - IČO {result['ico']} ({result['country']})")
    
    return results

def analyze_data_quality(results):
    """Analyze the quality and completeness of extracted data"""
    print_header("DATA QUALITY ANALYSIS")
    
    print_info("Expected data fields from background extraction:")
    expected_fields = [
        "identifier", "name", "country", "address", "postal_code", "city", 
        "region", "district", "legal_form", "executives", "shareholders", 
        "founded", "status", "dic", "ic_dph", "risk_score", "financial_data", 
        "virtual_seat", "source", "data_quality", "related_companies"
    ]
    
    for field in expected_fields:
        print(f"  • {field}")
    
    print_info("\nData completeness depends on:")
    print_info("  • Register availability (ORSR, ARES, KRS, NAV)")
    print_info("  • Live scraping success rate")
    print_info("  • Cache freshness")
    print_info("  • Cross-border data integration")
    print_info("  • Risk scoring algorithms")

if __name__ == "__main__":
    print_header("ILUMINATI SYSTEM - Real IČO Testing")
    print_info(f"Testing against: {BASE_URL}")
    print_info(f"Test started at: {datetime.now().isoformat()}")
    
    # Authenticate first
    headers = get_auth_headers()
    
    if headers:
        # Run tests
        results = test_background_data_extraction(headers)
        analyze_data_quality(results)
        
        print_header("TESTING COMPLETE")
        print_info("Review the output above to see what real data we get from background extraction")
        print_info("This helps understand the actual data quality and completeness")
    else:
        print_error("Skipping tests due to authentication failure")