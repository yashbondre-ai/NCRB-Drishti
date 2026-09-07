from pathlib import Path
from .extractors.detector import checkextension

def extract(file_path: Path) -> str:
    extension = file_path.suffix.lower()
    return checkextension(extension, file_path)
