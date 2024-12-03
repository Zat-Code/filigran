# 🚀**Aggregator Stix/PDF**
Cet outil permet de comparer des fichiers STIX JSON à des PDF afin d'identifier et de mettre en évidence des correspondances, comme des malwares ou des termes spécifiques. L'application dispose d'une interface frontend intuitive et d'un backend puissant pour le traitement des données.

## 🖼️ Exemple de la vue principale :
![frondend](doc/frontend-1.png)

## 🖼️ Exemple de la vue des résultats :
![frondend](doc/frontend-2.png)

## 🐳 Démarrer avec Docker Compose

### Étape 1️⃣ : Lancer les conteneurs  

```bash
docker-compose up -d
```

#### ⚠️ Remarque importante :
**Temps de démarrage initial prolongé** : Le conteneur fastapi-app peut prendre du temps à démarrer lors de la première exécution. Cela est dû au traitement initial des fichiers PDF présents dans le dossier data/pdfs.
Pendant ce processus, vous pouvez vérifier les journaux du conteneur pour suivre l'avancement 

```bash	
docker logs fastapi-app
```

## 🌐 Accéder à l'application :

### Étape 2️⃣ : Ouvrir l'interface
Une fois les conteneurs démarrés, ouvrez votre navigateur et rendez-vous sur :

 👉 [Application frontend](http://localhost:80)

### Étape 3️⃣ : Tester l'application

* 📂 Uploader un fichier STIX JSON.
* 🔍 Obtenir les correspondances directement dans l'interface.

<!-- # Launch backend

cd backend
python3 -m pip install -r requirements.txt
uvicorn main:app --reload

# Launch frontend

cd frontend
npm install
npm run dev -->