# models/reserva_model.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReservaModel(BaseModel):
    usuario_id: str  # Referencia al ID del usuario
    recurso_id: str  # Referencia al ID del recurso
    fecha_reserva: datetime
    estado: Optional[str] = "Pendiente"  # Puede ser "Pendiente", "Confirmada", "Cancelada"
