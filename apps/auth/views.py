from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Organization
from .permissions import HasPermission
from .serializers import (
    OrganizationSerializer,
    RegisterSerializer,
    LoginSerializer,
)


class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all().order_by("id")
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "ORG_VIEW"


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
                "message": "Registration successful.",
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
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
