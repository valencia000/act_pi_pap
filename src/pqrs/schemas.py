from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PQRSCreate(BaseModel):
    nombre_usuario: str
    email: EmailStr
    tipo: str
    mensaje: str

class PQRSUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    tipo: Optional[str] = None
    mensaje: Optional[str] = None

class PQRSOut(BaseModel):
    id: int
    nombre_usuario: str
    email: str
    tipo: str
    mensaje: str
    fecha: datetime
    
    class Config:
        from_attributes = True