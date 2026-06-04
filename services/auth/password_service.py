from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password):
    """Function to hash a password using pwdlib."""
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    """Function to verify a password against its hash."""
    return password_hash.verify(password, hashed_password)