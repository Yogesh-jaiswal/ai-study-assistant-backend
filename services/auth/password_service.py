from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Function to hash a password using pwdlib."""
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Function to verify a password against its hash."""
    return password_hash.verify(password, hashed_password)