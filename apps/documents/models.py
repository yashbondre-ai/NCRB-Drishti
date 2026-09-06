from django.conf import settings
from django.db import models

from apps.cases.models import Case


class Document(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.PROTECT,
        related_name="documents",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_documents",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="deleted_documents",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class DocumentVersion(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.PROTECT,
        related_name="versions",
    )

    version_number = models.PositiveIntegerField()

    file = models.FileField(upload_to="documents/%Y/%m/%d/")

    sha256_hash = models.CharField(
        max_length=64,
        db_index=True,
    )

    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveBigIntegerField()
    mime_type = models.CharField(max_length=100)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_document_versions",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-version_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["document", "version_number"],
                name="unique_document_version",
            )
        ]

    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"

class BlockchainRecord(models.Model):
    document_version = models.OneToOneField(
        DocumentVersion,
        on_delete=models.PROTECT,
        related_name="blockchain_record",
    )

    document_hash = models.CharField(
        max_length=64,
        db_index=True,
    )

    blockchain_hash = models.CharField(
        max_length=64,
        unique=True,
    )

    status = models.CharField(
        max_length=50,
        default="confirmed",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"Blockchain Record - "
            f"{self.document_version.document.title} "
            f"v{self.document_version.version_number}"
        )

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("upload", "Upload"),
        ("version_upload", "Version Upload"),
        ("download", "Download"),
        ("verify", "Verify"),
        ("delete", "Delete"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="document_audit_logs",
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.PROTECT,
        related_name="audit_logs",
    )

    document_version = models.ForeignKey(
        DocumentVersion,
        on_delete=models.PROTECT,
        related_name="audit_logs",
        null=True,
        blank=True,
    )

    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
    )

    details = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.action} - "
            f"{self.document.title} - "
            f"{self.user.username}"
        )