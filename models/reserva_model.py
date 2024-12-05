from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

class ReservaModel(BaseModel):
    _id: str = None
    cliente_id: str = None
    mesa_id: str = None
    fecha_reserva: datetime = None
    estado: Optional[str] = "Pendiente"  # "Pendiente", "Confirmada", "Cancelada"
    notas: Optional[str] = None
