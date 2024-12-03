# Utiliser une image Python officielle
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install fastapi uvicorn

RUN python3 -m spacy download en_core_web_sm

# Étape 3: Exposer le port et définir le point d'entrée
EXPOSE 8000

# Définir le point d'entrée pour uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]