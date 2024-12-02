
from db.database import db
from models.pdf_object import PDFObject
from pymongo import ReturnDocument


COLLECTION_NAME = "pdf_objects"

async def add_pdf_object(pdf_object: PDFObject):
    """
    Ajouter un objet PDF à la base de données
    """
    result = await db[COLLECTION_NAME].insert_one(pdf_object.dict())
    return str(result.inserted_id)

async def get_pdf_object(pdf_object_id: str):
    """
    Récupérer un objet PDF
    """
    pdf_object = await db[COLLECTION_NAME].find_one({"_id": pdf_object_id})
    return pdf_object

async def get_all_pdf_objects():
    """
    Récupérer tous les objets PDF
    """
    pdf_objects = await db[COLLECTION_NAME].find().to_list()
    return pdf_objects

async def update_pdf_object(pdf_object_id: str, update_data: dict):
    """
    Mettre à jour un objet PDF existant
    """
    updated_pdf_object = await db[COLLECTION_NAME].find_one_and_update(
        {"_id": pdf_object_id},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )
    return updated_pdf_object

async def delete_pdf_object(pdf_object_id: str):
    """
    Supprimer un objet PDF
    """
    deleted_pdf_object = await db[COLLECTION_NAME].delete_one({"_id": pdf_object_id})    
    return deleted_pdf_object

