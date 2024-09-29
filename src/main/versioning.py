from rest_framework.versioning import BaseVersioning


class XAPIVersionScheme(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        return request.META.get("HTTP_X_API_VERSION", None)
