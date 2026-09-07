from django.contrib import admin

from .models import Organization, Permission, Role, RolePermission, User, UserRole


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["org_code", "org_name", "org_type", "is_active", "created_at"]
    search_fields = ["org_code", "org_name"]
    list_filter = ["org_type", "is_active"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "full_name", "role", "status", "organization"]
    search_fields = ["email", "full_name", "employee_code"]
    list_filter = ["role", "status"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "is_active"]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "is_active"]


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "assigned_at"]


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ["role", "permission"]
