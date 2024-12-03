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
        pdf_obj = PDFObject(**pdf_object_data)

        # Passer le texte extrait à reconcile_fuzzy
        fuzzy_matches = reconcile_fuzzy(
            stix_malwares, 
            pdf_obj.malwares, 
            extracted_text=pdf_obj.extracted_text
        )
        
        if fuzzy_matches:
            matched_results.append({
                "pdf_file": pdf_obj.file_name,
                "extracted_text": pdf_obj.extracted_text,
                "matches": fuzzy_matches
            })

    return matched_results

def reconcile_fuzzy(stix_malwares, pdf_malwares, extracted_text="", threshold=80):
    matched = []
    for stix_malware in stix_malwares:
        # Stocker toutes les positions pour ce malware STIX
        all_locations = []
        
        for pdf_malware in pdf_malwares:
            # Normaliser les chaînes avant la comparaison
            stix_norm = stix_malware.lower().strip()
            pdf_norm = pdf_malware["entity"].lower().strip()
            
            score = fuzz.token_set_ratio(stix_norm, pdf_norm)
            
            if score >= threshold:
                text = extracted_text
                text_lower = text.lower()
                start = 0
                
                while True:
                    index = text_lower.find(pdf_norm, start)
                    if index == -1:
                        break
                    
                    # Ajouter la position avec la longueur du texte trouvé
                    all_locations.append({
                        'start': index,
                        'end': index + len(pdf_norm),
                        'text': text[index:index + len(pdf_norm)],
                        'score': score
                    })
                    start = index + 1
        
        if all_locations:
            # Trier les positions par début
            all_locations.sort(key=lambda x: x['start'])
            
            # Fusionner les positions qui se chevauchent
            merged_locations = []
            current = all_locations[0]
            
            for next_loc in all_locations[1:]:
                if next_loc['start'] <= current['end']:
                    # Chevauchement : prendre la plus longue correspondance
                    if next_loc['end'] > current['end']:
                        current['end'] = next_loc['end']
                        current['text'] = extracted_text[current['start']:current['end']]
                    # Garder le meilleur score
                    current['score'] = max(current['score'], next_loc['score'])
                else:
                    merged_locations.append([current['start'], current['end']])
                    current = next_loc
            
            merged_locations.append([current['start'], current['end']])
            
            matched.append({
                "stix_malware": stix_malware,
                "pdf_malware": stix_malware,  # Utiliser le malware STIX comme référence
                "score": max(loc['score'] for loc in all_locations),
                "locations": merged_locations
            })
    
    return matched