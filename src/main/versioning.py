from django.conf import settings
from rest_framework.versioning import BaseVersioning


class XAPIVersionScheme(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        default = settings.REST_FRAMEWORK.get("DEFAULT_VERSION", None)
        return request.META.get("HTTP_X_API_VERSION", default)
