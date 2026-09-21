"""
Migration: Pridať PostgreSQL full-text search podporu
Vytvorí GIN indexy a nastaví pg_trgm rozšírenie
"""

from services.database import get_db_session
from sqlalchemy import text


def add_fulltext_search_support():
    """
    Pridá PostgreSQL full-text search podporu.

    Vykoná:
    1. Vytvorí pg_trgm rozšírenie (ak neexistuje)
    2. Vytvorí GIN indexy pre full-text search
    3. Vytvorí trigram indexy pre podobnosť
    """
    with get_db_session() as db:
        if not db:
            print("❌ Databáza nie je dostupná")
            return False

        try:
            # 1. Vytvoriť pg_trgm rozšírenie
            db.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
            print("✅ pg_trgm rozšírenie vytvorené")

            # 2. Vytvoriť GIN index pre company_name (full-text search)
            db.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS idx_company_name_gin 
                    ON company_cache USING gin(to_tsvector('slovak', company_name));
                    """
                )
            )
            print("✅ GIN index pre company_name vytvorený")

            # 3. Vytvoriť trigram index pre podobnosť (pg_trgm)
            db.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS idx_company_name_trgm 
                    ON company_cache USING gin(company_name gin_trgm_ops);
                    """
                )
            )
            print("✅ Trigram index pre company_name vytvorený")

            # 4. Vytvoriť index pre JSON data (adresa, atď.)
            db.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS idx_company_data_gin 
                    ON company_cache USING gin(to_tsvector('slovak', CAST(data AS text)));
                    """
                )
            )
            print("✅ GIN index pre company_data vytvorený")

            db.commit()
            print("✅ Full-text search podpora pridaná")
            return True

        except Exception as e:
            print(f"❌ Chyba pri vytváraní full-text search: {e}")
            db.rollback()
            return False


if __name__ == "__main__":
    add_fulltext_search_support()
