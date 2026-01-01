"""
Migration: Add stripe_customer_id column to users table
Run this script to add the new column to existing database
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database URL
_default_user = os.getenv("USER", os.getenv("USERNAME", "postgres"))
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{_default_user}@localhost:5432/iluminati_db"
)

def run_migration():
    """Pridá stripe_customer_id stĺpec do users tabuľky"""
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # Skontrolovať, či stĺpec už existuje
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='stripe_customer_id'
            """))
            
            if result.fetchone():
                print("✅ Stĺpec 'stripe_customer_id' už existuje")
                return True
            
            # Pridať stĺpec
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN stripe_customer_id VARCHAR(255)
            """))
            
            # Vytvoriť index
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_users_stripe_customer_id 
                ON users(stripe_customer_id)
            """))
            
            conn.commit()
            print("✅ Stĺpec 'stripe_customer_id' úspešne pridaný")
            return True
            
    except Exception as e:
        print(f"❌ Chyba pri migrácii: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)

