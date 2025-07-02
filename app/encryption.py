from cryptography.fernet import Fernet, InvalidToken
import base64

# In production, use a secure, persistent key (e.g., from env variable)
FERNET_KEY = base64.urlsafe_b64encode(b"supersecretfernetkey123456789012")  # 32 bytes
fernet = Fernet(FERNET_KEY)

def encrypt_id(plain_id: int) -> str:
    return fernet.encrypt(str(plain_id).encode()).decode()

def decrypt_id(token: str) -> int:
    try:
        decrypted = fernet.decrypt(token.encode()).decode()
        return int(decrypted)
    except (InvalidToken, ValueError):
        return None 