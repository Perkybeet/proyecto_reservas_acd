# /services/crud_operations.py
from services.mongo_service import get_collection
from models.user_model import UserModel
from models.mesa_model import MesaModel
from models.reserva_model import ReservaModel
from bson.objectid import ObjectId

# --- Funciones CRUD para Usuarios ---
def insertar_usuario(user: UserModel):
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

# --- Funciones CRUD para Mesas ---
def insertar_mesa(mesa: MesaModel):
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

# --- Funciones CRUD para Reservas ---
def insertar_reserva(reserva: ReservaModel):
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
        reserva["fecha_reserva"] = str(reserva["fecha_reserva"]).split()[0]
    return reservas

def actualizar_reserva(reserva_id: str, reserva: ReservaModel):
    collection = get_collection("reservas")
    # Convertir a diccionario y asegurar que las IDs son cadenas
    reserva_model_dump = reserva.model_dump()
    collection.update_one({"_id": ObjectId(reserva_id)}, {"$set": reserva_model_dump})

def eliminar_reserva(reserva_id: str):
    collection = get_collection("reservas")
    collection.delete_one({"_id": ObjectId(reserva_id)})

# --- Funciones de Conteo ---
def contar_usuarios():
    collection = get_collection("usuarios")
    return collection.count_documents({})

def contar_mesas():
    collection = get_collection("mesas")
    return collection.count_documents({})

def contar_reservas():
    collection = get_collection("reservas")
    return collection.count_documents({})

def obtener_usuarios_para_dropdown():
    usuarios = leer_usuarios()
    return [{"id": usuario["_id"], "nombre": usuario["nombre"], "email": usuario["email"]} for usuario in usuarios]