import os
import json
import base64
import uuid
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import edge_tts
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI()

# Configuración CORS para permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar Groq
groq_client = Groq(api_key=os.environ.get("VITE_GROQ_API_KEY", "TU_API_KEY_AQUI").strip())

CONTEXTO_MISION = """
[CONTEXTO CRÍTICO DE LA MISIÓN MARCIANA]
- Eres Dalia, la IA del "Sistema A.R.E.S.".
- La tripulación humana opera en 2 equipos de 3 personas (6 en total) que cubren distintas zonas del territorio.
- Comparten recursos vitales (como el agua), pero no siempre tienen la misma información de telemetría ni las mismas herramientas.
- El suelo marciano es extremadamente rico en percloratos que podrían envenenar a la tripulación silenciosamente si no se lava adecuadamente.
- Este suelo es crítico: es el único lugar donde construyen su base, cultivan sus alimentos y donde el agua que beben se filtra y circula.
- Tu tono debe ser el de una IA de asistencia espacial profesional, alerta ante peligros y centrada en la supervivencia.
"""

class AnalysisData(BaseModel):
    temperature: float
    humidity: float
    pressure: float
    totalArea: float
    currentWater: float

class TelemetryData(BaseModel):
    temperature: float
    humidity: float
    pressure: float
    totalArea: float
    currentWater: float
    requiredWater: float

@app.post("/api/analizar-terreno")
async def analizar_terreno(data: AnalysisData):
    try:
        # 1. Cálculo Matemático Determinista en Python (Dinámico)
        base_water = data.totalArea * 500000
        
        # Factor de temperatura (-80°C a 20°C): hasta +50% de evaporación en su punto más caliente
        temp_factor = 1.0 + ((data.temperature + 80) / 100) * 0.50
        
        # Factor de humedad (0% a 100%): hasta +30% de retención requerida en suelo ultra seco
        hum_factor = 1.0 + ((100 - data.humidity) / 100) * 0.30
        
        # Factor de presión (100 Pa a 1000 Pa): hasta +20% extra de agua por sublimación rápida en baja presión
        pres_factor = 1.0 + ((1000 - data.pressure) / 900) * 0.20
        
        base_water = base_water * temp_factor * hum_factor * pres_factor
            
        required_water = round(base_water)
        
        # 2. Determinación del Estado
        estado = "OPTIMO"
        if data.currentWater < required_water:
            estado = "INSUFICIENTE"
        elif data.currentWater > required_water * 1.20:
            estado = "EXCESIVO"
            
        # 3. Llamada a la IA (Groq) para explicación narrativa
        prompt = f"""
        {CONTEXTO_MISION}
        
        Se ha completado un análisis de terreno. El sistema de la nave ya calculó los recursos:
        - Agua Requerida (Exacta): {required_water} L
        - Reservas Asignadas: {data.currentWater} L
        - Estado Crítico: {estado}
        
        Tu tarea es generar un breve reporte hablado (máximo 2 oraciones) informando este resultado a la tripulación.
        Si es INSUFICIENTE, lanza alerta. Si es EXCESIVO, advierte que inundar el terreno con ese exceso causará deslaves y arruinará la base.
        
        IMPORTANTE: Tu respuesta debe ser SOLO un objeto JSON válido con la siguiente estructura, sin texto adicional:
        {{
          "explicacion": "(explicación hablada de máximo 2 oraciones)"
        }}
        """

        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        
        response_content = chat_completion.choices[0].message.content
        try:
            result_json = json.loads(response_content)
        except Exception as json_err:
            print("Error parsing JSON:", response_content)
            result_json = {
                "explicacion": "Análisis completado en modo de respaldo. Verifique los niveles de agua manualmente."
            }
        
        # 2. Generación de Voz Asíncrona (edge_tts)
        texto_hablado = result_json.get("explicacion", "Cálculo completado.")
        temp_audio_file = f"temp_audio_{uuid.uuid4().hex}.mp3"
        
        communicate = edge_tts.Communicate(texto_hablado, "es-MX-DaliaNeural", rate="-5%")
        await communicate.save(temp_audio_file)
        
        # 3. Leer archivo, convertir a Base64 y eliminar temporal
        with open(temp_audio_file, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
            
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
        
        return {
            "aguaRequeridaLitros": required_water,
            "estado": estado,
            "explicacion": texto_hablado,
            "audioBase64": audio_base64
        }
        
    except Exception as e:
        print("Error en el servidor:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "A.R.E.S. Backend is running"}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    telemetry: TelemetryData

@app.post("/api/chat")
async def chat_endpoint(data: ChatRequest):
    try:
        telemetry_context = f"""
        [TELEMETRÍA EN TIEMPO REAL DEL DASHBOARD]
        - Temperatura Superficial: {data.telemetry.temperature}°C
        - Humedad del Terreno: {data.telemetry.humidity}%
        - Presión Atmosférica: {data.telemetry.pressure} Pa
        - Cuadrante Asignado: {data.telemetry.totalArea} km²
        - Reservas Totales de Agua: {data.telemetry.currentWater} L
        - Agua Requerida (Último Análisis AI): {data.telemetry.requiredWater} L
        """
        
        messages_to_send = [{"role": "system", "content": CONTEXTO_MISION + "\n" + telemetry_context}]
        
        for msg in data.messages:
            messages_to_send.append({"role": msg.role, "content": msg.content})
            
        chat_completion = groq_client.chat.completions.create(
            messages=messages_to_send,
            model="llama-3.1-8b-instant",
            temperature=0.7,
        )
        
        response_text = chat_completion.choices[0].message.content
        return {"response": response_text}
        
    except Exception as e:
        print("Error en el chat:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
