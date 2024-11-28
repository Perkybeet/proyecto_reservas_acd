# models/recurso_model.py

from pydantic import BaseModel

class RecursoModel(BaseModel):
    nombre: str
    descripcion: str
    disponibilidad: bool
