from django.http import JsonResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from api.serializers import (
    PackageInSerializer,
    PackageSerializer,
    TrackingHistoryInSerializer,
    PackageCreatedSerializer,
)
from core.models import Package, TrackingHistory


class AnonPackagesViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.filter(status=Package.ACTIVE_STATUS)
    lookup_field = "tracking_number"
    serializer_class = PackageSerializer


class CourierTrackingViewSet(viewsets.ModelViewSet):
    queryset = TrackingHistory.objects.all()
    lookup_field = "tracking_number"
    serializer_class = TrackingHistoryInSerializer

    def create(self, request, *args, **kwargs):
        package = get_object_or_404(
            Package.objects.filter(status=Package.ACTIVE_STATUS), tracking_number=kwargs["tracking_number"]
        )
        data = request.data.copy()
        data["package"] = package.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostalClerkPackagesViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    lookup_field = "tracking_number"
    serializer_class = PackageInSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            package = serializer.save()
            output = {"tracking_number": package.tracking_number}
            return JsonResponse(output, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
