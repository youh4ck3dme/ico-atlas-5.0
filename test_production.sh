#!/bin/bash

# 🧪 Production Testing Script - ILUMINATI SYSTEM
# Testuje všetky V4 krajiny s reálnym IČO

BASE_URL="${BASE_URL:-http://localhost:8000}"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "═══════════════════════════════════════════════════════════"
echo "🧪 ILUMINATI SYSTEM - Production Testing"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Test 1: Health Check
echo "📋 Test 1: Health Check"
echo "───────────────────────────────────────────────────────────"
response=$(curl -s -w "\n%{http_code}" "${BASE_URL}/health")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" == "200" ]; then
    echo -e "${GREEN}✅ Health check: OK${NC}"
    echo "   Response: $body"
else
    echo -e "${RED}❌ Health check: FAILED (HTTP $http_code)${NC}"
    exit 1
fi
echo ""

# Test 2: Slovensko (SK)
echo "📋 Test 2: Slovensko (SK)"
echo "───────────────────────────────────────────────────────────"
echo "Testing IČO: 52374220 (Tavira, s.r.o.)"
start_time=$(date +%s%N)
response=$(curl -s -w "\n%{http_code}" "${BASE_URL}/api/search?q=52374220")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')
end_time=$(date +%s%N)
duration=$(( (end_time - start_time) / 1000000 ))

if [ "$http_code" == "200" ]; then
    nodes=$(echo "$body" | grep -o '"nodes":\[' | wc -l)
    if [ "$nodes" -gt 0 ] || echo "$body" | grep -q "Tavira\|tavira"; then
        echo -e "${GREEN}✅ SK search: OK${NC} (${duration}ms)"
        echo "$body" | python3 -m json.tool 2>/dev/null | head -20 || echo "$body" | head -5
    else
        echo -e "${YELLOW}⚠️ SK search: Response OK but no data found${NC} (${duration}ms)"
    fi
else
    echo -e "${RED}❌ SK search: FAILED (HTTP $http_code)${NC}"
    echo "   Response: $body"
fi
echo ""

# Test 3: Česká republika (CZ)
echo "📋 Test 3: Česká republika (CZ)"
echo "───────────────────────────────────────────────────────────"
echo "Testing IČO: 27074358 (Agrofert, a.s.)"
start_time=$(date +%s%N)
response=$(curl -s -w "\n%{http_code}" "${BASE_URL}/api/search?q=27074358")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')
end_time=$(date +%s%N)
duration=$(( (end_time - start_time) / 1000000 ))

if [ "$http_code" == "200" ]; then
    nodes=$(echo "$body" | grep -o '"nodes":\[' | wc -l)
    if [ "$nodes" -gt 0 ] || echo "$body" | grep -q "Agrofert\|agrofert"; then
        echo -e "${GREEN}✅ CZ search: OK${NC} (${duration}ms)"
        echo "$body" | python3 -m json.tool 2>/dev/null | head -20 || echo "$body" | head -5
    else
        echo -e "${YELLOW}⚠️ CZ search: Response OK but no data found${NC} (${duration}ms)"
    fi
else
    echo -e "${RED}❌ CZ search: FAILED (HTTP $http_code)${NC}"
    echo "   Response: $body"
fi
echo ""

# Test 4: Poľsko (PL)
echo "📋 Test 4: Poľsko (PL)"
echo "───────────────────────────────────────────────────────────"
echo "Testing KRS: 0000123456 (test)"
start_time=$(date +%s%N)
response=$(curl -s -w "\n%{http_code}" "${BASE_URL}/api/search?q=0000123456")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')
end_time=$(date +%s%N)
duration=$(( (end_time - start_time) / 1000000 ))

if [ "$http_code" == "200" ]; then
    echo -e "${GREEN}✅ PL search: OK${NC} (${duration}ms)"
    echo "$body" | python3 -m json.tool 2>/dev/null | head -20 || echo "$body" | head -5
else
    echo -e "${YELLOW}⚠️ PL search: HTTP $http_code${NC} (${duration}ms)"
    echo "   Response: $body" | head -3
fi
echo ""

# Test 5: Maďarsko (HU)
echo "📋 Test 5: Maďarsko (HU)"
echo "───────────────────────────────────────────────────────────"
echo "Testing Adószám: 12345678 (test)"
start_time=$(date +%s%N)
response=$(curl -s -w "\n%{http_code}" "${BASE_URL}/api/search?q=12345678")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')
end_time=$(date +%s%N)
duration=$(( (end_time - start_time) / 1000000 ))

if [ "$http_code" == "200" ]; then
    echo -e "${GREEN}✅ HU search: OK${NC} (${duration}ms)"
    echo "$body" | python3 -m json.tool 2>/dev/null | head -20 || echo "$body" | head -5
else
    echo -e "${YELLOW}⚠️ HU search: HTTP $http_code${NC} (${duration}ms)"
    echo "   Response: $body" | head -3
fi
echo ""

# Test 6: Error Handling
echo "📋 Test 6: Error Handling"
echo "───────────────────────────────────────────────────────────"
echo "Testing invalid IČO: 99999999"
start_time=$(date +%s%N)
response=$(curl -s -w "\n%{http_code}" "${BASE_URL}/api/search?q=99999999")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')
end_time=$(date +%s%N)
duration=$(( (end_time - start_time) / 1000000 ))

if [ "$http_code" == "200" ] || [ "$http_code" == "404" ]; then
    echo -e "${GREEN}✅ Error handling: OK${NC} (HTTP $http_code, ${duration}ms)"
    echo "$body" | python3 -m json.tool 2>/dev/null | head -10 || echo "$body" | head -3
else
    echo -e "${YELLOW}⚠️ Error handling: HTTP $http_code${NC} (${duration}ms)"
fi
echo ""

# Test 7: Performance (Cache Test)
echo "📋 Test 7: Performance (Cache Test)"
echo "───────────────────────────────────────────────────────────"
echo "Testing cache with repeated request: 52374220"
echo "First request:"
start_time=$(date +%s%N)
response1=$(curl -s -w "\n%{http_code}" "${BASE_URL}/api/search?q=52374220")
http_code1=$(echo "$response1" | tail -n1)
end_time=$(date +%s%N)
duration1=$(( (end_time - start_time) / 1000000 ))

sleep 1

echo "Second request (should be cached):"
start_time=$(date +%s%N)
response2=$(curl -s -w "\n%{http_code}" "${BASE_URL}/api/search?q=52374220")
http_code2=$(echo "$response2" | tail -n1)
end_time=$(date +%s%N)
duration2=$(( (end_time - start_time) / 1000000 ))

if [ "$http_code1" == "200" ] && [ "$http_code2" == "200" ]; then
    speedup=$(( duration1 - duration2 ))
    if [ "$duration2" -lt "$duration1" ]; then
        echo -e "${GREEN}✅ Cache test: OK${NC}"
        echo "   First request: ${duration1}ms"
        echo "   Second request: ${duration2}ms (${speedup}ms faster)"
    else
        echo -e "${YELLOW}⚠️ Cache test: Both requests similar speed${NC}"
        echo "   First request: ${duration1}ms"
        echo "   Second request: ${duration2}ms"
    fi
else
    echo -e "${RED}❌ Cache test: FAILED${NC}"
fi
echo ""

# Test 8: API Metrics
echo "📋 Test 8: API Metrics"
echo "───────────────────────────────────────────────────────────"
response=$(curl -s "${BASE_URL}/api/metrics")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Metrics endpoint: OK${NC}"
    echo "$response" | python3 -m json.tool 2>/dev/null | head -30 || echo "$response" | head -10
else
    echo -e "${YELLOW}⚠️ Metrics endpoint: Not available${NC}"
fi
echo ""

# Summary
echo "═══════════════════════════════════════════════════════════"
echo "📊 Test Summary"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "✅ Tests completed!"
echo ""
echo "💡 Next steps:"
echo "   1. Review test results above"
echo "   2. Check backend logs for any errors"
echo "   3. Test via frontend UI at http://localhost:5173"
echo "   4. Review docs/PRODUCTION_TESTING_PLAN.md for more scenarios"
echo ""

