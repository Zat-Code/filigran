import React, { useState } from "react";
import axios from "axios";

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
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Chargement..." : "Envoyer"}
      </button>
      {error && <div className="text-red-500">{error}</div>}
      {results && (
        <div>
          <h2 className="text-xl font-bold mb-4">Résultats :</h2>
          {results.map((result, index) => (
            <div key={index} className="mb-8 p-4 border rounded">
              <h3 className="text-lg font-bold mb-2">Fichier PDF : {result.pdf_file}</h3>
              
              {/* Liste des malwares trouvés */}
              <div className="mb-4 p-4 bg-black-50 rounded">
                <h4 className="font-semibold mb-2">Malwares détectés :</h4>
                {result.matches.map((match, i) => (
                  <div key={i} className="mb-1 flex items-center gap-2">
                    <span className="bg-red-600 px-2 py-1 rounded">
                      {match.pdf_malware}
                    </span>
                    <span className="text-white-600">→</span>
                    <span className="font-medium">{match.stix_malware}</span>
                    <span className="text-white-600">
                      (Score: {match.score}%)
                    </span>
                    <span className="text-white-600">
                      ({match.locations.length} occurrence{match.locations.length > 1 ? 's' : ''})
                    </span>
                  </div>
                ))}
              </div>

              {/* Texte complet avec surlignage */}
              <div className="whitespace-pre-wrap font-mono text-sm bg-black-50 p-4 rounded border">
                {highlightMatches(result.extracted_text, result.matches)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// Fonction pour surligner les correspondances dans le texte
const highlightMatches = (text: string, matches: any[]) => {
  const segments: { text: string; isMatch: boolean }[] = [];
  let currentPosition = 0;

  const allPositions = matches.flatMap(match =>
    match.locations.map(([start, end]: number[]) => ({ start, end }))
  ).sort((a, b) => a.start - b.start);

  allPositions.forEach(({ start, end }) => {
    if (start > currentPosition) {
      segments.push({
        text: text.slice(currentPosition, start),
        isMatch: false
      });
    }
    segments.push({
      text: text.slice(start, end),
      isMatch: true
    });
    currentPosition = end;
  });

  if (currentPosition < text.length) {
    segments.push({
      text: text.slice(currentPosition),
      isMatch: false
    });
  }

  return segments.map((segment, index) => (
    segment.isMatch ? (
      <span key={index} className="bg-red-700 font-bold">
        {segment.text}
      </span>
    ) : (
      <span key={index}>{segment.text}</span>
    )
  ));
};

export default FileUploader;
