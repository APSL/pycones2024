from django.contrib import admin

from core.models import Address, Package, TrackingHistory


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "street_address",
        "city",
        "state",
        "postal_code",
        "country",
    )


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "tracking_number",
        "created",
        "modified",
        "status",
        "activate_date",
        "deactivate_date",
        "origin_address",
        "destination_address",
    )
    list_filter = (
        "status",
        "created",
        "modified",
        "activate_date",
        "deactivate_date",
        "origin_address",
        "destination_address",
    )
    search_fields = ("tracking_number",)


@admin.register(TrackingHistory)
class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "package", "location", "timestamp")
    list_filter = ("package", "timestamp")
