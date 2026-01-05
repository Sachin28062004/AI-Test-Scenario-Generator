import os
from cryptography.fernet import Fernet

# Use ENCRYPTION_KEY from env (base64), otherwise generate a throwaway key (NOT recommended in prod)
KEY = os.getenv("ENCRYPTION_KEY")
if not KEY:
    print("WARNING: ENCRYPTION_KEY not found. Using temporary key (DEV ONLY).")
    KEY = Fernet.generate_key().decode()

fernet = Fernet(KEY.encode())

def encrypt_text(plaintext: str) -> str:
    return fernet.encrypt(plaintext.encode()).decode()

def decrypt_text(ciphertext: str) -> str:
    return fernet.decrypt(ciphertext.encode()).decode()
