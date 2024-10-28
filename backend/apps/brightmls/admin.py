from django.contrib import admin
from brightmls import models as bright_models
from backend.core.admin import ViewOnlyAdminMixin


@admin.register(bright_models.Lookup)
class LookupAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "lookup_key",
        "lookup_name",
        "lookup_value",
        "standard_lookup_value",
        "legacy_odata_value",
        "modification_timestamp",
    ]
    list_filter = ["lookup_name"]
    search_fields = [
        "lookup_key",
        "lookup_value",
    ]


@admin.register(bright_models.RelatedLookup)
class RelatedLookupAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    """
    related_lookup_key = models.BigIntegerField(primary_key=True)
    lookup_key = models.ForeignKey(Lookup, on_delete=models.CASCADE)
    modification_timestamp = models.DateTimeField(null=True)
    """

    list_display = [
        "related_lookup_key",
        "lookup_key",
        "modification_timestamp",
    ]


@admin.register(bright_models.City)
class CityAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "cty_city_key",
        "cty_city_name",
        "cty_city_county",
        "cty_city_type",
        "cty_city_towhnship",
        "cty_county_state",
        "cty_modification_timestamp",
    ]
    list_filter = ["cty_county_state", "cty_city_type"]
    search_fields = [
        "cty_city_key",
        "cty_city_name",
        "cty_city_county",
    ]


@admin.register(bright_models.CityZipCode)
class CityZipCodeAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "city_zip_code_key",
        "city_zip_code_city",
        "city_zip_code_city_name",
        "city_zip_code_county",
        "city_zip_code_state",
        "city_zip_code_zip",
        "city_zip_code_preferred_city",
        "city_zip_modification_timestamp",
    ]
    list_filter = ["city_zip_code_state", "city_zip_code_preferred_city"]
    search_fields = [
        "city_zip_code_key",
        "city_zip_code_city_name",
        "city_zip_code_zip",
    ]
