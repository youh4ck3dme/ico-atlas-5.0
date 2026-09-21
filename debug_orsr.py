
import sys
import os
import logging

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

# Configure logging
logging.basicConfig(level=logging.INFO)

from services.sk_orsr_provider import get_orsr_provider

def debug_orsr(ico):
    print(f"🔍 Debugging ORSR for IČO: {ico}")
    provider = get_orsr_provider()
    
    # Force refresh to bypass cache/db
    data = provider.lookup_by_ico(ico, force_refresh=True)
    
    if data:
        print("✅ Data found:")
        print(data)
    else:
        print("❌ No data found")

if __name__ == "__main__":
    ico = "57206236"  # BEKA COMPANY
    if len(sys.argv) > 1:
        ico = sys.argv[1]
        
    debug_orsr(ico)
