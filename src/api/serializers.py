from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers

from core.models import Address, Package, TrackingHistory


class AddressRelatedSerializer(serializers.ModelSerializer):
    """Origin and destination addresses of a Package and PackageIn."""

    class Meta:
        model = Address
        fields = ["street_address", "city", "state", "postal_code", "country"]


class TrackingHistoryLineSerializer(serializers.ModelSerializer):
    """Lines of tracking history of a Package and PackageCreated."""

    class Meta:
        model = TrackingHistory
        fields = ["location", "timestamp"]


class TrackingHistoryInSerializer(serializers.ModelSerializer):
    """Tracking history to log location of the package."""

    class Meta:
        model = TrackingHistory
        fields = ["package", "location", "timestamp"]

    @staticmethod
    def examples() -> list[OpenApiExample]:
        return [
            OpenApiExample(
                name="Pick-up",
                value={
                    "location": "Pick-up / Driver’s Pick-up.",
                },
            ),
            OpenApiExample(
                name="Shipment",
                value={
                    "location": "Shipment departed from the facility.",
                },
            ),
            OpenApiExample(
                name="In transit",
                value={
                    "location": "In transit.",
                },
            ),
            OpenApiExample(
                name="Hub scan",
                value={
                    "location": "Hub scan.",
                },
            ),
            OpenApiExample(
                name="Warehouse",
                value={
                    "location": "Shipment ready for dispatch from a warehouse, parcel outbound from transit facility.",
                },
            ),
            OpenApiExample(
                name="Delivered",
                value={
                    "location": "Delivered, POD Available.",
                },
            ),
        ]


class PackageArchiveSerializer(serializers.ModelSerializer):
    """Archive a package with tracking number."""
    pass


class PackageSerializer(serializers.ModelSerializer):
    """A complete package model."""

    origin_address = AddressRelatedSerializer()
    destination_address = AddressRelatedSerializer()
    tracking_history = TrackingHistoryLineSerializer(many=True)

    class Meta:
        model = Package
        fields = ["origin_address", "destination_address", "tracking_number", "created", "tracking_history"]

    @staticmethod
    def examples() -> list[OpenApiExample]:
        return [
            OpenApiExample(
                name="Example",
                value={
                    "tracking_number": "hYHnBAIy",
                    "created": "2024-09-05T15:44:19.724065Z",
                    "origin_address": {
                        "street_address": "Avenida de Beiramar, 51",
                        "city": "Vigo",
                        "state": "Pontevedra",
                        "postal_code": "36202",
                        "country": "España",
                    },
                    "destination_address": {
                        "street_address": "Av. del Dr. Peset Aleixandre, 12",
                        "city": "Valencia",
                        "state": "Valenciag",
                        "postal_code": "46019",
                        "country": "España",
                    },
                    "tracking_history": [
                        {
                            "location": "Info received/Registered parcel data, parcel not dispatched yet / Pre-advice",
                            "timestamp": "2024-09-05T15:43:26.838273Z",
                        }
                    ],
                },
            )
        ]


class PackageInSerializer(serializers.ModelSerializer):
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

    @staticmethod
    def examples() -> list[OpenApiExample]:
        return [
            OpenApiExample(
                name="Example",
                value={
                    "origin_address": {
                        "street_address": "Avenida de Beiramar, 51",
                        "city": "Vigo",
                        "state": "Pontevedra",
                        "postal_code": "36202",
                        "country": "España",
                    },
                    "destination_address": {
                        "street_address": "Av. del Dr. Peset Aleixandre, 12",
                        "city": "Valencia",
                        "state": "Valenciag",
                        "postal_code": "46019",
                        "country": "España",
                    },
                },
            )
        ]


class PackageCreatedSerializer(serializers.ModelSerializer):
    """Output to retrieve a created package."""

    tracking_history = TrackingHistoryLineSerializer(many=True)

    class Meta:
        model = Package
        fields = ["tracking_number", "tracking_history"]

    @staticmethod
    def examples() -> list[OpenApiExample]:
        return [
            OpenApiExample(
                name="Example",
                value={
                    "tracking_number": "hYHnBAIy",
                    "tracking_history": [
                        {
                            "location": "Info received/Registered parcel data, parcel not dispatched yet / Pre-advice",
                            "timestamp": "2024-09-05T15:44:19.724065Z",
                        }
                    ],
                },
            )
        ]
