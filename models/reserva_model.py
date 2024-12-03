from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

class ReservaModel(BaseModel):
    cliente_id: int = None
    mesa_id: int = None
    fecha_hora: datetime = None
    estado: Optional[str] = "Pendiente"  # "Pendiente", "Confirmada", "Cancelada"
    notas: Optional[str] = None
