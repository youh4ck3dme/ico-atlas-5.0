from services.graph_service import graph_service
from services.database import get_db_session, GraphNode

def test_direct():
    print("Testing GraphService directly...")
    
    # Fake data
    ico = "35763469"
    data = {
        "name": "Slovak Telekom, a.s.",
        "address": {"street": "Bajkalská 28", "city": "Bratislava", "postal_code": "817 62"},
        "executives": ["Ing. VLADIMÍR DANIŠKA"], # Simple
        "executive_people": [{"name": "Ing. VLADIMÍR DANIŠKA", "role": "Konateľ", "since": "2024-01-01"}], # Structured
        "shareholders": ["Deutsche Telekom Europe B.V."],
        "shareholder_people": [{"name": "Deutsche Telekom Europe B.V.", "percentage": 100}]
    }

    try:
        print("1. Ingesting...")
        graph_service.ingest_company_relationships(
            atlas_id=ico,
            country="SK",
            company_label=data["name"],
            address=data["address"],
            executives=data["executives"],
            owners=data["shareholders"],
            executive_people=data["executive_people"],
            shareholder_people=data["shareholder_people"],
            source="TEST"
        )
        print("Ingest done.")
    except Exception as e:
        print(f"!!! Ingest FAILED: {e}")
        import traceback
        traceback.print_exc()

    try:
        print("2. Building Graph...")
        g = graph_service.build_company_graph(ico, "SK")
        print(f"Graph Nodes: {len(g.get('nodes', []))}")
        for n in g.get('nodes', []):
            print(f" - {n['label']} ({n['id']})")
            
    except Exception as e:
        print(f"!!! Build FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct()
