from pydantic import BaseModel, EmailStr
from typing import Optional

class UserModel(BaseModel):
    id: str = None
    nombre: str = None
    telefono: str = None
    email: EmailStr = None
    direccion: str = None
