from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app import schemas, models, auth, database
from app.database import get_db
from app.auth import hash_password, verify_password, create_access_token
from app.deps import require_ops_user
import os
import uuid
import shutil
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if user.role != "ops":
        raise HTTPException(status_code=403, detail="Only ops users can login here")
    access_token = auth.create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

ALLOWED_EXTENSIONS = {"pptx", "docx", "xlsx"}

@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    current_user=Depends(require_ops_user),
    db: Session = Depends(get_db)
):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only pptx, docx, xlsx files are allowed")
    unique_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join("files", unique_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    db_file = models.File(filename=unique_name, original_filename=file.filename, uploader_id=current_user.id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return {"message": "File uploaded successfully", "file_id": db_file.id} 