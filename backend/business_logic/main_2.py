from strix_extrator import StixExtractor
from pdf_extractor import PdfExtractor
from rapidfuzz import fuzz, process
import os


def associate_files(stix_folder, pdf_folder):
    # Lister les fichiers dans les deux dossiers
    stix_files = sorted(os.listdir(stix_folder))  # Liste des fichiers dans stix_bundles
    pdf_files = sorted(os.listdir(pdf_folder))  # Liste des fichiers dans pdfs

    # Vérifier que les dossiers contiennent le même nombre de fichiers
    if len(stix_files) != len(pdf_files):
        print(f"Le nombre de fichiers dans {stix_folder} et {pdf_folder} ne correspond pas.")
        return

    # Associer les fichiers en utilisant les indices
    file_pairs = []
    for i in range(len(stix_files)):
        stix_file = stix_files[i]
        pdf_file = pdf_files[i]

        # Construire les chemins complets des fichiers
        stix_path = os.path.join(stix_folder, stix_file)
        pdf_path = os.path.join(pdf_folder, pdf_file)

        # Ajouter à la liste des associations
        file_pairs.append((stix_path, pdf_path))

    return file_pairs

def reconcile_fuzzy(pdf_malwares, stix_malwares, threshold=80):
    matched = []
    for stix_malware in stix_malwares:
        # Vérifier si l'extraction est valide (qu'il y a bien un match trouvé)
        result = process.extractOne(stix_malware, pdf_malwares, scorer=fuzz.token_set_ratio)
        if result:  # S'il y a un résultat, il sera un tuple (match, score)
            match, score, index = result
            if score >= threshold:
                matched.append((stix_malware, match, score))  # Ajouter le match et le score
    return matched

def main():
    stix_folder = 'data_stix/stix_bundles'
    pdf_folder = 'data_stix/pdfs'

    strix_extractor = StixExtractor()
    extractor = PdfExtractor()

    # Associer les fichiers STIX et PDF
    file_pairs = associate_files(stix_folder, pdf_folder)

    # Afficher les associations des fichiers
    if file_pairs:
        for stix_file, pdf_file in file_pairs:


            strix_malwares = strix_extractor.extract(stix_file)
            pdf_text =  extractor.extract_text_from_pdf(pdf_file)

            pdf_malwares =  extractor.predict(pdf_text)
            fuzzy_matches = reconcile_fuzzy([malware["entity"] for malware in pdf_malwares], strix_malwares)

            print(fuzzy_matches)




main()