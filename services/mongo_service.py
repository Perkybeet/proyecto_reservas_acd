from pymongo import MongoCLient

def get_db():
    cliente = MongoCLient("localhost:27017")
    db = cliente["Reservas"]