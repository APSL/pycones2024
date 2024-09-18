from django.urls import path

from api.views import PostalClerkPackagesViewSet, AnonPackagesViewSet, CourierTrackingViewSet

app_name = "api"
urlpatterns = [
    #path(
    #    "public/packages/<str:tracking_number>/",
    #    AnonPackagesViewSet.as_view(),
    #    name="anon-packages-detail",
    #),
    # courier
    #path(
    #    "courier/packages/<str:tracking_number>/tracking/",
    #    CourierTrackingViewSet.as_view(),
    #    name="courier-packages-detail",
    #),
    # admin
    #path(
    #    "postal-clerk/packages/",
    #    PostalClerkPackagesViewSet.as_view(),
    #    name="admin-packages",
    #),
    path(
        "postal-clerk/packages/<str:tracking_number>/",
        PostalClerkPackagesViewSet.as_view({"delete": "destroy"}),
        name="admin-packages-delete",
    ),
]
