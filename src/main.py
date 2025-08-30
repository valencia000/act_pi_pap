from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.router import router as auth_router
from src.auth.router import router as auth_router  # ← Cambié la importación

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Proyecto Integrador API",
    description="API para el proyecto integrador de Juan Valencia",
    version="1.0.0"
)

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido al Proyecto Integrador API",
        "version": "1.0.0",
        "author": "Juan Valencia Moreno",
        "grupo": "pap-tarde"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
