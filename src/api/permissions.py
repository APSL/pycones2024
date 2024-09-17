from rest_framework.permissions import BasePermission

from core import enums


class PostalClerkPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=enums.Permissions.POSTAL_CLERK).exists()


class CourierPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=enums.Permissions.COURIER).exists()
