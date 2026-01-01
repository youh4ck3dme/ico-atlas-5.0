# 💳 Stripe Integrácia - Dokumentácia

## ✅ Implementované funkcie

### 1. Stripe Service (`backend/services/stripe_service.py`)

#### Funkcie:
- ✅ `create_checkout_session()` - Vytvorí Stripe checkout session
- ✅ `handle_webhook()` - Spracováva Stripe webhook events
- ✅ `get_subscription_status()` - Získa subscription status
- ✅ `cancel_subscription()` - Zruší subscription

### 2. API Endpoints

#### `POST /api/payment/checkout`
Vytvorí Stripe checkout session pre upgrade tieru.

**Request:**
```
tier: "pro" alebo "enterprise"
Authorization: Bearer <token>
```

**Response:**
```json
{
  "session_id": "cs_test_...",
  "url": "https://checkout.stripe.com/...",
  "status": "created"
}
```

#### `POST /api/payment/webhook`
Stripe webhook endpoint pre subscription events.

**Headers:**
```
stripe-signature: <signature>
```

**Events handled:**
- `checkout.session.completed` - Upgrade tier po úspešnej platbe
- `customer.subscription.deleted` - Downgrade na FREE tier

#### `GET /api/payment/subscription`
Získa subscription status používateľa.

**Response:**
```json
{
  "status": "active",
  "current_period_end": 1234567890,
  "cancel_at_period_end": false
}
```

#### `POST /api/payment/cancel`
Zruší subscription používateľa.

**Response:**
```json
{
  "status": "success",
  "canceled": true,
  "cancel_at_period_end": true
}
```

### 3. Subscription Tiers

#### PRO Tier
- **Cena:** €19.99/month (default)
- **Features:**
  - 100 searches/day
  - 2000 searches/month
  - 100 exports
  - Advanced features

#### ENTERPRISE Tier
- **Cena:** €99.99/month (default)
- **Features:**
  - Unlimited searches
  - Unlimited exports
  - API access
  - Advanced features

## 🔧 Konfigurácia

### Environment Variables

```env
# Stripe API Keys
STRIPE_SECRET_KEY=sk_test_...  # alebo sk_live_... pre produkciu
STRIPE_WEBHOOK_SECRET=whsec_...

# Stripe Price IDs (voliteľné)
STRIPE_PRO_PRICE_ID=price_...
STRIPE_ENTERPRISE_PRICE_ID=price_...

# Frontend URL (pre redirect)
FRONTEND_URL=http://localhost:5173
```

### Stripe Dashboard Setup

1. **Vytvoriť Products:**
   - PRO subscription product
   - ENTERPRISE subscription product

2. **Nastaviť Webhook:**
   - URL: `https://your-domain.com/api/payment/webhook`
   - Events: `checkout.session.completed`, `customer.subscription.deleted`

3. **Získať Webhook Secret:**
   - Z Stripe Dashboard → Webhooks → Signing secret

## 🔄 Workflow

### Customer ID Mapping

**Important:** The application maintains a mapping between Stripe customers and users via `User.stripe_customer_id`.

When a user initiates checkout:
1. Backend gets or creates a Stripe customer using their email
2. The Stripe customer ID is stored in `User.stripe_customer_id` field
3. This mapping is crucial for webhook processing

When Stripe sends subscription webhooks:
1. Stripe includes the `customer` ID (not email) in the webhook payload
2. Backend looks up the user by `stripe_customer_id`
3. User's tier is updated accordingly

**Note:** Stripe subscription objects contain `customer` (ID), NOT `customer_email`. The customer ID mapping is essential for proper webhook handling.

### Upgrade Process

1. User klikne na "Upgrade to PRO"
2. Frontend volá `POST /api/payment/checkout?tier=pro`
3. Backend vytvorí Stripe checkout session:
   - Gets or creates Stripe customer by email
   - Stores customer ID in user record
4. User je presmerovaný na Stripe checkout
5. Po úspešnej platbe Stripe pošle webhook
6. Backend aktualizuje tier používateľa na PRO
7. User je presmerovaný na success page

### Subscription Management

- User môže zrušiť subscription cez `POST /api/payment/cancel`
- Subscription sa zruší na konci platobného obdobia
- When subscription is deleted, Stripe sends webhook with customer ID
- Backend looks up user by customer ID and downgrades tier to FREE

## 📝 Poznámky

- V testovacom prostredí používa Stripe test keys
- V produkcii treba nastaviť live keys
- Webhook musí byť overený Stripe signature
- Ceny sú v centoch (EUR)

---

*Posledná aktualizácia: December 2024*

