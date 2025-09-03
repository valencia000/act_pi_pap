from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.router import router as auth_router
from src.database import Base, engine

# Crear tablas en DB
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Proyecto Integrador API",
    description="API para el registro de personas",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas Auth
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido al Proyecto Integrador API",
        "version": "1.0.0",
        "author": "Juan Valencia, Esneyder Vasquez, Luis Fernando Zuluaga",
        "grupo": "pap-tarde"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
