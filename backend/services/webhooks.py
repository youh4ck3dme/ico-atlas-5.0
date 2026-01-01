"""
Webhooks Delivery Service
Pre Enterprise tier - real-time event notifications
"""

import json
import hashlib
import hmac
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import Session, relationship
from services.database import Base, get_db_session
from services.auth import User


class Webhook(Base):
    """Webhook model"""
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    url = Column(String(500), nullable=False)  # Webhook URL endpoint
    secret = Column(String(255), nullable=False)  # Secret key for HMAC signature
    events = Column(Text, nullable=False)  # JSON array: ["company_updated", "new_risk_score"]
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_delivered_at = Column(DateTime, nullable=True)
    success_count = Column(Integer, default=0, nullable=False)
    failure_count = Column(Integer, default=0, nullable=False)

    # Relationship
    user = relationship("User", back_populates="webhooks")


class WebhookDelivery(Base):
    """Webhook delivery log"""
    __tablename__ = "webhook_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(Integer, ForeignKey("webhooks.id"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False)
    response_status = Column(Integer, nullable=True)
    response_body = Column(Text, nullable=True)
    delivery_time = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    success = Column(Boolean, default=False, nullable=False)
    error_message = Column(Text, nullable=True)

    # Relationship
    webhook = relationship("Webhook", back_populates="deliveries")


# Add relationships
Webhook.deliveries = relationship("WebhookDelivery", back_populates="webhook", cascade="all, delete-orphan")


def generate_webhook_secret() -> str:
    """Generovať secret pre webhook HMAC signature"""
    return os.urandom(32).hex()


def create_webhook(
    db: Session,
    user_id: int,
    url: str,
    events: List[str],
    secret: Optional[str] = None
) -> Dict:
    """
    Vytvoriť nový webhook.
    
    Args:
        db: Database session
        user_id: ID používateľa
        url: Webhook URL endpoint
        events: Zoznam event types
        secret: Optional secret (ak nie je poskytnutý, vygeneruje sa)
        
    Returns:
        Dict s webhook informáciami
    """
    if not secret:
        secret = generate_webhook_secret()
    
    webhook = Webhook(
        user_id=user_id,
        url=url,
        secret=secret,
        events=json.dumps(events),
        is_active=True
    )
    
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    
    return {
        "id": webhook.id,
        "url": webhook.url,
        "events": events,
        "secret": secret,  # Vrátiť len raz!
        "created_at": webhook.created_at.isoformat(),
        "is_active": webhook.is_active
    }


def get_user_webhooks(db: Session, user_id: int) -> List[Webhook]:
    """Získať všetky webhooks pre používateľa"""
    return db.query(Webhook).filter(
        Webhook.user_id == user_id
    ).order_by(Webhook.created_at.desc()).all()


def get_webhook_by_id(db: Session, webhook_id: int, user_id: int) -> Optional[Webhook]:
    """Získať webhook podľa ID (s security check)"""
    return db.query(Webhook).filter(
        Webhook.id == webhook_id,
        Webhook.user_id == user_id
    ).first()


def delete_webhook(db: Session, webhook_id: int, user_id: int) -> bool:
    """Zmazať webhook"""
    webhook = get_webhook_by_id(db, webhook_id, user_id)
    if not webhook:
        return False
    
    db.delete(webhook)
    db.commit()
    return True


def generate_webhook_signature(payload: str, secret: str) -> str:
    """
    Generovať HMAC SHA256 signature pre webhook payload.
    
    Args:
        payload: JSON string payload
        secret: Webhook secret
        
    Returns:
        HMAC signature (hex)
    """
    return hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


async def deliver_webhook(webhook: Webhook, event_type: str, payload: Dict[str, Any]) -> bool:
    """
    Dodať webhook event.
    
    Args:
        webhook: Webhook object
        event_type: Type of event
        payload: Event payload data
        
    Returns:
        True ak úspešné, False inak
    """
    import requests
    
    # Skontrolovať, či webhook je aktívny
    if not webhook.is_active:
        return False
    
    # Skontrolovať, či event type je v zozname
    webhook_events = json.loads(webhook.events)
    if event_type not in webhook_events:
        return False
    
    # Pripraviť payload
    webhook_payload = {
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": payload
    }
    
    payload_json = json.dumps(webhook_payload, default=str)
    
    # Generovať signature
    signature = generate_webhook_signature(payload_json, webhook.secret)
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "X-ILUMINATI-Signature": f"sha256={signature}",
        "X-ILUMINATI-Event": event_type,
        "User-Agent": "ILUMINATI-System-Webhooks/1.0"
    }
    
    # Deliver webhook
    try:
        response = requests.post(
            webhook.url,
            data=payload_json,
            headers=headers,
            timeout=10
        )
        
        success = 200 <= response.status_code < 300
        
        # Log delivery
        with get_db_session() as db:
            if db:
                delivery = WebhookDelivery(
                    webhook_id=webhook.id,
                    event_type=event_type,
                    payload=webhook_payload,
                    response_status=response.status_code,
                    response_body=response.text[:1000],  # Limit response body
                    success=success,
                    error_message=None if success else f"HTTP {response.status_code}"
                )
                db.add(delivery)
                
                # Update webhook stats
                webhook.last_delivered_at = datetime.utcnow()
                if success:
                    webhook.success_count += 1
                else:
                    webhook.failure_count += 1
                
                db.commit()
        
        return success
        
    except Exception as e:
        # Log error
        with get_db_session() as db:
            if db:
                delivery = WebhookDelivery(
                    webhook_id=webhook.id,
                    event_type=event_type,
                    payload=webhook_payload,
                    success=False,
                    error_message=str(e)[:500]
                )
                db.add(delivery)
                
                webhook.failure_count += 1
                db.commit()
        
        return False


async def deliver_event_to_all_webhooks(event_type: str, payload: Dict[str, Any], user_id: Optional[int] = None):
    """
    Dodať event všetkým relevantným webhookom.
    
    Args:
        event_type: Type of event
        payload: Event payload
        user_id: Optional user ID filter (ak None, pošle všetkým)
    """
    with get_db_session() as db:
        if not db:
            return
        
        query = db.query(Webhook).filter(Webhook.is_active == True)
        if user_id:
            query = query.filter(Webhook.user_id == user_id)
        
        webhooks = query.all()
        
        for webhook in webhooks:
            await deliver_webhook(webhook, event_type, payload)


def get_webhook_deliveries(db: Session, webhook_id: int, user_id: int, limit: int = 50) -> List[WebhookDelivery]:
    """Získať delivery históriu pre webhook"""
    webhook = get_webhook_by_id(db, webhook_id, user_id)
    if not webhook:
        return []
    
    return db.query(WebhookDelivery).filter(
        WebhookDelivery.webhook_id == webhook_id
    ).order_by(WebhookDelivery.delivery_time.desc()).limit(limit).all()


def get_webhook_stats(db: Session, webhook_id: int, user_id: int) -> Optional[Dict]:
    """Získať štatistiky pre webhook"""
    webhook = get_webhook_by_id(db, webhook_id, user_id)
    if not webhook:
        return None
    
    return {
        "id": webhook.id,
        "url": webhook.url,
        "events": json.loads(webhook.events),
        "is_active": webhook.is_active,
        "created_at": webhook.created_at.isoformat(),
        "last_delivered_at": webhook.last_delivered_at.isoformat() if webhook.last_delivered_at else None,
        "success_count": webhook.success_count,
        "failure_count": webhook.failure_count,
        "total_deliveries": webhook.success_count + webhook.failure_count
    }

