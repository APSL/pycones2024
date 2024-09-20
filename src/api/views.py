from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.permissions import CourierPermission, PostalClerkPermission
from api.serializers import (
    PackageInSerializer,
    PackageCreatedSerializer,
    PackageSerializer,
    TrackingHistoryInSerializer,
)
from core.models import Package, TrackingHistory


class AnonPackagesViewSet(viewsets.ModelViewSet):
    queryset = Package.objects
    lookup_field = "tracking_number"
    serializer_class = PackageSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Package Detail.",
        description="Gets the complete detail of a package by tracking number.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Gets the complete detail of package.",
                response=PackageSerializer,
                examples=PackageSerializer.examples(),
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Unauthorized."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="No Package matches the given query."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CourierTrackingViewSet(viewsets.GenericViewSet):

    @extend_schema(
        summary="Tracking History Create.",
        description="Create a tracking status for a package.",
        request=TrackingHistoryInSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Create new tracking story.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Unauthorized."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="No permissions."),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(description="Package not found."),
        },
        examples=TrackingHistoryInSerializer.examples(),
    )
    def create(self, request, *args, **kwargs):
        pass


class PostalClerkPackagesViewSet(viewsets.ModelViewSet):
    queryset = Package.objects
    lookup_field = "tracking_number"
    serializer_class = PackageSerializer
    permission_classes = (PostalClerkPermission,)

    @extend_schema(
        summary="Package Create.",
        description="Create a new package and two addresses to track the package.",
        request=PackageInSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Gets the tracking number of the created package.",
                response=PackageCreatedSerializer,
                examples=PackageCreatedSerializer.examples(),
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad Request."),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Unauthorized."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="No permissions."),
        },
        examples=PackageInSerializer.examples(),
    )
    def create(self, request, *args, **kwargs):
        serializer = PackageInSerializer(data=request.data)
        if serializer.is_valid():
            package = serializer.save()
            history = TrackingHistory.objects.create(
                package=package,
                location="Info received / Registered parcel data, parcel not dispatched yet / Pre-advice",
            )
            history.save()
            data = PackageCreatedSerializer(package).data
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Package Destroy.",
        description="Logical delete of package in cascade.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Package successfully deleted.",
                response=PackageSerializer,
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Unauthorized."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="No permissions."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="No Package matches the given query."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
