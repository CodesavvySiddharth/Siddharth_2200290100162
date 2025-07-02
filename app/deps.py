from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.auth import decode_access_token
from app.database import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/client/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exception
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if user is None:
        raise credentials_exception
    return user

def require_ops_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "ops":
        raise HTTPException(status_code=403, detail="Only Ops users allowed")
    return current_user

def require_client_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only Client users allowed")
    return current_user

def require_verified_user(current_user: User = Depends(require_client_user)):
    if not current_user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    return current_user 