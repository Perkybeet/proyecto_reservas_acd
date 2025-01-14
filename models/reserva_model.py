from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReservaModel(BaseModel):
    cliente_id: str = None
    mesa_id: str = None
    fecha_reserva: datetime = None
    estado: Optional[str] = "Pendiente"  # "Pendiente", "Confirmada", "Cancelada"
    notas: Optional[str] = None
