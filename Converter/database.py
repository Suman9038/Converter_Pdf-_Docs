from pymongo import MongoClient
from config import settings


client= MongoClient(settings.DB_URL)


db= client["Converting_db"]

users_collection= db["users"]

users_collection.create_index([("username",1)])

def get_users_collection() :
    yield users_collection

