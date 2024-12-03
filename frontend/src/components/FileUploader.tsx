import React, { useState } from "react";
import axios from "axios";

const FileUploader = () => {
  const [file, setFile] = useState(null); // Fichier sélectionné
  const [results, setResults] = useState(null); // Résultats de la comparaison
  const [error, setError] = useState(null); // Erreurs éventuelles
  const [loading, setLoading] = useState(false); // Indicateur de chargement

  // Gestion de la sélection de fichier
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null); // Réinitialiser les erreurs si un nouveau fichier est sélectionné
    setResults(null); // Réinitialiser les résultats
  };

  // Envoi du fichier au backend
  const handleUpload = async () => {
    if (!file) {
      setError("Veuillez sélectionner un fichier avant de soumettre.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post("http://localhost:8000/aggregator/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResults(response.data.matches); // Mettre à jour les résultats avec les correspondances
    } catch (err) {
      setError(
        err.response?.data?.detail || "Une erreur s'est produite lors de la soumission du fichier."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Comparez un fichier STIX avec les malwares des fichiers PDF</h1>

      <input type="file" accept=".json" onChange={handleFileChange} />

      <button onClick={handleUpload} disabled={loading} style={{ margin: "10px" }}>
        {loading ? "Chargement..." : "Soumettre"}
      </button>

      {error && <div style={{ color: "red" }}>{error}</div>}

      {results && (
        <div>
          <h2>Résultats :</h2>
          {results.map((result, index) => (
            <div key={index}>
              <h3>Fichier PDF : {result.pdf_file}</h3>
              <ul>
                {result.matches.map((match, i) => (
                  <li key={i}>
                    Malware STIX : <b>{match[0]}</b> - Correspondance PDF : <b>{match[1]}</b> - Score : <b>{match[2]}%</b>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FileUploader;
