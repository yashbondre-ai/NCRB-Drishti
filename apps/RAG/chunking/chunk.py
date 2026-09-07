import logging

logger = logging.getLogger(__name__)


def createchunks(text, chunksize, chunkoverlap):
    text = text or ""
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunksize,
            chunk_overlap=chunkoverlap,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = splitter.split_text(text)
    except ImportError:
        chunks = _fallback_split(text, chunksize, chunkoverlap)

    logger.info("Total Chunks: %d", len(chunks))
    return chunks


def _fallback_split(text, chunksize, chunkoverlap):
    if not text:
        return []
    chunks = []
    start = 0
    length = len(text)
    overlap = min(chunkoverlap, chunksize - 1) if chunksize > 1 else 0
    while start < length:
        end = min(start + chunksize, length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= length:
            break
        start = end - overlap
    return chunks
