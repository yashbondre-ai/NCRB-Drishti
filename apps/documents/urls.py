from django.urls import path

from .views import (
    upload_document_view,
    upload_document_version_view,
)


urlpatterns = [
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
]