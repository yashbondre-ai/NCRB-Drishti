from django.http import FileResponse, JsonResponse
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .models import Document, DocumentVersion
from .services.access import user_can_access_case
from .services.audit_service import create_audit_log
from .services.blockchain_service import verify_blockchain_record
from .services.delete_service import soft_delete_document
from .services.upload_service import (
    upload_document,
    upload_document_version,
)


def _forbidden():
    return JsonResponse(
        {"success": False, "error": "You do not have access to this resource."},
        status=403,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_document_view(request):
    case_id = request.data.get("case_id")
    title = request.data.get("title")
    description = request.data.get("description", "")
    uploaded_file = request.FILES.get("file")

    if not case_id:
        return JsonResponse(
            {"success": False, "error": "Case is required."},
            status=400,
        )

    if not title:
        return JsonResponse(
            {"success": False, "error": "Document title is required."},
            status=400,
        )

    if not uploaded_file:
        return JsonResponse(
            {"success": False, "error": "Document file is required."},
            status=400,
        )

    if not user_can_access_case(request.user, case_id):
        return _forbidden()

    try:
        document, version = upload_document(
            case_id=case_id,
            title=title,
            description=description,
            uploaded_file=uploaded_file,
            user=request.user,
        )

    except Exception as exc:
        return JsonResponse(
            {
                "success": False,
                "error": str(exc),
            },
            status=400,
        )

    return JsonResponse(
        {
            "success": True,
            "message": "Document uploaded successfully.",
            "document": {
                "id": document.id,
                "title": document.title,
                "case_id": document.case_id,
                "version": version.version_number,
                "filename": version.original_filename,
                "sha256_hash": version.sha256_hash,
                "file_size": version.file_size,
                "mime_type": version.mime_type,
            },
        },
        status=201,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_document_version_view(request, document_id):
    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return JsonResponse(
            {
                "success": False,
                "error": "Document file is required.",
            },
            status=400,
        )

    try:
        document = Document.objects.get(pk=document_id, is_deleted=False)
    except Document.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Document not found."},
            status=404,
        )

    if not user_can_access_case(request.user, document.case_id):
        return _forbidden()

    try:
        version = upload_document_version(
            document_id=document_id,
            uploaded_file=uploaded_file,
            user=request.user,
        )

    except Exception as exc:
        return JsonResponse(
            {
                "success": False,
                "error": str(exc),
            },
            status=400,
        )

    return JsonResponse(
        {
            "success": True,
            "message": "Document version uploaded successfully.",
            "version": {
                "id": version.id,
                "document_id": version.document_id,
                "version_number": version.version_number,
                "filename": version.original_filename,
                "sha256_hash": version.sha256_hash,
                "file_size": version.file_size,
                "mime_type": version.mime_type,
                "uploaded_by": version.uploaded_by.email,
            },
        },
        status=201,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_document_version_view(request, version_id):
    try:
        version = DocumentVersion.objects.select_related(
            "document"
        ).get(
            pk=version_id,
            document__is_deleted=False,
        )

    except DocumentVersion.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "error": "Document version not found.",
            },
            status=404,
        )

    if not user_can_access_case(request.user, version.document.case_id):
        return _forbidden()

    create_audit_log(
        user=request.user,
        document=version.document,
        document_version=version,
        action="download",
        details={
            "filename": version.original_filename,
            "version": version.version_number,
        },
    )

    return FileResponse(
        version.file.open("rb"),
        as_attachment=True,
        filename=version.original_filename,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_document_version_view(request, version_id):
    try:
        version = DocumentVersion.objects.select_related(
            "document"
        ).get(
            pk=version_id,
            document__is_deleted=False,
        )

    except DocumentVersion.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "error": "Document version not found.",
            },
            status=404,
        )

    if not user_can_access_case(request.user, version.document.case_id):
        return _forbidden()

    result = verify_blockchain_record(
        document_version=version,
    )
    create_audit_log(
        user=request.user,
        document=version.document,
        document_version=version,
        action="verify",
        details={
            "verification_status": result["status"],
            "verified": result["verified"],
            "message": result["message"],
            "document_hash": result.get("document_hash"),
            "blockchain_hash": result.get("blockchain_hash"),
        },
    )

    return JsonResponse(
        {
            "success": True,
            "verification": result,
        },
        status=200,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_document_view(request, document_id):
    try:
        document = Document.objects.get(pk=document_id, is_deleted=False)
    except Document.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "error": "Document not found.",
            },
            status=404,
        )

    if not user_can_access_case(request.user, document.case_id):
        return _forbidden()

    try:
        document = soft_delete_document(
            document_id=document_id,
            user=request.user,
        )

    except Document.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "error": "Document not found.",
            },
            status=404,
        )

    except Exception as exc:
        return JsonResponse(
            {
                "success": False,
                "error": str(exc),
            },
            status=400,
        )

    create_audit_log(
        user=request.user,
        document=document,
        action="delete",
        details={
            "deleted_at": document.deleted_at.isoformat(),
            "reason": "Document soft deleted",
        },
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Document deleted successfully.",
            "document": {
                "id": document.id,
                "title": document.title,
                "is_deleted": document.is_deleted,
                "deleted_at": document.deleted_at,
            },
        },
        status=200,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def document_list_view(request):
    from apps.cases.services import CaseService

    visible_case_ids = CaseService.get_user_cases(request.user).values_list("id", flat=True)
    documents = Document.objects.filter(
        is_deleted=False,
        case_id__in=visible_case_ids,
    ).order_by("-created_at")

    return JsonResponse(
        {
            "success": True,
            "documents": [
                {
                    "id": document.id,
                    "title": document.title,
                    "case_id": document.case_id,
                }
                for document in documents
            ],
        }
    )
