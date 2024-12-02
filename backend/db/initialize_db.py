from db.database import db

COLLECTION_NAME = "pdf_objects"

async def initialize_collection():
    """
    Crée la collection si elle n'existe pas encore et applique des index si nécessaire.
    """
    if COLLECTION_NAME not in await db.list_collection_names():
        print(f"Création de la collection : {COLLECTION_NAME}")
        await db.create_collection(COLLECTION_NAME)
    
    # Exemple : création d'un index unique sur le chemin du fichier
    await db[COLLECTION_NAME].create_index("file_path", unique=True)