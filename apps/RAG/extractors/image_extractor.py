from pathlib import Path

_reader = None

def _get_reader():
    global _reader
    if _reader is None:
        import easyocr

        _reader = easyocr.Reader(["en"], gpu=False)
    return _reader


def extract_image(file_path: Path) -> str:
    reader = _get_reader()
    result = reader.readtext(str(file_path), detail=0)

    if not result:
        return ""

    output = "\n".join(result)

    return output