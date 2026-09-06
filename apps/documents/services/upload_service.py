from django.db import transaction

from apps.cases.models import Case
from apps.documents.models import Document, DocumentVersion

from .hash_service import calculate_sha256


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

    sha256_hash = calculate_sha256(uploaded_file)

    document = Document.objects.create(
        case=case,
        title=title,
        description=description,
        created_by=user,
    )

    version = DocumentVersion.objects.create(
        document=document,
        version_number=1,
        file=uploaded_file,
        sha256_hash=sha256_hash,
        original_filename=uploaded_file.name,
        file_size=uploaded_file.size,
        mime_type=uploaded_file.content_type or "",
        uploaded_by=user,
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
        mime_type=uploaded_file.content_type or "",
        uploaded_by=user,
    )

    return version