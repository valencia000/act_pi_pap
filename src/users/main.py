# main.py

from fastapi import FastAPI, HTTPException
from models import Tarea, TareaCreate
import database as db

app = FastAPI()

@app.get("/tareas", response_model=list[Tarea])
def listar_tareas():
    return db.get_all()

@app.get("/tareas/{tarea_id}", response_model=Tarea)
def obtener_tarea(tarea_id: int):
    tarea = db.get_by_id(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.post("/tareas", response_model=Tarea, status_code=201)
def crear_tarea(tarea: TareaCreate):
    return db.create(tarea.titulo)

@app.put("/tareas/{tarea_id}", response_model=Tarea)
def actualizar_tarea(tarea_id: int, tarea: TareaCreate):
    tarea_actualizada = db.update(tarea_id, {"titulo": tarea.titulo})
    if not tarea_actualizada:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea_actualizada

@app.delete("/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int):
    if not db.get_by_id(tarea_id):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea_id)
