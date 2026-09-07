from pathlib import Path


def checkextension(extension, file_path):
    if extension in [".txt", ".md"]:
        return Path(file_path).read_text(encoding="utf-8", errors="replace")

    if extension == ".pdf":
        from .pdf_extractor import extract_pdf
        return extract_pdf(file_path)

    if extension in [".doc", ".docx"]:
        from .docx_extractor import extract_docx
        return extract_docx(file_path)

    if extension in [".png", ".jpg", ".jpeg", ".webp"]:
        from .image_extractor import extract_image
        return extract_image(file_path)

    if extension in [".wav", ".mp3", ".m4a", ".webm"]:
        from .audio_extractor import extract_audio
        return extract_audio(file_path)

    raise ValueError(f"Unsupported file type: {extension}")
