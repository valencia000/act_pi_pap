from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from core.database import Base

# Tabla intermedia
orden_producto = Table(
    "orden_producto",
    Base.metadata,
    Column("orden_id", Integer, ForeignKey("ordenes.id")),
    Column("producto_id", Integer, ForeignKey("productos.id"))
)

class Orden(Base):
    __tablename__ = "ordenes"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"))
    productos = relationship("Producto", secondary=orden_producto)
