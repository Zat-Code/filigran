from business_logic.pdf_extractor import PdfExtractor
from db.services.pdf_object import add_pdf_object, get_pdf_object_by_one_variable, update_pdf_object
import os
from db.models.pdf_object import PDFObject

async def extract_pdfs_to_db(pdf_folder: str, process_all: bool = False):
    """
    Extraire les fichiers PDF et les enregistrer ou mettre à jour dans la base de données.
    - Si `process_all` est True, tous les fichiers sont retraités.
    - Sinon, seuls les nouveaux fichiers non présents dans la base de données sont traités.
    """
    extractor = PdfExtractor()

    # Lister les fichiers dans le dossier PDF
    pdf_files = sorted(os.listdir(pdf_folder))

    # Extraire et stocker chaque fichier PDF dans la base de données
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)

        if not process_all:
            # Vérifier si l'objet existe déjà en base
            existing_pdf_object = await get_pdf_object_by_one_variable("file_path", pdf_path)
            if existing_pdf_object:
                print(f"Le fichier PDF '{pdf_file}' existe déjà en base de données. Ignoré.")
                continue

        # Extraire le texte du PDF
        pdf_text = extractor.extract_text_from_pdf(pdf_path)

        # Extraire les malwares avec le prédicteur
        pdf_malwares = extractor.predict_entities(pdf_text)

        # Vérifier si le fichier existe déjà
        existing_pdf_object = await get_pdf_object_by_one_variable("file_path", pdf_path)

        if existing_pdf_object:
            # Si l'objet existe, on le met à jour
            print(existing_pdf_object)
            existing_pdf_object.extracted_text = pdf_text
            existing_pdf_object.malwares = pdf_malwares

            # Mettre à jour l'objet dans la base de données
            await update_pdf_object(existing_pdf_object)
            print(f"Le fichier PDF '{pdf_file}' existe déjà, mis à jour dans la base de données.")
        else:
            # Sinon, on crée un nouvel objet PDF
            pdf_object = PDFObject(
                file_name=pdf_file,
                file_path=pdf_path,
                extracted_text=pdf_text,
                malwares=pdf_malwares
            )

            # Enregistrer l'objet PDF dans la base de données
            await add_pdf_object(pdf_object)
            print(f"Fichier PDF '{pdf_file}' traité et enregistré dans la base de données.")