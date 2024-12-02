from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import json
import os
from services.associate_stix_with_pdfs import associate_stix_with_pdfs

# Créez un routeur pour les routes de comparaison
router = APIRouter()

# Répertoire contenant les fichiers PDF
PDF_DIRECTORY = "data/pdfs/"

@router.post("/aggregator")
async def compare_stix_with_pdfs(file: UploadFile = File(...)):
    """
    Endpoint permettant de comparer un fichier STIX JSON uploadé à une base de fichiers PDF.
    """
    # Vérification du type de fichier
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers JSON sont acceptés.")

    # Lire le fichier STIX JSON
    try:
        content = await file.read()
        stix_data = json.loads(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Erreur lors de la lecture du fichier JSON.")
    
    # Appeler le service associate_stix_with_pdfs
    matched_results = await associate_stix_with_pdfs(stix_data)

    # Vérifier si des correspondances ont été trouvées
    if not matched_results:
        raise HTTPException(status_code=400, detail="Aucune correspondance trouvée entre les malwares STIX et les fichiers PDF.")

    # Retourner les résultats
    return JSONResponse(content={"matches": matched_results})