from django.db import transaction
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Organization, Role, RoleRequest, User, UserRole
from .serializers import (
    OrganizationSerializer,
    RegisterSerializer,
    LoginSerializer,
    RoleRequestRejectSerializer,
    RoleRequestSerializer,
    ActiveRoleSerializer,
    DashboardSerializer,
)




from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .permissions import HasPermission


def testing_page(request, page):
    return render(request, f"testing/{page}.html")

class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all().order_by("id")
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "ORG_VIEW"


class ActiveRoleListView(generics.ListAPIView):
    serializer_class = ActiveRoleSerializer
    permission_classes = []
    queryset = Role.objects.filter(is_active=True).exclude(code="SUPER_ADMIN").order_by("name")


class ActiveOrganizationListView(generics.ListAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = []
    queryset = Organization.objects.filter(is_active=True).order_by("org_name")


class DashboardView(generics.RetrieveAPIView):
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "Registration successful. Your role request is pending Super Admin approval.",
                "user": {
                    "id": user.id,
                    "organization_id": user.organization_id,
                    "employee_code": user.employee_code,
                    "full_name": user.full_name,
                    "email": user.email,
                    "phone": user.phone,
                    "status": user.status,
                    "mfa_enabled": user.mfa_enabled,
                    "created_at": user.created_at,
                },
                "role_request": RoleRequestSerializer(
                    user.role_requests.latest("requested_at")
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "message": "Login endpoint. Use POST with email and password.",
                "next": request.GET.get("next"),
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            "email": request.data.get("email"),
            "password": request.data.get("password"),
        })
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email__iexact=request.data.get("email").strip())
        user.last_login_at = timezone.now()
        user.save(update_fields=["last_login_at"])
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Login successful.",
                "user": serializer.validated_data["user_data"],
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )


class RoleRequestListView(generics.ListAPIView):
    serializer_class = RoleRequestSerializer
    permission_classes = [HasPermission]
    required_permission = "ROLE_REQUEST_VIEW"
    queryset = RoleRequest.objects.select_related(
        "user", "requested_role", "reviewed_by"
    ).all()


class RoleRequestDetailView(generics.RetrieveAPIView):
    serializer_class = RoleRequestSerializer
    permission_classes = [HasPermission]
    required_permission = "ROLE_REQUEST_VIEW"
    queryset = RoleRequest.objects.select_related(
        "user", "requested_role", "reviewed_by"
    ).all()


class MyRoleRequestView(generics.ListAPIView):
    serializer_class = RoleRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RoleRequest.objects.select_related(
            "requested_role", "reviewed_by"
        ).filter(user=self.request.user)


class RoleRequestApproveView(APIView):
    permission_classes = [HasPermission]
    required_permission = "ROLE_REQUEST_APPROVE"

    def post(self, request, pk):
        with transaction.atomic():
            try:
                role_request = RoleRequest.objects.select_for_update().select_related(
                    "requested_role", "user"
                ).get(pk=pk)
            except RoleRequest.DoesNotExist:
                return Response({"detail": "Role request not found."}, status=404)

            if role_request.status != RoleRequest.Status.PENDING:
                return Response(
                    {"detail": "This role request has already been reviewed."},
                    status=status.HTTP_409_CONFLICT,
                )

            UserRole.objects.get_or_create(
                user=role_request.user,
                role=role_request.requested_role,
            )
            role_request.status = RoleRequest.Status.APPROVED
            role_request.reviewed_by = request.user
            role_request.reviewed_at = timezone.now()
            role_request.save(update_fields=["status", "reviewed_by", "reviewed_at"])

        return Response({
            "message": "Role request approved successfully.",
            "role_request": RoleRequestSerializer(role_request).data,
            "assigned_role": role_request.requested_role.code,
        })


class RoleRequestRejectView(APIView):
    permission_classes = [HasPermission]
    required_permission = "ROLE_REQUEST_REJECT"

    def post(self, request, pk):
        serializer = RoleRequestRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            try:
                role_request = RoleRequest.objects.select_for_update().select_related(
                    "requested_role", "user"
                ).get(pk=pk)
            except RoleRequest.DoesNotExist:
                return Response({"detail": "Role request not found."}, status=404)

            if role_request.status != RoleRequest.Status.PENDING:
                return Response(
                    {"detail": "This role request has already been reviewed."},
                    status=status.HTTP_409_CONFLICT,
                )

            role_request.status = RoleRequest.Status.REJECTED
            role_request.reviewed_by = request.user
            role_request.reviewed_at = timezone.now()
            role_request.remarks = serializer.validated_data.get("remarks", "")
            role_request.save(update_fields=[
                "status", "reviewed_by", "reviewed_at", "remarks"
            ])

        return Response({
            "message": "Role request rejected.",
            "role_request": RoleRequestSerializer(role_request).data,
        })
        
        
        
