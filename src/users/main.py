from fastapi import FastAPI
from core.database import Base, engine
from auth.router import router as auth_router

app = FastAPI(title="Proyecto Integrador API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
