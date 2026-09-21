from services.database import init_database
from services.auth import User # Ensure User model is registered with Base

def init_db():
    print("Calling init_database() with User model loaded...")
    success = init_database()
    if success:
        print("Database initialized successfully.")
    else:
        print("Failed to initialize database.")

if __name__ == "__main__":
    init_db()
