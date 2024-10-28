from django.db import models

# Create your models here.

from django.db import models
from django.utils.dateparse import parse_datetime


from django.db import models
from django.utils.dateparse import parse_datetime


class BaseModel(models.Model):
    """
    Base model that provides a generic from_python_odata method
    to map data from a python_odata entity to Django model fields.

    usage: instance = AnyModel.from_python_odata(odata_entity_object)
    """

    class Meta:
        abstract = True

    @classmethod
    def from_python_odata(cls, odata_obj):
        """
        Generic method to map python_odata entity fields to Django model fields.
        Automatically matches fields based on name.
        """
        field_values = {}
        for field in cls._meta.get_fields():
            field_name = field.name
            # Map python_odata field to the model field if it exists in the odata object
            odata_field = cls._map_field_name_to_odata(field_name)
            if hasattr(odata_obj, odata_field):
                value = getattr(odata_obj, odata_field)

                # Parse datetime fields if necessary (if returned as a string from odata)
                if isinstance(field, models.DateTimeField) and isinstance(value, str):
                    field_values[field_name] = parse_datetime(value)

                elif isinstance(field, models.ForeignKey) and isinstance(value, int):
                    print(">>>>>>> ForeignKey field found")
                    # Handle foreign key relationships
                    related_model = field.related_model
                    # print(">>>>>>> Related model:", related_model)
                    related_key = getattr(odata_obj, odata_field, None)
                    # print(">>>>>>> Related key:", related_key)
                    if related_key:
                        # find primary key from the related model
                        primary_key_field = related_model._meta.pk
                        # print(">>>>>>> Primary key field:", primary_key_field.name)

                        related_instance = related_model.objects.filter(
                            **{primary_key_field.name: related_key}
                        ).first()
                        # print(">>>>>>> Related instance:", related_instance)
                        field_values[field_name] = related_instance
                else:
                    field_values[field_name] = value

        return cls(**field_values)

    @staticmethod
    def _map_field_name_to_odata(field_name):
        """
        Map Django model field names (snake_case) to odata field names (CamelCase).
        """
        return "".join([word.capitalize() for word in field_name.split("_")])


class Lookup(BaseModel):
    lookup_key = models.CharField(max_length=15, primary_key=True)
    lookup_name = models.CharField(max_length=64, null=True)
    lookup_value = models.CharField(max_length=1024, null=True)
    standard_lookup_value = models.CharField(max_length=1024, null=True)
    legacy_odata_value = models.CharField(max_length=20, null=True)
    modification_timestamp = models.DateTimeField(null=True)

    class Meta:
        ordering = ["lookup_name", "lookup_value"]
        indexes = [
            models.Index(fields=["lookup_key"]),
            models.Index(fields=["lookup_name"]),
            models.Index(fields=["lookup_value"]),
            models.Index(fields=["lookup_name", "lookup_value"]),
        ]

    def __str__(self):
        return str(self.lookup_value)


class RelatedLookup(BaseModel):
    related_lookup_key = models.BigIntegerField(
        help_text="I do not know what this field is, "
        "it is not unique and not a foreign key of any Lookup. "
        "It is not used in RESO 1.7 too"
    )
    lookup_key = models.ForeignKey(Lookup, on_delete=models.CASCADE)
    modification_timestamp = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["related_lookup_key"]),
            models.Index(fields=["lookup_key"]),
        ]

    def __str__(self):
        return f"Related Lookup {self.lookup_key}"


class City(BaseModel):
    cty_city_key = models.BigIntegerField(primary_key=True)
    cty_city_name = models.CharField(max_length=50, null=True)
    cty_city_county = models.CharField(max_length=255, null=True)
    cty_city_type = models.CharField(max_length=255, null=True)
    cty_city_towhnship = models.IntegerField(null=True)
    cty_county_state = models.CharField(max_length=255, null=True)
    cty_modification_timestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ["cty_city_key"]
        indexes = [
            models.Index(fields=["cty_city_name"]),
            models.Index(fields=["cty_city_county"]),
            models.Index(fields=["cty_city_type"]),
            models.Index(fields=["cty_county_state"]),
        ]

    def __str__(self):
        return self.cty_city_name


class CityZipCode(BaseModel):
    city_zip_code_key = models.BigIntegerField(primary_key=True)
    city_zip_code_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    city_zip_code_city_name = models.CharField(max_length=50, null=True)
    city_zip_code_county = models.CharField(max_length=255, null=True)
    city_zip_code_state = models.CharField(max_length=255, null=True)
    city_zip_code_zip = models.CharField(max_length=5, null=True)
    city_zip_code_preferred_city = models.BooleanField(null=True)
    city_zip_modification_timestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "City Zip Codes"
        ordering = ["city_zip_code_key"]
        indexes = [
            models.Index(fields=["city_zip_code_city_name"]),
            models.Index(fields=["city_zip_code_county"]),
            models.Index(fields=["city_zip_code_state"]),
            models.Index(fields=["city_zip_code_zip"]),
        ]

    def __str__(self):
        return str(self.city_zip_code_zip)


# class BrightMedia(BaseModel):
#     media_key = models.BigIntegerField(primary_key=True)
#     location = models.JSONField(
#         null=True
#     )  # Assuming geoPoint is a complex object, stored as JSON
#     property_type = models.CharField(max_length=255, null=True)
#     county = models.CharField(max_length=255, null=True)
#     media_bytes = models.BigIntegerField(null=True)
#     media_category = models.CharField(max_length=255, null=True)
#     media_creation_timestamp = models.DateTimeField(null=True)
#     media_external_key = models.CharField(max_length=20, null=True)
#     media_file_name = models.CharField(max_length=3000, null=True)
#     media_image_of = models.CharField(max_length=255, null=True)
#     media_item_number = models.SmallIntegerField(null=True)
#     media_long_description = models.CharField(max_length=1024, null=True)
#     media_modification_timestamp = models.DateTimeField(null=True)
#     media_display_order = models.SmallIntegerField(null=True)
#     media_original_bytes = models.BigIntegerField(null=True)
#     media_original_height = models.SmallIntegerField(null=True)
#     media_original_width = models.SmallIntegerField(null=True)
#     media_short_description = models.CharField(max_length=50, null=True)
#     media_size_description = models.CharField(max_length=255, null=True)
#     media_source_file_name = models.CharField(max_length=3000, null=True)
#     media_sub_system_locale = models.CharField(max_length=255, null=True)
#     media_system_locale = models.CharField(max_length=255, null=True)
#     media_type = models.CharField(max_length=255, null=True)
#     media_url = models.URLField(max_length=8000, null=True)
#     media_url_full = models.URLField(max_length=4000, null=True)
#     media_url_hd = models.URLField(max_length=4000, null=True)
#     media_url_hi_res = models.URLField(max_length=4000, null=True)
#     media_url_medium = models.URLField(max_length=4000, null=True)
#     media_url_thumb = models.URLField(max_length=4000, null=True)
#     mls_status = models.CharField(max_length=255, null=True)
#     preferred_photo_yn = models.BooleanField(null=True)
#     resource_name = models.CharField(max_length=255, null=True)
#     listing_id = models.CharField(max_length=255, null=True)
#     resource_record_key = models.BigIntegerField(null=True)
#
#     def __str__(self):
#         return self.media_file_name
#
#
# class BuilderModel(BaseModel):
#     builder_model_key = models.BigIntegerField(primary_key=True)
#     builder_model_name = models.CharField(max_length=50, null=True)
#     builder_model_related_builder_model_key = models.ForeignKey(
#         "self", on_delete=models.SET_NULL, null=True
#     )
#     builder_model_status = models.CharField(max_length=255, null=True)
#     builder_model_county = models.CharField(max_length=255, null=True)
#     builder_model_modification_timestamp = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return self.builder_model_name
#
#
# class BuildingName(BaseModel):
#     bldg_name_key = models.BigIntegerField(primary_key=True)
#     bldg_name_name = models.CharField(max_length=50, null=True)
#     bldg_name_related_bldg_name_key = models.ForeignKey(
#         "self", on_delete=models.SET_NULL, null=True
#     )
#     bldg_name_status = models.CharField(max_length=255, null=True)
#     bldg_name_url = models.URLField(max_length=3000, null=True)
#     bldg_name_county = models.CharField(max_length=255, null=True)
#     bldg_name_state = models.CharField(max_length=255, null=True)
#     bldg_name_modification_timestamp = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return self.bldg_name_name
#
#
# class BusinessHistoryDeletions(BaseModel):
#     del_uch_hist_change_key = models.BigIntegerField(primary_key=True)
#     del_uch_hist_system_locale = models.CharField(max_length=255, null=True)
#     del_uch_hist_sub_system_locale = models.CharField(max_length=255, null=True)
#     del_uch_hist_deleted_timestamp = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return str(self.del_uch_hist_change_key)
#
#
# class GreenVerification(BaseModel):
#     green_verification_key = models.BigIntegerField(primary_key=True)
#     green_verification_system_locale = models.CharField(max_length=255, null=True)
#     green_verification_sub_system_locale = models.CharField(max_length=255, null=True)
#     green_verification_listing_key = models.BigIntegerField(
#         null=True
#     )  # ForeignKey('Listing', ...) ??
#     green_verification_body = models.CharField(max_length=255, null=True)
#     green_verification_program_type = models.CharField(max_length=255, null=True)
#     green_verification_year = models.SmallIntegerField(null=True)
#     green_verification_rating = models.CharField(max_length=255, null=True)
#     green_verification_score = models.SmallIntegerField(null=True)
#     green_verification_status = models.CharField(max_length=255, null=True)
#     county = models.CharField(max_length=255, null=True)
#     listing_source_record_key = models.CharField(max_length=30, null=True)
#     green_verification_modification_timestamp = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return self.green_verification_body


# class Team(BaseModel):
#     team_key = models.BigIntegerField(primary_key=True)
#     team_name = models.CharField(max_length=80, null=True, blank=True)
#     team_system_locale = models.CharField(max_length=255, null=True, blank=True)
#     team_sub_system_locale = models.CharField(max_length=255, null=True, blank=True)
#     team_lead_member_key = models.ForeignKey(
#         "TeamMember",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="lead_team",
#     )
#     team_modification_timestamp = models.DateTimeField(null=True, blank=True)
#     team_status = models.CharField(max_length=50, null=True, blank=True)
#     team_external_system_id = models.CharField(max_length=50, null=True, blank=True)
#
#     class Meta:
#         ordering = ["team_key"]
#
#     def __str__(self):
#         return str(self.team_name)
#
#
# class TeamMember(BaseModel):
#     team_member_key = models.BigIntegerField(primary_key=True)
#     team_member_team_key = models.ForeignKey(
#         "Team", on_delete=models.SET_NULL, null=True, blank=True, related_name="members"
#     )
#     team_member_member_key = models.BigIntegerField(null=True, blank=True)
#     team_member_relationship_key = models.BigIntegerField(null=True, blank=True)
#     team_member_relationship_active_flag = models.BooleanField(null=True, blank=True)
#     team_member_relationship_name = models.CharField(
#         max_length=80, null=True, blank=True
#     )
#     team_member_modification_timestamp = models.DateTimeField(null=True, blank=True)
#
#     class Meta:
#         ordering = ["team_member_key"]
#
#     def __str__(self):
#         return str(self.team_member_key)


# class SchoolDistrict(BaseModel):
#     school_district_key = models.BigIntegerField(primary_key=True)
#     school_district_name = models.CharField(max_length=80, null=True)
#     school_district_url = models.URLField(max_length=255, null=True)
#     school_district_county = models.CharField(max_length=255, null=True)
#     school_district_state = models.CharField(max_length=255, null=True)
#     school_district_modification_timestamp = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return self.school_district_name
#
#
# class School(BaseModel):
#     school_key = models.BigIntegerField(primary_key=True)
#     school_name = models.CharField(max_length=80, null=True)
#     school_county = models.CharField(max_length=255, null=True)
#     school_district_name = models.CharField(max_length=80, null=True)
#     school_district_key = models.ForeignKey(
#         "SchoolDistrict", on_delete=models.SET_NULL, null=True
#     )
#     school_modification_timestamp = models.DateTimeField(null=True)
#     school_type = models.CharField(max_length=255, null=True)
#
#     def __str__(self):
#         return self.school_name
#
#
# class Subdivision(BaseModel):
#     lo_subdivision_key = models.BigIntegerField(primary_key=True)
#     lo_subdivision_name = models.CharField(max_length=50, null=True)
#     lo_subdivision_system_validated_flag = models.BooleanField(null=True)
#     lo_subdivision_county = models.CharField(max_length=255, null=True)
#     lo_subdivision_state = models.CharField(max_length=255, null=True)
#     lo_subdivision_modification_timestamp = models.DateTimeField(null=True)
#     lo_subdivision_status = models.CharField(max_length=255, null=True)
#     lo_subdivision_url = models.URLField(max_length=255, null=True)
#     lo_subdivision_related_subdivision_key = models.ForeignKey(
#         "self", on_delete=models.SET_NULL, null=True
#     )
#
#     def __str__(self):
#         return self.lo_subdivision_name
#
#
# class SysAgentMedia(BaseModel):
#     sys_media_key = models.BigIntegerField(primary_key=True)
#     sys_media_object_key = models.ForeignKey(
#         "BrightMedia", on_delete=models.SET_NULL, null=True
#     )  # ???
#     sys_media_type = models.CharField(max_length=255, null=True)
#     sys_media_external_key = models.CharField(max_length=20, null=True)
#     sys_media_item_number = models.SmallIntegerField(null=True)
#     sys_media_display_order = models.SmallIntegerField(null=True)
#     sys_media_size = models.CharField(max_length=255, null=True)
#     sys_media_bytes = models.BigIntegerField(null=True)
#     sys_media_file_name = models.CharField(max_length=3000, null=True)
#     sys_media_caption = models.CharField(max_length=50, null=True)
#     sys_media_description = models.CharField(max_length=4000, null=True)
#     sys_media_url = models.URLField(max_length=4000, null=True)
#     sys_media_creation_timestamp = models.DateTimeField(null=True)
#     sys_media_modification_timestamp = models.DateTimeField(null=True)
#     sys_media_system_locale = models.CharField(max_length=255, null=True)
#     sys_media_sub_system_locale = models.CharField(max_length=255, null=True)
#     sys_media_processing_status = models.CharField(max_length=255, null=True)
#     sys_media_pending_file_name = models.CharField(max_length=3000, null=True)
#     sys_media_ext_sys_processing_code = models.CharField(max_length=100, null=True)
#     sys_media_ext_sys_processing_time = models.IntegerField(null=True)
#     sys_media_ext_sys_resize_time = models.IntegerField(null=True)
#
#     def __str__(self):
#         return self.sys_media_file_name
#
#
# class SysOfficeMedia(BaseModel):
#     sys_media_key = models.BigIntegerField(primary_key=True)
#     sys_media_object_key = models.ForeignKey(
#         "BrightMedia", on_delete=models.SET_NULL, null=True
#     )
#     sys_media_type = models.CharField(max_length=255, null=True)
#     sys_media_external_key = models.CharField(max_length=20, null=True)
#     sys_media_item_number = models.SmallIntegerField(null=True)
#     sys_media_display_order = models.SmallIntegerField(null=True)
#     sys_media_size = models.CharField(max_length=255, null=True)
#     sys_media_bytes = models.BigIntegerField(null=True)
#     sys_media_file_name = models.CharField(max_length=3000, null=True)
#     sys_media_caption = models.CharField(max_length=50, null=True)
#     sys_media_description = models.CharField(max_length=4000, null=True)
#     sys_media_url = models.URLField(max_length=4000, null=True)
#     sys_media_creation_timestamp = models.DateTimeField(null=True)
#     sys_media_modification_timestamp = models.DateTimeField(null=True)
#     sys_media_system_locale = models.CharField(max_length=255, null=True)
#     sys_media_sub_system_locale = models.CharField(max_length=255, null=True)
#     sys_media_processing_status = models.CharField(max_length=255, null=True)
#     sys_media_pending_file_name = models.CharField(max_length=3000, null=True)
#     sys_media_ext_sys_processing_code = models.CharField(max_length=100, null=True)
#     sys_media_ext_sys_processing_time = models.IntegerField(null=True)
#     sys_media_ext_sys_resize_time = models.IntegerField(null=True)
#
#     def __str__(self):
#         return self.sys_media_file_name
#
#
# class SysPartyLicense(BaseModel):
#     sys_party_license_key = models.BigIntegerField(primary_key=True)
#     sys_party_license_state = models.CharField(max_length=255, null=True)
#     sys_party_license_number = models.CharField(max_length=20, null=True)
#     sys_party_license_expiration_date = models.DateField(null=True)
#     sys_party_license_party_key = models.ForeignKey(
#         "BrightMember", on_delete=models.SET_NULL, null=True
#     )
#     sys_party_license_type = models.CharField(max_length=255, null=True)
#     sys_party_license_modification_timestamp = models.DateTimeField(null=True)
#     sys_party_license_system_locale = models.BigIntegerField(null=True)
#     sys_party_license_sub_system_locale = models.BigIntegerField(null=True)
#
#     def __str__(self):
#         return self.sys_party_license_number
#
#
# class PartyPermissions(BaseModel):
#     party_perm_key = models.BigIntegerField(primary_key=True)
#     party_perm_access_level_type = models.CharField(max_length=255, null=True)
#     party_perm_permission_type = models.CharField(max_length=255, null=True)
#     party_perm_grantor_party_key = models.ForeignKey(  # ???
#         "BrightMember",
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="grantor_permissions",
#     )
#     party_perm_grantee_party_key = models.ForeignKey(  # ???
#         "BrightMember",
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="grantee_permissions",
#     )
#     party_perm_system_locale = models.CharField(max_length=255, null=True)
#     pp_permission_group = models.CharField(max_length=255, null=True)
#     party_perm_sub_system_locale = models.CharField(max_length=255, null=True)
#     party_perm_modification_timestamp = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return str(self.party_perm_key)
#
#
# class PartyProfileOption(BaseModel):
#     ppo_key = models.BigIntegerField(primary_key=True)
#     po_name = models.CharField(max_length=255, null=True)
#     ppo_char_value = models.CharField(max_length=255, null=True)
#     ppo_date_value = models.DateField(null=True)
#     ppo_num_value = models.DecimalField(max_digits=18, decimal_places=2, null=True)
#     ppo_party_key = models.BigIntegerField(
#         null=True
#     )  # Not defined as a ForeignKey in the specification
#     ppo_poi_key = models.BigIntegerField(null=True)  # Not defined as a ForeignKey
#     ppo_user_customizable_flag = models.BooleanField(null=True)
#     ppo_clob_value = models.TextField(null=True)
#     ppo_modification_timestamp = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return self.po_name
#
#
# class Room(BaseModel):
#     room_key = models.BigIntegerField(primary_key=True)
#     room_listing_key = models.BigIntegerField(null=True)
#     county = models.CharField(max_length=255, null=True)
#     room_type = models.CharField(max_length=255, null=True)
#     room_length = models.IntegerField(null=True)
#     room_width = models.IntegerField(null=True)
#     room_level = models.CharField(max_length=255, null=True)
#     room_exists_yn = models.BooleanField(null=True)
#     room_display_order = models.IntegerField(null=True)
#     room_item_number = models.IntegerField(null=True)
#     room_area = models.IntegerField(null=True)
#     room_dimensions = models.CharField(max_length=50, null=True)
#     room_features = models.TextField(null=True)  # Assuming array of strings as text.
#     room_system_locale = models.CharField(max_length=255, null=True)
#     room_sub_system_locale = models.CharField(max_length=255, null=True)
#     listing_source_record_key = models.CharField(max_length=30, null=True)
#     room_modification_timestamp = models.DateTimeField(null=True)
#     room_description = models.CharField(max_length=1024, null=True)
#     room_source_record_key = models.CharField(max_length=50, null=True)
#
#     def __str__(self):
#         return f"Room {self.room_key}"
#
#
# class PropertyArea(BaseModel):
#     prop_area_key = models.BigIntegerField(primary_key=True)
#     location = models.JSONField(null=True)  # Assuming geoPoint as JSON
#     prop_area_county = models.CharField(max_length=255, null=True)
#     prop_area_type = models.CharField(max_length=255, null=True)
#     prop_area_modification_timestamp = models.DateTimeField(null=True)
#     prop_area_state = models.CharField(max_length=255, null=True)
#
#     def __str__(self):
#         return f"Property Area {self.prop_area_key}"
#
#
# class Unit(BaseModel):
#     unit_type_key = models.BigIntegerField(primary_key=True)
#     county = models.CharField(max_length=255, null=True)
#     unit_type_listing_key = models.BigIntegerField(null=True)
#     unit_type_item_number = models.IntegerField(null=True)
#     unit_type_type = models.CharField(max_length=255, null=True)
#     unit_type_monthly_rent = models.FloatField(null=True)
#     unit_type_pro_forma = models.FloatField(null=True)
#     unit_type_occupied_yn = models.BooleanField(null=True)
#     unit_type_level = models.BigIntegerField(null=True)
#     unit_type_finished_sqft = models.IntegerField(null=True)
#     unit_type_lease_type = models.CharField(max_length=255, null=True)
#     unit_type_lease_expiration_date = models.DateField(null=True)
#     unit_type_beds_total = models.IntegerField(null=True)
#     unit_type_baths_half = models.BigIntegerField(null=True)
#     unit_type_baths_full = models.IntegerField(null=True)
#     unit_type_baths_total = models.FloatField(null=True)
#     unit_type_features = models.CharField(max_length=128, null=True)
#     unit_type_total_rooms = models.IntegerField(null=True)
#     unit_type_contiguous_space_yn = models.BooleanField(null=True)
#     unit_type_security_deposit = models.FloatField(null=True)
#     listing_source_record_key = models.CharField(max_length=30, null=True)
#     prop_unit_modification_timestamp = models.DateTimeField(null=True)
#     unit_system_locale = models.CharField(max_length=255, null=True)
#     unit_sub_system_locale = models.CharField(max_length=255, null=True)
#     unit_type_source_record_key = models.CharField(max_length=50, null=True)
#
#     def __str__(self):
#         return f"Unit {self.unit_type_key}"
#
#
#
#
# class BrightOpenHouse(BaseModel):
#     open_house_key = models.BigIntegerField(primary_key=True)
#     county = models.CharField(max_length=255, null=True)
#     listing_id = models.CharField(max_length=255, null=True)
#     mls_status = models.CharField(max_length=255, null=True)
#     open_house_attended_by = models.CharField(max_length=255, null=True)
#     open_house_creation_timestamp = models.DateTimeField(null=True)
#     open_house_date = models.DateField(null=True)
#     open_house_item_number = models.IntegerField(null=True)
#     open_house_end_time = models.DateTimeField(null=True)
#     open_house_listing_key = models.BigIntegerField(null=True)
#     open_house_modification_timestamp = models.DateTimeField(null=True)
#     open_house_source_business_partner = models.CharField(max_length=255, null=True)
#     open_house_source_input = models.CharField(max_length=255, null=True)
#     open_house_remarks = models.TextField(null=True)
#     open_house_source_transport = models.CharField(max_length=255, null=True)
#     open_house_sub_system_locale = models.CharField(max_length=255, null=True)
#     open_house_system_locale = models.CharField(max_length=255, null=True)
#     listing_source_record_key = models.CharField(max_length=50, null=True)
#     open_house_external_system_id = models.CharField(max_length=50, null=True)
#     list_office_mls_id = models.CharField(max_length=255, null=True)
#     open_house_start_time = models.DateTimeField(null=True)
#     open_house_type = models.CharField(max_length=255, null=True)
#     open_house_method = models.CharField(max_length=255, null=True)
#     virtual_open_house_url = models.CharField(max_length=4000, null=True)
#     expected_on_market_date = models.DateField(null=True)
#
#     def __str__(self):
#         return f"Open House {self.open_house_key}"
#
#
# class BrightMember(BaseModel):
#     member_key = models.BigIntegerField(primary_key=True)
#     job_title = models.CharField(max_length=50, null=True)
#     member_address1 = models.CharField(max_length=50, null=True)
#     member_address2 = models.CharField(max_length=50, null=True)
#     member_box_number = models.CharField(max_length=10, null=True)
#     member_city = models.CharField(max_length=50, null=True)
#     member_country = models.CharField(max_length=50, null=True)
#     member_county = models.CharField(max_length=50, null=True)
#     member_designation = models.TextField(
#         null=True
#     )  # Assuming this is a list of strings
#     member_direct_phone = models.CharField(max_length=16, null=True)
#     member_email = models.CharField(max_length=80, null=True)
#     member_fax = models.CharField(max_length=16, null=True)
#     member_first_name = models.CharField(max_length=50, null=True)
#     member_full_name = models.CharField(max_length=150, null=True)
#     member_full_role_list = models.TextField(null=True)
#     member_join_date = models.DateField(null=True)
#     member_last_name = models.CharField(max_length=50, null=True)
#     member_license_expiration_date = models.DateField(null=True)
#     member_login_id = models.CharField(max_length=25, null=True)
#     member_middle_initial = models.CharField(max_length=5, null=True)
#     member_middle_name = models.CharField(max_length=50, null=True)
#     member_mls_id = models.CharField(max_length=25, null=True)
#     member_mobile_phone = models.CharField(max_length=16, null=True)
#     member_name_prefix = models.CharField(max_length=50, null=True)
#     member_name_suffix = models.CharField(max_length=50, null=True)
#     member_national_association_id = models.CharField(max_length=25, null=True)
#     member_nickname = models.CharField(max_length=50, null=True)
#     member_num_violations = models.IntegerField(null=True)
#     member_office_phone = models.CharField(max_length=16, null=True)
#     member_office_phone_ext = models.IntegerField(null=True)
#     member_pager = models.CharField(max_length=16, null=True)
#     member_postal_code = models.CharField(max_length=10, null=True)
#     member_postal_code_plus4 = models.CharField(max_length=4, null=True)
#     member_preferred_phone = models.CharField(max_length=16, null=True)
#     member_preferred_phone_ext = models.IntegerField(null=True)
#     member_private_email = models.TextField(null=True)
#     member_rate_plug_flag = models.BooleanField(null=True)
#     member_reinstatement_date = models.DateField(null=True)
#
#     def __str__(self):
#         return self.member_full_name
#
#
# class BrightOffice(BaseModel):
#     office_key = models.BigIntegerField(primary_key=True)
#     office_broker_lead_email = models.EmailField(null=True)
#     office_broker_lead_phone_number = models.CharField(max_length=50, null=True)
#     office_broker_mls_id = models.CharField(max_length=50, null=True)
#     office_city = models.CharField(max_length=255, null=True)
#     office_country = models.CharField(max_length=255, null=True)
#     office_county = models.CharField(max_length=255, null=True)
#     office_date_added = models.DateField(null=True)
#     office_date_terminated = models.DateField(null=True)
#     office_email = models.EmailField(null=True)
#     office_fax = models.CharField(max_length=50, null=True)
#     office_latitude = models.FloatField(null=True)
#     office_lead_to_listing_agent_yn = models.BooleanField(null=True)
#     office_longitude = models.FloatField(null=True)
#     office_manager_key = models.BigIntegerField(null=True)
#     office_manager_email = models.EmailField(null=True)
#     office_manager_mls_id = models.CharField(max_length=50, null=True)
#     office_manager_name = models.CharField(max_length=255, null=True)
#     office_mls_id = models.CharField(max_length=50, null=True)
#     office_name = models.CharField(max_length=255, null=True)
#     office_national_association_id = models.CharField(max_length=50, null=True)
#     office_num_violations = models.IntegerField(null=True)
#     office_phone = models.CharField(max_length=50, null=True)
#     office_phone_ext = models.CharField(max_length=50, null=True)
#     office_postal_code = models.CharField(max_length=20, null=True)
#     office_postal_code_plus4 = models.CharField(max_length=10, null=True)
#     office_role_list = models.TextField(null=True)
#     office_state_or_province = models.CharField(max_length=255, null=True)
#     office_status = models.CharField(max_length=50, null=True)
#     office_street_dir_suffix = models.CharField(max_length=50, null=True)
#     office_street_exception = models.CharField(max_length=50, null=True)
#     office_street_name = models.CharField(max_length=255, null=True)
#     office_street_number = models.CharField(max_length=50, null=True)
#     office_street_suffix = models.CharField(max_length=50, null=True)
#     office_trading_as = models.CharField(max_length=255, null=True)
#     office_type = models.CharField(max_length=50, null=True)
#     office_unit_designation = models.CharField(max_length=50, null=True)
#     office_unit_number = models.CharField(max_length=50, null=True)
#     office_user_name = models.CharField(max_length=255, null=True)
#
#     def __str__(self):
#         return self.office_name
#
#
# class BrightProperty(BaseModel):
#     pass
#
#
# class Deletion(BaseModel):
#     del_uch_hist_change_key = models.BigIntegerField(primary_key=True)
#     del_uch_hist_system_locale = models.CharField(max_length=255, null=True)
#     del_uch_hist_sub_system_locale = models.CharField(max_length=255, null=True)
#     del_uch_hist_deleted_timestamp = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return f"Deletion {self.del_uch_hist_change_key}"
#
#
# class ListingSubscription(BaseModel):
#     lsub_key = models.BigIntegerField(primary_key=True)
#     lsub_listing_key = models.BigIntegerField(null=True)
#     lsub_requested_class_key = models.CharField(max_length=255, null=True)
#     lsub_class_key = models.CharField(max_length=255, null=True)
#     req_subscription_class_service_key = models.CharField(max_length=255, null=True)
#     county = models.CharField(max_length=255, null=True)
#
#     def __str__(self):
#         return f"Listing Subscription {self.lsub_key}"
#
#
# class History(BaseModel):
#     prop_hist_key = models.BigIntegerField(primary_key=True)
#     prop_hist_listing_key = models.BigIntegerField(null=True)
#     prop_hist_record_key = models.BigIntegerField(null=True)
#     prop_hist_party_key = models.BigIntegerField(null=True)
#     prop_hist_change_type = models.CharField(max_length=255, null=True)
#     prop_hist_change_type_lkp = models.CharField(max_length=255, null=True)
#     prop_hist_change_timestamp = models.DateTimeField(null=True)
#     prop_hist_column_name = models.CharField(max_length=255, null=True)
#     prop_hist_table_name = models.CharField(max_length=255, null=True)
#     prop_hist_original_column_value = models.CharField(max_length=255, null=True)
#     prop_hist_new_column_value = models.CharField(max_length=255, null=True)
#     prop_hist_item_number = models.IntegerField(null=True)
#     prop_hist_sub_system_locale = models.CharField(max_length=255, null=True)
#     prop_hist_system_locale = models.CharField(max_length=255, null=True)
#     listing_id = models.CharField(max_length=255, null=True)
#     full_street_address = models.CharField(max_length=255, null=True)
#
#     def __str__(self):
#         return f"History {self.prop_hist_key}"
#
#
# class LisBusinessHistory(BaseModel):
#     uch_prop_hist_change_key = models.BigIntegerField(primary_key=True)
#     uch_prop_hist_listing_key = models.BigIntegerField(null=True)
#     uch_prop_hist_party_key = models.BigIntegerField(null=True)
#     uch_prop_hist_change_type = models.CharField(max_length=20, null=True)
#     uch_prop_hist_change_type_pck_item_key = models.CharField(max_length=255, null=True)
#     uch_prop_hist_change_timestamp = models.DateTimeField(null=True)
#     system_name = models.CharField(max_length=50, null=True)
#     prop_hist_column_name = models.CharField(max_length=64, null=True)
#     table_name = models.CharField(max_length=30, null=True)
#     table_schema_key = models.BigIntegerField(null=True)
#     uch_prop_hist_original_column_value = models.CharField(max_length=4000, null=True)
#     uch_prop_hist_new_column_value = models.CharField(max_length=4000, null=True)
#     uch_prop_hist_original_pick_list_value = models.CharField(max_length=80, null=True)
#     uch_prop_hist_new_pick_list_value = models.CharField(max_length=80, null=True)
#     uch_prop_hist_item_number = models.IntegerField(null=True)
#     uch_prop_hist_sub_system_locale = models.CharField(max_length=255, null=True)
#     uch_prop_hist_system_locale = models.CharField(max_length=255, null=True)
#     basic_listing_id = models.CharField(max_length=20, null=True)
#     full_street_address = models.CharField(max_length=80, null=True)
#     uch_prop_hist_creation_timestamp = models.DateTimeField(null=True)
#     uch_prop_hist_modification_timestamp = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return f"Business History {self.uch_prop_hist_change_key}"
