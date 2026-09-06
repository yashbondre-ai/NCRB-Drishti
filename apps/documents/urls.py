from django.urls import path

from .views import (
    document_list_view,
    upload_document_view,
    upload_document_version_view,
    download_document_version_view,
    verify_document_version_view,
    delete_document_view,
)


urlpatterns = [
    path(
    "",
    document_list_view,
    name="document-list",
),
    path(
        "upload/",
        upload_document_view,
        name="document-upload",
    ),

    path(
        "<int:document_id>/versions/upload/",
        upload_document_version_view,
        name="document-version-upload",
    ),

    path(
        "<int:version_id>/download/",
        download_document_version_view,
        name="document-version-download",
    ),
    path(
        "<int:version_id>/verify/",
        verify_document_version_view,
        name="document-version-verify",
    ),
    path(
        "<int:document_id>/delete/",
        delete_document_view,
        name="document-delete",
),
]