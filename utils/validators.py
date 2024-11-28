# utils/validators.py

import re

def validate_email(email: str):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Email no válido")

def validate_fecha(fecha: str):
    if not re.match(r"\d{4}-\d{2}-\d{2}", fecha):
        raise ValueError("Fecha debe tener el formato YYYY-MM-DD")

def validate_telefono(telefono: str):
    if not re.match(r"^\+?\d{10,15}$", telefono):
        raise ValueError("Teléfono no válido")
