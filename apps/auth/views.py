from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Organization, User
from .serializers import (
    OrganizationSerializer,
    RegisterSerializer,
    LoginSerializer,
)




from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .permissions import HasPermission

class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all().order_by("id")
    serializer_class = OrganizationSerializer
    permission_classes = [HasPermission]
    required_permission = "ORG_VIEW"

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            "email": request.data.get("email"),
            "password": request.data.get("password"),
        })

        serializer.is_valid(raise_exception=True)

        user = User.objects.get(
            email__iexact=request.data.get("email").strip()
        )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful.",
                "user": serializer.validated_data["user"],
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )
        
        
        
