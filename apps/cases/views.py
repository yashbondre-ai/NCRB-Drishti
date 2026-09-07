"""REST API endpoints for cases."""

from django.core.exceptions import ValidationError
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
try:
    from django_filters.rest_framework import DjangoFilterBackend
except ImportError:  # Keep startup usable until requirements are installed.
    DjangoFilterBackend = None

from .models import Case
from .permissions import CanEditCase, IsAdminOrOfficer, IsAdminUser
from .serializers import CaseSerializer
from .services import CaseService


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    filter_backends = [SearchFilter] if DjangoFilterBackend is None else [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'priority', 'case_type']
    search_fields = ['case_number', 'title', 'fir_number', 'description']

    def get_permissions(self):
        if self.action in {'list', 'retrieve', 'documents', 'my_cases', 'stats'}:
            classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            classes = [IsAdminUser]
        elif self.action in {'create', 'update', 'partial_update', 'change_status'}:
            classes = [permissions.IsAuthenticated, IsAdminOrOfficer, CanEditCase]
        else:
            classes = [permissions.IsAuthenticated]
        return [permission() for permission in classes]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Case.objects.none()
        return CaseService.get_user_cases(user)

    def get_object(self):
        obj = super().get_object()
        if self.action in {'update', 'partial_update', 'change_status', 'documents'}:
            self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(case_number=CaseService.generate_case_number(), created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        case = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Case.Status.choices):
            return Response({'status': 'Invalid case status.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            case = CaseService.change_status(case, new_status, request.user)
        except ValidationError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        self._audit_status_change(case, request.user)
        return Response(self.get_serializer(case).data)

    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        case = self.get_object()
        documents = case.documents.filter(is_deleted=False).order_by("-created_at")
        return Response(
            [
                {
                    "id": document.id,
                    "title": document.title,
                    "description": document.description,
                    "case_id": document.case_id,
                    "created_by": document.created_by_id,
                    "created_at": document.created_at,
                    "updated_at": document.updated_at,
                }
                for document in documents
            ]
        )

    @action(detail=False, methods=['get'])
    def my_cases(self, request):
        queryset = Case.objects.filter(assigned_officer=request.user)
        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        return Response(CaseService.get_case_stats(self.get_queryset()))

    @staticmethod
    def _audit_status_change(case, user):
        try:
            from apps.audit.services import AuditService
            AuditService.log_action(user=user, action='CASE_STATUS_CHANGED', instance=case)
        except (ImportError, AttributeError, TypeError):
            pass
