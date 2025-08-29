from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    categoria_id: int

class ProductoCreate(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id: int
    class Config:
        orm_mode = True
