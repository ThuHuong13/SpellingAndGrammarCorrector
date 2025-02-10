from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class DocumentCreate(BaseModel):
    content: str
    errors: Optional[dict] = None


class CorrectionCreate(BaseModel):
    document_id: str
    original_text: str
    suggested_text: str


class Checker(BaseModel):
    content: str
