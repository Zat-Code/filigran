from gliner import GLiNER
import spacy
import sys
import subprocess
from collections import defaultdict
import pdfplumber


class PdfExtractor:
    def __init__(self):
        # Initialisation du modèle GLiNER et Spacy
        self.model = GLiNER.from_pretrained("urchade/gliner_small-v2.1")
        self.split_text_model = self.ensure_spacy_model()

    def ensure_spacy_model(self, model_name="en_core_web_sm"):
        """
        Vérifie et charge le modèle Spacy nécessaire pour le découpage des textes.
        """
        try:
            split_text_model = spacy.load(model_name)
            print(f"Le modèle '{model_name}' est déjà installé.")
        except OSError:
            print(f"Le modèle '{model_name}' n'est pas installé. Installation en cours...")
            subprocess.run([sys.executable, "-m", "spacy", "download", model_name], check=True)
            split_text_model = spacy.load(model_name)
            print(f"Le modèle '{model_name}' a été installé avec succès.")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            sys.exit(1)

        return split_text_model

    def extract_text_from_pdf(self, path: str) -> str:
        """
        Extrait le texte d'un fichier PDF.
        """
        try:
            with pdfplumber.open(path) as pdf:
                pdf_text = ""
                for page in pdf.pages:
                    pdf_text += page.extract_text() or ""
            return pdf_text
        except Exception as e:
            print(f"Erreur lors de l'extraction du texte depuis le PDF : {e}")
            return ""

    def split_text(self, text, max_length=382):
        """
        Découpe le texte en segments basés sur le nombre de caractères.
        """
        doc = self.split_text_model(text)
        segments = []
        current_segment = []

        for sentence in doc.sents:
            if len(" ".join(current_segment + [sentence.text])) <= max_length:
                current_segment.append(sentence.text)
            else:
                segments.append(" ".join(current_segment))
                current_segment = [sentence.text]

        if current_segment:
            segments.append(" ".join(current_segment))

        return segments

    def split_text_token(self, text, max_tokens=30):
        """
        Découpe le texte en segments basés sur le nombre maximal de tokens.
        """
        tokens = list(self.model.data_processor.words_splitter(text))
        total_tokens = len(tokens)

        segments = []
        start = 0

        while start < total_tokens:
            end = min(start + max_tokens, total_tokens)
            segment = " ".join(str(token) for token in tokens[start:end])
            segments.append(segment)
            start = end

        return segments

    def predict_entities(self, text):
        """
        Effectue des prédictions d'entités nommées sur le texte fourni.
        """
        segments = self.split_text(text)  # Utilise le découpage par caractères (modifiez si nécessaire)
        labels = ['malware']  # Spécifiez les labels à détecter

        all_entities = []
        for segment in segments:
            entities = self.model.predict_entities(segment, labels=labels)
            all_entities.extend(entities)
            
        # Regroupe et calcule la fréquence et la moyenne des scores pour chaque entité
        entity_summary = defaultdict(lambda: {'count': 0, 'total_score': 0.0, 'locations': []})

        for entity in all_entities:
            entity_text = entity['text']
            entity_score = entity['score']
            entity_summary[entity_text]['count'] += 1
            entity_summary[entity_text]['total_score'] += entity_score
            entity_summary[entity_text]['locations'].append((entity['start'], entity['end']))

        # Calcul des moyennes
        summary_list = [
            {'entity': entity_text, 'count': data['count'], 'average_score': data['total_score'] / data['count'], 'locations': data['locations']}
            for entity_text, data in entity_summary.items()
        ]

        # Tri par fréquence décroissante
        return sorted(summary_list, key=lambda x: x['count'], reverse=True)