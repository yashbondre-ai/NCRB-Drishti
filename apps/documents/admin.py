from django.contrib import admin

from .models import AuditLog, BlockchainRecord, Document, DocumentVersion


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "case", "created_by", "is_deleted", "created_at"]
    list_filter = ["is_deleted"]
    search_fields = ["title"]


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ["document", "version_number", "sha256_hash", "uploaded_at"]


@admin.register(BlockchainRecord)
class BlockchainRecordAdmin(admin.ModelAdmin):
    list_display = ["document_version", "status", "created_at"]


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["action", "document", "user", "created_at"]
    list_filter = ["action"]
