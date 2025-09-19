from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.router import router as auth_router
from src.pqrs.router import router as pqrs_router

app = FastAPI(
    title="Sistema Integrado - PQRS y Autenticación",
    description="API completa para autenticación de usuarios y gestión de PQRS",
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

# Rutas
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(pqrs_router, tags=["PQRS"])

@app.get("/")
def read_root():
    return {
        "message": "Sistema Integrado - PQRS y Autenticación",
        "version": "1.0.0",
        "status": "🚀 Funcionando correctamente"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}