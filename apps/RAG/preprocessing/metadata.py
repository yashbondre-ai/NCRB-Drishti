from pathlib import Path
from datetime import datetime
import os

from pypdf import PdfReader


def get_filename(file_path):
    return Path(file_path).name


def get_extension(file_path):
    return Path(file_path).suffix.lower()


def get_file_size_mb(file_path):
    size = os.path.getsize(file_path)
    return round(size / (1024 * 1024), 2)


def count_pages(file_path):
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(str(file_path))
        return len(reader.pages)

    if extension in [".png", ".jpg", ".jpeg", ".webp"]:
        return 1

    return None


def get_upload_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_language(file_path):
    return "english"


def count_words(text):
    return len(text.split())


def count_characters(text):
    return len(text)


def generate_metadata(text, file_path, file_type):
    return {
        "filename": get_filename(file_path),
        "extension": get_extension(file_path),
        "document_type": file_type,
        "file_size_mb": get_file_size_mb(file_path),
        "pages": count_pages(file_path),
        "upload_date": get_upload_date(),
        "language": get_language(file_path),
        "word_count": count_words(text),
        "character_count": count_characters(text),
    }
