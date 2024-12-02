# services.py
from business_logic.stix_extractor import StixExtractor
from rapidfuzz import fuzz, process
from db.services.pdf_object import get_all_pdf_objects
from db.models.pdf_object import PDFObject 


async def associate_stix_with_pdfs(stix_file_path):
    # Extraire les malwares du fichier STIX
    stix_extractor = StixExtractor()
    stix_malwares = stix_extractor.extract(stix_file_path)

    # Récupérer tous les objets PDF depuis la base de données
    pdf_objects = await get_all_pdf_objects()

    # Associer les malwares STIX avec les malwares extraits des PDFs
    matched_results = []
    for pdf_object_data in pdf_objects:
        # Convertir l'objet de base de données en Pydantic pour valider et traiter les données
        pdf_obj = PDFObject(**pdf_object_data)  # Utilisation de Pydantic pour la validation

        pdf_malwares = [malware["entity"] for malware in pdf_obj.malwares]  # Liste des malwares dans ce PDF
        
        # Recherche floue pour associer les malwares STIX aux malwares PDF
        fuzzy_matches = reconcile_fuzzy(stix_malwares, pdf_malwares)
        if fuzzy_matches:
            matched_results.append({
                "pdf_file": pdf_obj.file_name,
                "matches": fuzzy_matches
            })

    return matched_results

def reconcile_fuzzy(stix_malwares, pdf_malwares, threshold=80):
    matched = []
    for stix_malware in stix_malwares:
        result = process.extractOne(stix_malware, pdf_malwares, scorer=fuzz.token_set_ratio)
        if result:
            match, score, index = result
            if score >= threshold:
                matched.append((stix_malware, match, score))
    return matched