from app.core.auth import get_password_hash, verify_password

# Test password hashing with the updated auth module
try:
    password = "testpass123"
    print(f"Password: {password}, Length: {len(password)}")

    # Hash the password
    hashed = get_password_hash(password)
    print(f"Password hashed successfully: {hashed[:30]}...")

    # Verify the password
    is_valid = verify_password(password, hashed)
    print(f"Password verification result: {is_valid}")

    # Test with wrong password
    is_valid_wrong = verify_password("wrongpassword", hashed)
    print(f"Wrong password verification result: {is_valid_wrong}")

except Exception as e:
    print(f"Error testing auth module: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()