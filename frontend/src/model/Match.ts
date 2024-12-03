export interface Match {
    pdf_malware: string;
    stix_malware: string;
    score: number;
    locations: [number, number][];
}

export interface Result {
    pdf_file: string;
    matches: Match[];
    extracted_text: string;
  }
  
export interface ResultViewerProps {
    results: Result[];
  }