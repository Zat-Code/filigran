import { useState } from "react";
import { Match, ResultViewerProps } from "../model/Match";


export const ResultViewer: React.FC<ResultViewerProps> = ({ results }) => {
  const [showTexts, setShowTexts] = useState<{ [key: number]: boolean }>({});

  const toggleText = (index: number) => {
    setShowTexts(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

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
        <span key={index} className="bg-red-700 font-bold text-white">
          {segment.text}
        </span>
      ) : (
        <span key={index} className="text-gray-300">{segment.text}</span>
      )
    ));
  };

  return (
    <div className="space-y-8">
      {results.map((result, index) => (
        <div key={index} className="bg-gray-800 rounded-lg shadow-xl p-6">
          <h3 className="text-xl font-bold mb-4 text-white">
            Fichier PDF : {result.pdf_file}
          </h3>
          
          {/* Liste des malwares trouvés */}
          <div className="mb-6 p-4 bg-gray-700 rounded-lg">
            <h4 className="font-semibold mb-3 text-white">Malwares détectés :</h4>
            <div className="grid gap-2">
              {result.matches.map((match: Match, i: number) => (
                <div key={i} className="flex items-center gap-2 text-sm">
                  <span className="bg-red-600 px-2 py-1 rounded text-white">
                    {match.pdf_malware}
                  </span>
                  <span className="text-gray-400">→</span>
                  <span className="font-medium text-white">{match.stix_malware}</span>
                  <span className="text-gray-400">
                    (Score: {match.score}%)
                  </span>
                  <span className="text-gray-400">
                    ({match.locations.length} occurrence{match.locations.length > 1 ? 's' : ''})
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Bouton pour afficher/masquer le texte */}
          <button
            onClick={() => toggleText(index)}
            className="mb-4 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
          >
            {showTexts[index] ? 'Masquer le pdf' : 'Afficher le pdf'}
          </button>

          {/* Texte avec surlignage */}
          {showTexts[index] && (
            <div className="whitespace-pre-wrap font-mono text-sm bg-gray-700 p-4 rounded-lg border border-gray-600">
              {highlightMatches(result.extracted_text, result.matches)}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}; 