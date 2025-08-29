from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from auth.router import router as auth_router

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Proyecto Integrador API - Juan Valencia",
    description="API para el proyecto integrador del grupo PAP-Tarde",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {
        "message": "Proyecto Integrador API - Juan Valencia Moreno",
        "identificacion": "1025761171",
        "grupo": "pap-tarde",
        "status": "funcionando"
    }