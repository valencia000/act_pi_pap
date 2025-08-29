from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from productos.models import Producto
from .models import Orden
from .schemas import OrdenCreate, OrdenOut

router = APIRouter(prefix="/ordenes", tags=["Órdenes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OrdenOut)
def crear_orden(data: OrdenCreate, db: Session = Depends(get_db)):
    productos = db.query(Producto).filter(Producto.id.in_(data.producto_ids)).all()
    nueva_orden = Orden(usuario_id=data.usuario_id, productos=productos)
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)
    return {
        "id": nueva_orden.id,
        "usuario_id": nueva_orden.usuario_id,
        "producto_ids": [p.id for p in productos]
    }

@router.get("/", response_model=list[OrdenOut])
def listar_ordenes(db: Session = Depends(get_db)):
    ordenes = db.query(Orden).all()
    result = []
    for o in ordenes:
        result.append({
            "id": o.id,
            "usuario_id": o.usuario_id,
            "producto_ids": [p.id for p in o.productos]
        })
    return result
