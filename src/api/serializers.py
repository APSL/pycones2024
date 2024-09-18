from rest_framework import serializers

from core.examples import PackageInExamples, PackageExamples, TrackingHistoryInExamples
from core.models import Address, Package, TrackingHistory


class AddressRelatedSerializer(serializers.ModelSerializer):
    """Origin and destination addresses of a Package and PackageIn."""

    class Meta:
        model = Address
        fields = ["street_address", "city", "state", "postal_code", "country"]


class TrackingHistoryInSerializer(serializers.ModelSerializer, TrackingHistoryInExamples):
    """Tracking history to log text of the package."""

    class Meta:
        model = TrackingHistory
        fields = ["package", "text"]


class TrackingHistoryLineSerializer(serializers.ModelSerializer):
    """Lines of tracking history of a Package and PackageCreated."""

    class Meta:
        model = TrackingHistory
        fields = ["text", "timestamp"]


class PackageSerializer(serializers.ModelSerializer, PackageExamples):
    """A complete package model."""

    origin_address = AddressRelatedSerializer()
    destination_address = AddressRelatedSerializer()
    tracking_history = TrackingHistoryLineSerializer(many=True)

    class Meta:
        model = Package
        fields = ["origin_address", "destination_address", "tracking_number", "created", "tracking_history"]


class PackageInSerializer(serializers.ModelSerializer, PackageInExamples):
    """Input to create a new package."""

    origin_address = AddressRelatedSerializer()
    destination_address = AddressRelatedSerializer()

    class Meta:
        model = Package
        fields = ["origin_address", "destination_address"]

    def create(self, validated_data):
        origin = AddressRelatedSerializer(data=validated_data.pop("origin_address"))
        destination = AddressRelatedSerializer(data=validated_data.pop("destination_address"))
        if origin.is_valid() and destination.is_valid():
            origin = Address.objects.create(**origin.validated_data)
            destination = Address.objects.create(**destination.validated_data)
            return Package.objects.create(**validated_data, origin_address=origin, destination_address=destination)
