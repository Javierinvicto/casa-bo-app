from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# --- Modelos de Datos (La estructura de tu información) ---
class Clase(BaseModel):
    id: int
    name: str
    instructor: str
    date: str
    time: str
    capacity: int
    booked: int

# --- Base de Datos de Ejemplo ---
# En un proyecto real, esto estaría en una base de datos como PostgreSQL o MySQL.
db = {
    "classes": [
        {"id": 1, "name": "bôldpilates", "instructor": "Sofía", "date": "2025-08-18", "time": "09:00", "capacity": 6, "booked": 2},
        {"id": 2, "name": "bôdysculpt", "instructor": "Lucía", "date": "2025-08-18", "time": "18:30", "capacity": 6, "booked": 5},
        {"id": 3, "name": "barrebôost", "instructor": "Elena", "date": "2025-08-19", "time": "09:00", "capacity": 6, "booked": 6},
    ]
}

app = FastAPI()

# --- IMPORTANTE: Configuración de CORS ---
# Esto permite que tu app (el frontend) pueda pedirle datos a tu servidor (el backend).
origins = ["*"] # Permite que cualquier web se conecte (ideal para empezar)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Rutas de la API (Las URLs que tu app usará para obtener datos) ---
@app.get("/clases", response_model=List[Clase])
async def get_clases():
    """Devuelve la lista de todas las clases."""
    return db["classes"]

@app.post("/clases/{class_id}/reservar")
async def reservar_clase(class_id: int):
    """Reserva una plaza en una clase."""
    clase = next((c for c in db["classes"] if c["id"] == class_id), None)
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    if clase["booked"] >= clase["capacity"]:
        raise HTTPException(status_code=400, detail="La clase está completa")
    
    clase["booked"] += 1
    return {"message": "Reserva confirmada", "clase": clase}

