from gliner import GLiNER
import spacy
import sys
import subprocess
from collections import defaultdict


class Predictor:
    def __init__(self):
        self.model = GLiNER.from_pretrained("urchade/gliner_small-v2.1")
        self.split_text_model = self.ensure_spacy_model()

    def ensure_spacy_model(self, model_name="en_core_web_sm"):
        try:
            # Essaye de charger le modèle pour vérifier s'il est déjà installé
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

    def split_text(self, text, max_length=382):
        """
        Découpe le texte en phrases ou segments plus courts pour éviter le dépassement de la limite du modèle.
        """
        doc = self.split_text_model(text)
        segments = []
        current_segment = []

        for sentence in doc.sents:  # Découpe le texte en phrases
            if len(" ".join(current_segment + [sentence.text])) <= max_length:
                current_segment.append(sentence.text)
            else:
                segments.append(" ".join(current_segment))
                current_segment = [sentence.text]

        if current_segment:
            segments.append(" ".join(current_segment))

        for i, segment in enumerate(segments):
            token_generator = self.model.data_processor.words_splitter(segment)

            # get the tokens
            tokens = [t for t in token_generator]
            # print(f"segment {i} : {len(tokens)}")

        return segments

    def split_text_token(self, text, max_tokens=30):
        # Get all tokens
        tokens = list(self.model.data_processor.words_splitter(text))
        total_tokens = len(tokens)

        segments = []
        start = 0

        while start < total_tokens:
            # Calculate end index, ensuring we don't exceed total tokens
            end = min(start + max_tokens, total_tokens)

            # Join tokens for the segment
            segment = " ".join(str(token) for token in tokens[start:end])
            segments.append(segment)

            start = end

        return segments

    def predict(self, text):

        # version less accurate but faster
        segments = self.split_text(text)

        # version more accurate but very slower
        # segments = self.split_text_token(text)

        labels = ['malware']

        all_entities = []
        for segment in segments:
            entities = self.model.predict_entities(segment, labels=labels)
            all_entities.extend(entities)

        # Calculer la fréquence et le score moyen pour chaque entité
        entity_summary = defaultdict(lambda: {'count': 0, 'total_score': 0.0})

        for entity in all_entities:
            entity_text = entity['text']
            entity_score = entity['score']
            entity_summary[entity_text]['count'] += 1
            entity_summary[entity_text]['total_score'] += entity_score

        # Calculer la moyenne des scores
        for entity_text, data in entity_summary.items():
            data['average_score'] = data['total_score'] / data['count']

        # Transformer l'output en une liste plus lisible
        summary_list = [
            {'entity': entity_text, 'count': data['count'], 'average_score': data['average_score']}
            for entity_text, data in entity_summary.items()
        ]

        # Trier la liste par count (du plus grand au plus petit)
        summary_list = sorted(summary_list, key=lambda x: x['count'], reverse=True)

        return summary_list