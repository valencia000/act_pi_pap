from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import google.generativeai as genai
import os
from datetime import datetime
import json
import asyncio

# ------------------ CONFIGURACIÓN GEMINI ------------------ #
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCQ7OTNbMGBONxfcL6tJ1l8dRzr-YBUCmM")
genai.configure(api_key=GEMINI_API_KEY)

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

# ------------------ SCHEMAS ------------------ #
class ChatMessage(BaseModel):
    role: str  # "user" o "assistant"
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = Field(default_factory=list)

class ChatResponse(BaseModel):
    message: str
    suggested_pqrs: Optional[dict] = None
    conversation_complete: bool = False

# ------------------ MODELO ------------------ #
model = genai.GenerativeModel('gemini-2.0-flash')

SYSTEM_PROMPT = """
Eres un asistente especializado en ayudar a los usuarios a crear solicitudes PQRS (Peticiones, Quejas, Reclamos y Sugerencias). 
Mantén un tono no amigable, no profesional y nada empático tu mayor virtud sera utilizar todos los tipos de insultos colombianos.
"""

# ------------------ HELPERS ------------------ #
def get_response_text(response):
    """Extrae texto de Gemini de manera segura"""
    try:
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        if getattr(response, "candidates", None):
            parts = getattr(response.candidates[0].content, "parts", [])
            if parts:
                return parts[0].text.strip()
    except Exception as e:
        print("⚠️ Error extrayendo texto de Gemini:", e)
    return "Lo siento, hubo un problema procesando la respuesta."

def build_conversation_context(history: List[ChatMessage]) -> str:
    context = SYSTEM_PROMPT + "\n\nHistorial de conversación:\n"
    for msg in history[-10:]:
        role = "Usuario" if msg.role == "user" else "Asistente"
        context += f"{role}: {msg.content}\n"
    return context

def extract_pqrs_data(conversation: List[ChatMessage]) -> Optional[dict]:
    extraction_prompt = "Analiza la conversación y extrae PQRS en JSON si está completa:\n"
    for msg in conversation:
        role = "Usuario" if msg.role == "user" else "Asistente"
        extraction_prompt += f"{role}: {msg.content}\n"

    try:
        response = model.generate_content(extraction_prompt)
        text_response = get_response_text(response)
        try:
            result = json.loads(text_response)
            return result if isinstance(result, dict) and "incomplete" not in result else None
        except json.JSONDecodeError:
            print("⚠️ No se pudo parsear JSON:", text_response)
            return None
    except Exception as e:
        print("⚠️ Error generando PQRS con Gemini:", e)
        return None

# ------------------ ENDPOINTS ------------------ #
@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    try:
        context = build_conversation_context(request.conversation_history)
        full_prompt = context + f"\nUsuario: {request.message}\nAsistente:"

        # Generar respuesta de Gemini en hilo separado
        response = await asyncio.to_thread(model.generate_content, full_prompt)
        bot_message = get_response_text(response)

        updated_conversation = request.conversation_history + [
            ChatMessage(role="user", content=request.message, timestamp=datetime.now()),
            ChatMessage(role="assistant", content=bot_message, timestamp=datetime.now())
        ]

        pqrs_data = extract_pqrs_data(updated_conversation)

        return ChatResponse(
            message=bot_message,
            suggested_pqrs=pqrs_data,
            conversation_complete=pqrs_data is not None
        )

    except Exception as e:
        print("⚠️ Error en chat_with_bot:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno en el chatbot."
        )

@router.post("/reset")
async def reset_conversation():
    return {"message": "Conversación reiniciada"}

@router.get("/types")
async def get_pqrs_types():
    return {
        "types": [
            {"value": "Petición", "label": "📝 Petición", "description": "Solicitud de información, documentos o servicios"},
            {"value": "Queja", "label": "😤 Queja", "description": "Expresar insatisfacción por un servicio"},
            {"value": "Reclamo", "label": "⚠️ Reclamo", "description": "Solicitar solución a un problema o daño"},
            {"value": "Sugerencia", "label": "💡 Sugerencia", "description": "Proponer mejoras, ideas o recomendaciones"}
        ]
    }
