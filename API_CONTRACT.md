# 📋 API Contract - IČO ATLAS 5.0

## 🔒 Stable Contract (Nemeniteľný)

Tento dokument definuje **stabilný API kontrakt**, ktorý sa **nikdy nemení**. Všetky provider integrácie musia dodržiavať tento formát.

---

## Endpoint

```
GET /api/company/search?ico=XXXXXXXX
```

**Parameters:**
- `ico` (required, string): 8-digit IČO number

---

## Response Format

### Success Response (200 OK)

```json
{
  "data": {
    "ico": "52374220",
    "name": "Company Name s.r.o.",
    "dic": "2023456789",
    "ic_dph": "SK2023456789",
    "legal_form": "s.r.o.",
    "address": "Hlavná 123",
    "city": "Bratislava",
    "zip": "81101",
    "district": "Bratislava I",
    "region": "Bratislavský kraj",
    "country": "SK",
    "source": "orsr|zrsr|ruz|stub"
  },
  "meta": {
    "cached": true,
    "latency_ms": 12
  }
}
```

**Field Descriptions:**
- `ico`: 8-digit IČO (required, string)
- `name`: Company name (nullable, string)
- `dic`: Tax ID (nullable, string)
- `ic_dph`: VAT ID (nullable, string)
- `legal_form`: Legal form (nullable, string)
- `address`: Street address (nullable, string)
- `city`: City name (nullable, string)
- `zip`: Postal code (nullable, string)
- `district`: District name (nullable, string)
- `region`: Region name (nullable, string)
- `country`: Country code, always "SK" (required, string)
- `source`: Data source identifier (required, string)
- `cached`: Whether response was from cache (required, boolean)
- `latency_ms`: Response latency in milliseconds (required, integer)

---

### Validation Error (422 Unprocessable Entity)

```json
{
  "message": "The given data was invalid.",
  "errors": {
    "ico": [
      "IČO musí mať presne 8 číslic."
    ]
  }
}
```

**Error Cases:**
- Missing `ico` parameter
- Invalid `ico` format (not 8 digits)
- Non-numeric characters in `ico`

---

### Rate Limit Error (429 Too Many Requests)

```json
{
  "message": "Too many requests. Please try again later.",
  "error": "rate_limit_exceeded"
}
```

**Rate Limit:** 30 requests per minute per IP address

---

### Server Error (500 Internal Server Error)

```json
{
  "message": "Internal server error.",
  "error": "ExceptionClassName"
}
```

**Note:** In development mode, additional debug information may be included.

---

## Request Headers

**Not Required:** API automatically forces `Accept: application/json` for all `/api/*` routes via `ForceJsonForApi` middleware.

**Optional:**
- `Accept: application/json` (automatically set)
- `Content-Type: application/json` (for POST requests)

---

## Response Headers

**Always:**
- `Content-Type: application/json`
- `Cache-Control: no-cache, private` (unless cached)

---

## Validation Rules

### IČO Format
- **Required:** Yes
- **Type:** String
- **Pattern:** `^\d{8}$` (exactly 8 digits)
- **Examples:**
  - ✅ Valid: `52374220`, `12345678`
  - ❌ Invalid: `123`, `123456789`, `ABC12345`, `1234-5678`

---

## Caching

- **TTL:** 1 hour (3600 seconds)
- **Cache Key:** `company:ico:{ico}`
- **Cache Hit Detection:** `meta.cached` field indicates if response was from cache

---

## Provider Integration

All providers (ORSR, ZRSR, RÚZ) must return data in this exact format. The `source` field indicates which provider returned the data.

**Provider Priority (fallback chain):**
1. ORSR (primary)
2. ZRSR (fallback)
3. RÚZ (fallback)
4. Stub (development/testing)

---

## Examples

### cURL Examples

**Valid Request:**
```bash
curl -sS "http://127.0.0.1:8000/api/company/search?ico=52374220" | jq
```

**Invalid Request:**
```bash
curl -sS "http://127.0.0.1:8000/api/company/search?ico=123" | jq
```

**Without Accept Header (still returns JSON):**
```bash
curl -sS "http://127.0.0.1:8000/api/company/search?ico=52374220" | jq
```

---

## Testing

All contract tests are in `tests/Feature/Api/CompanyApiTest.php`:

- ✅ Invalid IČO validation
- ✅ Missing IČO validation
- ✅ Valid IČO contract structure
- ✅ JSON format validation

---

## Version

**Contract Version:** 1.0.0  
**Last Updated:** December 2024  
**Status:** Stable (Phase 3 MVP)

---

**⚠️ IMPORTANT:** This contract is **immutable**. Any changes to the response structure must be done through versioning (e.g., `/api/v2/company/search`).

