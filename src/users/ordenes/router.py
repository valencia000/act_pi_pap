from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from .models import Producto
from .schemas import ProductoCreate, ProductoOut

router = APIRouter(prefix="/productos", tags=["Productos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductoOut)
def crear_producto(prod: ProductoCreate, db: Session = Depends(get_db)):
    db_prod = Producto(**prod.dict())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@router.get("/", response_model=list[ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()
