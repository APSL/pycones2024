from django.http import JsonResponse
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiParameter
from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from api.serializers import (
    PackageInSerializer,
    PackageSerializer,
    TrackingHistoryInSerializer,
    PackageCreatedSerializer,
    TrackingHistorySerializer,
)
from core.models import Package, TrackingHistory


class IsCourier(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="Courier").exists()


class IsPostalClerk(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="Postal clerk").exists()


class AnonPackagesViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.filter(status=Package.ACTIVE_STATUS)
    lookup_field = "tracking_number"
    serializer_class = PackageSerializer
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        summary="Package Detail.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Gets the complete detail of package.",
                response=PackageSerializer,
                examples=PackageSerializer.examples(),
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="No Package matches the given query."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a _active package_ instance by **tracking number**.
        * param request:
        * param args:
        * param kwargs:
        * return: serialized package
        """
        return super().retrieve(request, *args, **kwargs)


class CourierTrackingViewSet(viewsets.ModelViewSet):
    queryset = TrackingHistory.objects.all()
    lookup_field = "tracking_number"
    serializer_class = TrackingHistoryInSerializer
    permission_classes = (IsCourier,)

    @extend_schema(
        summary="Create new history entry for a package.",
        request=TrackingHistoryInSerializer,
        examples=TrackingHistoryInSerializer.examples(),
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(description="Create new tracking story for the package."),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Probably JSON parse error or required field is missing."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="You do not have permission."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Package not found."),
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new history entry for a package.
        * param request:
        * param args:
        * param kwargs:
        * return: serialized tracking history
        """
        serializer_in = self.get_serializer(data=request.data)
        if serializer_in.is_valid():
            package = get_object_or_404(
                Package.objects.filter(status=Package.ACTIVE_STATUS), tracking_number=kwargs["tracking_number"]
            )
            data = serializer_in.validated_data.copy()
            data["package"] = package.id
            serializer = TrackingHistorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer_in.errors, status=status.HTTP_400_BAD_REQUEST)


class PostalClerkPackagesViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.filter(status=Package.ACTIVE_STATUS)
    lookup_field = "tracking_number"
    serializer_class = PackageInSerializer
    permission_classes = (IsPostalClerk,)

    @extend_schema(
        summary="Create new package.",
        request=PackageInSerializer,
        examples=PackageInSerializer.examples(),
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Gets the tracking number of the created package.",
                response=PackageCreatedSerializer,
                examples=PackageCreatedSerializer.examples(),
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Probably JSON parse error or required field is missing."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="You do not have permission."),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            package = serializer.save()
            serializer_output = PackageCreatedSerializer(package)
            return JsonResponse(serializer_output.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Remove a package.",
        parameters=[
            OpenApiParameter(
                name="x-api-version",
                description="API version.",
                location=OpenApiParameter.HEADER,
                enum=["v1", "v2"],
                default="v2",
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Package successfully deleted.",
                response=None,
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="You do not have permission."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="No Package matches the given query."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        """
        Logical delete of a package. Actually disables a package.

        **IMPORTANT: v1 remove from database!**
        """
        if request.version == "v1":
            package = get_object_or_404(Package, tracking_number=kwargs["tracking_number"])
            package.delete()
            return JsonResponse(data={}, status=status.HTTP_204_NO_CONTENT)
        package = get_object_or_404(self.queryset, tracking_number=kwargs["tracking_number"])
        package.status = Package.INACTIVE_STATUS
        package.save()
        return JsonResponse(data={}, status=status.HTTP_204_NO_CONTENT)
