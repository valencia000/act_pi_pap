# models.py

from pydantic import BaseModel

class Tarea(BaseModel):
    id: int
    titulo: str
    completado: bool = False

class TareaCreate(BaseModel):
    titulo: str
