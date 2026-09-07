from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.auth.models import Organization, Role, RoleRequest, User, UserRole, Permission, RolePermission


class TestingPagesRenderTest(TestCase):
    """Verifies that all testing templates load successfully with proper HTML structures."""

    def setUp(self):
        self.client = APIClient()

    def test_testing_register_page_renders(self):
        response = self.client.get(reverse("testing-register"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn('name="organization"', content)
        self.assertIn('name="requested_role"', content)
        self.assertIn('name="employee_code"', content)
        self.assertIn('name="full_name"', content)
        self.assertIn('name="email"', content)
        self.assertIn('name="password"', content)
        self.assertIn('name="confirm_password"', content)

    def test_testing_login_page_renders(self):
        response = self.client.get(reverse("testing-login"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn('id="email"', content)
        self.assertIn('id="password"', content)
        self.assertIn('id="form"', content)

    def test_testing_dashboard_page_renders(self):
        response = self.client.get(reverse("testing-dashboard"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn('id="userFullName"', content)
        self.assertIn('id="requestStatus"', content)
        self.assertIn('id="permissions"', content)

    def test_testing_role_requests_page_renders(self):
        response = self.client.get(reverse("testing-role-requests"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn('id="rows"', content)
        self.assertIn('id="rejectModal"', content)


class UserModelAndPropertiesTest(TestCase):
    """Tests custom User model properties, active status mapping, and admin permissions."""

    def setUp(self):
        self.org = Organization.objects.create(
            org_code="TEST_ORG_01",
            org_name="Test Organization",
            org_type=Organization.OrganizationType.POLICE_STATION,
            is_active=True,
        )

    def test_is_active_getter_and_setter(self):
        user = User.objects.create_user(
            email="officer@ncrb.gov.in",
            password="SecurePassword123!",
            organization=self.org,
            employee_code="EMP001",
            full_name="Officer One",
        )
        self.assertTrue(user.is_active)
        self.assertEqual(user.status, User.Status.ACTIVE)

        user.is_active = False
        self.assertFalse(user.is_active)
        self.assertEqual(user.status, User.Status.DEACTIVATED)

        user.is_active = True
        self.assertTrue(user.is_active)
        self.assertEqual(user.status, User.Status.ACTIVE)

    def test_create_superuser_handles_is_active_without_crashing(self):
        su = User.objects.create_superuser(
            email="admin@ncrb.gov.in",
            password="SuperPassword123!",
            organization=self.org,
            employee_code="ADMIN001",
            full_name="Super Admin",
        )
        self.assertTrue(su.is_active)
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)
        self.assertTrue(su.has_perm("any_perm"))
        self.assertTrue(su.has_module_perms("ncrb_auth"))


class AuthFlowAPITest(TestCase):
    """Tests registration, login, last_login_at, and role requests approval workflow."""

    def setUp(self):
        self.client = APIClient()
        self.org = Organization.objects.create(
            org_code="POLICE_HQ",
            org_name="Police Headquarters",
            org_type=Organization.OrganizationType.POLICE_STATION,
            is_active=True,
        )
        self.role_super_admin, _ = Role.objects.get_or_create(
            code=Role.RoleCode.SUPER_ADMIN,
            defaults={"name": "Super Admin", "is_active": True},
        )
        self.role_officer, _ = Role.objects.get_or_create(
            code=Role.RoleCode.INVESTIGATION_OFFICER,
            defaults={"name": "Investigation Officer", "is_active": True},
        )
        # Seed permissions
        self.perm_view, _ = Permission.objects.get_or_create(
            code="ROLE_REQUEST_VIEW",
            defaults={"name": "View Role Requests", "is_active": True},
        )
        self.perm_approve, _ = Permission.objects.get_or_create(
            code="ROLE_REQUEST_APPROVE",
            defaults={"name": "Approve Role Requests", "is_active": True},
        )
        RolePermission.objects.get_or_create(role=self.role_super_admin, permission=self.perm_view)
        RolePermission.objects.get_or_create(role=self.role_super_admin, permission=self.perm_approve)

        # Create admin user
        self.admin_user = User.objects.create_user(
            email="superadmin@ncrb.gov.in",
            password="AdminPassword123!",
            organization=self.org,
            employee_code="SA001",
            full_name="Super Administrator",
            role=User.Role.ADMIN,
        )
        UserRole.objects.create(user=self.admin_user, role=self.role_super_admin)

    def test_registration_success(self):
        payload = {
            "organization": self.org.id,
            "requested_role": self.role_officer.code,
            "employee_code": "INV009",
            "full_name": "Ravi Kumar",
            "email": "ravi.kumar@ncrb.gov.in",
            "phone": "9876543210",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
        }
        response = self.client.post("/api/auth/register/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["role_request"]["status"], RoleRequest.Status.PENDING)
        self.assertEqual(response.data["role_request"]["requested_role"], self.role_officer.code)

    def test_login_updates_last_login_at(self):
        self.assertIsNone(self.admin_user.last_login_at)
        response = self.client.post("/api/auth/login/", {
            "email": "superadmin@ncrb.gov.in",
            "password": "AdminPassword123!",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])

        self.admin_user.refresh_from_db()
        self.assertIsNotNone(self.admin_user.last_login_at)

    def test_role_request_list_and_approval(self):
        # Register a regular user
        applicant = User.objects.create_user(
            email="applicant@ncrb.gov.in",
            password="Password12345!",
            organization=self.org,
            employee_code="APP01",
            full_name="Applicant Officer",
        )
        role_req = RoleRequest.objects.create(
            user=applicant,
            requested_role=self.role_officer,
        )

        # Authenticate as super admin
        login_res = self.client.post("/api/auth/login/", {
            "email": "superadmin@ncrb.gov.in",
            "password": "AdminPassword123!",
        }, format="json")
        token = login_res.data["tokens"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        # Verify RoleRequestListView works (was broken before)
        list_res = self.client.get("/api/auth/role-requests/")
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)
        self.assertTrue(any(r["id"] == role_req.id for r in list_res.data))

        # Approve the request
        approve_res = self.client.post(f"/api/auth/role-requests/{role_req.id}/approve/")
        self.assertEqual(approve_res.status_code, status.HTTP_200_OK)

        role_req.refresh_from_db()
        self.assertEqual(role_req.status, RoleRequest.Status.APPROVED)
        self.assertEqual(role_req.reviewed_by, self.admin_user)
        self.assertTrue(UserRole.objects.filter(user=applicant, role=self.role_officer).exists())
