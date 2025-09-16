from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from src.database import get_db
from src.models import PQRS

router = APIRouter(prefix="/pqrs", tags=["PQRS"])

# Schemas
class PQRSCreate(BaseModel):
    nombre_usuario: str
    email: EmailStr
    tipo: str
    mensaje: str

class PQRSOut(BaseModel):
    id: int
    nombre_usuario: str
    email: str
    tipo: str
    mensaje: str
    fecha: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=PQRSOut, status_code=status.HTTP_201_CREATED)
def crear_pqrs(pqrs: PQRSCreate, db: Session = Depends(get_db)):
    db_pqrs = PQRS(**pqrs.dict())
    db.add(db_pqrs)
    db.commit()
    db.refresh(db_pqrs)
    return db_pqrs

@router.get("/", response_model=List[PQRSOut])
def listar_pqrs(db: Session = Depends(get_db)):
    return db.query(PQRS).order_by(PQRS.fecha.desc()).all()

@router.get("/{pqrs_id}", response_model=PQRSOut)
def obtener_pqrs(pqrs_id: int, db: Session = Depends(get_db)):
    pqrs = db.query(PQRS).filter(PQRS.id == pqrs_id).first()
    if pqrs is None:
        raise HTTPException(status_code=404, detail="PQRS no encontrada")
    return pqrs

@router.put("/{pqrs_id}", response_model=PQRSOut)
def actualizar_pqrs(pqrs_id: int, pqrs_update: PQRSCreate, db: Session = Depends(get_db)):
    pqrs = db.query(PQRS).filter(PQRS.id == pqrs_id).first()
    if pqrs is None:
        raise HTTPException(status_code=404, detail="PQRS no encontrada")
    
    for field, value in pqrs_update.dict().items():
        setattr(pqrs, field, value)
    
    db.commit()
    db.refresh(pqrs)
    return pqrs

@router.delete("/{pqrs_id}")
def eliminar_pqrs(pqrs_id: int, db: Session = Depends(get_db)):
    pqrs = db.query(PQRS).filter(PQRS.id == pqrs_id).first()
    if pqrs is None:
        raise HTTPException(status_code=404, detail="PQRS no encontrada")
    
    db.delete(pqrs)
    db.commit()
    return {"message": "PQRS eliminada correctamente"}