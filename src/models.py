from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from src.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(String, nullable=False)

class PQRS(Base):
    __tablename__ = "pqrs"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)
    mensaje = Column(Text, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())