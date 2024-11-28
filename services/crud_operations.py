# services/crud_operations.py

from services.mongo_service import get_collection
from models.user_model import UserModel
from models.recurso_model import RecursoModel
from models.reserva_model import ReservaModel
from bson.objectid import ObjectId

# Usuarios
def create_usuario(user: UserModel):
    collection = get_collection("usuarios")
    result = collection.insert_one(user.dict())
    return str(result.inserted_id)

def leer_usuarios():
    collection = get_collection("usuarios")
    return list(collection.find())

def actualizar_usuario(user_id: str, user: UserModel):
    collection = get_collection("usuarios")
    collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})

def eliminar_usuario(user_id: str):
    collection = get_collection("usuarios")
    collection.delete_one({"_id": ObjectId(user_id)})

# Recursos
def create_recurso(recurso: RecursoModel):
    collection = get_collection("recursos")
    result = collection.insert_one(recurso.dict())
    return str(result.inserted_id)

def leer_recursos():
    collection = get_collection("recursos")
    return list(collection.find())

def actualizar_recurso(recurso_id: str, recurso: RecursoModel):
    collection = get_collection("recursos")
    collection.update_one({"_id": ObjectId(recurso_id)}, {"$set": recurso.dict()})

def eliminar_recurso(recurso_id: str):
    collection = get_collection("recursos")
    collection.delete_one({"_id": ObjectId(recurso_id)})

# Reservas
def create_reserva(reserva: ReservaModel):
    collection = get_collection("reservas")
    result = collection.insert_one(reserva.dict())
    return str(result.inserted_id)

def leer_reservas():
    collection = get_collection("reservas")
    return list(collection.find())

def actualizar_reserva(reserva_id: str, reserva: ReservaModel):
    collection = get_collection("reservas")
    collection.update_one({"_id": ObjectId(reserva_id)}, {"$set": reserva.dict()})

def eliminar_reserva(reserva_id: str):
    collection = get_collection("reservas")
    collection.delete_one({"_id": ObjectId(reserva_id)})
