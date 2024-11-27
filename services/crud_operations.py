import pymongo
from mongo_service import get_db
def insertarDatos():
    db = get_db()
    coleccion = db["clientes"]
    resultado = coleccion.insertOne({
        "_id": "cliente001",
        "nombre": "John Doe",
        "telefono": "1234567890",
        "email": "johndoe@example.com",
        "direccion": "Calle mayor, 45, Madrid"
    })
    print(resultado)
def leerDatos():
    pass
def actualizarDatos():
    pass
def eliminarDatos():
    pass

insertarDatos()