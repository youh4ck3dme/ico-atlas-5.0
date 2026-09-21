import sys
import os
import traceback

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    print("1. Importing User...")
    from services.auth import User
    print("2. Importing GraphService...")
    from services.graph_service import GraphService
    print("3. Instantiating GraphService...")
    gs = GraphService()
    print("4. SUCCESS.")
except Exception:
    traceback.print_exc()
