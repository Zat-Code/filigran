from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import json
import os
from services.associate_stix_with_pdfs import associate_stix_with_pdfs

# Créez un routeur pour les routes de comparaison
router = APIRouter()

# Répertoire contenant les fichiers PDF
PDF_DIRECTORY = "data/pdfs/"

@router.post("/")
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
        
        # Sauvegarder temporairement le fichier
        temp_file_path = "temp_stix.json"
        with open(temp_file_path, "w") as f:
            json.dump(stix_data, f)
        
        # Appeler le service avec le chemin du fichier
        matched_results = await associate_stix_with_pdfs(temp_file_path)
        
        # Nettoyer le fichier temporaire
        os.remove(temp_file_path)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors du traitement du fichier JSON: {str(e)}")
    
    # Vérifier si des correspondances ont été trouvées
    if not matched_results:
        raise HTTPException(status_code=400, detail="Aucune correspondance trouvée entre les malwares STIX et les fichiers PDF.")

    # Retourner les résultats
    return JSONResponse(content={"matches": matched_results})