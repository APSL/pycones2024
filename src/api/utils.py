from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def open_api_urls(version: str) -> list:
    """Adds path `schema/` to swagger-ui and `schema/download/` to download schema file"""
    return [
        path("schema/", SpectacularSwaggerView.as_view(url_name=f"api:{version}:schema"), name="swagger-ui"),
        path("schema/download/", SpectacularAPIView.as_view(), name="schema"),
        path("auth/", include(("auth.urls", "auth"))),
    ]
