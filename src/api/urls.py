from django.urls import path, include

from api.views import PostalClerkPackagesViewSet, AnonPackagesViewSet, CourierTrackingViewSet

app_name = "api"
urlpatterns = [
    path("auth/", include(("auth.urls", "auth"))),
    path(
        "public/packages/<str:tracking_number>/",
        AnonPackagesViewSet.as_view({"get": "retrieve"}),
    ),
    # courier
    path(
        "courier/packages/<str:tracking_number>/tracking/",
        CourierTrackingViewSet.as_view({"post": "create"}),
    ),
    # clerk / admin
    path(
        "public/packages/<str:tracking_number>/",
        AnonPackagesViewSet.as_view({"get": "retrieve"}),
    ),
    # courier
    path(
        "courier/packages/<str:tracking_number>/tracking/",
        CourierTrackingViewSet.as_view({"post": "create"}),
    ),
    # clerk / admin
    path(
        "postal-clerk/packages/",
        PostalClerkPackagesViewSet.as_view({"post": "create"}),
    ),
    path(
        "postal-clerk/packages/<str:tracking_number>/",
        PostalClerkPackagesViewSet.as_view({"delete": "destroy"}),
    ),
]
