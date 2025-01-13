from datetime import datetime
from services.crud_operations import leer_mesas
import re

def validate_email(email: str):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Email no válido")

def validate_fecha(fecha: datetime):
    if fecha < datetime.now():
        raise ValueError("La fecha y hora de reserva no pueden estar en el pasado.")

def validate_telefono(telefono: str):
    if not re.match(r"^\+?\d{10,15}$", telefono):
        raise ValueError("Teléfono no válido")
    
def validate_nmesa(nmesa: str):
    mesas = leer_mesas()
    if nmesa in [str(m['numero_mesa']) for m in mesas]:
        raise Exception("Número de mesa no válido")
