from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    nombre: str = None
    telefono: str = None
    email: EmailStr = None
    direccion: str = None
