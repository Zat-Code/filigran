from fastapi import APIRouter, File, UploadFile, HTTPException
from business_logic.strix_extrator import StixExtractor
from business_logic.pdf_extractor import PdfExtractor
from fastapi.responses import JSONResponse
import json
import os


# Créez un routeur pour les routes de comparaison
router = APIRouter()

# Initialisez les extracteurs
pdf_extractor = PdfExtractor()
stix_extractor = StixExtractor()

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
    
    # Extraire les malwares du fichier STIX
    stix_malwares = stix_extractor.extract_from_content(stix_data)

    if not stix_malwares:
        raise HTTPException(status_code=400, detail="Aucun malware trouvé dans le fichier STIX.")

    # Comparer avec tous les fichiers PDF
    results = []
    for pdf_file in os.listdir(PDF_DIRECTORY):
        pdf_path = os.path.join(PDF_DIRECTORY, pdf_file)
        pdf_text = pdf_extractor.extract_text_from_pdf(pdf_path)
        pdf_malwares = pdf_extractor.predict(pdf_text)

        # Comparaison des malwares
        common_malwares = set(m['entity'] for m in pdf_malwares).intersection(stix_malwares)
        results.append({
            "pdf_file": pdf_file,
            "common_malwares": list(common_malwares)
        })

    return JSONResponse(content={"results": results})