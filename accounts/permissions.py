from rest_framework.permissions import (
    DjangoModelPermissions, IsAdminUser, BasePermission, SAFE_METHODS)


class IsAdminOrReadOnly(BasePermission):
    message = "You do not have the permission to perform this action"

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or ((request.user.is_superuser) and
                                                       request.user.is_authenticated))

