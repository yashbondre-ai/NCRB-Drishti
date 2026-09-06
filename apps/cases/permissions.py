from rest_framework.permissions import BasePermission


def _role(user):
    return str(getattr(user, 'role', '')).upper()


def is_admin_user(user):
    return bool(user and user.is_authenticated and (_role(user) == 'ADMIN' or user.is_superuser))


class IsAdminOrOfficer(BasePermission):
    """Allow case creation and editing to administrators and officers."""

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated
            and _role(request.user) in {'ADMIN', 'OFFICER'}
        )


class CanEditCase(BasePermission):
    """Allow administrators or officers responsible for a case to edit it."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if is_admin_user(user):
            return True
        return _role(user) == 'OFFICER' and (
            obj.assigned_officer == user or obj.created_by == user
        )


class IsAdminUser(BasePermission):
    """Allow only administrators to delete cases."""

    def has_permission(self, request, view):
        return is_admin_user(request.user)
