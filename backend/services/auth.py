"""
Autentifikačný systém pre ILUMINATI SYSTEM
JWT token-based authentication
"""

import enum
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Session, relationship

from services.database import Base

# Password hashing
# Use sha256_crypt as default to avoid bcrypt issues on Windows
pwd_context = CryptContext(schemes=["sha256_crypt", "bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 dní


class UserTier(str, enum.Enum):
    """Subscription tiers"""

    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class User(Base):
    """
    User model

    The stripe_customer_id field links users to their Stripe customer record.
    This is critical for webhook handling - when Stripe sends subscription events,
    they include the customer ID (not email), so we need this mapping to identify
    which user's subscription was modified.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    tier = Column(SQLEnum(UserTier), default=UserTier.FREE, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    stripe_customer_id = Column(
        String, unique=True, index=True, nullable=True
    )  # Stripe customer ID for subscription management

    # GDPR Consent fields
    consent_given = Column(Boolean, default=True, nullable=False)
    consent_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    consent_ip = Column(String, nullable=True)
    consent_user_agent = Column(String, nullable=True)
    document_versions = Column(
        String, nullable=True
    )  # JSON string with document versions

    # Relationships
    api_keys = relationship(
        "ApiKey", back_populates="user", cascade="all, delete-orphan"
    )
    webhooks = relationship(
        "Webhook", back_populates="user", cascade="all, delete-orphan"
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Overí heslo"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashuje heslo"""
    return pwd_context.hash(password)


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Vytvorí JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict]:
    """Dekóduje JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Získa používateľa podľa emailu"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_stripe_customer_id(
    db: Session, stripe_customer_id: str
) -> Optional[User]:
    """
    Získa používateľa podľa Stripe customer ID

    This is essential for webhook handling - Stripe sends customer IDs in events,
    not emails, so we need this to map subscription events to users.

    Args:
        db: Database session
        stripe_customer_id: Stripe customer ID (e.g., 'cus_xxxxx')

    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.stripe_customer_id == stripe_customer_id).first()


def update_user_stripe_customer_id(
    db: Session, user_id: int, stripe_customer_id: str
) -> bool:
    """Aktualizuje Stripe customer ID používateľa"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    user.stripe_customer_id = stripe_customer_id
    db.commit()
    return True


def create_user(
    db: Session,
    email: str,
    password: str,
    full_name: Optional[str] = None,
    consent_given: bool = True,
    consent_ip: Optional[str] = None,
    consent_user_agent: Optional[str] = None,
    document_versions: Optional[Dict[str, str]] = None,
) -> User:
    """Vytvorí nového používateľa"""
    import json

    hashed_password = get_password_hash(password)

    # Default document versions if not provided
    if document_versions is None:
        document_versions = {"vop": "1.0", "privacy": "1.0", "cookies": "1.0"}

    user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        tier=UserTier.FREE,
        is_active=True,
        is_verified=False,
        consent_given=consent_given,
        consent_ip=consent_ip,
        consent_user_agent=consent_user_agent,
        document_versions=json.dumps(document_versions),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Autentifikuje používateľa"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


def update_user_tier(db: Session, user_id: int, tier: UserTier) -> bool:
    """Aktualizuje tier používateľa"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    user.tier = tier
    db.commit()
    return True


def get_user_tier_limits(tier: UserTier) -> Dict:
    """Vráti limity pre tier"""
    limits = {
        UserTier.FREE: {
            "searches_per_day": 10,
            "searches_per_month": 100,
            "export_limit": 5,
            "api_access": False,
            "advanced_features": False,
        },
        UserTier.PRO: {
            "searches_per_day": 100,
            "searches_per_month": 2000,
            "export_limit": 100,
            "api_access": False,
            "advanced_features": True,
        },
        UserTier.ENTERPRISE: {
            "searches_per_day": -1,  # Unlimited
            "searches_per_month": -1,  # Unlimited
            "export_limit": -1,  # Unlimited
            "api_access": True,
            "advanced_features": True,
        },
    }
    return limits.get(tier, limits[UserTier.FREE])
