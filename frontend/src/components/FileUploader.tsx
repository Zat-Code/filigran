import React, { useState } from "react";
import axios from "axios";
import { ResultViewer } from "./ResultViewer";

const FileUploader = () => {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<any[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files ? e.target.files[0] : null);
    setError(null);
    setResults(null);
  };

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
      const response = await axios.post("http://localhost:8000/aggregator", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResults(response.data.matches);
    } catch (err) {
      setError("Erreur lors de l'envoi du fichier.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section upload */}
        <div className="max-w-3xl mx-auto bg-gray-800 rounded-lg shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Analyse de fichier STIX
          </h2>
          
          <div className="space-y-4">
            {/* Zone de drop ou sélection de fichier */}
            <div className="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center">
              <input
                type="file"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
                accept=".json,.xml,.stix"
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer text-gray-300 hover:text-white"
              >
                <div className="space-y-2">
                  <div className="mx-auto h-12 w-12 text-gray-400">
                    📁
                  </div>
                  <div className="text-sm">
                    <span className="text-red-500 hover:text-red-400">
                      Cliquez pour sélectionner
                    </span>
                    {" "}ou glissez-déposez un fichier STIX
                  </div>
                </div>
              </label>
              {file && (
                <div className="mt-4 text-sm text-gray-300">
                  Fichier sélectionné : {file.name}
                </div>
              )}
            </div>

            {/* Bouton d'envoi */}
            <div className="text-center">
              <button
                onClick={handleUpload}
                disabled={loading}
                className={`
                  px-4 py-2 rounded-md text-white font-medium
                  ${loading 
                    ? 'bg-gray-600 cursor-not-allowed' 
                    : 'bg-red-600 hover:bg-red-700'}
                `}
              >
                {loading ? "Chargement..." : "Analyser le fichier"}
              </button>
            </div>

            {/* Message d'erreur */}
            {error && (
              <div className="text-red-500 text-center text-sm mt-2">
                {error}
              </div>
            )}
          </div>
        </div>

        {/* Affichage des résultats */}
        {results && <ResultViewer results={results} />}
      </div>
    </div>
  );
};

export default FileUploader;
