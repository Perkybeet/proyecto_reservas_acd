from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

class ReservaModel(BaseModel):
    usuario_id: str  # Almacenar como cadena para simplificar
    recurso_id: str  # Almacenar como cadena para simplificar
    fecha_reserva: datetime
    estado: Optional[str] = "Pendiente"  # "Pendiente", "Confirmada", "Cancelada"
