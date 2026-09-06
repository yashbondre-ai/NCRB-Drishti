"""Serializers for the case API."""

from rest_framework import serializers

from .models import Case


class CaseSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    assigned_officer_name = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = [field.name for field in Case._meta.fields] + [
            'created_by_name', 'assigned_officer_name', 'organization_name', 'document_count'
        ]
        read_only_fields = ['case_number', 'created_by', 'created_at', 'updated_at']

    def get_created_by_name(self, obj):
        return getattr(obj.created_by, 'full_name', str(obj.created_by))

    def get_assigned_officer_name(self, obj):
        return getattr(obj.assigned_officer, 'full_name', str(obj.assigned_officer)) if obj.assigned_officer else None

    def get_organization_name(self, obj):
        return getattr(obj.organization, 'org_name', str(obj.organization))

    def get_document_count(self, obj):
        documents = getattr(obj, 'documents', None)
        return documents.count() if documents is not None else 0
