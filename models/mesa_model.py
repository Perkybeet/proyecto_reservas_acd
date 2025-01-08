from pydantic import BaseModel

class MesaModel(BaseModel):
    numero_mesa: int = None
    capacidad: int = None
    ubicacion: str = None
