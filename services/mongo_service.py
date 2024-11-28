# services/mongo_service.py

from pymongo import MongoClient
from utils.config import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

def get_collection(collection_name: str):
    return db[collection_name]
