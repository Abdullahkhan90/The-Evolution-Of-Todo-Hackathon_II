import bcrypt

# Test bcrypt directly
try:
    password = "testpass123"
    print(f"Password length: {len(password)}")
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    print(f"Password '{password}' was hashed successfully with bcrypt: {hashed[:20]}...")
except Exception as e:
    print(f"Error hashing password with bcrypt: {e}")
    print(f"Error type: {type(e)}")

# Test with passlib
try:
    from passlib.hash import bcrypt as passlib_bcrypt
    password = "testpass123"
    hashed = passlib_bcrypt.hash(password)
    print(f"Password '{password}' was hashed successfully with passlib: {hashed[:20]}...")
except Exception as e:
    print(f"Error hashing password with passlib: {e}")
    print(f"Error type: {type(e)}")