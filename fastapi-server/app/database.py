from pymongo import MongoClient
from app.config import settings

class Database:
    client: MongoClient = None
    db = None

db_manager = Database()

async def connect_to_mongo():
    db_manager.client = MongoClient(settings.mongo_url)
    db_manager.client.admin.command('ping')
    db_manager.db = db_manager.client.get_database()
    print("✅ MongoDB connected")

async def close_mongo_connection():
    if db_manager.client:
        db_manager.client.close()

def get_db():
    return db_manager.db
