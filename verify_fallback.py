import os
import sys

# Simulation: Set DATABASE_URL to a non-existent postgres
os.environ["DATABASE_URL"] = "postgresql://invalid:invalid@localhost:9999/invalid"

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from services.database import init_database

print("Testing database initialization with invalid PostgreSQL URL...")
success = init_database()

if success:
    print("Verification SUCCESS: init_database() returned True (fallback likely worked)")
else:
    print("Verification FAILED: init_database() returned False")

# Check for fallback file
fallback_file = "backend/sql_app_fallback.db"
if os.path.exists(fallback_file):
    print(f"✅ Fallback file created: {fallback_file}")
    # Cleanup
    os.remove(fallback_file)
    print("   Fallback file cleaned up.")
else:
    print("❌ Fallback file NOT found.")
