from pydantic import BaseModel
from typing import List

class OrdenCreate(BaseModel):
    producto_ids: List[int]
    usuario_id: int

class OrdenOut(BaseModel):
    id: int
    usuario_id: int
    producto_ids: List[int]
    class Config:
        orm_mode = True
