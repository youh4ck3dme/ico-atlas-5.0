"""
Migration: Add GDPR consent fields to users table
Run this script to add consent tracking columns to existing database
"""

import os
import sys

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database URL
_default_user = os.getenv("USER", os.getenv("USERNAME", "postgres"))
DATABASE_URL = os.getenv(
    "DATABASE_URL", f"postgresql://{_default_user}@localhost:5432/iluminati_db"
)


def run_migration():
    """Pridá GDPR consent stĺpce do users tabuľky"""
    try:
        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            # Check if columns already exist
            consent_columns = [
                "consent_given",
                "consent_timestamp",
                "consent_ip",
                "consent_user_agent",
                "document_versions",
            ]

            for column in consent_columns:
                result = conn.execute(
                    text(f"""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name='users' AND column_name='{column}'
                """)
                )

                if result.fetchone():
                    print(f"✅ Stĺpec '{column}' už existuje")
                    continue

                # Add column based on type
                if column == "consent_given":
                    conn.execute(
                        text(f"""
                        ALTER TABLE users
                        ADD COLUMN {column} BOOLEAN DEFAULT TRUE NOT NULL
                    """)
                    )
                elif column in ["consent_timestamp"]:
                    conn.execute(
                        text(f"""
                        ALTER TABLE users
                        ADD COLUMN {column} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                    """)
                    )
                elif column in [
                    "consent_ip",
                    "consent_user_agent",
                    "document_versions",
                ]:
                    conn.execute(
                        text(f"""
                        ALTER TABLE users
                        ADD COLUMN {column} VARCHAR(500)
                    """)
                    )

                print(f"✅ Stĺpec '{column}' úspešne pridaný")

            conn.commit()
            print("✅ GDPR consent polia úspešne pridané")
            return True

    except Exception as e:
        print(f"❌ Chyba pri migrácii: {e}")
        return False


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
