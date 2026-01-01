"""
Migration: Pridať stĺpec company_data do company_cache tabuľky
"""

from services.database import get_db_session
from sqlalchemy import text


def add_company_data_column():
    """
    Pridá stĺpec company_data do company_cache tabuľky.
    """
    with get_db_session() as db:
        if not db:
            print("❌ Databáza nie je dostupná")
            return False

        try:
            # Skontrolovať, či stĺpec už existuje
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'company_cache' 
                AND column_name = 'company_data';
            """)
            result = db.execute(check_query).fetchone()

            if result:
                print("✅ Stĺpec company_data už existuje")
                return True

            # Pridať stĺpec company_data
            db.execute(text("""
                ALTER TABLE company_cache 
                ADD COLUMN company_data JSON;
            """))
            print("✅ Stĺpec company_data pridaný")

            # Skontrolovať, či existuje stĺpec last_synced_at
            check_synced = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'company_cache' 
                AND column_name = 'last_synced_at';
            """)
            result_synced = db.execute(check_synced).fetchone()

            if not result_synced:
                # Pridať stĺpec last_synced_at ak neexistuje
                db.execute(text("""
                    ALTER TABLE company_cache 
                    ADD COLUMN last_synced_at TIMESTAMP;
                """))
                print("✅ Stĺpec last_synced_at pridaný")

            db.commit()
            print("✅ Migrácia úspešne dokončená")
            return True

        except Exception as e:
            print(f"❌ Chyba pri migrácii: {e}")
            db.rollback()
            return False


if __name__ == "__main__":
    add_company_data_column()

