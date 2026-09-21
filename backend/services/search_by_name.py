"""
Vyhľadávanie podľa názvu - Full-text search v lokálnej DB
"""

from typing import Dict, List, Optional

from sqlalchemy import Text, func, or_

from services.database import CompanyCache, get_db_session


def normalize_query(query: str) -> str:
    """
    Normalizuje vyhľadávací query.

    - Odstráni diakritiku
    - Zmení na lowercase
    - Odstráni extra medzery
    """
    import unicodedata

    # Odstrániť diakritiku
    normalized = unicodedata.normalize("NFD", query)
    normalized = "".join(c for c in normalized if unicodedata.category(c) != "Mn")

    # Lowercase a trim
    normalized = normalized.lower().strip()

    # Odstrániť extra medzery
    normalized = " ".join(normalized.split())

    return normalized


def search_by_name(
    query: str, country: Optional[str] = None, limit: int = 20
) -> List[Dict]:
    """
    Vyhľadá firmy podľa názvu v lokálnej DB.

    Poznámka: Toto je len lokálna DB - nevykonáva live scraping.
    Firma sa nájde len ak už bola niekedy "objavená" cez IČO.

    Args:
        query: Vyhľadávací text (názov firmy)
        country: Krajina (SK, CZ, PL, HU) - voliteľné
        limit: Maximálny počet výsledkov

    Returns:
        List s firmami
    """
    if not query or len(query) < 2:
        return []

    # Normalizovať query
    query_normalized = normalize_query(query)

    with get_db_session() as db:
        if not db:
            return []

        # PostgreSQL full-text search alebo LIKE/ILIKE
        # Skúsiť najprv full-text search (ak je dostupný), potom fallback na ILIKE

        results = None

        # Skontrolovať, či existuje pg_trgm rozšírenie
        try:
            # Full-text search s pg_trgm (similarity)
            from sqlalchemy import text

            # Použiť similarity search (pg_trgm)
            similarity_query = text(
                """
                SELECT id, company_name, data, company_data, country, risk_score, 
                       updated_at, last_synced_at,
                       similarity(company_name, :query) as sim_score
                FROM company_cache
                WHERE company_name % :query
                   OR CAST(data AS text) % :query
                ORDER BY sim_score DESC, updated_at DESC
                LIMIT :limit
                """
            )

            results_raw = db.execute(
                similarity_query, {"query": query_normalized, "limit": limit}
            ).fetchall()

            if results_raw:
                # Konvertovať výsledky
                results = []
                for row in results_raw:
                    company = (
                        db.query(CompanyCache).filter(CompanyCache.id == row.id).first()
                    )
                    if company:
                        results.append(company)

                if results:
                    print(
                        f"✅ Full-text search (pg_trgm) použité pre: {query_normalized}"
                    )
        except Exception as e:
            print(f"⚠️ Full-text search nie je dostupný: {e}, používam ILIKE")
            results = None

        # Fallback na ILIKE ak full-text search zlyhal alebo nie je dostupný
        if not results:
            # Vytvoriť search pattern
            search_pattern = f"%{query_normalized}%"

            # Základný query
            db_query = db.query(CompanyCache).filter(
                or_(
                    CompanyCache.company_name.ilike(search_pattern),
                    # Môžeme hľadať aj v JSON dátach (adresa, atď.)
                    # Fix: Použiť správny typ Text bez zátvoriek a ošetriť DB dialekt
                    func.cast(CompanyCache.data, Text).ilike(search_pattern),
                )
            )

            # Filtrovať podľa krajiny ak je zadaná
            if country:
                db_query = db_query.filter(CompanyCache.country == country.upper())

            # Zoradiť podľa relevance (názov má prednosť)
            try:
                # SQLite nepodporuje .ilike() v order_by rovnako ako Postgres
                # Použijeme jednoduchšie zoradenie ak ilike zlyhá v order_by
                results = (
                    db_query.order_by(
                        CompanyCache.company_name.desc(),
                        CompanyCache.updated_at.desc(),
                    )
                    .limit(limit)
                    .all()
                )
            except Exception:
                results = db_query.limit(limit).all()

        # Konvertovať na dict
        companies = []
        for company in (results or []):
            try:
                company_data = company.company_data or company.data or {}
                companies.append(
                    {
                        "identifier": company.identifier,
                        "country": company.country,
                        "name": company.company_name
                        or company_data.get("name", "Neznáma firma"),
                        "legal_form": company_data.get("legal_form"),
                        "address": company_data.get("address"),
                        "risk_score": company.risk_score,
                        "last_synced_at": company.last_synced_at.isoformat()
                        if hasattr(company, 'last_synced_at') and company.last_synced_at
                        else None,
                    }
                )
            except Exception as e:
                print(f"⚠️ Error parsing company row: {e}")

        return companies


def search_by_address(
    query: str, country: Optional[str] = None, limit: int = 20
) -> List[Dict]:
    """
    Vyhľadá firmy podľa adresy v lokálnej DB.

    Args:
        query: Vyhľadávací text (adresa)
        country: Krajina (SK, CZ, PL, HU) - voliteľné
        limit: Maximálny počet výsledkov

    Returns:
        List s firmami
    """
    if not query or len(query) < 2:
        return []

    # Normalizovať query
    query_normalized = normalize_query(query)
    search_pattern = f"%{query_normalized}%"

    with get_db_session() as db:
        if not db:
            return []

        # Hľadať v JSON dátach (adresa)
        db_query = db.query(CompanyCache).filter(
            func.cast(CompanyCache.data, Text()).ilike(search_pattern)
        )

        if country:
            db_query = db_query.filter(CompanyCache.country == country.upper())

        results = db_query.order_by(CompanyCache.updated_at.desc()).limit(limit).all()

        companies = []
        for company in results:
            company_data = company.company_data or company.data or {}
            address = company_data.get("address", "")

            # Skontrolovať, či adresa obsahuje query
            if query_normalized in normalize_query(address):
                companies.append(
                    {
                        "identifier": company.identifier,
                        "country": company.country,
                        "name": company.company_name
                        or company_data.get("name", "Neznáma firma"),
                        "address": address,
                        "risk_score": company.risk_score,
                    }
                )

        return companies
