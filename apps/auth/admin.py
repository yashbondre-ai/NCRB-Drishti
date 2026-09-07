from django.contrib import admin
from .models import (
    Organization,
    User,
    Role,
    UserRole,
    RoleRequest,
    Permission,
    RolePermission,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "org_code", "org_name", "org_type", "state", "is_active")
    list_filter = ("org_type", "is_active", "state")
    search_fields = ("org_code", "org_name", "contact_email")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "employee_code", "organization", "role", "status")
    list_filter = ("status", "role", "organization")
    search_fields = ("email", "full_name", "employee_code")
    readonly_fields = ("created_at", "updated_at", "last_login_at")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role", "assigned_at")
    list_filter = ("role",)
    search_fields = ("user__email", "role__name", "role__code")


@admin.register(RoleRequest)
class RoleRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "requested_role", "status", "requested_at", "reviewed_by")
    list_filter = ("status", "requested_role")
    search_fields = ("user__email", "user__employee_code", "requested_role__code")


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "permission")
    list_filter = ("role", "permission")
    search_fields = ("role__code", "permission__code")
