# 🔐 Autentifikácia - Implementácia

## ✅ Backend Autentifikácia (DOKONČENÉ)

### Implementované funkcie

#### 1. User Model (`backend/services/auth.py`)
- ✅ User model s SQLAlchemy
- ✅ Email, password (hashed), full_name
- ✅ Subscription tiers (Free, Pro, Enterprise)
- ✅ User status (active, verified)
- ✅ Created_at, last_login tracking
- ✅ Stripe customer ID mapping (for subscription webhooks)

#### 2. Password Security
- ✅ Bcrypt password hashing
- ✅ Password verification
- ✅ Secure password storage

#### 3. JWT Authentication
- ✅ JWT token generation
- ✅ Token decoding and validation
- ✅ 30-day token expiration
- ✅ Token-based user authentication

#### 4. API Endpoints
- ✅ `POST /api/auth/register` - Registrácia nového používateľa
- ✅ `POST /api/auth/login` - Login s JWT token
- ✅ `GET /api/auth/me` - Získanie aktuálneho používateľa
- ✅ `GET /api/auth/tier/limits` - Limity pre tier používateľa

#### 5. Subscription Tiers
- ✅ **Free Tier:**
  - 10 searches/day
  - 100 searches/month
  - 5 exports
  - No API access
  - No advanced features

- ✅ **Pro Tier:**
  - 100 searches/day
  - 2000 searches/month
  - 100 exports
  - No API access
  - Advanced features

- ✅ **Enterprise Tier:**
  - Unlimited searches
  - Unlimited exports
  - API access
  - Advanced features

## 📋 API Dokumentácia

### Registrácia

**Endpoint:** `POST /api/auth/register`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "tier": "free",
  "is_active": true,
  "is_verified": false
}
```

### Login

**Endpoint:** `POST /api/auth/login`

**Request (form-data):**
```
username: user@example.com
password: securepassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "tier": "free",
    "limits": {
      "searches_per_day": 10,
      "searches_per_month": 100,
      "export_limit": 5,
      "api_access": false,
      "advanced_features": false
    }
  }
}
```

### Get Current User

**Endpoint:** `GET /api/auth/me`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "tier": "free",
  "is_active": true,
  "is_verified": false
}
```

## 🔒 Bezpečnosť

- ✅ Passwords hashed s bcrypt
- ✅ JWT tokens s expiration
- ✅ OAuth2 password flow
- ✅ Secure token storage
- ✅ User verification support

## ⚠️ Čo ešte treba

### Frontend
- [ ] Login page komponenta
- [ ] Register page komponenta
- [ ] Auth context/hook
- [ ] Token storage (localStorage)
- [ ] Protected routes
- [ ] User dashboard

### Backend
- [ ] Email verification
- [ ] Password reset
- [ ] User profile update
- [ ] Tier upgrade endpoint
- [ ] Rate limiting podľa tieru

## 🚀 Ďalšie kroky

1. Frontend autentifikácia (login/register pages)
2. Stripe integrácia pre tier upgrades
3. User dashboard
4. Protected routes

---

*Posledná aktualizácia: December 2024*

