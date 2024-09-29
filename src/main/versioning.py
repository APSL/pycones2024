from django.conf import settings
from rest_framework.versioning import BaseVersioning


class XAPIVersionScheme(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        pass
