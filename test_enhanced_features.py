#!/usr/bin/env python3
"""
Test script for Enhanced Data Extraction & Visualization Tool
"""

import asyncio
import json
import requests
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

def get_auth_headers():
    """Register/Login test user and return auth headers"""
    print_info("Authenticating test user...")
    
    # 1. Try to register
    register_url = f"{BASE_URL}/api/auth/register"
    try:
        requests.post(register_url, json=TEST_USER, timeout=5)
    except Exception:
        pass # User likely already exists

    # 2. Login to get token
    login_url = f"{BASE_URL}/api/auth/login"
    login_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    
    try:
        response = requests.post(login_url, data=login_data, timeout=5)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print_success("Authentication successful")
            return {"Authorization": f"Bearer {token}"}
        else:
            print_error(f"Authentication failed: {response.text}")
            return {}
    except Exception as e:
        print_error(f"Authentication error: {e}")
        return {}

async def test_enhanced_search(headers):
    """Test enhanced search functionality"""
    print_test("Testing Enhanced Search API")
    
    url = f"{BASE_URL}/api/v2/search"
    payload = {
        "query": "Agrofert",
        "countries": ["SK", "CZ"],
        "include_related": True,
        "risk_threshold": 0,
        "limit": 10,
        "format": "detailed"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Enhanced search successful")
            print_info(f"Found {len(data.get('data', {}).get('companies', []))} companies")
            print_info(f"Execution time: {data.get('metadata', {}).get('timestamp', 'N/A')}")
            return True
        else:
            print_error(f"Enhanced search failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Enhanced search error: {e}")
        return False

async def test_company_details(headers):
    """Test company details endpoint"""
    print_test("Testing Company Details API")
    
    # Using specific IČO that exists in ORSR
    url = f"{BASE_URL}/api/v2/company/SK/35855304"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Company details retrieved")
            print_info(f"Company: {data.get('data', {}).get('name', 'N/A')}")
            print_info(f"Risk Score: {data.get('data', {}).get('risk_score', 'N/A')}")
            return True
        else:
            print_error(f"Company details failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Company details error: {e}")
        return False

async def test_pdf_export(headers):
    """Test PDF export functionality"""
    print_test("Testing PDF Export")
    
    url = f"{BASE_URL}/api/v2/export"
    payload = {
        "format": "pdf",
        "data": {
            "companies": [
                {
                    "identifier": "35855304",
                    "name": "Agentúra Viky s.r.o.",
                    "country": "SK",
                    "risk_score": 8.5,
                    "address": "Strmý vŕšok 59, Bratislava",
                    "legal_form": "s.r.o."
                }
            ]
        },
        "options": {
            "include_graph": False,
            "branding": "premium",
            "executive_summary": True,
            "risk_analysis": True
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            # Check if response is PDF
            if response.headers.get('content-type', '').startswith('application/pdf'):
                print_success(f"PDF export successful")
                print_info(f"PDF size: {len(response.content)} bytes")
                
                # Save test PDF
                filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print_info(f"PDF saved as: {filename}")
                return True
            else:
                print_error("Response is not a PDF file")
                return False
        else:
            print_error(f"PDF export failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"PDF export error: {e}")
        return False

async def test_excel_export(headers):
    """Test Excel export functionality"""
    print_test("Testing Excel Export")
    
    url = f"{BASE_URL}/api/v2/export"
    payload = {
        "format": "excel",
        "data": {
            "nodes": [
                {"id": "1", "label": "Test Company", "type": "company", "country": "SK", "risk_score": 5.0},
                {"id": "2", "label": "Test Person", "type": "person", "country": "SK", "risk_score": 3.0}
            ],
            "edges": [
                {"source": "1", "target": "2", "type": "MANAGED_BY"}
            ]
        },
        "options": {
            "include_graph": True
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            # Check if response is Excel
            content_type = response.headers.get('content-type', '')
            if 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
                print_success(f"Excel export successful")
                print_info(f"Excel size: {len(response.content)} bytes")
                
                # Save test Excel file
                filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print_info(f"Excel saved as: {filename}")
                return True
            else:
                print_error("Response is not an Excel file")
                return False
        else:
            print_error(f"Excel export failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Excel export error: {e}")
        return False

async def test_related_companies(headers):
    """Test related companies endpoint"""
    print_test("Testing Related Companies")
    
    url = f"{BASE_URL}/api/v2/related/SK/35855304"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Related companies retrieved")
            print_info(f"Found {len(data.get('data', []))} related companies")
            return True
        else:
            print_error(f"Related companies failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Related companies error: {e}")
        return False

async def test_health_check(headers):
    """Test health check endpoint"""
    print_test("Testing Health Check")
    
    url = f"{BASE_URL}/api/health"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check successful")
            print_info(f"Status: {data.get('status', 'N/A')}")
            print_info(f"Cache available: {data.get('cache', {}).get('available', False)}")
            print_info(f"Database available: {data.get('features', {}).get('database', False)}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

async def main():
    """Run all tests"""
    print_header("ILUMINATI SYSTEM - Enhanced Features Test Suite")
    print_info(f"Testing against: {BASE_URL}")
    print_info(f"Test started at: {datetime.now().isoformat()}")
    
    # Authenticate first
    headers = get_auth_headers()
    if not headers:
        print_error("Skipping tests due to authentication failure")
        return

    tests = [
        ("Health Check", lambda: test_health_check(headers)),
        ("Enhanced Search", lambda: test_enhanced_search(headers)),
        ("Company Details", lambda: test_company_details(headers)),
        ("Related Companies", lambda: test_related_companies(headers)),
        ("PDF Export", lambda: test_pdf_export(headers)),
        ("Excel Export", lambda: test_excel_export(headers)),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Results Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("🎉 All tests passed! Enhanced features are working correctly.")
    else:
        print_error(f"⚠️  {total - passed} test(s) failed. Please check the implementation.")
    
    print(f"\nTest completed at: {datetime.now().isoformat()}")

if __name__ == "__main__":
    asyncio.run(main())