# models/user_model.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserModel(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str
    # Puedes agregar más campos según sea necesario
