from datetime import timedelta
from services.mongo_service import get_collection
from models.user_model import UserModel
from models.mesa_model import MesaModel
from models.reserva_model import ReservaModel
from bson.objectid import ObjectId

# --- Usuarios ---
def insertar_usuario(user: UserModel):
    collection = get_collection("usuarios")
    result = collection.insert_one(user.model_dump())
    return str(result.inserted_id)

def leer_usuarios():
    collection = get_collection("usuarios")
    usuarios = list(collection.find())
    for usuario in usuarios:
        usuario["id"] = str(usuario["_id"])
    return usuarios

def actualizar_usuario(user_id: str, user: UserModel):
    collection = get_collection("usuarios")
    collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.model_dump()})

def eliminar_usuario(user_id: str):
    collection = get_collection("usuarios")
    collection.delete_one({"_id": ObjectId(user_id)})

# --- Mesas ---
def insertar_mesa(mesa: MesaModel):
    collection = get_collection("mesas")
    result = collection.insert_one(mesa.model_dump())
    return str(result.inserted_id)

def leer_mesas():
    collection = get_collection("mesas")
    mesas = list(collection.find())
    for mesa in mesas:
        mesa["id"] = str(mesa["_id"])
    return mesas

def actualizar_mesa(mesa_id: str, mesa: MesaModel):
    collection = get_collection("mesas")
    collection.update_one({"_id": ObjectId(mesa_id)}, {"$set": mesa.model_dump()})

def eliminar_mesa(mesa_id: str):
    collection = get_collection("mesas")
    collection.delete_one({"_id": ObjectId(mesa_id)})

# --- Reservas ---
def insertar_reserva(reserva: ReservaModel):
    collection = get_collection("reservas")
    
    # Definir el rango de tiempo para la validación
    rango = timedelta(hours=2)
    fecha_inicio = reserva.fecha_reserva - rango
    fecha_fin = reserva.fecha_reserva + rango
    
    # Buscar reservas superpuestas para diferentes personas en la misma mesa
    reserva_existente = collection.find_one({
        "mesa_id": reserva.mesa_id,
        "cliente_id": {"$ne": reserva.cliente_id},
        "fecha_reserva": {
            "$gte": fecha_inicio,
            "$lte": fecha_fin
        }
    })
    
    if reserva_existente:
        raise ValueError("Ya existe una reserva para esta mesa en este horario.")
    
    result = collection.insert_one(reserva.model_dump())
    return str(result.inserted_id)

def leer_reservas():
    collection = get_collection("reservas")
    reservas = list(collection.find())
    for reserva in reservas:
        reserva["id"] = str(reserva["_id"])
        reserva["fecha_reserva"] = str(reserva["fecha_reserva"])
    return reservas

def actualizar_reserva(reserva_id: str, reserva: ReservaModel):
    collection = get_collection("reservas")
    
    # Definir el rango de tiempo para la validación
    rango = timedelta(hours=2)
    fecha_inicio = reserva.fecha_reserva - rango
    fecha_fin = reserva.fecha_reserva + rango
    
    reserva_existente = collection.find_one({
        "mesa_id": reserva.mesa_id,
        "cliente_id": {"$ne": reserva.cliente_id},
        "fecha_reserva": {
            "$gte": fecha_inicio,
            "$lte": fecha_fin
        },
        "_id": {"$ne": ObjectId(reserva_id)}
    })
    
    if reserva_existente:
        raise ValueError("Ya existe una reserva para esta mesa en este horario.")
    
    collection.update_one({"_id": ObjectId(reserva_id)}, {"$set": reserva.model_dump()})

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
    return [{"id": usuario["id"], "nombre": usuario["nombre"], "email": usuario["email"]} for usuario in usuarios]