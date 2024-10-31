from django.contrib import admin
from django.utils.safestring import mark_safe
from brightmls import models as bright_models
from backend.core.admin import ViewOnlyAdminMixin, ImageUrlFieldsAdminMixin


@admin.register(bright_models.SysOfficeMedia)
class SysOfficeMediaAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "SysMediaKey",
        "SysMediaObjectKey",
        "SysMediaType",
        "SysMediaExternalKey",
        "SysMediaItemNumber",
        "SysMediaDisplayOrder",
        "SysMediaSize",
        "SysMediaMimeType",
        "SysMediaBytes",
        "SysMediaFileName",
        "SysMediaCaption",
        "SysMediaDescription",
        "SysMediaURL",
        "SysMediaCreationTimestamp",
        "SysMediaModificationTimestamp",
        "SysMediaSystemLocale",
        "SysMediaSubSystemLocale",
        "SysMediaProcessingStatus",
        "SysMediaPendingFileName",
        "SysMediaExtSysProcessingCode",
        "SysMediaExtSysProcessingTime",
        "SysMediaExtSysResizeTime",
        "SysMediaExtSysTotalBytes",
        "SysMediaExtSysWriteTime",
        "SysMediaExtSysErrorMessage",
        "SysMediaObjectID",
    ]


@admin.register(bright_models.PropertyArea)
class PropertyAreaAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "PropAreaKey",
        "Location",
        "PropAreaCounty",
        "PropAreaType",
        "PropAreaModificationTimestamp",
        "PropAreaState",
    ]


@admin.register(bright_models.RelatedLookup)
class RelatedLookupAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "RelatedLookupKey",
        "LookupKey",
        "ModificationTimestamp",
    ]


@admin.register(bright_models.CityZipCode)
class CityZipCodeAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "CityZipCodeKey",
        "CityZipCodeCity",
        "CityZipCodeCityName",
        "CityZipCodeCounty",
        "CityZipCodeState",
        "CityZipCodeZip",
        "CityZipCodePreferredCity",
        "CityZipModificationTimestamp",
    ]


@admin.register(bright_models.BrightMedia)
class BrightMediaAdmin(ViewOnlyAdminMixin, ImageUrlFieldsAdminMixin, admin.ModelAdmin):
    list_display = [
        "MediaKey",
        "display_media_url_thumb",
        "Location",
        "PropertyType",
        "County",
        "MediaBytes",
        "MediaCategory",
        "MediaCreationTimestamp",
        "MediaExternalKey",
        "MediaFileName",
        "MediaImageOf",
        "MediaItemNumber",
        "MediaLongDescription",
        "MediaModificationTimestamp",
        "MediaDisplayOrder",
        "MediaOriginalBytes",
        "MediaOriginalHeight",
        "MediaOriginalWidth",
        "MediaShortDescription",
        "MediaSizeDescription",
        "MediaSourceFileName",
        "MediaSubSystemLocale",
        "MediaSystemLocale",
        "MediaType",
        "MediaURL",
        "MediaURLFull",
        "MediaURLHD",
        "MediaURLHiRes",
        "MediaURLMedium",
        "MediaURLThumb",
        "MlsStatus",
        "PreferredPhotoYN",
        "ResourceName",
        "ListingId",
        "ResourceRecordKey",
        "MediaVendorID",
        "MediaVendorName",
        "MediaVendorIDType",
        "MediaSourceBusinessPartner",
        "MediaSourceInput",
        "MediaSourceTransport",
        "MediaImageHeight",
        "MediaImageWidth",
        "ListingSourceRecordKey",
        "MediaVisibility",
        "PropMediaProcessingStatus",
        "PropMediaPendingFileName",
        "PropMediaExtSysProcessingCode",
        "PropMediaExtSysProcessingTime",
        "PropMediaExtSysResizeTime",
        "PropMediaExtSysTotalBytes",
        "PropMediaExtSysWriteTime",
        "PropMediaExtSysErrorMessage",
        "MediaObjectId",
    ]
    readonly_fields = [
        "display_media_url_thumb",
        "display_media_url_full",
    ]
    # list_filter = [
    #     "PropertyType",
    #     "MediaCategory",
    #     "MediaImageOf",
    #     "MlsStatus",
    #     "County",
    # ]
    search_fields = [
        "MediaKey",
    ]

    @mark_safe
    @admin.display(description="Media URL thumb")
    def display_media_url_thumb(self, obj):
        if obj.MediaURLThumb:
            return self.render_image_field(obj.MediaURLThumb, max_size=100)
        return "-"

    @mark_safe
    @admin.display(description="Media URL Full")
    def display_media_url_full(self, obj):
        if obj.MediaURLFull:
            return self.render_url_field(obj.MediaURLFull)
        return "-"


@admin.register(bright_models.TeamMember)
class TeamMemberAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "TeamMemberKey",
        "TeamMemberTeamKey",
        "TeamMemberMemberKey",
        "TeamMemberRelationshipKey",
        "TeamMemberRelationshipActiveFlag",
        "TeamMemberRelationshipName",
        "TeamMemberModificationTimestamp",
    ]
    search_fields = [
        "TeamMemberKey",
    ]


@admin.register(bright_models.Deletion)
class DeletionAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "UniversalKey",
        "TableName",
        "SchemaShortName",
        "DeletionTimestamp",
        "DeleteKey",
    ]
    search_fields = [
        "UniversalKey",
    ]


@admin.register(bright_models.BrightOffices)
class BrightOfficesAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "OfficeKey",
        "FranchiseAffiliation",
        "IDXOfficeParticipationYN",
        "MainOfficeKey",
        "MainOfficeMlsId",
        "ModificationTimestamp",
        "OfficeAssociationPrimary",
        "OfficeAddress1",
        "OfficeAddress2",
        "OfficeBoxNumber",
        "OfficeBranchType",
        "OfficeBrokerAcceptedPortalTermsOfUseYN",
        "OfficeBrokerAcceptedPortalTermsOfUseVersion",
        "OfficeBrokerKey",
        "OfficeBrokerLeadEmail",
        "OfficeBrokerLeadPhoneNumber",
        "OfficeBrokerMlsId",
        "OfficeCity",
        "OfficeCountry",
        "OfficeCounty",
        "OfficeDateAdded",
        "OfficeDateTerminated",
        "OfficeEmail",
        "OfficeFax",
        "OfficeManagerKey",
        "OfficeLatitude",
        "OfficeLeadToListingAgentYN",
        "OfficeLongitude",
        "OfficeManagerEmail",
        "OfficeManagerMlsId",
        "OfficeManagerName",
        "OfficeMlsId",
        "OfficeName",
        "OfficeNationalAssociationId",
        "OfficeNumViolations",
        "OfficePhone",
        "OfficePhoneExt",
        "OfficePhoneOther",
        "OfficePostalCode",
        "OfficePostalCodePlus4",
        "OfficeRoleList",
        "OfficeStateOrProvince",
        "OfficeStatus",
        "OfficeStreetDirSuffix",
        "OfficeStreetException",
        "OfficeStreetName",
        "OfficeStreetNumber",
        "OfficeStreetSuffix",
        "OfficeTradingAs",
        "OfficeType",
        "OfficeUnitDesignation",
        "OfficeUnitNumber",
        "OfficeUserName",
        "OfficeSubSystemLocale",
        "OfficeSystemLocale",
        "SocialMediaBlogUrlOrId",
        "SocialMediaFacebookUrlOrId",
        "SocialMediaLinkedInUrlOrId",
        "SocialMediaTwitterUrlOrId",
        "SocialMediaWebsiteUrlOrId",
        "SocialMediaYouTubeUrlOrId",
        "OfficeSourceBusinessPartner",
        "OfficeSourceRecordKey",
        "SyndicateAgentOption",
        "SyndicateTo",
        "OfficeSourceRecordID",
        "OfficeBrightConvertedYN",
        "OfficeSourceInput",
        "OfficeSourceTransport",
        "MainOfficeName",
        "OfficeAssociationsFullList",
        "OfficeValidationStatus",
        "OfficeCorporateLicense",
        "SourceModificationTimestamp",
        "OfficeStreetDirPrefix",
    ]
    search_fields = [
        "OfficeKey",
    ]


@admin.register(bright_models.SchoolDistrict)
class SchoolDistrictAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "SchoolDistrictKey",
        "SchoolDistrictName",
        "SchoolDistrictURL",
        "SchoolDistrictCounty",
        "SchoolDistrictState",
        "SchoolDistrictModificationTimestamp",
    ]
    search_fields = [
        "SchoolDistrictKey",
    ]


@admin.register(bright_models.PartyPermissions)
class PartyPermissionsAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "PartyPermKey",
        "PartyPermAccessLevelType",
        "PartyPermPermissionType",
        "PartyPermGrantorPartyKey",
        "PartyPermGranteePartyKey",
        "PartyPermSystemLocale",
        "PpPermissionGroup",
        "PartyPermSubSystemLocale",
        "PartyPermModificationTimestamp",
    ]
    search_fields = [
        "PartyPermKey",
    ]


@admin.register(bright_models.SysPartyLicense)
class SysPartyLicenseAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "SysPartyLicenseKey",
        "SysPartyLicenseState",
        "SysPartyLicenseNumber",
        "SysPartyLicenseExpirationDate",
        "SysPartyLicensePartyKey",
        "SysPartyLicenseType",
        "SysPartyLicenseModificationTimestamp",
        "SysPartyLicenseSystemLocale",
        "SysPartyLicenseSubSystemLocale",
    ]
    search_fields = [
        "SysPartyLicenseKey",
    ]


@admin.register(bright_models.BrightOpenHouses)
class BrightOpenHouseAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "OpenHouseKey",
        "County",
        "ListingId",
        "MlsStatus",
        "OpenHouseAttendedBy",
        "OpenHouseCreationTimestamp",
        "OpenHouseDate",
        "OpenHouseItemNumber",
        "OpenHouseEndTime",
        "OpenHouseListingKey",
        "OpenHouseModificationTimestamp",
        "OpenHouseSourceBusinessPartner",
        "OpenHouseSourceInput",
        "OpenHouseRemarks",
        "OpenHouseSourceTransport",
        "OpenHouseSubSystemLocale",
        "OpenHouseSystemLocale",
        "ListingSourceRecordKey",
        "OpenHouseExternalSystemID",
        "ListOfficeMlsId",
        "OpenHouseStartTime",
        "OpenHouseType",
        "OpenHouseMethod",
        "VirtualOpenHouseUrl",
        "ExpectedOnMarketDate",
    ]
    search_fields = [
        "OpenHouseKey",
    ]


@admin.register(bright_models.History)
class HistoryAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "PropHistKey",
        "PropHistListingKey",
        "PropHistRecordKey",
        "PropHistPartyKey",
        "PropHistChangeType",
        "PropHistChangeTypeLkp",
        "PropHistChangeTimestamp",
        "PropHistColumnName",
        "PropHistTableName",
        "PropHistOriginalColumnValue",
        "PropHistNewColumnValue",
        "PropHistOriginalPickListValue",
        "PropHistNewPickListValue",
        "PropHistItemNumber",
        "PropHistSubSystemLocale",
        "PropHistSystemLocale",
        "ListingID",
        "FullStreetAddress",
        "SystemName",
        "BasicComingSoonEndDate",
        "BasicLocaleListingStatus",
        "PropHistNewColumnCharValue",
        "PropHistNewColumnDatetimeValue",
        "PropHistNewColumnNumValue",
        "PropHistOriginalColumnCharValue",
        "PropHistOriginalColumnDatetimeValue",
        "PropHistOriginalColumnNumValue",
        "PropHistHistColumnKey",
    ]
    list_filter = [
        "PropHistTableName",
    ]
    search_fields = [
        "PropHistKey",
        "PropHistListingKey",
    ]


@admin.register(bright_models.GreenVerification)
class GreenVerificationAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "GreenVerificationKey",
        "GreenVerificationSystemLocale",
        "GreenVerificationSubSystemLocale",
        "GreenVerificationListingKey",
        "GreenVerificationBody",
        "GreenVerificationProgramType",
        "GreenVerificationYear",
        "GreenVerificationRating",
        "GreenVerificationScore",
        "GreenVerificationStatus",
        "County",
        "ListingSourceRecordKey",
        "GreenVerificationModificationTimestamp",
    ]
    search_fields = [
        "GreenVerificationKey",
    ]


@admin.register(bright_models.City)
class CityAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "CtyCityKey",
        "CtyCityName",
        "CtyCityCounty",
        "CtyCityType",
        "CtyCityTowhnship",
        "CtyCountyState",
        "CtyModificationTimestamp",
    ]
    search_fields = [
        "CtyCityKey",
    ]


@admin.register(bright_models.BrightMembers)
class BrightMembersAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "MemberKey",
        "JobTitle",
        "MemberAddress1",
        "MemberAddress2",
        "MemberBoxNumber",
        "MemberCity",
        "MemberCountry",
        "MemberCounty",
        "MemberDesignation",
        "MemberDirectPhone",
        "MemberEmail",
        "MemberFax",
        "MemberFirstName",
        "MemberFullName",
        "MemberFullRoleList",
        "MemberJoinDate",
        "MemberLastName",
        "MemberLicenseExpirationDate",
        "MemberLoginId",
        "MemberMiddleInitial",
        "MemberMiddleName",
        "MemberMlsId",
        "MemberMobilePhone",
        "MemberNamePrefix",
        "MemberNameSuffix",
        "MemberNationalAssociationId",
        "MemberNickname",
        "MemberNumViolations",
        "MemberOfficePhone",
        "MemberOfficePhoneExt",
        "MemberPager",
        "MemberPostalCode",
        "MemberPostalCodePlus4",
        "MemberPreferredPhone",
        "MemberPreferredPhoneExt",
        "MemberPrivateEmail",
        "MemberRatePlugFlag",
        "MemberReinstatementDate",
        "MemberRoleList",
        "MemberStateLicense",
        "MemberStateLicenseState",
        "MemberStateOrProvince",
        "MemberStatus",
        "MemberStreetDirSuffix",
        "MemberStreetException",
        "MemberStreetName",
        "MemberStreetNumber",
        "MemberStreetSuffix",
        "MemberTerminationDate",
        "MemberType",
        "MemberSubType",
        "MemberUnitDesignation",
        "MemberUnitNumber",
        "MemberVoiceMailExt",
        "MemberVoiceMail",
        "ModificationTimestamp",
        "OfficeKey",
        "OfficeMlsId",
        "OfficeBrokerKey",
        "OfficeName",
        "OfficeBrokerMlsId",
        "MemberDateAdded",
        "SocialMediaBlogUrlOrId",
        "SocialMediaFacebookUrlOrId",
        "SocialMediaLinkedInUrlOrId",
        "SocialMediaTwitterUrlOrId",
        "SocialMediaWebsiteUrlOrId",
        "SocialMediaYouTubeUrlOrId",
        "MemberSourceInput",
        "MemberSourceRecordKey",
        "MemberSourceRecordID",
        "MemberSourceBusinessPartner",
        "MemberSourceTransport",
        "SyndicateTo",
        "MemberSubSystemLocale",
        "MemberSystemLocale",
        "MemberPreferredFirstName",
        "MemberPreferredLastName",
        "MemberBrightConvertedYN",
        "MemberAssociationPrimary",
        "MemberAssociationsFullList",
        "MemberPreviewYN",
        "SourceModificationTimestamp",
        "MemberStreetDirPrefix",
    ]
    search_fields = [
        "MemberKey",
    ]


@admin.register(bright_models.Unit)
class UnitAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "UnitTypeKey",
        "County",
        "UnitTypeListingKey",
        "UnitTypeItemNumber",
        "UnitTypeType",
        "UnitTypeMonthlyRent",
        "UnitTypeProForma",
        "UnitTypeOccupiedYN",
        "UnitTypeLevel",
        "UnitTypeFinishedSQFT",
        "UnitTypeLeaseType",
        "UnitTypeLeaseExpirationDate",
        "UnitTypeBedsTotal",
        "UnitTypeBathsHalf",
        "UnitTypeBathsFull",
        "UnitTypeBathsTotal",
        "UnitTypeFeatures",
        "UnitTypeTotalRooms",
        "UnitTypeContiguousSpaceYN",
        "UnitTypeSecurityDeposit",
        "ListingSourceRecordKey",
        "PropUnitModificationTimestamp",
        "UnitSystemLocale",
        "UnitSubSystemLocale",
        "UnitTypeSourceRecordKey",
    ]
    search_fields = [
        "UnitTypeKey",
    ]


@admin.register(bright_models.Lookup)
class LookupAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "LookupKey",
        "LookupName",
        "LookupValue",
        "StandardLookupValue",
        "LegacyODataValue",
        "ModificationTimestamp",
    ]
    search_fields = [
        "LookupKey",
    ]


@admin.register(bright_models.Subdivision)
class SubdivisionAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "LoSubdivisionKey",
        "LoSubdivisionName",
        "LoSubdivisionSystemValidatedFlag",
        "LoSubdivisionCounty",
        "LoSubdivisionState",
        "LoSubdivisionModificationTimestamp",
        "LoSubdivisionStatus",
        "LoSubdivisionURL",
        "LoSubdivisionRelatedSubdivisionKey",
    ]
    search_fields = [
        "LoSubdivisionKey",
    ]


@admin.register(bright_models.SysAgentMedia)
class SysAgentMediaAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "SysMediaKey",
        "SysMediaObjectKey",
        "SysMediaType",
        "SysMediaExternalKey",
        "SysMediaItemNumber",
        "SysMediaDisplayOrder",
        "SysMediaSize",
        "SysMediaMimeType",
        "SysMediaBytes",
        "SysMediaFileName",
        "SysMediaCaption",
        "SysMediaDescription",
        "SysMediaURL",
        "SysMediaCreationTimestamp",
        "SysMediaModificationTimestamp",
        "SysMediaSystemLocale",
        "SysMediaSubSystemLocale",
        "SysMediaProcessingStatus",
        "SysMediaPendingFileName",
        "SysMediaExtSysProcessingCode",
        "SysMediaExtSysProcessingTime",
        "SysMediaExtSysResizeTime",
        "SysMediaExtSysTotalBytes",
        "SysMediaExtSysWriteTime",
        "SysMediaExtSysErrorMessage",
        "SysMediaObjectID",
    ]
    search_fields = [
        "SysMediaKey",
    ]


@admin.register(bright_models.Team)
class TeamAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "TeamKey",
        "TeamName",
        "TeamSystemLocale",
        "TeamSubSystemLocale",
        "TeamLeadMemberKey",
        "TeamModificationTimestamp",
        "TeamStatus",
        "TeamExternalSystemID",
    ]
    search_fields = [
        "TeamKey",
    ]


@admin.register(bright_models.School)
class SchoolAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "SchoolKey",
        "SchoolName",
        "SchoolCounty",
        "SchoolDistrictName",
        "SchoolDistrictKey",
        "SchoolModificationTimestamp",
        "SchoolType",
    ]
    search_fields = [
        "SchoolKey",
    ]


@admin.register(bright_models.BuildingName)
class BuildingNameAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "BldgNameKey",
        "BldgNameName",
        "BldgNameRelatedBldgNameKey",
        "BldgNameStatus",
        "BldgNameURL",
        "BldgNameCounty",
        "BldgNameState",
        "BldgNameModificationTimestamp",
    ]
    search_fields = [
        "BldgNameKey",
    ]


@admin.register(bright_models.Room)
class RoomAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "RoomKey",
        "RoomListingKey",
        "County",
        "RoomType",
        "RoomLength",
        "RoomWidth",
        "RoomLevel",
        "RoomExistsYN",
        "RoomDisplayOrder",
        "RoomItemNumber",
        "RoomArea",
        "RoomDimensions",
        "RoomFeatures",
        "RoomSystemLocale",
        "RoomSubSystemLocale",
        "ListingSourceRecordKey",
        "RoomModificationTimestamp",
        "RoomDescription",
        "RoomSourceRecordKey",
    ]
    search_fields = [
        "RoomKey",
    ]


@admin.register(bright_models.BusinessHistoryDeletions)
class BusinessHistoryDeletionsAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "DelUchHistChangeKey",
        "DelUchHistSystemLocale",
        "DelUchHistSubSystemLocale",
        "DelUchHistDeletedTimestamp",
    ]
    search_fields = [
        "DelUchHistChangeKey",
    ]


@admin.register(bright_models.BuilderModel)
class BuilderModelAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "BuilderModelKey",
        "BuilderModelName",
        "BuilderModelRelatedBuilderModelKey",
        "BuilderModelStatus",
        "BuilderModelCounty",
        "BuilderModelModificationTimestamp",
    ]
    search_fields = [
        "BuilderModelKey",
    ]


@admin.register(bright_models.LisBusinessHistory)
class LisBusinessHistoryAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "UchPropHistChangeKey",
        "UchPropHistListingKey",
        "UchPropHistPartyKey",
        "UchPropHistChangeType",
        "UchPropHistChangeTypePckItemKey",
        "UchPropHistChangeTimestamp",
        "SystemName",
        "PropHistColumnName",
        "TableName",
        "TableSchemaKey",
        "UchPropHistOriginalColumnValue",
        "UchPropHistNewColumnValue",
        "UchPropHistOriginalPickListValue",
        "UchPropHistNewPickListValue",
        "UchPropHistItemNumber",
        "UchPropHistSubSystemLocale",
        "UchPropHistSystemLocale",
        "BasicListingID",
        "FullStreetAddress",
        "UchPropHistCreationTimestamp",
        "UchPropHistModificationTimestamp",
    ]
    search_fields = [
        "UchPropHistChangeKey",
    ]


@admin.register(bright_models.ListingSubscription)
class ListingSubscriptionAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "LsubKey",
        "LsubListingKey",
        "LsubRequestedClassKey",
        "LsubClassKey",
        "ReqSubscriptionClassServiceKey",
        "County",
    ]
    search_fields = [
        "LsubKey",
    ]


@admin.register(bright_models.PartyProfileOption)
class PartyProfileOptionAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "POName",
        "PPOCharValue",
        "PPODateValue",
        "PPOKey",
        "PPONumValue",
        "PPOPartyKey",
        "PPOPOIKey",
        "PPOUserCustomizableFlag",
        "PPOClobValue",
    ]
    search_fields = [
        "PPOKey",
    ]


@admin.register(bright_models.BrightProperties)
class BrightPropertiesAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "ListingKey",
        "Location",
        "ModificationTimestamp",
    ]
    search_fields = [
        "ListingKey",
    ]
