from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import schemas, models, auth, email_utils, encryption, database
from app.database import get_db
from app.auth import hash_password, verify_password, create_access_token
from app.email_utils import create_email_token, send_verification_email, verify_email_token
from app.encryption import encrypt_id, decrypt_id
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.deps import require_verified_user

router = APIRouter()

@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, request: Request, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    db_user = models.User(email=user.email, password_hash=hashed, role="client", is_verified=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Generate verification token and URL
    token = create_email_token(db_user.email)
    verify_url = str(request.base_url) + f"client/verify/{token}"
    send_verification_email(db_user.email, verify_url)
    return db_user

@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        return {"message": "Email already verified"}
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if user.role != "client":
        raise HTTPException(status_code=403, detail="Only client users can login here")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    access_token = auth.create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/files", response_model=list[schemas.FileOut])
def list_files(current_user=Depends(require_verified_user), db: Session = Depends(get_db)):
    files = db.query(models.File).all()
    return files

@router.get("/download-link/{file_id}", response_model=schemas.DownloadLinkResponse)
def get_download_link(file_id: int, request: Request, current_user=Depends(require_verified_user), db: Session = Depends(get_db)):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    encrypted_id = encrypt_id(file.id)
    download_url = str(request.base_url) + f"client/download/{encrypted_id}"
    return {"download_link": download_url, "message": "success"}

@router.get("/download/{encrypted_id}")
def download_file(encrypted_id: str, current_user=Depends(require_verified_user), db: Session = Depends(get_db)):
    file_id = decrypt_id(encrypted_id)
    if not file_id:
        raise HTTPException(status_code=400, detail="Invalid or expired download link")
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    file_path = f"files/{file.filename}"
    return FileResponse(path=file_path, filename=file.original_filename, media_type="application/octet-stream") 