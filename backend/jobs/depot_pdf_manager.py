import os
import requests
import json

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "Zat-Code"      # Exemple : "octocat"
REPO_NAME = "filigran"
DOWNLOAD_DIR = "backend/data/pdfs"                # Répertoire où télécharger les PDFs
STATE_FILE = "state.json"            # Fichier pour stocker l'état précédent

# Fonction pour récupérer les fichiers du dépôt
def fetch_files_from_repo(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tree = response.json().get("tree", [])
        files = [item["path"] for item in tree if item["type"] == "blob"]
        return files
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return []

# Fonction pour télécharger un fichier spécifique
def download_file(owner, repo, file_path, download_dir):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{file_path}"
    response = requests.get(url)
    
    if response.status_code == 200:
        os.makedirs(download_dir, exist_ok=True)
        file_name = os.path.join(download_dir, os.path.basename(file_path))
        with open(file_name, "wb") as f:
            f.write(response.content)
        print(f"Téléchargé : {file_name}")
    else:
        print(f"Erreur lors du téléchargement de {file_path} : {response.status_code}")

# Fonction pour lire et sauvegarder l'état
def load_previous_state(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return set(json.load(f))
    return set()

def save_current_state(file, data):
    with open(file, "w") as f:
        json.dump(list(data), f)

# Détection et téléchargement des nouveaux fichiers PDF
def detect_and_download_pdfs():
    previous_files = load_previous_state(STATE_FILE)
    current_files = fetch_files_from_repo(REPO_OWNER, REPO_NAME)
    

    print(current_files)
    # Filtrer uniquement les fichiers PDF
    current_pdfs = {file for file in current_files if file.endswith(".pdf")}
    new_pdfs = current_pdfs - previous_files

    if new_pdfs:
        print(f"Nouveaux fichiers PDF détectés : {new_pdfs}")
        for pdf in new_pdfs:
            download_file(REPO_OWNER, REPO_NAME, pdf, DOWNLOAD_DIR)
    else:
        print("Aucun nouveau fichier PDF détecté.")
    
    # Sauvegarder l'état actuel
    save_current_state(STATE_FILE, current_pdfs)

# Exécution principale
if __name__ == "__main__":
    detect_and_download_pdfs()