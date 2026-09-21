"""
API Authentication Middleware
Validácia API keys pre Enterprise tier používateľov
"""

from typing import Optional
from fastapi import HTTPException, status, Header
from sqlalchemy.orm import Session
from services.api_keys import get_api_key_by_token, update_api_key_usage
from services.database import get_db_session
from services.auth import User, UserTier


async def verify_api_key(
    authorization: Optional[str] = Header(None),
    x_forwarded_for: Optional[str] = Header(None)
) -> User:
    """
    Middleware pre validáciu API key.
    
    Args:
        authorization: Authorization header (Bearer il_xxxx...)
        x_forwarded_for: IP adresa klienta (pre IP whitelist)
        
    Returns:
        User object ak je key validný
        
    Raises:
        HTTPException ak key nie je validný
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )
    
    # Parse Bearer token
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Use: Bearer <api_key>"
        )
    
    api_key_token = authorization.replace("Bearer ", "").strip()
    
    # Get IP address
    client_ip = x_forwarded_for.split(",")[0].strip() if x_forwarded_for else None
    
    # Validate API key
    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database unavailable"
            )
        
        api_key = get_api_key_by_token(db, api_key_token)
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        # Check IP whitelist
        if api_key.ip_whitelist:
            import json
            whitelist = json.loads(api_key.ip_whitelist)
            if client_ip and client_ip not in whitelist:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"IP address {client_ip} not whitelisted"
                )
        
        # Get user
        user = db.query(User).filter(User.id == api_key.user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Check if user has Enterprise tier
        if user.tier != UserTier.ENTERPRISE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="API access requires Enterprise tier"
            )
        
        # Update usage stats
        update_api_key_usage(db, api_key, client_ip)
        
        return user


def check_api_permission(api_key, permission: str) -> bool:
    """
    Skontrolovať, či API key má požadované permission.
    
    Args:
        api_key: ApiKey object
        permission: Permission name ("read", "write")
        
    Returns:
        True ak má permission, False inak
    """
    if not api_key.permissions:
        return False
    
    import json
    permissions = json.loads(api_key.permissions)
    return permission in permissions

