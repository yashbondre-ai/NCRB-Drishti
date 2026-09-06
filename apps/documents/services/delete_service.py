from django.utils import timezone

from apps.documents.models import Document


def soft_delete_document(
    *,
    document_id,
    user,
):
    """
    Soft delete a document.

    The document and its physical files are not deleted.
    Only the document's deleted status and metadata are updated.
    """

    document = Document.objects.get(
        pk=document_id,
        is_deleted=False,
    )

    document.is_deleted = True
    document.deleted_at = timezone.now()
    document.deleted_by = user
    document.save(
        update_fields=[
            "is_deleted",
            "deleted_at",
            "deleted_by",
            "updated_at",
        ]
    )

    return document