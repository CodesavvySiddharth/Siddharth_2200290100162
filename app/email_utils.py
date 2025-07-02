from jose import jwt
from datetime import datetime, timedelta
from app.auth import SECRET_KEY, ALGORITHM
import smtplib
from email.message import EmailMessage
from typing import Optional

EMAIL_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# Generate a token for email verification
def create_email_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=EMAIL_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decode and verify the email token
def verify_email_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None

# Send a verification email (simple SMTP example)
def send_verification_email(to_email: str, verify_url: str):
    msg = EmailMessage()
    msg["Subject"] = "Verify your email"
    msg["From"] = "noreply@example.com"
    msg["To"] = to_email
    msg.set_content(f"Please verify your email by clicking the following link: {verify_url}")

    # For local dev, print instead of sending
    print(f"[DEV] Verification email to {to_email}: {verify_url}")
    # Uncomment below to send via SMTP
    # with smtplib.SMTP('localhost', 1025) as server:
    #     server.send_message(msg) 