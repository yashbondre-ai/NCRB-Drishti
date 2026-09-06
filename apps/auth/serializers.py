from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Organization


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

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user
    
    
    
    
    
   


class LoginSerializer(TokenObtainPairSerializer):

    username_field = "email"

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

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if user.status != User.Status.ACTIVE:
            raise serializers.ValidationError(
                f"Account is {user.status.lower()}. Please contact your administrator."
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        data = super().validate({
            "email": email,
            "password": password,
        })

        data["user"] = {
            "id": user.id,
            "organization_id": user.organization_id,
            "employee_code": user.employee_code,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "status": user.status,
            "mfa_enabled": user.mfa_enabled,
        }

        return data