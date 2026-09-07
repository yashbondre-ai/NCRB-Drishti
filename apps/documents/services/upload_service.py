from django.db import transaction
from .audit_service import create_audit_log
from apps.cases.models import Case
from apps.documents.models import (
    Document,
    DocumentVersion,
    BlockchainRecord,
)

from .hash_service import calculate_sha256
from .blockchain_service import create_blockchain_record

import logging
import os
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


@transaction.atomic
def upload_document(
    *,
    case_id,
    title,
    description,
    uploaded_file,
    user,
):
    """
    Create a new Document with its first version.
    """

    case = Case.objects.get(pk=case_id)

    document = Document.objects.create(
        case=case,
        title=title,
        description=description,
        created_by=user,
    )

    _process_document_for_rag(document.id, uploaded_file)

    sha256_hash = calculate_sha256(uploaded_file)

    version = DocumentVersion.objects.create(
        document=document,
        version_number=1,
        file=uploaded_file,
        sha256_hash=sha256_hash,
        original_filename=uploaded_file.name,
        file_size=uploaded_file.size,
        mime_type=getattr(uploaded_file, "content_type", None) or "",
        uploaded_by=user,
    )

    blockchain_data = create_blockchain_record(
        document_version=version,
    )

    BlockchainRecord.objects.create(
        document_version=version,
        document_hash=blockchain_data["document_hash"],
        blockchain_hash=blockchain_data["blockchain_hash"],
        status=blockchain_data["status"],
    )
    create_audit_log(
        user=user,
        document=document,
        document_version=version,
        action="upload",
        details={
            "filename": version.original_filename,
            "version": version.version_number,
            "sha256_hash": version.sha256_hash,
            "file_size": version.file_size,
            "mime_type": version.mime_type,
        },
    )

    return document, version


@transaction.atomic
def upload_document_version(
    *,
    document_id,
    uploaded_file,
    user,
):
    """
    Upload a new version for an existing document.
    """

    document = Document.objects.get(
        pk=document_id,
        is_deleted=False,
    )

    _process_document_for_rag(document.id, uploaded_file)

    sha256_hash = calculate_sha256(uploaded_file)

    last_version = (
        DocumentVersion.objects
        .filter(document=document)
        .order_by("-version_number")
        .first()
    )

    next_version_number = (
        last_version.version_number + 1
        if last_version
        else 1
    )

    version = DocumentVersion.objects.create(
        document=document,
        version_number=next_version_number,
        file=uploaded_file,
        sha256_hash=sha256_hash,
        original_filename=uploaded_file.name,
        file_size=uploaded_file.size,
        mime_type=getattr(uploaded_file, "content_type", None) or "",
        uploaded_by=user,
    )

    blockchain_data = create_blockchain_record(
        document_version=version,
    )

    BlockchainRecord.objects.create(
        document_version=version,
        document_hash=blockchain_data["document_hash"],
        blockchain_hash=blockchain_data["blockchain_hash"],
        status=blockchain_data["status"],
    )
    create_audit_log(
        user=user,
        document=document,
        document_version=version,
        action="version_upload",
        details={
            "filename": version.original_filename,
            "version": version.version_number,
            "sha256_hash": version.sha256_hash,
            "file_size": version.file_size,
            "mime_type": version.mime_type,
        },
    )

    return version


def _process_document_for_rag(document_id: int, uploaded_file):
    """Best-effort RAG indexing. Failures must not block document storage."""
    try:
        from apps.RAG.extractor import extract as rag_extract
        from apps.RAG.chunking.chunk import createchunks
        from apps.RAG.chunking.chunk_config import CHUNK_CONFIG
        from apps.RAG.embeddings.generator import generate_embeddings
        from apps.RAG.vectorstore.index import VectorIndexer
    except ImportError:
        logger.warning("RAG dependencies are not installed; skipping indexing.")
        _rewind(uploaded_file)
        return

    suffix = Path(getattr(uploaded_file, "name", "")).suffix
    tmp_path = None

    try:
        uploaded_file.seek(0)
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)
            tmp_path = Path(tmp_file.name)

        raw_text = rag_extract(tmp_path)
        cfg = CHUNK_CONFIG.get(suffix.lower(), {"chunk_size": 500, "chunk_overlap": 100})
        chunks = createchunks(raw_text, cfg["chunk_size"], cfg["chunk_overlap"])

        if not chunks:
            return

        embeddings = generate_embeddings(chunks)

        metadata_list = []
        for idx, chunk_text in enumerate(chunks):
            metadata_list.append({
                "document_id": document_id,
                "chunk_index": idx,
                "text": chunk_text,
                "chunk_text": chunk_text,
            })

        VectorIndexer().add_embeddings(embeddings, metadata_list)
    except Exception:
        logger.exception("RAG indexing failed for document %s; upload will continue.", document_id)
    finally:
        if tmp_path:
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        _rewind(uploaded_file)


def _rewind(uploaded_file):
    try:
        uploaded_file.seek(0)
    except Exception:
        pass
