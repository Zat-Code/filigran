from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017")
DB_NAME = os.getenv("DB_NAME", "filigran")

client = None
db = None

async def connect_to_mongo():
    global client, db
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DB_NAME]
        print(f"Successfully connected to MongoDB at {MONGO_URI}")
    except ConnectionFailure as e:
        print("Error connecting to MongoDB", e)

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Closed connection to MongoDB")