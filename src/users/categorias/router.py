from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from .models import Categoria
from .schemas import CategoriaCreate, CategoriaOut

router = APIRouter(prefix="/categorias", tags=["Categorías"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategoriaOut)
def crear_categoria(cat: CategoriaCreate, db: Session = Depends(get_db)):
    db_cat = Categoria(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@router.get("/", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()
