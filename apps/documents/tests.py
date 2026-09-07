from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.auth.models import Organization, User
from apps.cases.models import Case
from apps.cases.services import CaseService
from apps.documents.models import Document
from apps.documents.services.hash_service import calculate_sha256
from apps.documents.services.upload_service import upload_document


class DocumentServiceTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            org_code="ORG-DOC",
            org_name="Document Unit",
            org_type="POLICE_STATION",
        )
        self.officer = User.objects.create_user(
            email="docs@example.com",
            password="DocsPass!2026",
            organization=self.organization,
            employee_code="EMP-DOC",
            full_name="Docs Officer",
            role=User.Role.OFFICER,
        )
        self.case = Case.objects.create(
            case_number=CaseService.generate_case_number(),
            title="Hash case",
            case_type=Case.CaseType.CIVIL,
            organization=self.organization,
            created_by=self.officer,
        )

    def test_hash_rewinds_file(self):
        uploaded = SimpleUploadedFile("note.txt", b"abc123")
        digest = calculate_sha256(uploaded)
        self.assertEqual(len(digest), 64)
        self.assertEqual(uploaded.read(), b"abc123")

    def test_upload_succeeds_without_rag_stack(self):
        uploaded = SimpleUploadedFile("note.txt", b"abc123")
        document, version = upload_document(
            case_id=self.case.id,
            title="Note",
            description="",
            uploaded_file=uploaded,
            user=self.officer,
        )
        self.assertFalse(document.is_deleted)
        self.assertEqual(version.version_number, 1)
        self.assertEqual(Document.objects.filter(pk=document.id).count(), 1)
        self.assertEqual(len(version.sha256_hash), 64)
