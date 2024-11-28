from pydantic import BaseModel, EmailStr
from typing import Optional

class UserModel(BaseModel):
    nombre: str = None
    email: EmailStr = None
    telefono: str = None