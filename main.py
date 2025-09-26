from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.pqrs.router import router as pqrs_router
from src.chatbot.router import router as chatbot_router

app = FastAPI(title="Sistema PQRS con Chatbot")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 en producción cámbialo por tu frontend, ej: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)
app.include_router(pqrs_router)
app.include_router(chatbot_router)

@app.get("/")
async def root():
    return {"message": "Bienvenido al sistema PQRS con Chatbot 🤖"}
