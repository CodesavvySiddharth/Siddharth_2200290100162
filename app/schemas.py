from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_verified: bool
    class Config:
        orm_mode = True

class FileOut(BaseModel):
    id: int
    original_filename: str
    upload_time: datetime.datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class DownloadLinkResponse(BaseModel):
    download_link: str
    message: str 