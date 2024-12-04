from pydantic import BaseModel

class MesaModel(BaseModel):
    _id: str = None
    numero_mesa: int = None
    capacidad: int = None
    ubicacion: str = None
