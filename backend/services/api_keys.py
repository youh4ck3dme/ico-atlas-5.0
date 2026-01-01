"""
API Keys Management Service
Pre Enterprise tier používateľov - generovanie a správa API kľúčov
"""

import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import Session, relationship
from services.database import Base, get_db_session


class ApiKey(Base):
    """API Key model"""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)  # Description/name of the key
    key_hash = Column(String(255), unique=True, nullable=False, index=True)  # Hashed API key
    prefix = Column(String(20), nullable=False)  # First 8 chars for display (il_xxxx)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)  # Optional expiration
    last_used_at = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    permissions = Column(Text, nullable=True)  # JSON string: ["read", "write"]
    ip_whitelist = Column(Text, nullable=True)  # JSON string: ["1.2.3.4", "5.6.7.8"]

    # Relationship
    user = relationship("User", back_populates="api_keys")


def generate_api_key(prefix: str = "il") -> tuple[str, str]:
    """
    Generovať nový API key.
    
    Args:
        prefix: Prefix pre key (default: "il")
        
    Returns:
        Tuple (full_key, key_hash)
    """
    # Generovať 32-byte random string
    random_bytes = secrets.token_bytes(32)
    key_suffix = secrets.token_urlsafe(32)
    full_key = f"{prefix}_{key_suffix}"
    
    # Hash key pre bezpečné uloženie
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()
    
    return full_key, key_hash


def create_api_key(
    db: Session,
    user_id: int,
    name: str,
    expires_days: Optional[int] = None,
    permissions: Optional[List[str]] = None,
    ip_whitelist: Optional[List[str]] = None
) -> Dict:
    """
    Vytvoriť nový API key.
    
    Args:
        db: Database session
        user_id: ID používateľa
        name: Názov/opis key
        expires_days: Počet dní do expirácie (None = bez expirácie)
        permissions: Zoznam permissions (["read", "write"])
        ip_whitelist: Zoznam povolených IP adries
        
    Returns:
        Dict s key informáciami (key sa vráti len raz!)
    """
    import json
    
    # Generovať key
    full_key, key_hash = generate_api_key()
    prefix = full_key[:8]  # Prvých 8 znakov pre display
    
    # Expiration
    expires_at = None
    if expires_days:
        expires_at = datetime.utcnow() + timedelta(days=expires_days)
    
    # Permissions default
    if permissions is None:
        permissions = ["read"]
    
    # Vytvoriť API key record
    api_key = ApiKey(
        user_id=user_id,
        name=name,
        key_hash=key_hash,
        prefix=prefix,
        expires_at=expires_at,
        permissions=json.dumps(permissions),
        ip_whitelist=json.dumps(ip_whitelist) if ip_whitelist else None,
        is_active=True
    )
    
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    return {
        "id": api_key.id,
        "name": api_key.name,
        "key": full_key,  # Vrátiť len raz!
        "prefix": prefix,
        "created_at": api_key.created_at.isoformat(),
        "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
        "permissions": permissions,
        "ip_whitelist": ip_whitelist
    }


def get_api_key_by_hash(db: Session, key_hash: str) -> Optional[ApiKey]:
    """Získať API key podľa hash"""
    return db.query(ApiKey).filter(ApiKey.key_hash == key_hash).first()


def get_api_key_by_token(db: Session, token: str) -> Optional[ApiKey]:
    """
    Získať API key podľa tokenu (validácia).
    
    Args:
        db: Database session
        token: API key token (il_xxxx...)
        
    Returns:
        ApiKey object alebo None
    """
    # Hash token
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    
    # Nájsť key
    api_key = get_api_key_by_hash(db, token_hash)
    
    if not api_key:
        return None
    
    # Kontrola aktivity
    if not api_key.is_active:
        return None
    
    # Kontrola expirácie
    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        return None
    
    return api_key


def get_user_api_keys(db: Session, user_id: int) -> List[ApiKey]:
    """Získať všetky API keys pre používateľa"""
    return db.query(ApiKey).filter(
        ApiKey.user_id == user_id
    ).order_by(ApiKey.created_at.desc()).all()


def revoke_api_key(db: Session, key_id: int, user_id: int) -> bool:
    """
    Zrušiť (deaktivovať) API key.
    
    Args:
        db: Database session
        key_id: ID API key
        user_id: ID používateľa (security check)
        
    Returns:
        True ak úspešné, False ak key neexistuje alebo nepatrí používateľovi
    """
    api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == user_id
    ).first()
    
    if not api_key:
        return False
    
    api_key.is_active = False
    db.commit()
    return True


def update_api_key_usage(db: Session, api_key: ApiKey, ip_address: Optional[str] = None):
    """
    Aktualizovať usage štatistiky pre API key.
    
    Args:
        db: Database session
        api_key: ApiKey object
        ip_address: IP adresa requestu (pre logging)
    """
    api_key.usage_count += 1
    api_key.last_used_at = datetime.utcnow()
    db.commit()


def get_api_key_stats(db: Session, key_id: int, user_id: int) -> Optional[Dict]:
    """
    Získať štatistiky pre API key.
    
    Args:
        db: Database session
        key_id: ID API key
        user_id: ID používateľa
        
    Returns:
        Dict so štatistikami alebo None
    """
    api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == user_id
    ).first()
    
    if not api_key:
        return None
    
    import json
    
    return {
        "id": api_key.id,
        "name": api_key.name,
        "prefix": api_key.prefix,
        "created_at": api_key.created_at.isoformat(),
        "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
        "last_used_at": api_key.last_used_at.isoformat() if api_key.last_used_at else None,
        "usage_count": api_key.usage_count,
        "is_active": api_key.is_active,
        "permissions": json.loads(api_key.permissions) if api_key.permissions else [],
        "ip_whitelist": json.loads(api_key.ip_whitelist) if api_key.ip_whitelist else None
    }

