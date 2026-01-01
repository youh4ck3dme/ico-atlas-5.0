import sys
import os

# Add backend directory to sys.path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "backend"))

from backend.services import database
from backend.services.database import init_database
from backend.services.auth import create_user, authenticate_user

def debug_direct():
    print("Initializing DB...")
    init_database()
    # Access SessionLocal from the module to get the updated value
    db = database.SessionLocal()
    
    print("Creating User...")
    email = "test_direct@example.com"
    password = "TestPassword123!"
    
    try:
        user = create_user(db, email, password, full_name="Direct Debug User")
        print(f"User Created: {user.id} - {user.email}")
        print(f"Hash: {user.hashed_password}")
    except Exception as e:
        print(f"CRASH during create_user: {e}")
        import traceback
        traceback.print_exc()

    print("\nAuthenticating...")
    try:
        auth_user = authenticate_user(db, email, password)
        if auth_user:
            print("Authentication SUCCESS")
        else:
            print("Authentication FAILED (None)")
    except Exception as e:
        print(f"CRASH during authenticate_user: {e}")
        import traceback
        traceback.print_exc()
        
    db.close()

if __name__ == "__main__":
    debug_direct()
