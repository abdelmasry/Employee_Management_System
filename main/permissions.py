from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Custom permission to allow only Admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.role == "ADMIN"


class IsManagerUser(BasePermission):
    """
    Custom permission to allow only Manager users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.role == "MANAGER"


class IsEmployeeUser(BasePermission):
    """
    Custom permission to allow only Employee users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.role == "EMPLOYEE"
