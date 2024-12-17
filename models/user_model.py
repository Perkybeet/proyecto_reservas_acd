from pydantic import BaseModel, EmailStr
from typing import Optional

class UserModel(BaseModel):
    nombre: str = None
    telefono: str = None
    email: EmailStr = None
    direccion: str = None
