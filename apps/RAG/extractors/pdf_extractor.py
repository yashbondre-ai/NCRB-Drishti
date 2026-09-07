from pathlib import Path
from pypdf import PdfReader


def extract_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n\n"
    return text
