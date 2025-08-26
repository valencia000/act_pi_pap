# database.py

tareas = [
    {"id": 1, "titulo": "Aprender FastAPI", "completado": False},
    {"id": 2, "titulo": "Probar API en Postman", "completado": False}
]

def get_all():
    return tareas

def get_by_id(tarea_id: int):
    return next((t for t in tareas if t["id"] == tarea_id), None)

def create(titulo: str):
    nueva = {"id": len(tareas) + 1, "titulo": titulo, "completado": False}
    tareas.append(nueva)
    return nueva

def update(tarea_id: int, data: dict):
    tarea = get_by_id(tarea_id)
    if tarea:
        tarea.update(data)
    return tarea

def delete(tarea_id: int):
    global tareas
    tareas = [t for t in tareas if t["id"] != tarea_id]
