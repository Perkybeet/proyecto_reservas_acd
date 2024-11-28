from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReservaModel(BaseModel):
    usuario_id: str
    recurso_id: str
    fecha_reserva: datetime
    estado: Optional[str] = "Pendiente"