from pymongo import MongoClient

def get_db():
    cliente = MongoClient("localhost:27017")
    db = cliente["Reservas"]
    return db