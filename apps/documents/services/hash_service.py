import hashlib


def calculate_sha256(file):
    """
    Calculate SHA-256 hash of an uploaded file or stored FieldFile.
    Always rewind before and after hashing so later readers see the full file.
    """
    sha256 = hashlib.sha256()

    if hasattr(file, "seek"):
        file.seek(0)

    chunks = file.chunks() if hasattr(file, "chunks") else [file.read()]
    for chunk in chunks:
        sha256.update(chunk)

    if hasattr(file, "seek"):
        file.seek(0)

    return sha256.hexdigest()
