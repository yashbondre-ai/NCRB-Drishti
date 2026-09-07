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

        is_active = extra_fields.pop("is_active", None)
        if is_active is not None and "status" not in extra_fields:
            extra_fields["status"] = User.Status.ACTIVE if is_active else User.Status.DEACTIVATED

        user = self.model(
            email=email,
            **extra_fields
        )

        if password:
            user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

<<<<<<< HEAD
        is_active = extra_fields.pop("is_active", True)
        extra_fields.setdefault("status", User.Status.ACTIVE if is_active else User.Status.DEACTIVATED)
        extra_fields.setdefault("role", User.Role.ADMIN)
=======
        extra_fields.pop("is_active", None)
        extra_fields.setdefault("status", self.model.Status.ACTIVE)
        extra_fields.setdefault("role", self.model.Role.ADMIN)
>>>>>>> 12ae628cce659f21e1111b535650f8ce5843efc5

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        OFFICER = "OFFICER", "Officer"
        JUDGE = "JUDGE", "Judge"
        CLERK = "CLERK", "Clerk"
        FORENSIC = "FORENSIC", "Forensic"
        AUDITOR = "AUDITOR", "Auditor"

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

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OFFICER
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

    # AbstractBaseUser.last_login is not a DB column on this model.
    # Map it onto last_login_at so Django auth signals do not crash.
    @property
    def last_login(self):
        return self.last_login_at

    @last_login.setter
    def last_login(self, value):
        self.last_login_at = value

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
    def is_active(self):
        return self.status == self.Status.ACTIVE

    @is_active.setter
    def is_active(self, value):
<<<<<<< HEAD
        self.status = self.Status.ACTIVE if value else self.Status.DEACTIVATED

    @property
    def is_staff(self):
        if self.role == self.Role.ADMIN:
            return True
        if hasattr(self, "user_roles"):
            return self.user_roles.filter(
                role__code="SUPER_ADMIN",
                role__is_active=True
            ).exists()
        return False

    @property
    def is_superuser(self):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
=======
        if value:
            self.status = self.Status.ACTIVE
        elif self.status == self.Status.ACTIVE:
            self.status = self.Status.DEACTIVATED

    @property
    def is_staff(self):
        return self.role == self.Role.ADMIN

    @property
    def is_superuser(self):
        return self.role == self.Role.ADMIN

    def get_username(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields")
        if update_fields and "last_login" in update_fields:
            kwargs["update_fields"] = [
                "last_login_at" if field == "last_login" else field
                for field in update_fields
            ]
        super().save(*args, **kwargs)
>>>>>>> 12ae628cce659f21e1111b535650f8ce5843efc5

    def __str__(self):
        return self.email


class Role(models.Model):

    class RoleCode(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        DEPARTMENT_ADMIN = "DEPARTMENT_ADMIN", "Department Admin"
        INVESTIGATION_OFFICER = "INVESTIGATION_OFFICER", "Investigation Officer"
        CASE_OFFICER = "CASE_OFFICER", "Case Officer / Case Manager"
        LEGAL_OFFICER = "LEGAL_OFFICER", "Legal Officer"
        FORENSIC_OFFICER = "FORENSIC_OFFICER", "Evidence / Forensic Officer"
        REVIEWER = "REVIEWER", "Reviewer / Approver"
        AUDITOR = "AUDITOR", "Auditor"
        VIEWER = "VIEWER", "Viewer"

    id = models.BigAutoField(primary_key=True)
    code = models.CharField(
        max_length=30,
        choices=RoleCode.choices,
        unique=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "roles"
        ordering = ["id"]

    def __str__(self):
        return self.name


class UserRole(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_roles",
        db_column="user_id"
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.RESTRICT,
        related_name="user_roles",
        db_column="role_id"
    )

    assigned_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "user_roles"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role"],
                name="unique_user_role"
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


class RoleRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="role_requests",
        db_column="user_id",
    )

    requested_role = models.ForeignKey(
        Role,
        on_delete=models.RESTRICT,
        related_name="role_requests",
        db_column="requested_role_id",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    requested_at = models.DateTimeField(default=timezone.now)

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="reviewed_role_requests",
        db_column="reviewed_by_id",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "role_requests"
        ordering = ["-requested_at"]
        indexes = [
            models.Index(fields=["status", "requested_at"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.requested_role.code} ({self.status})"
    


class Permission(models.Model):

    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "permissions"
        ordering = ["id"]

    def __str__(self):
        return self.code




class RolePermission(models.Model):

    id = models.BigAutoField(primary_key=True)

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_permissions",
        db_column="role_id"
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name="role_permissions",
        db_column="permission_id"
    )

    class Meta:
        db_table = "role_permissions"
        constraints = [
            models.UniqueConstraint(
                fields=["role", "permission"],
                name="unique_role_permission"
            )
        ]

    def __str__(self):
        return f"{self.role.code} - {self.permission.code}"