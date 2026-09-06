from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class Organization(models.Model):

    class OrganizationType(models.TextChoices):
        POLICE_STATION = "POLICE_STATION", "Police Station"
        COURT = "COURT", "Court"
        NCRB = "NCRB", "NCRB"
        FORENSIC_LAB = "FORENSIC_LAB", "Forensic Lab"
        LEGAL_DEPT = "LEGAL_DEPT", "Legal Department"

    id = models.BigAutoField(
        primary_key=True
    )

    org_code = models.CharField(
        max_length=30
    )

    org_name = models.CharField(
        max_length=150
    )

    org_type = models.CharField(
        max_length=20,
        choices=OrganizationType.choices
    )

    jurisdiction_code = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    state = models.CharField(
        max_length=60,
        null=True,
        blank=True
    )

    district = models.CharField(
        max_length=60,
        null=True,
        blank=True
    )

    address = models.TextField(
        null=True,
        blank=True
    )

    contact_email = models.CharField(
        max_length=120,
        null=True,
        blank=True
    )

    contact_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    updated_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        db_table = "organizations"

    def __str__(self):
        return f"{self.org_code} - {self.org_name}"


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        if password:
            user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"
        DEACTIVATED = "DEACTIVATED", "Deactivated"

    # Required database primary key
    id = models.BigAutoField(
        primary_key=True
    )

    # Organization relationship
    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        related_name="users",
        db_column="organization_id"
    )

    employee_code = models.CharField(
        max_length=40
    )

    full_name = models.CharField(
        max_length=120
    )

    email = models.EmailField(
        max_length=120,
        unique=True
    )

    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    # Django's password field mapped to required DB column
    password = models.CharField(
        max_length=255,
        db_column="password_hash"
    )

    mfa_enabled = models.BooleanField(
        default=False
    )

    mfa_secret_encrypted = models.BinaryField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    last_login_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    updated_at = models.DateTimeField(
        default=timezone.now
    )

    # Django authentication needs this property,
    # but we don't want a last_login database column.
    @property
    def last_login(self):
        return None

    @last_login.setter
    def last_login(self, value):
        pass

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "organization",
        "employee_code",
        "full_name",
    ]

    objects = UserManager()

    class Meta:
        db_table = "users"

    @property
    def is_staff(self):
        return False

    @property
    def is_superuser(self):
        return False

    def __str__(self):
        return self.email