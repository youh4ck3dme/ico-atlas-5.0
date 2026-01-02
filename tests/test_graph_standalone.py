import sys
import os
import traceback
from unittest.mock import MagicMock, patch

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def run_tests():
    print("Running standalone Graph Service tests...")
    
    try:
        # 1. Safe Import Order
        from services.auth import User # Fix registry
        from services.graph_service import GraphService, _person_node_id, _owner_node_id, _looks_like_legal_entity
        
        # Mock GraphNode to avoid DB interaction just for testing logic
        GraphNode = MagicMock()
        GraphNode.return_value = MagicMock(id="mock_node")

        # 2. Instantiate
        service = GraphService()
        
        # 3. Test: ID Stability
        print(" - Testing ID stability...")
        id1 = _person_node_id("SK", "Janko Mrkvička")
        # Note: Outline shows signature _person_node_id(country, name, birth_date)
        id2 = _person_node_id("SK", "Janko Mrkvička")
        if id1 != id2:
            raise AssertionError(f"IDs not stable: {id1} != {id2}")
            
        id3 = _owner_node_id("SK", "Materská Firma")
        id4 = _owner_node_id("SK", "Materská Firma")
        if id3 != id4:
            raise AssertionError(f"Owner IDs not stable: {id3} != {id4}")
            
        # 4. Test: Legal Entity Detection
        print(" - Testing Entity Detection...")
        if not _looks_like_legal_entity("Firma s.r.o."):
             raise AssertionError("Failed to detect s.r.o.")
        if _looks_like_legal_entity("Janko Mrkvička"):
             raise AssertionError("False positive for person name")

        # 5. Test: Ingest (Mocked)
        print(" - Testing Ingest Logic (Mocked)...")
        
        # Mock the instance methods directly
        service.upsert_node = MagicMock()
        service.upsert_edge = MagicMock()
        
        service.ingest_company_relationships(
            atlas_id="123", 
            country="SK", 
            company_label="Test Company", 
            address={"city": "Bratislava"},
            executives=["Boss"]
        )
        
        # Assertions
        if not service.upsert_node.called:
             raise AssertionError("Ingest did not call upsert_node")
             
        # Check specific calls
        # 1. Company Node
        company_args = [c for c in service.upsert_node.call_args_list if c.kwargs.get('node_type') == 'company']
        if not company_args:
             raise AssertionError("Company node not created")
        if company_args[0].kwargs['node_id'] != "sk_123":
             raise AssertionError(f"Wrong company ID: {company_args[0].kwargs['node_id']}")
             
        # 2. Executive Node
        person_args = []
        for call in service.upsert_node.call_args_list:
            args, kwargs = call
            # Check positional (index 2 is node_type) or keyword
            if (len(args) > 2 and args[2] == 'person') or kwargs.get('node_type') == 'person':
                person_args.append((args, kwargs))
                
        if not person_args:
             raise AssertionError("Executive (Person) node not created")
        
        # Verify Person ID
        # ID is usually first arg or kwargs['node_id']
        p_args, p_kwargs = person_args[0]
        pid = p_args[0] if len(p_args) > 0 else p_kwargs.get('node_id')
        
        if not pid or not pid.startswith("pers_sk_"):
             raise AssertionError(f"Wrong person ID format: {pid}")

        print("✅ All standalone tests passed.")
        sys.exit(0)


    except Exception as e:
        print(f"❌ Tests Failed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
