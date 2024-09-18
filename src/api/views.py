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
        raise NotImplementedError("Not implemented yet")


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
