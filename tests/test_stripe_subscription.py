"""
Testy pre Stripe subscription management
Tests webhook handling, customer ID mapping, and tier downgrade logic
"""
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Pridať backend do path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Set up in-memory database for testing
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from services.stripe_service import create_checkout_session, handle_webhook
from services.auth import User, UserTier, get_user_by_stripe_customer_id, create_user, update_user_tier
from services.database import get_db_session, init_database, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def test_user_model_has_stripe_customer_id():
    """Test that User model has stripe_customer_id field"""
    print("🔍 Test: User model has stripe_customer_id field...")
    try:
        # Check if User model has the stripe_customer_id column
        assert hasattr(User, 'stripe_customer_id'), "User model should have stripe_customer_id field"
        print("   ✅ User model has stripe_customer_id field")
        return True
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False


def test_get_user_by_stripe_customer_id():
    """Test getting user by Stripe customer ID"""
    print("🔍 Test: Get user by Stripe customer ID...")
    try:
        with get_db_session() as db:
            if db is None:
                print("   ⚠️  Database not available, skipping test")
                return True
            
            # Create test user
            test_email = f"test_stripe_user_{os.getpid()}@example.com"
            
            # Clean up existing test user if any
            try:
                existing = db.query(User).filter(User.email == test_email).first()
                if existing:
                    db.delete(existing)
                    db.commit()
            except:
                pass
            
            user = create_user(db, test_email, "password123", "Test User")
            test_customer_id = f"cus_test_{os.getpid()}"
            
            # Set stripe customer ID
            user.stripe_customer_id = test_customer_id
            db.commit()
            db.refresh(user)
            
            # Test retrieval
            retrieved_user = get_user_by_stripe_customer_id(db, test_customer_id)
            assert retrieved_user is not None, "Should find user by stripe customer ID"
            assert retrieved_user.id == user.id, "Should return correct user"
            assert retrieved_user.stripe_customer_id == test_customer_id, "Should have correct customer ID"
            
            # Clean up
            db.delete(user)
            db.commit()
            
        print("   ✅ Get user by Stripe customer ID works")
        return True
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


@patch('services.stripe_service.stripe.Customer')
@patch('services.stripe_service.stripe.checkout.Session')
def test_create_checkout_session_stores_customer_id(mock_session, mock_customer):
    """Test that create_checkout_session stores Stripe customer ID"""
    print("🔍 Test: Create checkout session stores customer ID...")
    try:
        # Mock Stripe customer
        mock_customer_obj = Mock()
        mock_customer_obj.id = f"cus_test_new_{os.getpid()}"
        mock_customer.create.return_value = mock_customer_obj
        mock_customer.list.return_value = Mock(data=[])
        
        # Mock checkout session
        mock_session_obj = Mock()
        mock_session_obj.id = "cs_test_12345"
        mock_session_obj.url = "https://checkout.stripe.com/test"
        mock_session.create.return_value = mock_session_obj
        
        with get_db_session() as db:
            if db is None:
                print("   ⚠️  Database not available, skipping test")
                return True
            
            # Create test user
            test_email = f"test_checkout_{os.getpid()}@example.com"
            
            # Clean up existing test user if any
            try:
                existing = db.query(User).filter(User.email == test_email).first()
                if existing:
                    db.delete(existing)
                    db.commit()
            except:
                pass
            
            user = create_user(db, test_email, "password123", "Test Checkout User")
            user_id = user.id
            db.commit()
            
            # Call create_checkout_session
            result = create_checkout_session(user_id, test_email, UserTier.PRO)
            
            # Verify result
            assert "error" not in result, f"Should not have error: {result.get('error')}"
            assert result["status"] == "created", "Should return created status"
            
            # Verify customer ID was stored
            db.refresh(user)
            assert user.stripe_customer_id is not None, "Should have stored Stripe customer ID"
            assert user.stripe_customer_id == mock_customer_obj.id, "Should store correct customer ID"
            
            # Clean up
            db.delete(user)
            db.commit()
        
        print("   ✅ Create checkout session stores customer ID")
        return True
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


@patch('services.stripe_service.stripe.Webhook.construct_event')
def test_webhook_subscription_deleted_downgrades_user(mock_construct_event):
    """Test that webhook handler downgrades user when subscription is deleted"""
    print("🔍 Test: Webhook subscription deleted downgrades user...")
    try:
        with get_db_session() as db:
            if db is None:
                print("   ⚠️  Database not available, skipping test")
                return True
            
            # Create test user with PRO tier
            test_email = f"test_webhook_{os.getpid()}@example.com"
            test_customer_id = f"cus_webhook_test_{os.getpid()}"
            
            # Clean up existing test user if any
            try:
                existing = db.query(User).filter(User.email == test_email).first()
                if existing:
                    db.delete(existing)
                    db.commit()
            except:
                pass
            
            user = create_user(db, test_email, "password123", "Test Webhook User")
            user.stripe_customer_id = test_customer_id
            user.tier = UserTier.PRO
            db.commit()
            db.refresh(user)
            user_id = user.id
            
            # Mock webhook event for subscription deleted
            mock_event = {
                'type': 'customer.subscription.deleted',
                'data': {
                    'object': {
                        'id': 'sub_test_12345',
                        'customer': test_customer_id  # This is what Stripe actually sends
                    }
                }
            }
            mock_construct_event.return_value = mock_event
            
            # Call webhook handler
            result = handle_webhook(b'payload', 'signature')
            
            # Verify result
            assert result["status"] == "success", "Should return success"
            assert result["action"] == "downgrade_to_free", "Should indicate downgrade action"
            
            # Verify user was downgraded
            db.refresh(user)
            assert user.tier == UserTier.FREE, f"User tier should be FREE, got {user.tier}"
            
            # Clean up
            db.delete(user)
            db.commit()
        
        print("   ✅ Webhook subscription deleted downgrades user")
        return True
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


@patch('services.stripe_service.stripe.Webhook.construct_event')
def test_webhook_handles_missing_customer_id_gracefully(mock_construct_event):
    """Test that webhook handler handles missing customer ID gracefully"""
    print("🔍 Test: Webhook handles missing customer ID gracefully...")
    try:
        # Mock webhook event with no customer ID
        mock_event = {
            'type': 'customer.subscription.deleted',
            'data': {
                'object': {
                    'id': 'sub_test_12345'
                    # No customer field
                }
            }
        }
        mock_construct_event.return_value = mock_event
        
        # Call webhook handler
        result = handle_webhook(b'payload', 'signature')
        
        # Verify it doesn't crash and returns success
        assert result["status"] == "success", "Should return success even if no customer"
        assert result["action"] == "downgrade_to_free", "Should indicate downgrade action"
        
        print("   ✅ Webhook handles missing customer ID gracefully")
        return True
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all Stripe subscription tests"""
    print("")
    print("═══════════════════════════════════════")
    print("🧪 STRIPE SUBSCRIPTION TESTS")
    print("═══════════════════════════════════════")
    print("")
    
    # Initialize in-memory database for testing
    try:
        # Create in-memory SQLite database
        engine = create_engine("sqlite:///:memory:", echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        
        # Override database module with test database
        import services.database as db_module
        db_module.engine = engine
        db_module.SessionLocal = SessionLocal
        db_module._initialized = True
        
        print("✅ In-memory test database initialized")
    except Exception as e:
        print(f"⚠️  Could not initialize test database: {e}")
        print("   Some tests may fail")
    
    tests = [
        test_user_model_has_stripe_customer_id,
        test_get_user_by_stripe_customer_id,
        test_create_checkout_session_stores_customer_id,
        test_webhook_subscription_deleted_downgrades_user,
        test_webhook_handles_missing_customer_id_gracefully,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ❌ Test crashed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("")
    print("═══════════════════════════════════════")
    print(f"📊 RESULTS: {passed} passed, {failed} failed")
    print("═══════════════════════════════════════")
    print("")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
