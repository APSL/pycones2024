from django.urls import path

from api.views import PostalClerkPackagesViewSet, AnonPackagesViewSet, CourierTrackingViewSet

app_name = "api"
urlpatterns = [
    path(
        "postal-clerk/packages/",
        PostalClerkPackagesViewSet.as_view({"post": "create"}),
    ),
    path(
        "postal-clerk/packages/<str:tracking_number>/",
        PostalClerkPackagesViewSet.as_view({"delete": "destroy"}),
    ),
]
