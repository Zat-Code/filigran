from pydantic import BaseModel, Field
from typing import List, Dict, Any

class PDFObject(BaseModel):
    file_name: str = Field(..., description="Nom du fichier PDF")
    file_path: str = Field(..., description="Chemin du fichier PDF")
    extracted_text: str = Field(..., description="Texte extrait du fichier PDF")
    malwares: List[Dict[str, Any]] = Field(..., description="Résultats du prédicteur")