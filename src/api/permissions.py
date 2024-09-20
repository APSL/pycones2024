from rest_framework.permissions import BasePermission

from core import enums


class PostalClerkPermission(BasePermission):
    def has_permission(self, request, view):
        raise NotImplementedError("not implemented")


class CourierPermission(BasePermission):
    def has_permission(self, request, view):
        raise NotImplementedError("not implemented")
