from django.test import TestCase
from rest_framework.test import APIRequestFactory

from apps.auth.models import Organization, User

from .models import Case
from .permissions import CanEditCase, IsAdminOrOfficer
from .serializers import CaseSerializer
from .services import CaseService


class CaseModelTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            org_code='ORG-1', org_name='Central Unit', org_type='POLICE_STATION'
        )
        self.officer = User.objects.create_user(
            email='officer@example.com', password='password', organization=self.organization,
            employee_code='EMP-1', full_name='Case Officer', role=User.Role.OFFICER
        )

    def test_string_representation(self):
        case = Case.objects.create(
            case_number='NCRB/TEST0001', title='Test case', case_type=Case.CaseType.CRIMINAL,
            organization=self.organization, created_by=self.officer
        )
        self.assertEqual(str(case), 'NCRB/TEST0001 - Test case')

    def test_case_number_generation(self):
        self.assertRegex(CaseService.generate_case_number(), r'^NCRB/[A-F0-9]{8}$')

    def test_serializer_has_document_count(self):
        case = Case.objects.create(
            case_number='NCRB/TEST0002', title='Test case', case_type=Case.CaseType.CIVIL,
            organization=self.organization, created_by=self.officer
        )
        self.assertEqual(CaseSerializer(case).data['document_count'], 0)

    def test_officer_can_edit_own_case(self):
        case = Case.objects.create(
            case_number='NCRB/TEST0003', title='Test case', case_type=Case.CaseType.INVESTIGATION,
            organization=self.organization, created_by=self.officer, assigned_officer=self.officer
        )
        request = APIRequestFactory().patch('/')
        request.user = self.officer
        self.assertTrue(CanEditCase().has_object_permission(request, None, case))
        self.assertTrue(IsAdminOrOfficer().has_permission(request, None))
