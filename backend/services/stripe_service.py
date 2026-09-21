"""
Stripe integrácia pre monetizáciu ILUMINATI SYSTEM
Subscription management a payment processing

Customer ID Mapping Flow:
1. When user initiates checkout, we get/create Stripe customer and store customer.id in user.stripe_customer_id
2. Stripe sends webhooks with customer ID (not email) in subscription events
3. On subscription.deleted webhook, we look up user by stripe_customer_id and downgrade to FREE tier
4. This ensures proper mapping between Stripe customers and application users
"""

import os
from typing import Dict, Optional

import stripe

from services.auth import (
    UserTier,
    get_user_by_stripe_customer_id,
    update_user_stripe_customer_id,
    update_user_tier,
)
from services.database import get_db_session

# Stripe konfigurácia
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")  # V produkcii z env
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# Subscription prices (v centoch)
PRICES = {
    UserTier.PRO: os.getenv("STRIPE_PRO_PRICE_ID", "price_pro_monthly"),
    UserTier.ENTERPRISE: os.getenv(
        "STRIPE_ENTERPRISE_PRICE_ID", "price_enterprise_monthly"
    ),
}

# Default prices (ak nie sú nastavené)
DEFAULT_PRICES = {
    UserTier.PRO: 1999,  # $19.99/month
    UserTier.ENTERPRISE: 9999,  # $99.99/month
}


def create_checkout_session(user_id: int, user_email: str, tier: UserTier) -> Dict:
    """
    Vytvorí Stripe checkout session pre upgrade tieru.
    Creates or retrieves Stripe customer and stores customer ID in user record.

    Args:
        user_id: ID používateľa
        user_email: Email používateľa
        tier: Tier na upgrade (PRO alebo ENTERPRISE)

    Returns:
        Dict s checkout session URL
    """
    try:
        # Získať alebo vytvoriť Stripe customer
        customer_id = None
        with get_db_session() as db:
            if db:
                from services.auth import get_user_by_email

                user = get_user_by_email(db, user_email)

                if user and user.stripe_customer_id:
                    # Použiť existujúci customer ID
                    customer_id = user.stripe_customer_id
                else:
                    # Vytvoriť nový Stripe customer
                    customer = stripe.Customer.create(
                        email=user_email,
                        metadata={
                            "user_id": str(user_id),
                        },
                    )
                    customer_id = customer.id

                    # Uložiť customer ID do databázy
                    if user:
                        update_user_stripe_customer_id(db, user_id, customer_id)

        # Vytvoriť checkout session s customer ID
        session_params = {
            "payment_method_types": ["card"],
            "line_items": [
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": f"ILUMINATI SYSTEM - {tier.value.upper()}",
                            "description": f"Upgrade na {tier.value.upper()} tier",
                        },
                        "unit_amount": DEFAULT_PRICES.get(tier, 1999),
                        "recurring": {
                            "interval": "month",
                        },
                    },
                    "quantity": 1,
                }
            ],
            "mode": "subscription",
            "success_url": f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            "cancel_url": f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/payment/cancel",
            "metadata": {
                "user_id": str(user_id),
                "tier": tier.value,
            },
        }

        # Použiť customer ID ak existuje, inak customer_email
        if customer_id:
            session_params["customer"] = customer_id
        else:
            session_params["customer_email"] = user_email

        checkout_session = stripe.checkout.Session.create(**session_params)

        return {
            "session_id": checkout_session.id,
            "url": checkout_session.url,
            "status": "created",
            "customer_id": customer_id,
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}


def handle_webhook(payload: bytes, signature: str) -> Dict:
    """
    Spracuje Stripe webhook event.

    Important: Stripe subscription webhooks contain 'customer' (ID), not 'customer_email'.
    We must look up users by their stored stripe_customer_id to properly handle subscription events.

    Supported events:
    - checkout.session.completed: Upgrade user tier when payment succeeds
    - customer.subscription.deleted: Downgrade user to FREE when subscription is canceled

    Args:
        payload: Raw webhook payload
        signature: Stripe signature

    Returns:
        Dict s výsledkom
    """
    try:
        event = stripe.Webhook.construct_event(
            payload, signature, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return {"error": "Invalid payload", "status": "error"}
    except stripe.error.SignatureVerificationError:
        return {"error": "Invalid signature", "status": "error"}

    # Spracovať event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = int(session["metadata"]["user_id"])
        tier_str = session["metadata"]["tier"]
        tier = UserTier(tier_str)
        customer_id = session.get("customer")

        # Aktualizovať tier používateľa a uložiť customer ID ak existuje
        with get_db_session() as db:
            if db:
                update_user_tier(db, user_id, tier)
                # Uložiť Stripe customer ID ak ešte nie je uložený
                if customer_id:
                    update_user_stripe_customer_id(db, user_id, customer_id)

        return {
            "status": "success",
            "user_id": user_id,
            "tier": tier_str,
            "customer_id": customer_id,
        }

    elif event["type"] == "customer.subscription.deleted":
        # Subscription zrušená - downgrade na FREE
        # Use Stripe customer ID to look up user (not email, which isn't in subscription object)
        subscription = event["data"]["object"]
        customer_id = subscription.get("customer")

        if customer_id:
            with get_db_session() as db:
                if db:
                    user = get_user_by_stripe_customer_id(db, customer_id)
                    if user:
                        update_user_tier(db, user.id, UserTier.FREE)
                        return {
                            "status": "success",
                            "action": "downgrade_to_free",
                            "user_id": user.id,
                            "customer_id": customer_id,
                        }
                    else:
                        return {
                            "status": "warning",
                            "action": "downgrade_to_free",
                            "message": f"User not found for customer_id: {customer_id}",
                        }

        return {
            "status": "error",
            "action": "downgrade_to_free",
            "message": "No customer_id in subscription",
        }

    return {"status": "ignored", "event_type": event["type"]}


def get_subscription_status(user_email: str) -> Optional[Dict]:
    """
    Získa status subscriptionu pre používateľa.

    Args:
        user_email: Email používateľa

    Returns:
        Dict so subscription status alebo None
    """
    try:
        customers = stripe.Customer.list(email=user_email, limit=1)
        if not customers.data:
            return None

        customer = customers.data[0]
        subscriptions = stripe.Subscription.list(customer=customer.id, limit=1)

        if not subscriptions.data:
            return None

        subscription = subscriptions.data[0]
        return {
            "status": subscription.status,
            "current_period_end": subscription.current_period_end,
            "cancel_at_period_end": subscription.cancel_at_period_end,
        }
    except Exception as e:
        return {"error": str(e)}


def cancel_subscription(user_email: str) -> Dict:
    """
    Zruší subscription používateľa.

    Args:
        user_email: Email používateľa

    Returns:
        Dict s výsledkom
    """
    try:
        customers = stripe.Customer.list(email=user_email, limit=1)
        if not customers.data:
            return {"error": "Customer not found", "status": "error"}

        customer = customers.data[0]
        subscriptions = stripe.Subscription.list(customer=customer.id, limit=1)

        if not subscriptions.data:
            return {"error": "No active subscription", "status": "error"}

        subscription = subscriptions.data[0]
        canceled = stripe.Subscription.modify(
            subscription.id, cancel_at_period_end=True
        )

        return {
            "status": "success",
            "canceled": True,
            "cancel_at_period_end": canceled.cancel_at_period_end,
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}
