from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@mongodb:27017")
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

async def get_db(retries=5, delay_ms=500):
    """
    Récupère l'objet `db`, avec plusieurs tentatives si la connexion n'est pas établie.

    Args:
        retries (int): Nombre maximal de tentatives.
        delay_ms (int): Délai entre les tentatives en millisecondes.

    Returns:
        db: L'objet MongoDB connecté.

    Raises:
        RuntimeError: Si toutes les tentatives échouent.
    """
    global db

    for attempt in range(1, retries + 1):
        if db:
            return db  # Retourne immédiatement si la connexion est active
        try:
            await connect_to_mongo()
            return db
        except ConnectionFailure as e:
            print(f"Attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                await asyncio.sleep(delay_ms / 1000)  # Délai avant une nouvelle tentative
            else:
                raise RuntimeError(
                    f"Failed to connect to MongoDB after {retries} attempts."
                ) from e