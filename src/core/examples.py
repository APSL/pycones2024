"""
Esta clase contiene código que no quiero visible en el taller en el momento de la explicación de los serializadores.
Mis apologizes :3
"""

from typing import List

from drf_spectacular.utils import OpenApiExample


class TrackingHistoryInExamples:
    @staticmethod
    def examples() -> List[OpenApiExample]:
        return [
            OpenApiExample(
                name="Pick-up",
                value={
                    "text": "Pick-up / Driver’s Pick-up.",
                },
            ),
            OpenApiExample(
                name="Shipment",
                value={
                    "text": "Shipment departed from the facility.",
                },
            ),
            OpenApiExample(
                name="In transit",
                value={
                    "text": "In transit.",
                },
            ),
            OpenApiExample(
                name="Hub scan",
                value={
                    "text": "Hub scan.",
                },
            ),
            OpenApiExample(
                name="Warehouse",
                value={
                    "text": "Shipment ready for dispatch from a warehouse, parcel outbound from transit facility.",
                },
            ),
            OpenApiExample(
                name="Delivered",
                value={
                    "text": "Delivered, POD Available.",
                },
            ),
        ]


class TrackingHistoryExamples:
    @staticmethod
    def examples() -> List[OpenApiExample]:
        return [
            OpenApiExample(
                name="Pick-up",
                value={
                    "text": "Pick-up / Driver’s Pick-up.",
                    "timestamp": "2024-09-05T15:44:19.724065Z",
                },
            ),
        ]


class PackageExamples:
    @staticmethod
    def examples() -> List[OpenApiExample]:
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
                            "text": "Info received/Registered parcel data, parcel not dispatched yet / Pre-advice",
                            "timestamp": "2024-09-05T15:43:26.838273Z",
                        }
                    ],
                },
            )
        ]


class PackageInExamples:
    @staticmethod
    def examples() -> List[OpenApiExample]:
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


class PackageCreatedExamples:
    @staticmethod
    def examples() -> List[OpenApiExample]:
        return [
            OpenApiExample(
                name="Example",
                value={
                    "tracking_number": "hYHnBAIy",
                },
            )
        ]
