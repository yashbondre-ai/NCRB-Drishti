from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from apps.auth.models import Organization, Permission, Role, RolePermission, User, UserRole
from apps.cases.models import Case
from apps.cases.services import CaseService
from apps.documents.models import AuditLog, BlockchainRecord, Document, DocumentVersion


class AuthAndDocumentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.organization = Organization.objects.create(
            org_code="PS-DEL-001",
            org_name="Delhi Central Police Station",
            org_type="POLICE_STATION",
        )
        self.officer = User.objects.create_user(
            email="officer@example.com",
            password="OfficerPass!2026",
            organization=self.organization,
            employee_code="EMP-1",
            full_name="Case Officer",
            role=User.Role.OFFICER,
        )
        self.other_org = Organization.objects.create(
            org_code="PS-MUM-001",
            org_name="Mumbai Police Station",
            org_type="POLICE_STATION",
        )
        self.outsider = User.objects.create_user(
            email="outsider@example.com",
            password="OutsiderPass!2026",
            organization=self.other_org,
            employee_code="EMP-2",
            full_name="Other Officer",
            role=User.Role.OFFICER,
        )

    def _login(self, email, password):
        response = self.client.post(
            "/api/auth/login/",
            {"email": email, "password": password},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.content)
        token = response.data["tokens"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return response

    def test_register_and_login(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "organization": self.organization.id,
                "employee_code": "EMP-1001",
                "full_name": "Asha Sharma",
                "email": "asha.sharma@example.com",
                "phone": "9876543210",
                "password": "AshaStrongPass!2026",
                "confirm_password": "AshaStrongPass!2026",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.content)
        login = self.client.post(
            "/api/auth/login/",
            {"email": "asha.sharma@example.com", "password": "AshaStrongPass!2026"},
            format="json",
        )
        self.assertEqual(login.status_code, 200)
        self.assertIn("access", login.data["tokens"])

    def test_login_rejects_bad_password(self):
        response = self.client.post(
            "/api/auth/login/",
            {"email": "officer@example.com", "password": "wrong"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_organization_requires_rbac_permission(self):
        self._login("officer@example.com", "OfficerPass!2026")
        response = self.client.get("/api/auth/organizations/")
        self.assertEqual(response.status_code, 403)

        role = Role.objects.create(code=Role.RoleCode.DEPARTMENT_ADMIN, name="Dept Admin")
        permission = Permission.objects.create(code="ORG_VIEW", name="View organizations")
        RolePermission.objects.create(role=role, permission=permission)
        UserRole.objects.create(user=self.officer, role=role)

        response = self.client.get("/api/auth/organizations/")
        self.assertEqual(response.status_code, 200)

    def test_case_and_document_jwt_flow(self):
        self._login("officer@example.com", "OfficerPass!2026")
        create_case = self.client.post(
            "/api/cases/cases/",
            {
                "fir_number": "FIR-DEL-2026-0001",
                "title": "Central Delhi burglary investigation",
                "description": "Investigation into a reported residential burglary.",
                "case_type": "INVESTIGATION",
                "status": "OPEN",
                "priority": "HIGH",
                "organization": self.organization.id,
                "assigned_officer": self.officer.id,
            },
            format="json",
        )
        self.assertEqual(create_case.status_code, 201, create_case.content)
        case_id = create_case.data["id"]

        upload = self.client.post(
            "/documents/upload/",
            {
                "case_id": case_id,
                "title": "Initial witness statement",
                "description": "Signed statement",
                "file": SimpleUploadedFile("witness-statement.txt", b"Witness saw a person leave."),
            },
            format="multipart",
        )
        self.assertEqual(upload.status_code, 201, upload.content)
        document_id = upload.json()["document"]["id"]
        self.assertEqual(len(upload.json()["document"]["sha256_hash"]), 64)

        version = DocumentVersion.objects.get(document_id=document_id, version_number=1)
        self.assertTrue(BlockchainRecord.objects.filter(document_version=version).exists())
        self.assertTrue(
            AuditLog.objects.filter(document_id=document_id, action="upload").exists()
        )

        verify = self.client.get(f"/documents/{version.id}/verify/")
        self.assertEqual(verify.status_code, 200, verify.content)
        self.assertTrue(verify.json()["verification"]["verified"])

        download = self.client.get(f"/documents/{version.id}/download/")
        self.assertEqual(download.status_code, 200)
        self.assertEqual(b"".join(download.streaming_content), b"Witness saw a person leave.")

        case_docs = self.client.get(f"/api/cases/cases/{case_id}/documents/")
        self.assertEqual(case_docs.status_code, 200)
        self.assertEqual(len(case_docs.data), 1)

    def test_outsider_cannot_access_other_org_document(self):
        case = Case.objects.create(
            case_number=CaseService.generate_case_number(),
            title="Restricted case",
            case_type=Case.CaseType.CRIMINAL,
            organization=self.organization,
            created_by=self.officer,
            assigned_officer=self.officer,
        )
        self._login("officer@example.com", "OfficerPass!2026")
        upload = self.client.post(
            "/documents/upload/",
            {
                "case_id": case.id,
                "title": "Secret",
                "file": SimpleUploadedFile("secret.txt", b"classified"),
            },
            format="multipart",
        )
        self.assertEqual(upload.status_code, 201, upload.content)
        version_id = DocumentVersion.objects.get(document_id=upload.json()["document"]["id"]).id

        self._login("outsider@example.com", "OutsiderPass!2026")
        verify = self.client.get(f"/documents/{version_id}/verify/")
        self.assertEqual(verify.status_code, 403)
        listing = self.client.get("/documents/")
        self.assertEqual(listing.json()["documents"], [])
