from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    """
    Allows access only when the authenticated user has
    the required RBAC permission.
    """

    required_permission = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        permission_code = getattr(
            view,
            "required_permission",
            self.required_permission
        )

        if not permission_code:
            return False

        return request.user.user_roles.filter(
            role__is_active=True,
            role__role_permissions__permission__code=permission_code,
            role__role_permissions__permission__is_active=True,
        ).exists()