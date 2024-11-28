from services.crud_operations import create_usuario
from models import user_model


# Creamos el objeto usuario heredando de user_model y le asignamos los datos que requiera dicho modelo
usuario = user_model(
    nombre = "Yago",
    email = "yago@gmail.com",
    etc=...
)


# Guardamos la respuesta de create_usuario
response = create_usuario(usuario)