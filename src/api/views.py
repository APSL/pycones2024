from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.permissions import CourierPermission, PostalClerkPermission
from api.serializers import (
    PackageInSerializer,
    PackageCreatedSerializer,
    PackageSerializer,
    TrackingHistoryInSerializer,
    PackageArchiveSerializer,
)
from core.models import Package, TrackingHistory


class AnonPackagesViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.filter(status=1)
    lookup_field = "tracking_number"
    serializer_class = PackageSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Package Detail.",
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
        """
        Gets the complete detail of a package by tracking number.
        """
        return super().retrieve(request, *args, **kwargs)


class CourierTrackingViewSet(viewsets.GenericViewSet):
    queryset = TrackingHistory.objects.filter(package__status=1)
    permission_classes = (CourierPermission,)

    @extend_schema(
        summary="Create new history entry for a package.",
        request=TrackingHistoryInSerializer,
        examples=TrackingHistoryInSerializer.examples(),
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(description="Create new tracking story."),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Unauthorized."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="No permissions."),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(description="Package not found."),
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Create a tracking status for a package.
        """
        package = Package.objects.get(tracking_number=kwargs.pop("tracking_number"))
        data = {"package": package.id}
        data.update(request.data)
        serializer = TrackingHistoryInSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostalClerkPackagesViewSet(viewsets.ModelViewSet):
    queryset = Package.objects
    lookup_field = "tracking_number"
    permission_classes = (PostalClerkPermission,)

    def get_serializer_class(self):
        match self.request.method:
            case "POST":
                return PackageInSerializer
            case "PATCH":
                return PackageArchiveSerializer
        return PackageSerializer

    @extend_schema(
        summary="Create new package with default started history.",
        request=PackageInSerializer,
        examples=PackageInSerializer.examples(),
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
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new package and two addresses to track the package.
        """
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
        deprecated=True,
        summary="Remove a package.",
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
        """
        Logical delete of package in cascade.
        """
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Logical delete of package.",
        request=None,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Package successfully archived.",
                response=PackageArchiveSerializer,
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Unauthorized."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="No permissions."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="No Package matches the given query."),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        """Archive a package.

        An archived package is equivalent to a **logical deletion**.

        Turn `is_active = False` and sets `deactivate_date`.
        """
        request.data.update({"status": 0, "deactivate_date": timezone.now()})
        return super().partial_update(request, *args, **kwargs)
