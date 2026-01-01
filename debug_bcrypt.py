from passlib.context import CryptContext
import sys

def test_bcrypt():
    print("Testing bcrypt...")
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hash = pwd_context.hash("test")
        print(f"Hash success: {hash}")
        verify = pwd_context.verify("test", hash)
        print(f"Verify success: {verify}")
    except Exception as e:
        print(f"Bcrypt ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bcrypt()
