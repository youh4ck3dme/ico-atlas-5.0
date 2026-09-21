"""
Favorites service pre ILUMINATI SYSTEM
Správa obľúbených firiem používateľov
"""

from typing import Dict, List, Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from services.database import get_db_session, FavoriteCompany


def add_favorite(
    db: Session,
    user_id: int,
    company_identifier: str,
    company_name: str,
    country: str,
    company_data: Optional[Dict] = None,
    risk_score: Optional[float] = None,
    notes: Optional[str] = None,
) -> FavoriteCompany:
    """
    Pridá firmu do obľúbených.
    
    Args:
        db: Database session
        user_id: ID používateľa
        company_identifier: IČO, KRS, etc.
        company_name: Názov firmy
        country: Krajina (SK, CZ, PL, HU)
        company_data: Full company data (optional)
        risk_score: Risk score (optional)
        notes: User notes (optional)
    
    Returns:
        FavoriteCompany object
    """
    # Skontrolovať, či už existuje
    existing = (
        db.query(FavoriteCompany)
        .filter(
            and_(
                FavoriteCompany.user_id == user_id,
                FavoriteCompany.company_identifier == company_identifier,
                FavoriteCompany.country == country,
            )
        )
        .first()
    )
    
    if existing:
        # Aktualizovať existujúci
        existing.company_name = company_name
        if company_data:
            existing.company_data = company_data
        if risk_score is not None:
            existing.risk_score = risk_score
        if notes:
            existing.notes = notes
        db.commit()
        db.refresh(existing)
        return existing
    
    # Vytvoriť nový
    favorite = FavoriteCompany(
        user_id=user_id,
        company_identifier=company_identifier,
        company_name=company_name,
        country=country,
        company_data=company_data,
        risk_score=risk_score,
        notes=notes,
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


def remove_favorite(
    db: Session,
    user_id: int,
    favorite_id: int,
) -> bool:
    """
    Odstráni firmu z obľúbených.
    
    Args:
        db: Database session
        user_id: ID používateľa
        favorite_id: ID favorite záznamu
    
    Returns:
        True ak bol odstránený, False ak neexistoval
    """
    favorite = (
        db.query(FavoriteCompany)
        .filter(
            and_(
                FavoriteCompany.id == favorite_id,
                FavoriteCompany.user_id == user_id,
            )
        )
        .first()
    )
    
    if favorite:
        db.delete(favorite)
        db.commit()
        return True
    
    return False


def get_user_favorites(
    db: Session,
    user_id: int,
    limit: Optional[int] = None,
) -> List[FavoriteCompany]:
    """
    Získa zoznam obľúbených firiem používateľa.
    
    Args:
        db: Database session
        user_id: ID používateľa
        limit: Max počet výsledkov (optional)
    
    Returns:
        List of FavoriteCompany objects
    """
    query = (
        db.query(FavoriteCompany)
        .filter(FavoriteCompany.user_id == user_id)
        .order_by(FavoriteCompany.created_at.desc())
    )
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def is_favorite(
    db: Session,
    user_id: int,
    company_identifier: str,
    country: str,
) -> bool:
    """
    Skontroluje, či je firma v obľúbených.
    
    Args:
        db: Database session
        user_id: ID používateľa
        company_identifier: IČO, KRS, etc.
        country: Krajina
    
    Returns:
        True ak je v obľúbených, False inak
    """
    favorite = (
        db.query(FavoriteCompany)
        .filter(
            and_(
                FavoriteCompany.user_id == user_id,
                FavoriteCompany.company_identifier == company_identifier,
                FavoriteCompany.country == country,
            )
        )
        .first()
    )
    
    return favorite is not None


def update_favorite_notes(
    db: Session,
    user_id: int,
    favorite_id: int,
    notes: str,
) -> Optional[FavoriteCompany]:
    """
    Aktualizuje poznámky k obľúbenej firme.
    
    Args:
        db: Database session
        user_id: ID používateľa
        favorite_id: ID favorite záznamu
        notes: Nové poznámky
    
    Returns:
        FavoriteCompany object alebo None ak neexistuje
    """
    favorite = (
        db.query(FavoriteCompany)
        .filter(
            and_(
                FavoriteCompany.id == favorite_id,
                FavoriteCompany.user_id == user_id,
            )
        )
        .first()
    )
    
    if favorite:
        favorite.notes = notes
        db.commit()
        db.refresh(favorite)
        return favorite
    
    return None

