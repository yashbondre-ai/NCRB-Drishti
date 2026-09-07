from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
<<<<<<< HEAD
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
=======
>>>>>>> 12ae628cce659f21e1111b535650f8ce5843efc5

from .models import Organization, Role, RoleRequest


User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = [
            "id",
            "org_code",
            "org_name",
            "org_type",
            "jurisdiction_code",
            "state",
            "district",
            "address",
            "contact_email",
            "contact_phone",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_org_code(self, value):
        value = value.strip().upper()

        if Organization.objects.filter(
            org_code__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "An organization with this code already exists."
            )

        return value

    def validate_org_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Organization name is required."
            )

        return value


class RegisterSerializer(serializers.ModelSerializer):

    requested_role = serializers.CharField(write_only=True, required=True)

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User

        fields = [
            "organization",
            "employee_code",
            "full_name",
            "email",
            "phone",
            "password",
            "confirm_password",
            "requested_role",
        ]

        extra_kwargs = {
            "organization": {
                "required": True,
            },
            "employee_code": {
                "required": True,
            },
            "full_name": {
                "required": True,
            },
            "email": {
                "required": True,
            },
        }

    def validate_email(self, value):
        value = value.lower().strip()

        if User.objects.filter(
            email__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return value

    def validate_employee_code(self, value):
        value = value.strip().upper()

        if User.objects.filter(
            employee_code__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "An account with this employee code already exists."
            )

        return value

    def validate_full_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Full name is required."
            )

        return value

    def validate_phone(self, value):
        if not value:
            return value

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if len(value) < 10 or len(value) > 20:
            raise serializers.ValidationError(
                "Phone number must contain between 10 and 20 digits."
            )

        return value

    def validate_organization(self, value):
        if not value.is_active:
            raise serializers.ValidationError(
                "This organization is currently inactive."
            )

        return value

    def validate_requested_role(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError("Requested role is required.")
        if value == Role.RoleCode.SUPER_ADMIN:
            raise serializers.ValidationError(
                "SUPER_ADMIN requires administrator approval or administrative creation."
            )

        role = Role.objects.filter(code=value, is_active=True).first()
        if not role:
            if Role.objects.filter(code=value).exists():
                raise serializers.ValidationError("This role is currently inactive.")
            raise serializers.ValidationError("Invalid requested role.")
        return role

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        password = validated_data.pop("password")
        requested_role = validated_data.pop("requested_role")

        with transaction.atomic():
            user = User.objects.create_user(password=password, **validated_data)
            RoleRequest.objects.create(user=user, requested_role=requested_role)

        return user
<<<<<<< HEAD


class RoleRequestSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="user_id", read_only=True)
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    organization = serializers.CharField(source="user.organization.org_name", read_only=True)
    requested_role = serializers.CharField(source="requested_role.code", read_only=True)
    reviewed_by = serializers.IntegerField(source="reviewed_by_id", read_only=True)

    class Meta:
        model = RoleRequest
        fields = [
            "id", "user", "user_name", "user_email", "organization",
            "requested_role", "status", "requested_at",
            "reviewed_by", "reviewed_at", "remarks",
        ]
        read_only_fields = fields


class RoleRequestRejectSerializer(serializers.Serializer):
    remarks = serializers.CharField(required=False, allow_blank=True)


class ActiveRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["code", "name"]


class DashboardSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source="organization.org_name", read_only=True)
    assigned_roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    role_request = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "organization", "assigned_roles", "permissions", "role_request"]

    def get_assigned_roles(self, user):
        return list(user.user_roles.filter(role__is_active=True).values_list("role__code", flat=True))

    def get_permissions(self, user):
        return list(user.user_roles.filter(
            role__is_active=True,
            role__role_permissions__permission__is_active=True,
        ).values_list("role__role_permissions__permission__code", flat=True).distinct())

    def get_role_request(self, user):
        request = user.role_requests.select_related("requested_role").first()
        if not request:
            return None
        return {
            "requested_role": request.requested_role.code,
            "status": request.status,
            "remarks": request.remarks,
        }
    
    
    
    
    
   
=======
>>>>>>> 12ae628cce659f21e1111b535650f8ce5843efc5


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                "Email and password are required."
            )

        email = email.lower().strip()

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if user.status != User.Status.ACTIVE:
            raise serializers.ValidationError(
                f"Account is {user.status.lower()}. Please contact your administrator."
            )

        attrs["user"] = user
        attrs["user_data"] = {
            "id": user.id,
            "organization_id": user.organization_id,
            "employee_code": user.employee_code,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "status": user.status,
            "mfa_enabled": user.mfa_enabled,
        }
        return attrs
