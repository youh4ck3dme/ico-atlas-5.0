import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.auth import User # Fix registry
from services.graph_service import GraphService
from services.database import GraphNode, GraphEdge

class TestGraphService(unittest.TestCase):

    def setUp(self):
        # We need to mock get_db_session inside the module or instance
        self.service = GraphService()
        
        # Mock the helper methods to avoid DB calls
        self.service._get_or_create_node = MagicMock()
        self.service._get_or_create_edge = MagicMock()
        
        # Mock the session context manager
        self.mock_session = MagicMock()
        self.mock_ctx = MagicMock()
        self.mock_ctx.__enter__.return_value = self.mock_session
        self.mock_ctx.__exit__.return_value = None
        
        # Patch get_db_session at the module level used by GraphService instance usage
        # But GraphService matches "services.database.get_db_session" if imported?
        # No, GraphService methods usually call "get_db_session()" imported from database.
        # We should patch 'services.graph_service.get_db_session'.

    @patch('services.graph_service.get_db_session')
    def test_ingest_company_relationships(self, mock_get_db_session):
        mock_get_db_session.return_value = self.mock_ctx
        
        # Setup mocks
        mock_company = GraphNode(id="sk_12345678", label="Test Company", type="company") 
        self.service._get_or_create_node.return_value = mock_company

        # Test data
        atlas_id = "12345678"
        executives = [{"name": "Test Executive", "role": "Konateľ"}]
        
        # Run
        with patch.object(self.service, '_get_or_create_node', return_value=mock_company) as mock_node_creator:
             self.service.ingest_company_relationships(
                atlas_id=atlas_id,
                country="SK", 
                company_label="Test Company", 
                executives=["Test Executive"]
             )
             
             # Assertions
             self.assertTrue(mock_node_creator.called)
             # Check if company node was created
             mock_node_creator.assert_any_call(self.mock_session, "sk_12345678", "Test Company", "company", country="SK", details=None)

    def test_person_node_id_stability(self):
        """Test that person IDs are deterministic."""
        name = "Janko Mrkvička"
        company_id = "sk_12345678"
        id1 = self.service._person_node_id(name, company_id)
        id2 = self.service._person_node_id(name, company_id)
        self.assertEqual(id1, id2)

    def test_owner_node_id_stability(self):
        """Test that owner IDs are deterministic."""
        name = "Materská Firma, s.r.o."
        company_id = "sk_12345678"
        id1 = self.service._owner_node_id(name, company_id)
        id2 = self.service._owner_node_id(name, company_id)
        self.assertEqual(id1, id2)

    def test_looks_like_legal_entity(self):
        self.assertTrue(self.service._looks_like_legal_entity("Firma s.r.o."))
        self.assertFalse(self.service._looks_like_legal_entity("Janko Mrkvička"))

if __name__ == '__main__':
    unittest.main()
