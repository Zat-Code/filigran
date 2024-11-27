import pdfplumber


class PdfExtractor:
    def __init__(self) -> None:
        pass


    def extract(self, path: str) -> str:
        with pdfplumber.open(path) as pdf:
            pdf_text = ""
            for page in pdf.pages:
                pdf_text += page.extract_text()
        return pdf_text

