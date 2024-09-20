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


class CourierTrackingViewSet(viewsets.GenericViewSet):
    queryset = TrackingHistory.objects
    permission_classes = (CourierPermission,)

    def create(self, request, *args, **kwargs):
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
    serializer_class = PackageInSerializer
    permission_classes = (PostalClerkPermission,)

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
