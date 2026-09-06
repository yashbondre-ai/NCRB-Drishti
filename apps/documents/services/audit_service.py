from apps.documents.models import AuditLog


def create_audit_log(
    *,
    user,
    document,
    action,
    document_version=None,
    details=None,
):
    """
    Create an audit log entry for a document-related action.
    """

    return AuditLog.objects.create(
        user=user,
        document=document,
        document_version=document_version,
        action=action,
        details=details or {},
    )