from services.mongo_service import get_collection
from models.user_model import UserModel
from models.mesa_model import MesaModel
from models.reserva_model import ReservaModel
from bson.objectid import ObjectId

def create_usuario(user: UserModel):
    collection = get_collection("usuarios")
    result = collection.insert_one(user.model_dump())
    return str(result.inserted_id)

def leer_usuarios():
    collection = get_collection("usuarios")
    return list(collection.find())

def actualizar_usuario(user_id: str, user: UserModel):
    collection = get_collection("usuarios")
    collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.model_dump()})

def eliminar_usuario(user_id: str):
    collection = get_collection("usuarios")
    collection.delete_one({"_id": ObjectId(user_id)})

# Mesas
def create_mesa(mesa: MesaModel):
    collection = get_collection("mesas")
    result = collection.insert_one(mesa.model_dump())
    return str(result.inserted_id)

def leer_mesas():
    collection = get_collection("mesas")
    return list(collection.find())

def actualizar_mesa(mesa_id: str, mesa: MesaModel):
    collection = get_collection("mesas")
    collection.update_one({"_id": ObjectId(mesa_id)}, {"$set": mesa.model_dump()})

def eliminar_mesa(mesa_id: str):
    collection = get_collection("mesas")
    collection.delete_one({"_id": ObjectId(mesa_id)})

# Reservas
def create_reserva(reserva: ReservaModel):
    collection = get_collection("reservas")
    # Convertir a diccionario y asegurar que las IDs son cadenas
    reserva_model_dump = reserva.model_dump()
    collection.insert_one(reserva_model_dump)
    return True

def leer_reservas():
    collection = get_collection("reservas")
    reservas = list(collection.find())
    # Convertir ObjectId a cadena para facilitar el manejo en la UI
    for reserva in reservas:
        reserva["_id"] = str(reserva["_id"])
    return reservas

def actualizar_reserva(reserva_id: str, reserva: ReservaModel):
    collection = get_collection("reservas")
    # Convertir a diccionario y asegurar que las IDs son cadenas
    reserva_model_dump = reserva.model_dump()
    collection.update_one({"_id": ObjectId(reserva_id)}, {"$set": reserva_model_dump})

def eliminar_reserva(reserva_id: str):
    collection = get_collection("reservas")
    collection.delete_one({"_id": ObjectId(reserva_id)})