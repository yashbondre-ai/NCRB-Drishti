from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services.upload_service import (
    upload_document,
    upload_document_version,
)

@login_required
@require_POST
def upload_document_view(request):
    case_id = request.POST.get("case_id")
    title = request.POST.get("title")
    description = request.POST.get("description", "")
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

@login_required
@require_POST
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
                "uploaded_by": version.uploaded_by.username,
            },
        },
        status=201,
    )