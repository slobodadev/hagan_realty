from django.db import models
from django.utils.dateparse import parse_datetime
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class BaseModel(models.Model):
    """
    Base model that provides a generic from_python_odata method
    to map data from a python_odata entity to Django model fields.

    usage: instance = AnyModel.from_python_odata(odata_entity_object)
    """

    objects = BulkUpdateOrCreateQuerySet.as_manager()

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
            # print(">>>>>>> OData field:", odata_field)
            if hasattr(odata_obj, odata_field):
                value = getattr(odata_obj, odata_field)

                # Parse datetime fields if necessary (if returned as a string from odata)
                if isinstance(field, models.DateTimeField) and isinstance(value, str):
                    field_values[field_name] = parse_datetime(value)

                elif isinstance(field, models.ForeignKey) and isinstance(value, int):
                    # print(">>>>>>> ForeignKey field found")
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

        # print("field_values:", field_values)
        return cls(**field_values)

    @staticmethod
    def _map_field_name_to_odata(field_name):
        """
        Map Django model field names (snake_case) to odata field names (CamelCase).
        """
        if field_name[0].isupper():
            return field_name
        return "".join([word.capitalize() for word in field_name.split("_")])

    def update_from_odata(self, odata_obj):
        """
        Update the model instance from a python_odata entity object.
        """
        for field in self._meta.get_fields():
            # do not update primary key
            if field.primary_key:
                continue

            field_name = field.name
            if hasattr(odata_obj, field_name):
                value = getattr(odata_obj, field_name)
                if isinstance(field, models.DateTimeField) and isinstance(value, str):
                    value = parse_datetime(value)

                setattr(self, field_name, value)


class BrightMedia(BaseModel):
    Location = models.CharField(max_length=255, null=True)
    PropertyType = models.CharField(max_length=255, null=True)
    County = models.CharField(max_length=255, null=True)
    MediaBytes = models.CharField(max_length=255, null=True)
    MediaCategory = models.CharField(max_length=255, null=True)
    MediaCreationTimestamp = models.DateTimeField(null=True)
    MediaExternalKey = models.CharField(max_length=20, null=True)
    MediaFileName = models.CharField(max_length=3000, null=True)
    MediaImageOf = models.CharField(max_length=255, null=True)
    MediaItemNumber = models.IntegerField(null=True)
    MediaKey = models.BigIntegerField(primary_key=True)
    MediaLongDescription = models.CharField(max_length=1024, null=True)
    MediaModificationTimestamp = models.DateTimeField(null=True)
    MediaDisplayOrder = models.IntegerField(null=True)
    MediaOriginalBytes = models.CharField(max_length=255, null=True)
    MediaOriginalHeight = models.IntegerField(null=True)
    MediaOriginalWidth = models.IntegerField(null=True)
    MediaShortDescription = models.CharField(max_length=50, null=True)
    MediaSizeDescription = models.CharField(max_length=255, null=True)
    MediaSourceFileName = models.CharField(max_length=3000, null=True)
    MediaSubSystemLocale = models.CharField(max_length=255, null=True)
    MediaSystemLocale = models.CharField(max_length=255, null=True)
    MediaType = models.CharField(max_length=255, null=True)
    MediaURL = models.URLField(max_length=4000, null=True)
    MediaURLFull = models.URLField(max_length=4000, null=True)
    MediaURLHD = models.URLField(max_length=4000, null=True)
    MediaURLHiRes = models.URLField(max_length=4000, null=True)
    MediaURLMedium = models.URLField(max_length=4000, null=True)
    MediaURLThumb = models.URLField(max_length=4000, null=True)
    MlsStatus = models.CharField(max_length=255, null=True)
    PreferredPhotoYN = models.BooleanField(null=True)
    ResourceName = models.CharField(max_length=255, null=True)
    ListingId = models.CharField(max_length=255, null=True)
    ResourceRecordKey = models.CharField(max_length=255, null=True)
    MediaVendorID = models.CharField(max_length=30, null=True)
    MediaVendorName = models.CharField(max_length=80, null=True)
    MediaVendorIDType = models.CharField(max_length=255, null=True)
    MediaSourceBusinessPartner = models.CharField(max_length=255, null=True)
    MediaSourceInput = models.CharField(max_length=255, null=True)
    MediaSourceTransport = models.CharField(max_length=255, null=True)
    MediaImageHeight = models.IntegerField(null=True)
    MediaImageWidth = models.IntegerField(null=True)
    ListingSourceRecordKey = models.CharField(max_length=30, null=True)
    MediaVisibility = models.CharField(max_length=255, null=True)
    PropMediaProcessingStatus = models.CharField(max_length=255, null=True)
    PropMediaPendingFileName = models.CharField(max_length=3000, null=True)
    PropMediaExtSysProcessingCode = models.CharField(max_length=4000, null=True)
    PropMediaExtSysProcessingTime = models.IntegerField(null=True)
    PropMediaExtSysResizeTime = models.IntegerField(null=True)
    PropMediaExtSysTotalBytes = models.CharField(max_length=255, null=True)
    PropMediaExtSysWriteTime = models.IntegerField(null=True)
    PropMediaExtSysErrorMessage = models.CharField(max_length=4000, null=True)
    MediaObjectId = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "BrightMedia"
        indexes = [
            models.Index(fields=["MediaModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.MediaKey)


class BrightMembers(BaseModel):
    JobTitle = models.CharField(max_length=50, null=True)
    MemberAddress1 = models.CharField(max_length=50, null=True)
    MemberAddress2 = models.CharField(max_length=50, null=True)
    MemberBoxNumber = models.CharField(max_length=10, null=True)
    MemberCity = models.CharField(max_length=50, null=True)
    MemberCountry = models.CharField(max_length=255, null=True)
    MemberCounty = models.CharField(max_length=255, null=True)
    MemberDesignation = models.JSONField(default=list)
    MemberDirectPhone = models.CharField(max_length=16, null=True)
    MemberEmail = models.CharField(max_length=80, null=True)
    MemberFax = models.CharField(max_length=16, null=True)
    MemberFirstName = models.CharField(max_length=50, null=True)
    MemberFullName = models.CharField(max_length=150, null=True)
    MemberFullRoleList = models.CharField(max_length=4000, null=True)
    MemberJoinDate = models.DateField(null=True)
    MemberKey = models.BigIntegerField(primary_key=True)
    MemberLastName = models.CharField(max_length=50, null=True)
    MemberLicenseExpirationDate = models.DateField(null=True)
    MemberLoginId = models.CharField(max_length=25, null=True)
    MemberMiddleInitial = models.CharField(max_length=5, null=True)
    MemberMiddleName = models.CharField(max_length=50, null=True)
    MemberMlsId = models.CharField(max_length=25, null=True)
    MemberMobilePhone = models.CharField(max_length=16, null=True)
    MemberNamePrefix = models.CharField(max_length=255, null=True)
    MemberNameSuffix = models.CharField(max_length=255, null=True)
    MemberNationalAssociationId = models.CharField(max_length=25, null=True)
    MemberNickname = models.CharField(max_length=50, null=True)
    MemberNumViolations = models.IntegerField(null=True)
    MemberOfficePhone = models.CharField(max_length=16, null=True)
    MemberOfficePhoneExt = models.IntegerField(null=True)
    MemberPager = models.CharField(max_length=16, null=True)
    MemberPostalCode = models.CharField(max_length=10, null=True)
    MemberPostalCodePlus4 = models.CharField(max_length=4, null=True)
    MemberPreferredPhone = models.CharField(max_length=16, null=True)
    MemberPreferredPhoneExt = models.IntegerField(null=True)
    MemberPrivateEmail = models.CharField(max_length=3000, null=True)
    MemberRatePlugFlag = models.BooleanField(null=True)
    MemberReinstatementDate = models.DateField(null=True)
    MemberRoleList = models.CharField(max_length=4000, null=True)
    MemberStateLicense = models.CharField(max_length=50, null=True)
    MemberStateLicenseState = models.CharField(max_length=255, null=True)
    MemberStateOrProvince = models.CharField(max_length=255, null=True)
    MemberStatus = models.CharField(max_length=255, null=True)
    MemberStreetDirSuffix = models.CharField(max_length=255, null=True)
    MemberStreetException = models.CharField(max_length=10, null=True)
    MemberStreetName = models.CharField(max_length=50, null=True)
    MemberStreetNumber = models.IntegerField(null=True)
    MemberStreetSuffix = models.CharField(max_length=255, null=True)
    MemberTerminationDate = models.DateField(null=True)
    MemberType = models.CharField(max_length=255, null=True)
    MemberSubType = models.CharField(max_length=255, null=True)
    MemberUnitDesignation = models.CharField(max_length=255, null=True)
    MemberUnitNumber = models.CharField(max_length=20, null=True)
    MemberVoiceMailExt = models.CharField(max_length=15, null=True)
    MemberVoiceMail = models.CharField(max_length=16, null=True)
    ModificationTimestamp = models.DateTimeField(null=True)
    OfficeKey = models.CharField(max_length=255, null=True)
    OfficeMlsId = models.CharField(max_length=25, null=True)
    OfficeBrokerKey = models.CharField(max_length=255, null=True)
    OfficeName = models.CharField(max_length=80, null=True)
    OfficeBrokerMlsId = models.CharField(max_length=25, null=True)
    MemberDateAdded = models.DateTimeField(null=True)
    SocialMediaBlogUrlOrId = models.CharField(max_length=8000, null=True)
    SocialMediaFacebookUrlOrId = models.CharField(max_length=8000, null=True)
    SocialMediaLinkedInUrlOrId = models.CharField(max_length=8000, null=True)
    SocialMediaTwitterUrlOrId = models.CharField(max_length=8000, null=True)
    SocialMediaWebsiteUrlOrId = models.CharField(max_length=8000, null=True)
    SocialMediaYouTubeUrlOrId = models.CharField(max_length=8000, null=True)
    MemberSourceInput = models.CharField(max_length=255, null=True)
    MemberSourceRecordKey = models.CharField(max_length=255, null=True)
    MemberSourceRecordID = models.CharField(max_length=128, null=True)
    MemberSourceBusinessPartner = models.CharField(max_length=255, null=True)
    MemberSourceTransport = models.CharField(max_length=255, null=True)
    SyndicateTo = models.JSONField(default=list)
    MemberSubSystemLocale = models.CharField(max_length=255, null=True)
    MemberSystemLocale = models.CharField(max_length=255, null=True)
    MemberPreferredFirstName = models.CharField(max_length=128, null=True)
    MemberPreferredLastName = models.CharField(max_length=128, null=True)
    MemberBrightConvertedYN = models.BooleanField(null=True)
    MemberAssociationPrimary = models.CharField(max_length=255, null=True)
    MemberAssociationsFullList = models.JSONField(default=list)
    MemberPreviewYN = models.BooleanField(null=True)
    SourceModificationTimestamp = models.DateTimeField(null=True)
    MemberStreetDirPrefix = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "BrightMembers"
        indexes = [
            models.Index(fields=["ModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return self.MemberStreetDirPrefix


class BrightOffices(BaseModel):
    FranchiseAffiliation = models.CharField(max_length=50, null=True)
    IDXOfficeParticipationYN = models.BooleanField(null=True)
    MainOfficeKey = models.CharField(max_length=255, null=True)
    MainOfficeMlsId = models.CharField(max_length=25, null=True)
    ModificationTimestamp = models.DateTimeField(null=True)
    OfficeAssociationPrimary = models.CharField(max_length=255, null=True)
    OfficeAddress1 = models.CharField(max_length=50, null=True)
    OfficeAddress2 = models.CharField(max_length=50, null=True)
    OfficeBoxNumber = models.CharField(max_length=10, null=True)
    OfficeBranchType = models.CharField(max_length=255, null=True)
    OfficeBrokerAcceptedPortalTermsOfUseYN = models.BooleanField(null=True)
    OfficeBrokerAcceptedPortalTermsOfUseVersion = models.CharField(
        max_length=10, null=True
    )
    OfficeBrokerKey = models.CharField(max_length=255, null=True)
    OfficeBrokerLeadEmail = models.CharField(max_length=128, null=True)
    OfficeBrokerLeadPhoneNumber = models.CharField(max_length=128, null=True)
    OfficeBrokerMlsId = models.CharField(max_length=25, null=True)
    OfficeCity = models.CharField(max_length=50, null=True)
    OfficeCountry = models.CharField(max_length=255, null=True)
    OfficeCounty = models.CharField(max_length=255, null=True)
    OfficeDateAdded = models.DateTimeField(null=True)
    OfficeDateTerminated = models.DateTimeField(null=True)
    OfficeEmail = models.CharField(max_length=80, null=True)
    OfficeFax = models.CharField(max_length=16, null=True)
    OfficeKey = models.BigIntegerField(primary_key=True)
    OfficeManagerKey = models.CharField(max_length=255, null=True)
    OfficeLatitude = models.CharField(max_length=255, null=True)
    OfficeLeadToListingAgentYN = models.BooleanField(null=True)
    OfficeLongitude = models.CharField(max_length=255, null=True)
    OfficeManagerEmail = models.CharField(max_length=3000, null=True)
    OfficeManagerMlsId = models.CharField(max_length=25, null=True)
    OfficeManagerName = models.CharField(max_length=80, null=True)
    OfficeMlsId = models.CharField(max_length=25, null=True)
    OfficeName = models.CharField(max_length=80, null=True)
    OfficeNationalAssociationId = models.CharField(max_length=25, null=True)
    OfficeNumViolations = models.IntegerField(null=True)
    OfficePhone = models.CharField(max_length=16, null=True)
    OfficePhoneExt = models.IntegerField(null=True)
    OfficePhoneOther = models.CharField(max_length=10, null=True)
    OfficePostalCode = models.CharField(max_length=10, null=True)
    OfficePostalCodePlus4 = models.CharField(max_length=4, null=True)
    OfficeRoleList = models.CharField(max_length=4000, null=True)
    OfficeStateOrProvince = models.CharField(max_length=255, null=True)
    OfficeStatus = models.CharField(max_length=255, null=True)
    OfficeStreetDirSuffix = models.CharField(max_length=255, null=True)
    OfficeStreetException = models.CharField(max_length=10, null=True)
    OfficeStreetName = models.CharField(max_length=50, null=True)
    OfficeStreetNumber = models.IntegerField(null=True)
    OfficeStreetSuffix = models.CharField(max_length=255, null=True)
    OfficeTradingAs = models.CharField(max_length=50, null=True)
    OfficeType = models.CharField(max_length=255, null=True)
    OfficeUnitDesignation = models.CharField(max_length=255, null=True)
    OfficeUnitNumber = models.CharField(max_length=20, null=True)
    OfficeUserName = models.CharField(max_length=30, null=True)
    OfficeSubSystemLocale = models.CharField(max_length=255, null=True)
    OfficeSystemLocale = models.CharField(max_length=255, null=True)
    SocialMediaBlogUrlOrId = models.CharField(max_length=8000, null=True)
    SocialMediaFacebookUrlOrId = models.CharField(max_length=8000, null=True)
    SocialMediaLinkedInUrlOrId = models.CharField(max_length=8000, null=True)
    SocialMediaTwitterUrlOrId = models.CharField(max_length=8000, null=True)
    SocialMediaWebsiteUrlOrId = models.CharField(max_length=8000, null=True)
    SocialMediaYouTubeUrlOrId = models.CharField(max_length=8000, null=True)
    OfficeSourceBusinessPartner = models.CharField(max_length=255, null=True)
    OfficeSourceRecordKey = models.CharField(max_length=255, null=True)
    SyndicateAgentOption = models.CharField(max_length=255, null=True)
    SyndicateTo = models.JSONField(default=list)
    OfficeSourceRecordID = models.CharField(max_length=128, null=True)
    OfficeBrightConvertedYN = models.BooleanField(null=True)
    OfficeSourceInput = models.CharField(max_length=255, null=True)
    OfficeSourceTransport = models.CharField(max_length=255, null=True)
    MainOfficeName = models.CharField(max_length=50, null=True)
    OfficeAssociationsFullList = models.JSONField(default=list)
    OfficeValidationStatus = models.CharField(max_length=255, null=True)
    OfficeCorporateLicense = models.CharField(max_length=50, null=True)
    SourceModificationTimestamp = models.DateTimeField(null=True)
    OfficeStreetDirPrefix = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "BrightOffices"
        indexes = [
            models.Index(fields=["ModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.OfficeKey)


class BrightOpenHouses(BaseModel):
    County = models.CharField(max_length=255, null=True)
    ListingId = models.CharField(max_length=255, null=True)
    MlsStatus = models.CharField(max_length=255, null=True)
    OpenHouseAttendedBy = models.CharField(max_length=255, null=True)
    OpenHouseCreationTimestamp = models.DateTimeField(null=True)
    OpenHouseDate = models.DateField(null=True)
    OpenHouseItemNumber = models.IntegerField(null=True)
    OpenHouseEndTime = models.DateTimeField(null=True)
    OpenHouseKey = models.BigIntegerField(primary_key=True)
    OpenHouseListingKey = models.CharField(max_length=255, null=True)
    OpenHouseModificationTimestamp = models.DateTimeField(null=True)
    OpenHouseSourceBusinessPartner = models.CharField(max_length=255, null=True)
    OpenHouseSourceInput = models.CharField(max_length=255, null=True)
    OpenHouseRemarks = models.CharField(max_length=500, null=True)
    OpenHouseSourceTransport = models.CharField(max_length=255, null=True)
    OpenHouseSubSystemLocale = models.CharField(max_length=255, null=True)
    OpenHouseSystemLocale = models.CharField(max_length=255, null=True)
    ListingSourceRecordKey = models.CharField(max_length=30, null=True)
    OpenHouseExternalSystemID = models.CharField(max_length=30, null=True)
    ListOfficeMlsId = models.CharField(max_length=25, null=True)
    OpenHouseStartTime = models.DateTimeField(null=True)
    OpenHouseType = models.CharField(max_length=255, null=True)
    OpenHouseMethod = models.CharField(max_length=255, null=True)
    VirtualOpenHouseUrl = models.CharField(max_length=4000, null=True)
    ExpectedOnMarketDate = models.DateField(null=True)

    class Meta:
        verbose_name_plural = "BrightOpenHouses"
        indexes = [
            models.Index(fields=["OpenHouseModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.OpenHouseKey)


class BrightProperties(BaseModel):
    Location = models.CharField(max_length=255, null=True)
    BuyerAgentMlsId = models.CharField(max_length=25, null=True)
    BuyerAgentCellPhone = models.CharField(max_length=16, null=True)
    BuyerAgentDirectPhone = models.CharField(max_length=16, null=True)
    SourceBuyerTeamName = models.CharField(max_length=100, null=True)
    BuyerAgentEmail = models.CharField(max_length=80, null=True)
    BuyerAgentFax = models.CharField(max_length=16, null=True)
    BuyerAgentFirstName = models.CharField(max_length=50, null=True)
    BuyerAgentFullName = models.CharField(max_length=150, null=True)
    BuyerAgentKey = models.CharField(max_length=255, null=True)
    BuyerAgentLastName = models.CharField(max_length=50, null=True)
    BuyerAgentNameSuffix = models.CharField(max_length=255, null=True)
    BuyerAgentOfficePhone = models.CharField(max_length=16, null=True)
    BuyerAgentOfficePhoneExt = models.IntegerField(null=True)
    BuyerAgentPreferredPhone = models.CharField(max_length=16, null=True)
    BuyerAgentPreferredPhoneExt = models.IntegerField(null=True)
    BuyerAgentAOR = models.CharField(max_length=255, null=True)
    BuyerAgentNamePrefix = models.CharField(max_length=10, null=True)
    BuyerAgentURL = models.URLField(max_length=4000, null=True)
    BuyerAgentVoiceMail = models.CharField(max_length=16, null=True)
    BuyerAgentVoiceMailExt = models.IntegerField(null=True)
    BuyerAgentStateLicenseNumber = models.CharField(max_length=25, null=True)
    BuyerAgentTeamKey = models.CharField(max_length=255, null=True)
    BuyerAgentTeamLeadAgentKey = models.CharField(max_length=255, null=True)
    BuyerAgentTeamLeadStateLicenseNumber = models.CharField(max_length=256, null=True)
    BuyerAgentTeamName = models.CharField(max_length=250, null=True)
    BuyerAgentTeamLeadAgentName = models.CharField(max_length=150, null=True)
    LeaseConsideredYN = models.BooleanField(null=True)
    DualAgencyYN = models.BooleanField(null=True)
    HomeWarrantyYN = models.BooleanField(null=True)
    ListingAgreementType = models.CharField(max_length=255, null=True)
    ProspectsExcludedYN = models.BooleanField(null=True)
    ListingId = models.CharField(max_length=255, null=True)
    ListingKey = models.BigIntegerField(primary_key=True)
    ListingServiceType = models.CharField(max_length=255, null=True)
    StandardStatus = models.CharField(max_length=255, null=True)
    MlsStatus = models.CharField(max_length=255, null=True)
    AuctionBuyerPremium = models.CharField(max_length=255, null=True)
    AuctionBuyerPremiumType = models.CharField(max_length=255, null=True)
    AuctionEndDate = models.DateField(null=True)
    AuctionLocation = models.CharField(max_length=30, null=True)
    AuctionPreview1EndDate = models.DateField(null=True)
    AuctionPreview1StartDate = models.DateField(null=True)
    AuctionPublishedMinBid = models.CharField(max_length=255, null=True)
    AuctionRegistrationDeadline = models.DateField(null=True)
    AuctionRegistrationURL = models.URLField(max_length=4000, null=True)
    AuctionStartDate = models.DateField(null=True)
    AuctionTermsURL = models.URLField(max_length=4000, null=True)
    AuctionTime = models.CharField(max_length=24, null=True)
    AuctionType = models.CharField(max_length=255, null=True)
    EarnestMoney = models.CharField(max_length=255, null=True)
    OnSitePhone = models.CharField(max_length=10, null=True)
    PropertyRelationshipList = models.JSONField(default=list)
    ListingSourceRecordID = models.CharField(max_length=255, null=True)
    ListingSourceRecordKey = models.CharField(max_length=30, null=True)
    ListingSourceBusinessPartner = models.CharField(max_length=255, null=True)
    SystemLocale = models.CharField(max_length=255, null=True)
    SubSystemLocale = models.CharField(max_length=255, null=True)
    TotalBrokerOpenHouses = models.IntegerField(null=True)
    TotalOpenHouses = models.IntegerField(null=True)
    TotalPublicOpenHouses = models.IntegerField(null=True)
    TotalShowings = models.IntegerField(null=True)
    TotalTaxesPaymentFrequency = models.CharField(max_length=255, null=True)
    TotalVirtualTours = models.IntegerField(null=True)
    ComparableYN = models.BooleanField(null=True)
    ListingSourceTransport = models.CharField(max_length=255, null=True)
    ListingSourceInput = models.CharField(max_length=255, null=True)
    MunicipalInspectionsYN = models.BooleanField(null=True)
    DistanceToBodyOfWaterUnits = models.CharField(max_length=255, null=True)
    DistanceToBodyOfWater = models.CharField(max_length=255, null=True)
    ListAgentBrightConvertedYN = models.BooleanField(null=True)
    ListOfficeBrightConvertedYN = models.BooleanField(null=True)
    OneBedroomUnits = models.CharField(max_length=255, null=True)
    ThreeBedroomUnits = models.CharField(max_length=255, null=True)
    TwoBedroomUnits = models.CharField(max_length=255, null=True)
    UseCopiedPhoto = models.CharField(max_length=255, null=True)
    SingleRoomUnits = models.CharField(max_length=255, null=True)
    OpenHouseList = models.JSONField(default=list)
    ProfessionalRelationshipList = models.JSONField(default=list)
    VacationRentalYN = models.BooleanField(null=True)
    ComingSoonEligibilityDays = models.CharField(max_length=255, null=True)
    CwaKey = models.CharField(max_length=255, null=True)
    LossMitigationFeeYN = models.BooleanField(null=True)
    SmokingAllowedYN = models.BooleanField(null=True)
    CloseAgencyType = models.CharField(max_length=255, null=True)
    AcceptableFinancing = models.JSONField(default=list)
    DuplicateListingYN = models.BooleanField(null=True)
    DuplicateSurvivingListingKey = models.CharField(max_length=255, null=True)
    DuplicateMlsIDs = models.JSONField(default=list)
    ClientApplicationEditedYN = models.BooleanField(null=True)
    ScheduledSubmissionAction = models.CharField(max_length=255, null=True)
    CopiedFromKeys = models.CharField(max_length=128, null=True)
    BuyerOfficeKey = models.CharField(max_length=255, null=True)
    BuyerOfficeEmail = models.CharField(max_length=80, null=True)
    BuyerOfficeFax = models.CharField(max_length=16, null=True)
    BuyerOfficeName = models.CharField(max_length=50, null=True)
    BuyerOfficeMlsId = models.CharField(max_length=25, null=True)
    BuyerOfficePhone = models.CharField(max_length=16, null=True)
    BuyerOfficePhoneExt = models.IntegerField(null=True)
    BuyerOfficeAOR = models.CharField(max_length=255, null=True)
    BuyerOfficeURL = models.URLField(max_length=4000, null=True)
    BuyerOfficeBrokerOfRecordID = models.CharField(max_length=50, null=True)
    BuyerOfficeBrokerOfRecordKey = models.CharField(max_length=255, null=True)
    BuyerOfficeDistance = models.CharField(max_length=255, null=True)
    BuyerOfficeResponsibleBrokerKey = models.CharField(max_length=255, null=True)
    BuyerOfficeResponsibleBrokerLicenseNumber = models.CharField(
        max_length=128, null=True
    )
    ClosePrice = models.CharField(max_length=255, null=True)
    ListPriceLow = models.CharField(max_length=255, null=True)
    PreviousListPrice = models.CharField(max_length=255, null=True)
    ListPrice = models.CharField(max_length=255, null=True)
    OriginalListPrice = models.CharField(max_length=255, null=True)
    CancelationDate = models.DateField(null=True)
    CloseDate = models.DateField(null=True)
    PurchaseContractDate = models.DateField(null=True)
    DaysOnMarket = models.IntegerField(null=True)
    CumulativeDaysOnMarket = models.IntegerField(null=True)
    ExpirationDate = models.DateField(null=True)
    OriginalEntryTimestamp = models.DateTimeField(null=True)
    MLSListDate = models.DateField(null=True)
    ListingContractDate = models.DateField(null=True)
    PriceChangeTimestamp = models.DateTimeField(null=True)
    MajorChangeType = models.CharField(max_length=255, null=True)
    ModificationTimestamp = models.DateTimeField(null=True)
    BaseOffMarketDate = models.DateField(null=True)
    OffMarketDate = models.DateField(null=True)
    OffMarketTimestamp = models.DateTimeField(null=True)
    OnMarketDate = models.DateField(null=True)
    OnMarketTimestamp = models.DateTimeField(null=True)
    PendingTimestamp = models.DateTimeField(null=True)
    MajorChangeTimestamp = models.DateTimeField(null=True)
    StatusChangeTimestamp = models.DateTimeField(null=True)
    WithdrawnDate = models.DateField(null=True)
    ContingentDate = models.DateField(null=True)
    ContractStatusChangeDate = models.DateField(null=True)
    BackToActiveDate = models.DateField(null=True)
    DaysOnComingSoon = models.IntegerField(null=True)
    DomPropertyActiveYN = models.BooleanField(null=True)
    DomPropertyCalculatedDate = models.DateTimeField(null=True)
    ExpectedOnMarketDate = models.DateField(null=True)
    RawDomListing = models.IntegerField(null=True)
    RawDomProperty = models.IntegerField(null=True)
    SourceModificationTimestamp = models.DateTimeField(null=True)
    DomPropertyLisLtKey = models.CharField(max_length=255, null=True)
    SourceDaysOnMarketProperty = models.CharField(max_length=255, null=True)
    SourceDaysOnMarket = models.CharField(max_length=255, null=True)
    CoBuyerAgentCellPhone = models.CharField(max_length=16, null=True)
    CoBuyerAgentDirectPhone = models.CharField(max_length=16, null=True)
    CoBuyerAgentEmail = models.CharField(max_length=80, null=True)
    CoBuyerAgentFax = models.CharField(max_length=16, null=True)
    CoBuyerAgentFirstName = models.CharField(max_length=50, null=True)
    CoBuyerAgentFullName = models.CharField(max_length=150, null=True)
    CoBuyerAgentMlsId = models.CharField(max_length=25, null=True)
    CoBuyerAgentKey = models.CharField(max_length=255, null=True)
    CoBuyerAgentLastName = models.CharField(max_length=50, null=True)
    CoBuyerAgentNameSuffix = models.CharField(max_length=255, null=True)
    CoBuyerAgentOfficePhone = models.CharField(max_length=16, null=True)
    CoBuyerAgentOfficePhoneExt = models.IntegerField(null=True)
    CoBuyerAgentPreferredPhone = models.CharField(max_length=16, null=True)
    CoBuyerAgentPreferredPhoneExt = models.IntegerField(null=True)
    CoBuyerAgentAOR = models.CharField(max_length=255, null=True)
    CoBuyerAgentNamePrefix = models.CharField(max_length=10, null=True)
    CoBuyerAgentURL = models.URLField(max_length=4000, null=True)
    CoBuyerAgentVoiceMail = models.CharField(max_length=16, null=True)
    CoBuyerAgentVoiceMailExt = models.IntegerField(null=True)
    CoBuyerAgentStateLicenseNumber = models.CharField(max_length=25, null=True)
    CoBuyerAgentTeamKey = models.CharField(max_length=255, null=True)
    CoBuyerAgentTeamLeadAgentKey = models.CharField(max_length=255, null=True)
    CoBuyerAgentTeamLeadStateLicenseNumber = models.CharField(max_length=256, null=True)
    CoBuyerAgentTeamName = models.CharField(max_length=250, null=True)
    CoBuyerAgentTeamLeadAgentName = models.CharField(max_length=150, null=True)
    CoBuyerOfficeKey = models.CharField(max_length=255, null=True)
    CoBuyerOfficeEmail = models.CharField(max_length=80, null=True)
    CoBuyerOfficeFax = models.CharField(max_length=16, null=True)
    CoBuyerOfficeName = models.CharField(max_length=50, null=True)
    CoBuyerOfficeMlsId = models.CharField(max_length=25, null=True)
    CoBuyerOfficePhone = models.CharField(max_length=16, null=True)
    CoBuyerOfficePhoneExt = models.IntegerField(null=True)
    CoBuyerOfficeAOR = models.CharField(max_length=255, null=True)
    CoBuyerOfficeURL = models.URLField(max_length=4000, null=True)
    AssociationAmenities = models.JSONField(default=list)
    AssociationFee = models.CharField(max_length=255, null=True)
    AssociationFee2 = models.CharField(max_length=255, null=True)
    AssociationFee2Frequency = models.CharField(max_length=255, null=True)
    AssociationFeeFrequency = models.CharField(max_length=255, null=True)
    AssociationFeeIncludes = models.JSONField(default=list)
    AssociationName = models.CharField(max_length=50, null=True)
    AssociationName2 = models.CharField(max_length=50, null=True)
    AssociationPhone = models.CharField(max_length=16, null=True)
    AssociationPhone2 = models.CharField(max_length=16, null=True)
    CondoYN = models.BooleanField(null=True)
    AssociationYN = models.BooleanField(null=True)
    AssociationManagementType = models.JSONField(default=list)
    CommunityRules = models.JSONField(default=list)
    ElevatorUseFee = models.CharField(max_length=255, null=True)
    ManagementAltPhone = models.CharField(max_length=10, null=True)
    ManagementFax = models.CharField(max_length=10, null=True)
    ManagementPhone = models.CharField(max_length=10, null=True)
    NonPowerBoatsPermitted = models.CharField(max_length=255, null=True)
    NumberOfCommunitySlips = models.CharField(max_length=255, null=True)
    NumberOfCommunityDocks = models.CharField(max_length=255, null=True)
    PhysicalDockSlipConveysYN = models.BooleanField(null=True)
    PowerBoatsPermitted = models.CharField(max_length=255, null=True)
    PropertyManagerYN = models.BooleanField(null=True)
    PropertyManagerFirstName = models.CharField(max_length=10, null=True)
    PropertyManagerLastName = models.CharField(max_length=20, null=True)
    PropertyManagmentCompany = models.CharField(max_length=80, null=True)
    CapitalContributionFee = models.CharField(max_length=255, null=True)
    OtherFees = models.CharField(max_length=255, null=True)
    OtherFeesFrequency = models.CharField(max_length=255, null=True)
    AdditionalAssociationFees = models.JSONField(default=list)
    AssociationRecreationFeeYN = models.BooleanField(null=True)
    AssociationRecreationFee = models.CharField(max_length=255, null=True)
    Transportation = models.JSONField(default=list)
    CoListAgentCellPhone = models.CharField(max_length=16, null=True)
    CoListAgentDirectPhone = models.CharField(max_length=16, null=True)
    CoListAgentEmail = models.CharField(max_length=80, null=True)
    CoListAgentFax = models.CharField(max_length=16, null=True)
    CoListAgentFirstName = models.CharField(max_length=50, null=True)
    CoListAgentFullName = models.CharField(max_length=150, null=True)
    CoListAgentMlsId = models.CharField(max_length=25, null=True)
    CoListAgentKey = models.CharField(max_length=255, null=True)
    CoListAgentLastName = models.CharField(max_length=50, null=True)
    CoListAgentNameSuffix = models.CharField(max_length=255, null=True)
    CoListAgentOfficePhone = models.CharField(max_length=16, null=True)
    CoListAgentOfficePhoneExt = models.IntegerField(null=True)
    CoListAgentPreferredPhone = models.CharField(max_length=16, null=True)
    CoListAgentPreferredPhoneExt = models.IntegerField(null=True)
    CoListAgentAOR = models.CharField(max_length=255, null=True)
    CoListAgentNamePrefix = models.CharField(max_length=10, null=True)
    CoListAgentURL = models.URLField(max_length=4000, null=True)
    CoListAgentVoiceMail = models.CharField(max_length=16, null=True)
    CoListAgentVoiceMailExt = models.IntegerField(null=True)
    CoListAgentStateLicenseNumber = models.CharField(max_length=25, null=True)
    CoListAgentTeamKey = models.CharField(max_length=255, null=True)
    CoListAgentTeamLeadAgentKey = models.CharField(max_length=255, null=True)
    CoListAgentTeamLeadStateLicenseNumber = models.CharField(max_length=256, null=True)
    CoListAgentTeamName = models.CharField(max_length=250, null=True)
    CoListAgentTeamLeadAgentName = models.CharField(max_length=150, null=True)
    City = models.CharField(max_length=50, null=True)
    CityID = models.CharField(max_length=255, null=True)
    Country = models.CharField(max_length=255, null=True)
    County = models.CharField(max_length=255, null=True)
    IncorporatedCityName = models.CharField(max_length=50, null=True)
    StreetNumber = models.CharField(max_length=25, null=True)
    PostalCode = models.CharField(max_length=10, null=True)
    StateOrProvince = models.CharField(max_length=255, null=True)
    StreetDirPrefix = models.CharField(max_length=255, null=True)
    StreetDirSuffix = models.CharField(max_length=255, null=True)
    StreetName = models.CharField(max_length=50, null=True)
    StreetNumberNumeric = models.IntegerField(null=True)
    StreetSuffix = models.CharField(max_length=255, null=True)
    StreetSuffixModifier = models.CharField(max_length=25, null=True)
    UnitNumber = models.CharField(max_length=25, null=True)
    UnparsedAddress = models.CharField(max_length=255, null=True)
    PostalCodePlus4 = models.CharField(max_length=4, null=True)
    ValidationStatus = models.CharField(max_length=255, null=True)
    TrafficCount = models.JSONField(default=list)
    ListingLocale = models.CharField(max_length=255, null=True)
    FullStreetAddress = models.CharField(max_length=80, null=True)
    TrafficCountSource = models.CharField(max_length=30, null=True)
    StreetNameAndSuffix = models.CharField(max_length=65, null=True)
    IncorporatedCityKey = models.CharField(max_length=255, null=True)
    CoListOfficeKey = models.CharField(max_length=255, null=True)
    CoListOfficeMlsId = models.CharField(max_length=25, null=True)
    CoListOfficeEmail = models.CharField(max_length=80, null=True)
    CoListOfficeFax = models.CharField(max_length=16, null=True)
    CoListOfficeName = models.CharField(max_length=50, null=True)
    CoListOfficePhone = models.CharField(max_length=16, null=True)
    CoListOfficePhoneExt = models.IntegerField(null=True)
    CoListOfficeAOR = models.CharField(max_length=255, null=True)
    CoListOfficeURL = models.URLField(max_length=4000, null=True)
    MLSAreaMajor = models.CharField(max_length=255, null=True)
    SussexDEQuadrants = models.CharField(max_length=255, null=True)
    MLSAreaMinor = models.CharField(max_length=255, null=True)
    LegalSubdivision = models.CharField(max_length=50, null=True)
    SubdivisionName = models.CharField(max_length=50, null=True)
    AvailabilityDate = models.DateField(null=True)
    BuyerFinancing = models.JSONField(default=list)
    Concessions = models.CharField(max_length=255, null=True)
    ConcessionsSubsidy = models.CharField(max_length=255, null=True)
    ConcessionRemarks = models.CharField(max_length=100, null=True)
    LastContingencyExpires = models.DateField(null=True)
    KickOutClauseYN = models.BooleanField(null=True)
    NumDaysInKickOutClause = models.CharField(max_length=255, null=True)
    Possession = models.JSONField(default=list)
    ContingencyList = models.JSONField(default=list)
    AutomaticallyCloseOnCloseDateYN = models.BooleanField(null=True)
    CrossStreet = models.CharField(max_length=50, null=True)
    OCCrossStreet = models.CharField(max_length=255, null=True)
    Directions = models.CharField(max_length=1024, null=True)
    Latitude = models.CharField(max_length=255, null=True)
    Longitude = models.CharField(max_length=255, null=True)
    MapURL = models.URLField(max_length=4000, null=True)
    BuyerAgencyCompensationType = models.CharField(max_length=255, null=True)
    BuyerAgencyCompensation = models.CharField(max_length=25, null=True)
    SubAgencyAdditionalCompensation = models.CharField(max_length=128, null=True)
    SubAgencyCompensation = models.CharField(max_length=25, null=True)
    SubAgencyCompensationType = models.CharField(max_length=255, null=True)
    TransactionBrokerCompensation = models.CharField(max_length=25, null=True)
    TransactionBrokerCompensationType = models.CharField(max_length=255, null=True)
    DualVariableCompensationYN = models.BooleanField(null=True)
    LeaseRenewalCompensation = models.JSONField(default=list)
    CompensationList = models.JSONField(default=list)
    BuyerAgencyCompensation2 = models.CharField(max_length=25, null=True)
    BuyerAgencyCompensation2Type = models.CharField(max_length=255, null=True)
    SubAgencyCompensation2 = models.CharField(max_length=25, null=True)
    SubAgencyCompensation2Type = models.CharField(max_length=255, null=True)
    TransactionBrokerCompensation2 = models.CharField(max_length=25, null=True)
    TransactionBrokerCompensation2Type = models.CharField(max_length=255, null=True)
    TransactionBrokerCompensationSelection = models.CharField(max_length=255, null=True)
    BuyerAgencyCompensationSelection = models.CharField(max_length=255, null=True)
    SubAgencyCompensationSelection = models.CharField(max_length=255, null=True)
    ListAgentMlsId = models.CharField(max_length=25, null=True)
    ListAgentCellPhone = models.CharField(max_length=16, null=True)
    ListAgentDirectPhone = models.CharField(max_length=16, null=True)
    ListAgentEmail = models.CharField(max_length=80, null=True)
    SourceListTeamName = models.CharField(max_length=100, null=True)
    ListAgentFax = models.CharField(max_length=16, null=True)
    ListAgentFirstName = models.CharField(max_length=50, null=True)
    ListAgentFullName = models.CharField(max_length=150, null=True)
    ListAgentKey = models.CharField(max_length=255, null=True)
    ListAgentLastName = models.CharField(max_length=50, null=True)
    ListAgentNameSuffix = models.CharField(max_length=255, null=True)
    ListAgentOfficePhone = models.CharField(max_length=16, null=True)
    ListAgentOfficePhoneExt = models.IntegerField(null=True)
    ListAgentPreferredPhone = models.CharField(max_length=16, null=True)
    ListAgentPreferredPhoneExt = models.IntegerField(null=True)
    ListAgentAOR = models.CharField(max_length=255, null=True)
    ListAgentNamePrefix = models.CharField(max_length=10, null=True)
    ListAgentURL = models.URLField(max_length=4000, null=True)
    ListAgentVoiceMail = models.CharField(max_length=16, null=True)
    ListAgentVoiceMailExt = models.IntegerField(null=True)
    ListAgentRatePlugYN = models.BooleanField(null=True)
    ListAgentStateLicenseNumber = models.CharField(max_length=25, null=True)
    ListAgentTeamKey = models.CharField(max_length=255, null=True)
    ListAgentTeamLeadAgentKey = models.CharField(max_length=255, null=True)
    ListAgentTeamLeadStateLicenseNumber = models.CharField(max_length=256, null=True)
    ListAgentTeamName = models.CharField(max_length=250, null=True)
    ListAgentTeamLeadAgentName = models.CharField(max_length=150, null=True)
    ListAgentTeamLeadAgentEmail = models.CharField(max_length=3000, null=True)
    ListAgentTeamLeadAgentURL = models.URLField(max_length=4000, null=True)
    ListAgentTeamLeadAgentCellPhone = models.CharField(max_length=10, null=True)
    ListAgentTeamLeadAgentDirectPhone = models.CharField(max_length=10, null=True)
    ListAgentTeamLeadAgentFax = models.CharField(max_length=10, null=True)
    ListAgentTeamLeadAgentOfficePhone = models.CharField(max_length=10, null=True)
    ListAgentTeamLeadAgentOfficePhoneExt = models.IntegerField(null=True)
    ListAgentTeamLeadAgentPreferredPhone = models.CharField(max_length=10, null=True)
    ListAgentTeamLeadAgentPreferredPhoneExt = models.IntegerField(null=True)
    ListAgentTeamLeadAgentVoiceMail = models.CharField(max_length=10, null=True)
    ListAgentTeamLeadAgentVoiceMailExt = models.CharField(max_length=5, null=True)
    ListAgentTeamLeadAgentNameSuffix = models.CharField(max_length=255, null=True)
    ListAgentTeamLeadAgentLastName = models.CharField(max_length=50, null=True)
    ListAgentTeamLeadAgentFirstName = models.CharField(max_length=50, null=True)
    ListAgentTeamLeadAgentNamePrefix = models.CharField(max_length=256, null=True)
    ListAgentTeamLeadAgentRatePlugYN = models.BooleanField(null=True)
    ListAgentTeamLeadAgentAOR = models.CharField(max_length=255, null=True)
    ListSyndicateListingsAsTeamLeadPartyPermKey = models.CharField(
        max_length=255, null=True
    )
    ListAgentTeamLeadAgentMlsId = models.CharField(max_length=30, null=True)
    ListAgentTeamLeadAgentBrightConvertedYN = models.BooleanField(null=True)
    AutoPopulateSchoolsYN = models.BooleanField(null=True)
    ElementarySchool = models.CharField(max_length=80, null=True)
    ElementarySchoolSource = models.CharField(max_length=255, null=True)
    HighSchool = models.CharField(max_length=80, null=True)
    HighSchoolSource = models.CharField(max_length=255, null=True)
    MiddleOrJuniorSchool = models.CharField(max_length=80, null=True)
    MiddleSchoolSource = models.CharField(max_length=255, null=True)
    SchoolDistrictName = models.CharField(max_length=50, null=True)
    SchoolDistrictSource = models.CharField(max_length=255, null=True)
    SchoolDistrictKey = models.CharField(max_length=255, null=True)
    ListOfficeKey = models.CharField(max_length=255, null=True)
    ListOfficeEmail = models.CharField(max_length=80, null=True)
    ListOfficeFax = models.CharField(max_length=16, null=True)
    ListOfficeName = models.CharField(max_length=50, null=True)
    ListOfficeMlsId = models.CharField(max_length=25, null=True)
    ListOfficePhone = models.CharField(max_length=16, null=True)
    ListOfficePhoneExt = models.IntegerField(null=True)
    ListOfficeAOR = models.CharField(max_length=255, null=True)
    ListOfficeURL = models.URLField(max_length=4000, null=True)
    ListOfficeBrokerOfRecordID = models.CharField(max_length=50, null=True)
    ListOfficeBrokerOfRecordKey = models.CharField(max_length=255, null=True)
    ListOfficeDistance = models.CharField(max_length=255, null=True)
    ListOfficeCounty = models.CharField(max_length=128, null=True)
    ListOfficeResponsibleBrokerKey = models.CharField(max_length=255, null=True)
    ListOfficeResponsibleBrokerLicenseNumber = models.CharField(
        max_length=128, null=True
    )
    InternetAddressDisplayYN = models.BooleanField(null=True)
    InternetAutomatedValuationDisplayYN = models.BooleanField(null=True)
    InternetConsumerCommentYN = models.BooleanField(null=True)
    InternetEntireListingDisplayYN = models.BooleanField(null=True)
    SignOnPropertyYN = models.BooleanField(null=True)
    SyndicateToOption = models.JSONField(default=list)
    SyndicateTo = models.JSONField(default=list)
    VOWAVMYN = models.BooleanField(null=True)
    VOWAddrYN = models.BooleanField(null=True)
    VOWCommentYN = models.BooleanField(null=True)
    VOWListYN = models.BooleanField(null=True)
    VirtualTourURLUnbranded = models.URLField(max_length=4000, null=True)
    AboveGradeFinishedArea = models.IntegerField(null=True)
    AboveGradeFinishedAreaUnits = models.CharField(max_length=255, null=True)
    AttachedGarageYN = models.BooleanField(null=True)
    BelowGradeFinishedArea = models.IntegerField(null=True)
    BelowGradeFinishedAreaSource = models.CharField(max_length=255, null=True)
    Basement = models.JSONField(default=list)
    BathroomsTotalInteger = models.CharField(max_length=255, null=True)
    BathroomsFull = models.IntegerField(null=True)
    BathroomsHalf = models.IntegerField(null=True)
    BedroomsTotal = models.IntegerField(null=True)
    BelowGradeFinishedAreaUnits = models.CharField(max_length=255, null=True)
    BuilderName = models.CharField(max_length=50, null=True)
    BuildingAreaUnits = models.CharField(max_length=255, null=True)
    Skirt = models.JSONField(default=list)
    CarportSpaces = models.IntegerField(null=True)
    CarportYN = models.BooleanField(null=True)
    Cooling = models.JSONField(default=list)
    CoolingYN = models.BooleanField(null=True)
    DeptOfHousingDecal1 = models.CharField(max_length=25, null=True)
    DeptOfHousingDecal2 = models.CharField(max_length=25, null=True)
    DeptOfHousingDecal3 = models.CharField(max_length=25, null=True)
    DoorFeatures = models.JSONField(default=list)
    EntryLevel = models.CharField(max_length=255, null=True)
    EntryLocation = models.CharField(max_length=255, null=True)
    DirectionFaces = models.CharField(max_length=255, null=True)
    ConstructionMaterials = models.JSONField(default=list)
    ExteriorFeatures = models.JSONField(default=list)
    FireplaceYN = models.BooleanField(null=True)
    FireplaceFeatures = models.JSONField(default=list)
    FireplacesTotal = models.IntegerField(null=True)
    Flooring = models.JSONField(default=list)
    ArchitectName = models.CharField(max_length=50, null=True)
    FoundationDetails = models.JSONField(default=list)
    GarageSpaces = models.CharField(max_length=255, null=True)
    BuildingAreaTotal = models.CharField(max_length=255, null=True)
    AccessibilityFeatures = models.JSONField(default=list)
    GarageYN = models.BooleanField(null=True)
    Heating = models.JSONField(default=list)
    HeatingYN = models.BooleanField(null=True)
    NumberOfSeparateElectricMeters = models.CharField(max_length=255, null=True)
    AboveGradeFinishedAreaSource = models.CharField(max_length=255, null=True)
    NumberOfSeparateGasMeters = models.CharField(max_length=255, null=True)
    BuildingAreaSource = models.CharField(max_length=255, null=True)
    NumberOfSeparateWaterMeters = models.CharField(max_length=255, null=True)
    InteriorFeatures = models.JSONField(default=list)
    LivingAreaSource = models.CharField(max_length=255, null=True)
    License1 = models.CharField(max_length=25, null=True)
    License2 = models.CharField(max_length=25, null=True)
    License3 = models.CharField(max_length=25, null=True)
    LivingArea = models.IntegerField(null=True)
    LivingAreaUnits = models.CharField(max_length=255, null=True)
    Make = models.CharField(max_length=50, null=True)
    Model = models.CharField(max_length=50, null=True)
    BuilderModel = models.CharField(max_length=50, null=True)
    LisBuilderModel = models.CharField(max_length=50, null=True)
    NewConstructionYN = models.BooleanField(null=True)
    ConstructionCompletedYN = models.BooleanField(null=True)
    OpenParkingYN = models.BooleanField(null=True)
    OpenParkingSpaces = models.CharField(max_length=255, null=True)
    ParkingFeatures = models.JSONField(default=list)
    PatioAndPorchFeatures = models.JSONField(default=list)
    PropertyAttachedYN = models.BooleanField(null=True)
    CommonWalls = models.JSONField(default=list)
    Roof = models.JSONField(default=list)
    SerialU = models.CharField(max_length=25, null=True)
    SerialX = models.CharField(max_length=25, null=True)
    SerialXX = models.CharField(max_length=25, null=True)
    Stories = models.IntegerField(null=True)
    StoriesTotal = models.CharField(max_length=255, null=True)
    Levels = models.JSONField(default=list)
    BodyType = models.JSONField(default=list)
    OtherStructures = models.JSONField(default=list)
    ArchitecturalStyle = models.JSONField(default=list)
    ParkingTotal = models.CharField(max_length=255, null=True)
    HabitableResidenceYN = models.BooleanField(null=True)
    WallsCeilings = models.JSONField(default=list)
    WindowFeatures = models.JSONField(default=list)
    YearBuilt = models.IntegerField(null=True)
    YearBuiltEffective = models.CharField(max_length=255, null=True)
    WalkScore = models.CharField(max_length=255, null=True)
    MobileDimUnits = models.CharField(max_length=255, null=True)
    MobileLength = models.IntegerField(null=True)
    MobileWidth = models.IntegerField(null=True)
    NumberOfPads = models.CharField(max_length=255, null=True)
    LeasableArea = models.IntegerField(null=True)
    LeasableAreaUnits = models.CharField(max_length=255, null=True)
    YearBuiltSource = models.CharField(max_length=255, null=True)
    PropertyCondition = models.JSONField(default=list)
    BuildingWinterizedYN = models.BooleanField(null=True)
    BuildoutAllowanceYN = models.BooleanField(null=True)
    AboveGradeUnfinishedArea = models.IntegerField(null=True)
    AboveGradeUnfinishedAreaSource = models.CharField(max_length=255, null=True)
    AboveGradeUnfinishedAreaUnits = models.CharField(max_length=255, null=True)
    BasementFinishedPercent = models.CharField(max_length=255, null=True)
    BasementFootprintPercent = models.CharField(max_length=255, null=True)
    BasementYN = models.BooleanField(null=True)
    BelowGradeUnfinishedArea = models.IntegerField(null=True)
    BelowGradeUnfinishedAreaSource = models.CharField(max_length=255, null=True)
    ContiguousSquareFeetAvailableYN = models.BooleanField(null=True)
    BelowGradeUnfinishedAreaUnits = models.CharField(max_length=255, null=True)
    CoolingFuel = models.JSONField(default=list)
    Elevators = models.CharField(max_length=255, null=True)
    TotalLoadingDocks = models.CharField(max_length=255, null=True)
    TotalLevelers = models.CharField(max_length=255, null=True)
    TotalDriveInDoors = models.CharField(max_length=255, null=True)
    HeatingFuel = models.JSONField(default=list)
    HotWater = models.JSONField(default=list)
    OtherUnits = models.CharField(max_length=4000, null=True)
    ParkingSpaceNumber = models.CharField(max_length=5, null=True)
    UnitFloors = models.CharField(max_length=255, null=True)
    StoryList = models.JSONField(default=list)
    ApproximateOfficeSquareFeet = models.IntegerField(null=True)
    ApproximateRetailSquareFeet = models.IntegerField(null=True)
    ApproximateWarehouseSquareFeet = models.IntegerField(null=True)
    ClearSpanCeilingHeight = models.JSONField(default=list)
    DriveInDoorHeight = models.JSONField(default=list)
    NetSquareFeet = models.CharField(max_length=255, null=True)
    NumberOfOverheadDoors = models.CharField(max_length=255, null=True)
    TotalRestrooms = models.CharField(max_length=255, null=True)
    StructureDesignType = models.CharField(max_length=255, null=True)
    UnitWasherDryerHookupYN = models.BooleanField(null=True)
    CentralAirYN = models.BooleanField(null=True)
    LowerLevelsTotalBaths = models.CharField(max_length=255, null=True)
    LowerLevelsTotalBedrooms = models.CharField(max_length=255, null=True)
    LowerLevelsTotalFullBaths = models.CharField(max_length=255, null=True)
    LowerLevelsTotalHalfBaths = models.CharField(max_length=255, null=True)
    UpperLevelsTotalBaths = models.CharField(max_length=255, null=True)
    UpperLevelsTotalBedrooms = models.CharField(max_length=255, null=True)
    UpperLevelsTotalFullBaths = models.CharField(max_length=255, null=True)
    UpperLevel1Bedrooms = models.IntegerField(null=True)
    UpperLevel1FullBaths = models.IntegerField(null=True)
    UpperLevel1HalfBaths = models.IntegerField(null=True)
    UpperLevel1TotalBaths = models.CharField(max_length=255, null=True)
    UpperLevelsTotalHalfBaths = models.CharField(max_length=255, null=True)
    UpperLevel2Bedrooms = models.IntegerField(null=True)
    UpperLevel2FullBaths = models.IntegerField(null=True)
    UpperLevel2HalfBaths = models.IntegerField(null=True)
    UpperLevel2TotalBaths = models.CharField(max_length=255, null=True)
    UpperLevel3Bedrooms = models.IntegerField(null=True)
    UpperLevel3FullBaths = models.IntegerField(null=True)
    UpperLevel3HalfBaths = models.IntegerField(null=True)
    UpperLevel3TotalBaths = models.CharField(max_length=255, null=True)
    UpperLevel4Bedrooms = models.IntegerField(null=True)
    UpperLevel4FullBaths = models.IntegerField(null=True)
    UpperLevel4HalfBaths = models.IntegerField(null=True)
    UpperLevel4TotalBaths = models.CharField(max_length=255, null=True)
    UpperLevel5Bedrooms = models.IntegerField(null=True)
    UpperLevel5FullBaths = models.IntegerField(null=True)
    UpperLevel5HalfBaths = models.IntegerField(null=True)
    UpperLevel5TotalBaths = models.CharField(max_length=255, null=True)
    UpperLevel6Bedrooms = models.IntegerField(null=True)
    UpperLevel6FullBaths = models.IntegerField(null=True)
    UpperLevel6HalfBaths = models.IntegerField(null=True)
    UpperLevel6TotalBaths = models.CharField(max_length=255, null=True)
    MainLevelBedrooms = models.IntegerField(null=True)
    MainLevelFullBaths = models.IntegerField(null=True)
    MainLevelHalfBaths = models.IntegerField(null=True)
    MainLevelTotalBaths = models.CharField(max_length=255, null=True)
    LowerLevel1Bedrooms = models.IntegerField(null=True)
    LowerLevel1FullBaths = models.IntegerField(null=True)
    LowerLevel1TotalBaths = models.CharField(max_length=255, null=True)
    LowerLevel2Bedrooms = models.IntegerField(null=True)
    LowerLevel2FullBaths = models.IntegerField(null=True)
    LowerLevel2HalfBaths = models.IntegerField(null=True)
    LowerLevel2TotalBaths = models.CharField(max_length=255, null=True)
    LowerLevel3Bedrooms = models.IntegerField(null=True)
    LowerLevel3FullBaths = models.IntegerField(null=True)
    LowerLevel3HalfBaths = models.IntegerField(null=True)
    LowerLevel3TotalBaths = models.CharField(max_length=255, null=True)
    LowerLevel4Bedrooms = models.IntegerField(null=True)
    LowerLevel1HalfBaths = models.IntegerField(null=True)
    LowerLevel4FullBaths = models.IntegerField(null=True)
    LowerLevel4HalfBaths = models.IntegerField(null=True)
    LowerLevel4TotalBaths = models.CharField(max_length=255, null=True)
    LowerLevel5Bedrooms = models.IntegerField(null=True)
    LowerLevel5FullBaths = models.IntegerField(null=True)
    LowerLevel5HalfBaths = models.IntegerField(null=True)
    LowerLevel5TotalBaths = models.CharField(max_length=255, null=True)
    LowerLevel6Bedrooms = models.IntegerField(null=True)
    LowerLevel6FullBaths = models.IntegerField(null=True)
    LowerLevel6HalfBaths = models.IntegerField(null=True)
    LowerLevel6TotalBaths = models.CharField(max_length=255, null=True)
    BarnFeatures = models.JSONField(default=list)
    SeatingCapacity = models.CharField(max_length=255, null=True)
    UnitBuildingType = models.CharField(max_length=255, null=True)
    GarageSQFT = models.CharField(max_length=255, null=True)
    ParkingTypes = models.JSONField(default=list)
    GarageType = models.JSONField(default=list)
    NumParkingSpaces = models.CharField(max_length=255, null=True)
    NumDetachedGarageSpaces = models.CharField(max_length=255, null=True)
    NumAttachedGarageSpaces = models.CharField(max_length=255, null=True)
    NumAttachedCarportSpaces = models.CharField(max_length=255, null=True)
    NumDetachedCarportSpaces = models.CharField(max_length=255, null=True)
    NumParkingGarageSpaces = models.CharField(max_length=255, null=True)
    NumTruckTrailerParkingSpaces = models.CharField(max_length=255, null=True)
    NumCarParkingSpaces = models.CharField(max_length=255, null=True)
    TotalGarageAndParkingSpaces = models.CharField(max_length=255, null=True)
    BelowGradeAreaTotal = models.CharField(max_length=255, null=True)
    BelowGradeAreaTotalSource = models.CharField(max_length=255, null=True)
    AreaTotal = models.CharField(max_length=255, null=True)
    AreaTotalSource = models.CharField(max_length=255, null=True)
    OtherStructuresList = models.JSONField(default=list)
    BuildingClassification = models.CharField(max_length=255, null=True)
    AdditionalParcelsDescription = models.CharField(max_length=128, null=True)
    AdditionalParcelsYN = models.BooleanField(null=True)
    AgriculturalDistrict = models.CharField(max_length=128, null=True)
    AgriculturalTaxDue = models.CharField(max_length=255, null=True)
    AssessmentYear = models.IntegerField(null=True)
    InCityLimitsYN = models.BooleanField(null=True)
    CityTownTax = models.CharField(max_length=255, null=True)
    CityTownTaxPaymentFrequency = models.CharField(max_length=255, null=True)
    CountyTax = models.CharField(max_length=255, null=True)
    CountyTaxPaymentFrequency = models.CharField(max_length=255, null=True)
    TaxPageNumber = models.CharField(max_length=10, null=True)
    HistoricYN = models.BooleanField(null=True)
    HistoricID = models.CharField(max_length=12, null=True)
    ImprovementAssessmentAmount = models.CharField(max_length=255, null=True)
    LandAssessmentAmount = models.CharField(max_length=255, null=True)
    LandUseCode = models.CharField(max_length=128, null=True)
    Section = models.CharField(max_length=10, null=True)
    SourceTaxInternalKey = models.CharField(max_length=255, null=True)
    SpecialAssessment = models.CharField(max_length=255, null=True)
    SpecialAssessmentRemaining = models.CharField(max_length=255, null=True)
    SpecialTaxAssessmentPaymentFrequency = models.CharField(max_length=255, null=True)
    TaxAnnualAmount = models.CharField(max_length=255, null=True)
    TaxAssessmentAmount = models.CharField(max_length=255, null=True)
    TaxBlock = models.CharField(max_length=25, null=True)
    TaxBookNumber = models.CharField(max_length=25, null=True)
    TaxSubdivision = models.CharField(max_length=80, null=True)
    TaxLocalHistoricalDesignationName = models.CharField(max_length=50, null=True)
    TaxLocalHistoricalDesignationURL = models.URLField(max_length=4000, null=True)
    TaxLot = models.CharField(max_length=25, null=True)
    TaxMapNumber = models.CharField(max_length=25, null=True)
    TaxNationalHistoricalDesignationName = models.CharField(max_length=50, null=True)
    TaxNationalHistoricalDesignationURL = models.URLField(max_length=4000, null=True)
    TaxOtherAnnualAssessmentAmount = models.CharField(max_length=255, null=True)
    ParcelID = models.CharField(max_length=25, null=True)
    TaxTotalLivingArea = models.IntegerField(null=True)
    TaxTotalFinishedSqFt = models.CharField(max_length=255, null=True)
    TaxYear = models.IntegerField(null=True)
    Zoning = models.CharField(max_length=25, null=True)
    ZoningDescription = models.CharField(max_length=128, null=True)
    ListingTaxID = models.CharField(max_length=50, null=True)
    AutoUpdateTaxDataYN = models.BooleanField(null=True)
    TaxDataUpdatedYN = models.BooleanField(null=True)
    TaxPhase = models.CharField(max_length=128, null=True)
    SchoolTax = models.CharField(max_length=255, null=True)
    SchoolTaxPaymentFrequency = models.CharField(max_length=255, null=True)
    LeasableAreaAnnualTax = models.CharField(max_length=255, null=True)
    TaxesPerSquareFeet = models.CharField(max_length=255, null=True)
    TaxOpportunityZoneYN = models.BooleanField(null=True)
    DesignatedRepresentativeYN = models.BooleanField(null=True)
    Disclosures = models.JSONField(default=list)
    Exclusions = models.CharField(max_length=1024, null=True)
    Inclusions = models.CharField(max_length=1024, null=True)
    SaleIncludes = models.JSONField(default=list)
    ListingTerms = models.JSONField(default=list)
    OwnershipInterest = models.CharField(max_length=255, null=True)
    ShortSale = models.CharField(max_length=255, null=True)
    RealEstateOwnedYN = models.BooleanField(null=True)
    SaleType = models.JSONField(default=list)
    CloseSaleTerms = models.JSONField(default=list)
    ClosedLeaseTermsMonths = models.CharField(max_length=255, null=True)
    CloseAutoScheduleYN = models.BooleanField(null=True)
    Appliances = models.JSONField(default=list)
    DockType = models.CharField(max_length=255, null=True)
    Docks = models.CharField(max_length=255, null=True)
    LocationType = models.CharField(max_length=255, null=True)
    NavigableWaterYN = models.BooleanField(null=True)
    OtherEquipment = models.JSONField(default=list)
    RFactorBasement = models.CharField(max_length=5, null=True)
    RFactorCeilings = models.CharField(max_length=5, null=True)
    RFactorWalls = models.CharField(max_length=5, null=True)
    RiparianRightsYN = models.BooleanField(null=True)
    SecurityFeatures = models.JSONField(default=list)
    SpaFeatures = models.JSONField(default=list)
    SpaYN = models.BooleanField(null=True)
    MeanLowWaterFeet = models.CharField(max_length=255, null=True)
    AssignedParkingSpaces = models.IntegerField(null=True)
    AssignedParkingSpaceNumber = models.CharField(max_length=50, null=True)
    NumDrivewaySpaces = models.CharField(max_length=255, null=True)
    NumParkingLotSpaces = models.CharField(max_length=255, null=True)
    NumOffSiteSpaces = models.CharField(max_length=255, null=True)
    NumOffStreetSpaces = models.CharField(max_length=255, null=True)
    BuildingFeatures = models.JSONField(default=list)
    BuildingName = models.CharField(max_length=50, null=True)
    CableTvExpense = models.CharField(max_length=255, null=True)
    CropsIncludedYN = models.BooleanField(null=True)
    CultivatedArea = models.CharField(max_length=255, null=True)
    CurrentUse = models.JSONField(default=list)
    DevelopmentStatus = models.JSONField(default=list)
    DistanceToBodyOfWaterRemarks = models.CharField(max_length=255, null=True)
    DockSlipConveyance = models.CharField(max_length=255, null=True)
    ElectionDistrict = models.CharField(max_length=10, null=True)
    ElectricExpense = models.CharField(max_length=255, null=True)
    ElectricOnPropertyYN = models.BooleanField(null=True)
    FarmCreditServiceInclYN = models.BooleanField(null=True)
    FarmLandAreaSource = models.CharField(max_length=255, null=True)
    FarmLandAreaUnits = models.CharField(max_length=255, null=True)
    FederalFloodInsurance = models.CharField(max_length=255, null=True)
    FederalFloodZoneYN = models.BooleanField(null=True)
    FederalFloodZone = models.CharField(max_length=12, null=True)
    FencingYN = models.BooleanField(null=True)
    Fencing = models.JSONField(default=list)
    FrontageLength = models.CharField(max_length=255, null=True)
    FrontageType = models.JSONField(default=list)
    Furnished = models.CharField(max_length=255, null=True)
    FurnitureReplacementExpense = models.CharField(max_length=255, null=True)
    GrossScheduledIncome = models.CharField(max_length=255, null=True)
    HorseAmenities = models.JSONField(default=list)
    HorseYN = models.BooleanField(null=True)
    InsuranceExpense = models.CharField(max_length=255, null=True)
    IrrigationSource = models.JSONField(default=list)
    IrrigationWaterRightsAcres = models.CharField(max_length=255, null=True)
    IrrigationWaterRightsYN = models.BooleanField(null=True)
    LandLeaseAmount = models.CharField(max_length=255, null=True)
    LandLeaseAmountFrequency = models.CharField(max_length=255, null=True)
    LeaseInEffect = models.BooleanField(null=True)
    LeaseTerm = models.CharField(max_length=255, null=True)
    MinLease = models.IntegerField(null=True)
    MaxLease = models.IntegerField(null=True)
    LandLeaseYN = models.BooleanField(null=True)
    LicensesExpense = models.CharField(max_length=255, null=True)
    LotDimensionsSource = models.CharField(max_length=255, null=True)
    LotFeatures = models.JSONField(default=list)
    LotSizeAcres = models.CharField(max_length=255, null=True)
    LotSizeArea = models.CharField(max_length=255, null=True)
    LotSizeDimensions = models.CharField(max_length=128, null=True)
    LotSizeSource = models.CharField(max_length=255, null=True)
    LotSizeSquareFeet = models.CharField(max_length=255, null=True)
    LotSizeUnits = models.CharField(max_length=255, null=True)
    MaintenanceExpense = models.CharField(max_length=255, null=True)
    NetOperatingIncome = models.CharField(max_length=255, null=True)
    NumberOfBuildings = models.CharField(max_length=255, null=True)
    NumberOfLots = models.CharField(max_length=255, null=True)
    Slips = models.CharField(max_length=255, null=True)
    NumberOfUnitsLeased = models.CharField(max_length=255, null=True)
    NumberOfUnitsTotal = models.IntegerField(null=True)
    OperatingExpense = models.CharField(max_length=255, null=True)
    OtherExpense = models.CharField(max_length=255, null=True)
    ParkManagerName = models.CharField(max_length=50, null=True)
    ParkManagerPhone = models.CharField(max_length=16, null=True)
    ParkName = models.CharField(max_length=50, null=True)
    TillableArea = models.CharField(max_length=255, null=True)
    PastureArea = models.CharField(max_length=255, null=True)
    FencedArea = models.CharField(max_length=255, null=True)
    PestControlExpense = models.CharField(max_length=255, null=True)
    PetsAllowed = models.JSONField(default=list)
    PoolExpense = models.CharField(max_length=255, null=True)
    PoolFeatures = models.JSONField(default=list)
    PoolPrivateYN = models.BooleanField(null=True)
    Pool = models.JSONField(default=list)
    AccessToPoolYN = models.BooleanField(null=True)
    CommunityPoolFeatures = models.JSONField(default=list)
    PossibleUse = models.JSONField(default=list)
    ProfessionalManagementExpense = models.CharField(max_length=255, null=True)
    PropertySubType = models.CharField(max_length=255, null=True)
    PropertyType = models.CharField(max_length=255, null=True)
    RangeArea = models.IntegerField(null=True)
    RentControlYN = models.BooleanField(null=True)
    RoadResponsibility = models.JSONField(default=list)
    RoadFrontageLength = models.CharField(max_length=255, null=True)
    RoadSurfaceType = models.JSONField(default=list)
    SeniorCommunityAgeRequirement = models.CharField(max_length=255, null=True)
    SeniorCommunityYN = models.BooleanField(null=True)
    SoilTypes = models.JSONField(default=list)
    TenantPays = models.JSONField(default=list)
    TopographyList = models.JSONField(default=list)
    TotalActualRent = models.CharField(max_length=255, null=True)
    TrashExpense = models.CharField(max_length=255, null=True)
    VacancyAllowanceRate = models.CharField(max_length=255, null=True)
    View = models.JSONField(default=list)
    ViewYN = models.BooleanField(null=True)
    WaterAccessFeatures = models.JSONField(default=list)
    WaterAccessYN = models.BooleanField(null=True)
    WaterBodyName = models.CharField(max_length=50, null=True)
    WaterBodyType = models.CharField(max_length=255, null=True)
    WaterSewerExpense = models.CharField(max_length=255, null=True)
    WaterfrontFeatures = models.JSONField(default=list)
    WaterFrontageInFeet = models.CharField(max_length=255, null=True)
    WaterOrientedYN = models.BooleanField(null=True)
    WoodedArea = models.CharField(max_length=255, null=True)
    LaundryType = models.JSONField(default=list)
    PetDeposit = models.CharField(max_length=255, null=True)
    BedroomPercs = models.CharField(max_length=255, null=True)
    FarmFeatures = models.JSONField(default=list)
    PurchaseOptionalYN = models.BooleanField(null=True)
    PercSites = models.CharField(max_length=255, null=True)
    Storage = models.JSONField(default=list)
    FarmOperation = models.JSONField(default=list)
    SecurityDeposit = models.CharField(max_length=255, null=True)
    BuildingPermits = models.JSONField(default=list)
    FarmRemarks = models.CharField(max_length=400, null=True)
    BuildingSites = models.CharField(max_length=255, null=True)
    MoveInFee = models.CharField(max_length=255, null=True)
    PercType = models.CharField(max_length=255, null=True)
    ApplicationFee = models.CharField(max_length=255, null=True)
    TransferDevelopmentRights = models.CharField(max_length=255, null=True)
    DockAnnualFee = models.CharField(max_length=255, null=True)
    ExteriorAmenities = models.JSONField(default=list)
    GreenEnergyEfficient = models.JSONField(default=list)
    GreenEnergyGeneration = models.JSONField(default=list)
    GreenIndoorAirQuality = models.JSONField(default=list)
    GreenRemarks = models.CharField(max_length=4000, null=True)
    GreenSustainability = models.JSONField(default=list)
    GreenWaterConservation = models.JSONField(default=list)
    LossMitigationFee = models.CharField(max_length=255, null=True)
    CleanGreenAssessedYN = models.BooleanField(null=True)
    WellDepth = models.CharField(max_length=255, null=True)
    Topography = models.CharField(max_length=255, null=True)
    MonthlyPetRent = models.CharField(max_length=255, null=True)
    PetsAllowedYN = models.BooleanField(null=True)
    AssociationExpense = models.CharField(max_length=255, null=True)
    WaterfrontYN = models.BooleanField(null=True)
    GreenVerificationYN = models.BooleanField(null=True)
    LotSizeDescription = models.CharField(max_length=1024, null=True)
    PoultryFarmFeatures = models.JSONField(default=list)
    DockTypeAndFeatures = models.JSONField(default=list)
    DockSlipConveyanceMulti = models.JSONField(default=list)
    TidalWaterYN = models.BooleanField(null=True)
    WaterViewYN = models.BooleanField(null=True)
    FarmLandPreservationYN = models.BooleanField(null=True)
    Section8Approved = models.BooleanField(null=True)
    RepairDeductible = models.CharField(max_length=255, null=True)
    MonthsRentUpfront = models.CharField(max_length=255, null=True)
    PropertyUse = models.CharField(max_length=255, null=True)
    TenancySVO = models.CharField(max_length=255, null=True)
    AllowOnlineApplicationYN = models.BooleanField(null=True)
    LeaseLinkURL = models.URLField(max_length=4000, null=True)
    OccupantName = models.CharField(max_length=50, null=True)
    OccupantPhone = models.CharField(max_length=16, null=True)
    OccupantType = models.CharField(max_length=255, null=True)
    OwnerName = models.CharField(max_length=80, null=True)
    OwnerPhone = models.CharField(max_length=16, null=True)
    OwnerPays = models.JSONField(default=list)
    OwnerNameByTax = models.CharField(max_length=80, null=True)
    Owner1Name = models.CharField(max_length=80, null=True)
    Owner1Email = models.CharField(max_length=80, null=True)
    Owner1MobilePhone = models.CharField(max_length=16, null=True)
    Owner2Name = models.CharField(max_length=80, null=True)
    Owner2Email = models.CharField(max_length=80, null=True)
    Owner2MobilePhone = models.CharField(max_length=16, null=True)
    Owner1ViewedDate = models.DateTimeField(null=True)
    Owner2ViewedDate = models.DateTimeField(null=True)
    LockBoxLocation = models.CharField(max_length=128, null=True)
    LockBoxSerialNumber = models.CharField(max_length=25, null=True)
    LockBoxType = models.JSONField(default=list)
    ShowingContactPhone = models.CharField(max_length=16, null=True)
    ShowingRequirements = models.JSONField(default=list)
    ShowingContactName = models.CharField(max_length=80, null=True)
    ShowingRepresentativeType = models.CharField(max_length=255, null=True)
    ShowingDays = models.JSONField(default=list)
    ShowingTimeClose = models.CharField(max_length=255, null=True)
    ShowingTimeOpen = models.CharField(max_length=255, null=True)
    ShowingMethod = models.CharField(max_length=255, null=True)
    Electric = models.JSONField(default=list)
    ElectricAverageMonthly = models.CharField(max_length=255, null=True)
    ElectricLast12Months = models.CharField(max_length=255, null=True)
    GasAverageMonthly = models.CharField(max_length=255, null=True)
    GasLast12Months = models.CharField(max_length=255, null=True)
    HeatingOilAverageMonthly = models.CharField(max_length=255, null=True)
    HeatingOilLast12Months = models.CharField(max_length=255, null=True)
    Metering = models.JSONField(default=list)
    Sewer = models.JSONField(default=list)
    Utilities = models.JSONField(default=list)
    WaterAverageMonthly = models.CharField(max_length=255, null=True)
    WaterLast12Months = models.CharField(max_length=255, null=True)
    WaterSource = models.JSONField(default=list)
    InternetServices = models.JSONField(default=list)
    DocumentsAvailable = models.JSONField(default=list)
    DocumentsChangeTimestamp = models.DateTimeField(null=True)
    DocumentsCount = models.IntegerField(null=True)
    ListPicture2URL = models.URLField(max_length=4000, null=True)
    ListPicture3URL = models.URLField(max_length=4000, null=True)
    ListPictureURL = models.URLField(max_length=4000, null=True)
    PhotoKey = models.CharField(max_length=20, null=True)
    PhotoOption = models.CharField(max_length=255, null=True)
    PhotosChangeTimestamp = models.DateTimeField(null=True)
    TotalPhotos = models.IntegerField(null=True)
    LisMediaList = models.JSONField(default=list)
    MediaBy = models.CharField(max_length=80, null=True)
    PrivateRemarks = models.CharField(max_length=4000, null=True)
    PublicRemarks = models.CharField(max_length=4000, null=True)
    PrivateOfficeRemarks = models.CharField(max_length=4000, null=True)
    SyndicationRemarks = models.CharField(max_length=4000, null=True)
    BrokerRemarks = models.CharField(max_length=4000, null=True)
    SubAgencyCompensationRemarks = models.CharField(max_length=128, null=True)
    BuyerAgencyCompensationRemarks = models.CharField(max_length=250, null=True)
    TransactionBrokerCompensationRemarks = models.CharField(max_length=128, null=True)
    RoomsTotal = models.IntegerField(null=True)
    RoomList = models.JSONField(default=list)
    BusinessName = models.CharField(max_length=128, null=True)
    BusinessType = models.JSONField(default=list)
    PresentLicenses = models.JSONField(default=list)
    YearEstablished = models.CharField(max_length=255, null=True)
    FinancialDataSource = models.JSONField(default=list)
    ExistingLeaseType = models.JSONField(default=list)
    NumberOfUnitsMoMo = models.CharField(max_length=255, null=True)
    NumberOfUnitsVacant = models.CharField(max_length=255, null=True)
    OperatingExpenseIncludes = models.JSONField(default=list)
    UnitsFurnished = models.CharField(max_length=255, null=True)
    FinalLeaseType = models.JSONField(default=list)
    CapRate = models.CharField(max_length=255, null=True)
    FuelExpense = models.CharField(max_length=255, null=True)
    GrossIncome = models.CharField(max_length=255, null=True)
    IncomeIncludes = models.JSONField(default=list)
    GroundRentAmount = models.CharField(max_length=255, null=True)
    GroundRentPaymentFrequency = models.CharField(max_length=255, null=True)
    CapValueGroundRent = models.CharField(max_length=255, null=True)
    FrontFootFee = models.CharField(max_length=255, null=True)
    FrontFootFeePaymentFrequency = models.CharField(max_length=255, null=True)
    GroundRentYrsLeft = models.CharField(max_length=255, null=True)
    IncomeExpenseList = models.JSONField(default=list)
    InvestorRatio = models.CharField(max_length=255, null=True)
    MunicipalTrashYN = models.BooleanField(null=True)
    RefuseFee = models.CharField(max_length=255, null=True)
    RentIncludes = models.JSONField(default=list)
    WaterSewerHookupFee = models.CharField(max_length=255, null=True)
    AnnualGrossExpense = models.CharField(max_length=255, null=True)
    AnnualHeatingExpense = models.CharField(max_length=255, null=True)
    AnnualLeasePricePerSquareFoot = models.CharField(max_length=255, null=True)
    CommonAreaMaintenance = models.CharField(max_length=255, null=True)
    GroundRentExistsYN = models.BooleanField(null=True)
    LandLeaseYearsRemaining = models.IntegerField(null=True)
    LeaseAmount = models.CharField(max_length=255, null=True)
    LeaseAmountFrequency = models.CharField(max_length=255, null=True)
    LeaseExpiration = models.DateField(null=True)
    LeaseRenewalOptionYN = models.BooleanField(null=True)
    Load = models.JSONField(default=list)
    PricePerSquareFoot = models.CharField(max_length=255, null=True)
    CAMPricePerSquareFootSQFT = models.CharField(max_length=255, null=True)
    OfficeExclusiveYN = models.BooleanField(null=True)
    OfficeExclusiveTermsOfUse = models.BooleanField(null=True)
    OfficeExclusiveTermDate = models.DateTimeField(null=True)
    OfferManagementUrl = models.CharField(max_length=255, null=True)
    OfferManagementProvider = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "BrightProperties"
        indexes = [
            models.Index(fields=["ModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.ListingKey)


class BuildingName(BaseModel):
    BldgNameKey = models.BigIntegerField(primary_key=True)
    BldgNameName = models.CharField(max_length=50, null=True)
    BldgNameRelatedBldgNameKey = models.CharField(max_length=255, null=True)
    BldgNameStatus = models.CharField(max_length=255, null=True)
    BldgNameURL = models.URLField(max_length=4000, null=True)
    BldgNameCounty = models.CharField(max_length=255, null=True)
    BldgNameState = models.CharField(max_length=255, null=True)
    BldgNameModificationTimestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "BuildingName"
        indexes = [
            models.Index(fields=["BldgNameModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.BldgNameKey)


class City(BaseModel):
    CtyCityKey = models.BigIntegerField(primary_key=True)
    CtyCityName = models.CharField(max_length=50, null=True)
    CtyCityCounty = models.CharField(max_length=255, null=True)
    CtyCityType = models.CharField(max_length=255, null=True)
    CtyCityTowhnship = models.CharField(max_length=255, null=True)
    CtyCountyState = models.CharField(max_length=255, null=True)
    CtyModificationTimestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "City"
        indexes = [
            models.Index(fields=["CtyModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.CtyCityKey)


class CityZipCode(BaseModel):
    CityZipCodeKey = models.BigIntegerField(primary_key=True)
    CityZipCodeCity = models.CharField(max_length=255, null=True)
    CityZipCodeCityName = models.CharField(max_length=50, null=True)
    CityZipCodeCounty = models.CharField(max_length=255, null=True)
    CityZipCodeState = models.CharField(max_length=255, null=True)
    CityZipCodeZip = models.CharField(max_length=5, null=True)
    CityZipCodePreferredCity = models.BooleanField(null=True)
    CityZipModificationTimestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "CityZipCode"
        indexes = [
            models.Index(fields=["CityZipModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.CityZipCodeKey)


class Deletion(BaseModel):
    TableName = models.CharField(max_length=30, null=True)
    SchemaShortName = models.CharField(max_length=5, null=True)
    UniversalKey = models.BigIntegerField(primary_key=True)
    DeletionTimestamp = models.DateTimeField(null=True)
    DeleteKey = models.CharField(max_length=256, null=True)

    class Meta:
        verbose_name_plural = "Deletion"
        indexes = [
            models.Index(fields=["DeletionTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.UniversalKey)


class GreenVerification(BaseModel):
    GreenVerificationKey = models.BigIntegerField(primary_key=True)
    GreenVerificationSystemLocale = models.CharField(max_length=255, null=True)
    GreenVerificationSubSystemLocale = models.CharField(max_length=255, null=True)
    GreenVerificationListingKey = models.CharField(max_length=255, null=True)
    GreenVerificationBody = models.CharField(max_length=255, null=True)
    GreenVerificationProgramType = models.CharField(max_length=255, null=True)
    GreenVerificationYear = models.IntegerField(null=True)
    GreenVerificationRating = models.CharField(max_length=255, null=True)
    GreenVerificationScore = models.IntegerField(null=True)
    GreenVerificationStatus = models.CharField(max_length=255, null=True)
    County = models.CharField(max_length=255, null=True)
    ListingSourceRecordKey = models.CharField(max_length=30, null=True)
    GreenVerificationModificationTimestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "GreenVerification"
        indexes = [
            models.Index(fields=["GreenVerificationModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.GreenVerificationKey)


class History(BaseModel):
    PropHistKey = models.BigIntegerField(primary_key=True)
    PropHistListingKey = models.CharField(max_length=255, null=True)
    PropHistRecordKey = models.CharField(max_length=255, null=True)
    PropHistPartyKey = models.CharField(max_length=255, null=True)
    PropHistChangeType = models.CharField(max_length=20, null=True)
    PropHistChangeTypeLkp = models.CharField(max_length=255, null=True)
    PropHistChangeTimestamp = models.DateTimeField(null=True)
    PropHistColumnName = models.CharField(max_length=64, null=True)
    PropHistTableName = models.CharField(max_length=30, null=True)
    PropHistOriginalColumnValue = models.CharField(max_length=4000, null=True)
    PropHistNewColumnValue = models.CharField(max_length=4000, null=True)
    PropHistOriginalPickListValue = models.CharField(max_length=4000, null=True)
    PropHistNewPickListValue = models.CharField(max_length=4000, null=True)
    PropHistItemNumber = models.IntegerField(null=True)
    PropHistSubSystemLocale = models.CharField(max_length=255, null=True)
    PropHistSystemLocale = models.CharField(max_length=255, null=True)
    ListingID = models.CharField(max_length=20, null=True)
    FullStreetAddress = models.CharField(max_length=80, null=True)
    SystemName = models.CharField(max_length=50, null=True)
    BasicComingSoonEndDate = models.DateTimeField(null=True)
    BasicLocaleListingStatus = models.CharField(max_length=255, null=True)
    PropHistNewColumnCharValue = models.CharField(max_length=4000, null=True)
    PropHistNewColumnDatetimeValue = models.DateTimeField(null=True)
    PropHistNewColumnNumValue = models.CharField(max_length=255, null=True)
    PropHistOriginalColumnCharValue = models.CharField(max_length=4000, null=True)
    PropHistOriginalColumnDatetimeValue = models.DateTimeField(null=True)
    PropHistOriginalColumnNumValue = models.CharField(max_length=255, null=True)
    PropHistHistColumnKey = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "History"
        ordering = ["-PropHistChangeTimestamp"]
        indexes = [
            models.Index(fields=["PropHistChangeTimestamp"]),
            models.Index(fields=["PropHistListingKey"]),
            models.Index(fields=["PropHistTableName"]),
            models.Index(fields=["PropHistChangeType"]),
            models.Index(fields=["PropHistColumnName"]),
        ]

    def __str__(self) -> str:
        return str(self.PropHistKey)


class Lookup(BaseModel):
    LookupKey = models.BigIntegerField(primary_key=True)
    LookupName = models.CharField(max_length=64, null=True)
    LookupValue = models.CharField(max_length=1024, null=True)
    StandardLookupValue = models.CharField(max_length=1024, null=True)
    LegacyODataValue = models.CharField(max_length=20, null=True)
    ModificationTimestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Lookup"
        indexes = [
            models.Index(fields=["ModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.LookupKey)


class PartyPermissions(BaseModel):
    PartyPermKey = models.BigIntegerField(primary_key=True)
    PartyPermAccessLevelType = models.CharField(max_length=255, null=True)
    PartyPermPermissionType = models.CharField(max_length=255, null=True)
    PartyPermGrantorPartyKey = models.CharField(max_length=255, null=True)
    PartyPermGranteePartyKey = models.CharField(max_length=255, null=True)
    PartyPermSystemLocale = models.CharField(max_length=255, null=True)
    PpPermissionGroup = models.CharField(max_length=255, null=True)
    PartyPermSubSystemLocale = models.CharField(max_length=255, null=True)
    PartyPermModificationTimestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "PartyPermissions"
        indexes = [
            models.Index(fields=["PartyPermModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.PartyPermKey)


class PropertyArea(BaseModel):
    Location = models.CharField(max_length=255, null=True)
    PropAreaKey = models.BigIntegerField(primary_key=True)
    PropAreaCounty = models.CharField(max_length=255, null=True)
    PropAreaType = models.CharField(max_length=255, null=True)
    PropAreaModificationTimestamp = models.DateTimeField(null=True)
    PropAreaState = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "PropertyArea"
        indexes = [
            models.Index(fields=["PropAreaModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.PropAreaKey)


class RelatedLookup(BaseModel):
    LookupKey = models.CharField(max_length=15, null=True)
    RelatedLookupKey = models.BigIntegerField(primary_key=True)
    ModificationTimestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "RelatedLookup"
        indexes = [
            models.Index(fields=["ModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.RelatedLookupKey)


class Room(BaseModel):
    RoomKey = models.BigIntegerField(primary_key=True)
    RoomListingKey = models.CharField(max_length=255, null=True)
    County = models.CharField(max_length=255, null=True)
    RoomType = models.CharField(max_length=255, null=True)
    RoomLength = models.IntegerField(null=True)
    RoomWidth = models.IntegerField(null=True)
    RoomLevel = models.CharField(max_length=255, null=True)
    RoomExistsYN = models.BooleanField(null=True)
    RoomDisplayOrder = models.IntegerField(null=True)
    RoomItemNumber = models.IntegerField(null=True)
    RoomArea = models.IntegerField(null=True)
    RoomDimensions = models.CharField(max_length=50, null=True)
    RoomFeatures = models.JSONField(default=list)
    RoomSystemLocale = models.CharField(max_length=255, null=True)
    RoomSubSystemLocale = models.CharField(max_length=255, null=True)
    ListingSourceRecordKey = models.CharField(max_length=30, null=True)
    RoomModificationTimestamp = models.DateTimeField(null=True)
    RoomDescription = models.CharField(max_length=1024, null=True)
    RoomSourceRecordKey = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name_plural = "Room"
        indexes = [
            models.Index(fields=["RoomModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.RoomKey)


class School(BaseModel):
    SchoolName = models.CharField(max_length=80, null=True)
    SchoolCounty = models.CharField(max_length=255, null=True)
    SchoolKey = models.BigIntegerField(primary_key=True)
    SchoolDistrictName = models.CharField(max_length=80, null=True)
    SchoolDistrictKey = models.CharField(max_length=255, null=True)
    SchoolModificationTimestamp = models.DateTimeField(null=True)
    SchoolType = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "School"
        indexes = [
            models.Index(fields=["SchoolModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.SchoolKey)


class SchoolDistrict(BaseModel):
    SchoolDistrictKey = models.BigIntegerField(primary_key=True)
    SchoolDistrictName = models.CharField(max_length=80, null=True)
    SchoolDistrictURL = models.URLField(max_length=4000, null=True)
    SchoolDistrictCounty = models.CharField(max_length=255, null=True)
    SchoolDistrictState = models.CharField(max_length=255, null=True)
    SchoolDistrictModificationTimestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "SchoolDistrict"
        indexes = [
            models.Index(fields=["SchoolDistrictModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.SchoolDistrictKey)


# 'SchoolElementary': <class 'odata.metadata.EntitySetSchoolElementary'>,
# 'SchoolHigh': <class 'odata.metadata.EntitySetSchoolHigh'>,
# 'SchoolMiddle': <class 'odata.metadata.EntitySetSchoolMiddle'>,


class Subdivision(BaseModel):
    LoSubdivisionKey = models.BigIntegerField(primary_key=True)
    LoSubdivisionName = models.CharField(max_length=50, null=True)
    LoSubdivisionSystemValidatedFlag = models.BooleanField(null=True)
    LoSubdivisionCounty = models.CharField(max_length=255, null=True)
    LoSubdivisionState = models.CharField(max_length=255, null=True)
    LoSubdivisionModificationTimestamp = models.DateTimeField(null=True)
    LoSubdivisionStatus = models.CharField(max_length=255, null=True)
    LoSubdivisionURL = models.URLField(max_length=4000, null=True)
    LoSubdivisionRelatedSubdivisionKey = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "Subdivision"
        indexes = [
            models.Index(fields=["LoSubdivisionModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.LoSubdivisionKey)


class SysAgentMedia(BaseModel):
    SysMediaObjectKey = models.CharField(max_length=255, null=True)
    SysMediaKey = models.BigIntegerField(primary_key=True)
    SysMediaType = models.CharField(max_length=255, null=True)
    SysMediaExternalKey = models.CharField(max_length=20, null=True)
    SysMediaItemNumber = models.IntegerField(null=True)
    SysMediaDisplayOrder = models.IntegerField(null=True)
    SysMediaSize = models.CharField(max_length=255, null=True)
    SysMediaMimeType = models.CharField(max_length=255, null=True)
    SysMediaBytes = models.CharField(max_length=255, null=True)
    SysMediaFileName = models.CharField(max_length=3000, null=True)
    SysMediaCaption = models.CharField(max_length=50, null=True)
    SysMediaDescription = models.CharField(max_length=4000, null=True)
    SysMediaURL = models.URLField(max_length=4000, null=True)
    SysMediaCreationTimestamp = models.DateTimeField(null=True)
    SysMediaModificationTimestamp = models.DateTimeField(null=True)
    SysMediaSystemLocale = models.CharField(max_length=255, null=True)
    SysMediaSubSystemLocale = models.CharField(max_length=255, null=True)
    SysMediaProcessingStatus = models.CharField(max_length=255, null=True)
    SysMediaPendingFileName = models.CharField(max_length=3000, null=True)
    SysMediaExtSysProcessingCode = models.CharField(max_length=100, null=True)
    SysMediaExtSysProcessingTime = models.IntegerField(null=True)
    SysMediaExtSysResizeTime = models.IntegerField(null=True)
    SysMediaExtSysTotalBytes = models.CharField(max_length=255, null=True)
    SysMediaExtSysWriteTime = models.IntegerField(null=True)
    SysMediaExtSysErrorMessage = models.CharField(max_length=4000, null=True)
    SysMediaObjectID = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "SysAgentMedia"
        indexes = [
            models.Index(fields=["SysMediaModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.SysMediaKey)


class SysOfficeMedia(BaseModel):
    SysMediaObjectKey = models.CharField(max_length=255, null=True)
    SysMediaKey = models.BigIntegerField(primary_key=True)
    SysMediaType = models.CharField(max_length=255, null=True)
    SysMediaExternalKey = models.CharField(max_length=20, null=True)
    SysMediaItemNumber = models.IntegerField(null=True)
    SysMediaDisplayOrder = models.IntegerField(null=True)
    SysMediaSize = models.CharField(max_length=255, null=True)
    SysMediaMimeType = models.CharField(max_length=255, null=True)
    SysMediaBytes = models.CharField(max_length=255, null=True)
    SysMediaFileName = models.CharField(max_length=3000, null=True)
    SysMediaCaption = models.CharField(max_length=50, null=True)
    SysMediaDescription = models.CharField(max_length=4000, null=True)
    SysMediaURL = models.URLField(max_length=4000, null=True)
    SysMediaCreationTimestamp = models.DateTimeField(null=True)
    SysMediaModificationTimestamp = models.DateTimeField(null=True)
    SysMediaSystemLocale = models.CharField(max_length=255, null=True)
    SysMediaSubSystemLocale = models.CharField(max_length=255, null=True)
    SysMediaProcessingStatus = models.CharField(max_length=255, null=True)
    SysMediaPendingFileName = models.CharField(max_length=3000, null=True)
    SysMediaExtSysProcessingCode = models.CharField(max_length=100, null=True)
    SysMediaExtSysProcessingTime = models.IntegerField(null=True)
    SysMediaExtSysResizeTime = models.IntegerField(null=True)
    SysMediaExtSysTotalBytes = models.CharField(max_length=255, null=True)
    SysMediaExtSysWriteTime = models.IntegerField(null=True)
    SysMediaExtSysErrorMessage = models.CharField(max_length=4000, null=True)
    SysMediaObjectID = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "SysOfficeMedia"
        indexes = [
            models.Index(fields=["SysMediaModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.SysMediaKey)


class SysPartyLicense(BaseModel):
    SysPartyLicenseKey = models.BigIntegerField(primary_key=True)
    SysPartyLicenseState = models.CharField(max_length=255, null=True)
    SysPartyLicenseNumber = models.CharField(max_length=20, null=True)
    SysPartyLicenseExpirationDate = models.DateField(null=True)
    SysPartyLicensePartyKey = models.CharField(max_length=255, null=True)
    SysPartyLicenseType = models.CharField(max_length=255, null=True)
    SysPartyLicenseModificationTimestamp = models.DateTimeField(null=True)
    SysPartyLicenseSystemLocale = models.CharField(max_length=255, null=True)
    SysPartyLicenseSubSystemLocale = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = "SysPartyLicense"
        indexes = [
            models.Index(fields=["SysPartyLicenseModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.SysPartyLicenseKey)


class Team(BaseModel):
    TeamKey = models.BigIntegerField(primary_key=True)
    TeamName = models.CharField(max_length=80, null=True)
    TeamSystemLocale = models.CharField(max_length=255, null=True)
    TeamSubSystemLocale = models.CharField(max_length=255, null=True)
    TeamLeadMemberKey = models.CharField(max_length=255, null=True)
    TeamModificationTimestamp = models.DateTimeField(null=True)
    TeamStatus = models.CharField(max_length=255, null=True)
    TeamExternalSystemID = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name_plural = "Team"
        indexes = [
            models.Index(fields=["TeamModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.TeamKey)


class TeamMember(BaseModel):
    TeamMemberKey = models.BigIntegerField(primary_key=True)
    TeamMemberTeamKey = models.CharField(max_length=255, null=True)
    TeamMemberMemberKey = models.CharField(max_length=255, null=True)
    TeamMemberRelationshipKey = models.CharField(max_length=255, null=True)
    TeamMemberRelationshipActiveFlag = models.BooleanField(null=True)
    TeamMemberRelationshipName = models.CharField(max_length=80, null=True)
    TeamMemberModificationTimestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "TeamMember"
        indexes = [
            models.Index(fields=["TeamMemberModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.TeamMemberKey)


class Unit(BaseModel):
    """
    Fixme parsing fails by
    requests.exceptions.JSONDecodeError: Expecting ':' delimiter: line 1 column 15994 (char 15993)
    """

    County = models.CharField(max_length=255, null=True)
    UnitTypeKey = models.BigIntegerField(primary_key=True)
    UnitTypeListingKey = models.CharField(max_length=255, null=True)
    UnitTypeItemNumber = models.IntegerField(null=True)
    UnitTypeType = models.CharField(max_length=255, null=True)
    UnitTypeMonthlyRent = models.CharField(max_length=255, null=True)
    UnitTypeProForma = models.CharField(max_length=255, null=True)
    UnitTypeOccupiedYN = models.BooleanField(null=True)
    UnitTypeLevel = models.CharField(max_length=255, null=True)
    UnitTypeFinishedSQFT = models.IntegerField(null=True)
    UnitTypeLeaseType = models.CharField(max_length=255, null=True)
    UnitTypeLeaseExpirationDate = models.DateField(null=True)
    UnitTypeBedsTotal = models.IntegerField(null=True)
    UnitTypeBathsHalf = models.CharField(max_length=255, null=True)
    UnitTypeBathsFull = models.IntegerField(null=True)
    UnitTypeBathsTotal = models.CharField(max_length=255, null=True)
    UnitTypeFeatures = models.CharField(max_length=128, null=True)
    UnitTypeTotalRooms = models.IntegerField(null=True)
    UnitTypeContiguousSpaceYN = models.BooleanField(null=True)
    UnitTypeSecurityDeposit = models.CharField(max_length=255, null=True)
    ListingSourceRecordKey = models.CharField(max_length=30, null=True)
    PropUnitModificationTimestamp = models.DateTimeField(null=True)
    UnitSystemLocale = models.CharField(max_length=255, null=True)
    UnitSubSystemLocale = models.CharField(max_length=255, null=True)
    UnitTypeSourceRecordKey = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name_plural = "Unit"
        indexes = [
            models.Index(fields=["PropUnitModificationTimestamp"]),
        ]

    def __str__(self) -> str:
        return str(self.UnitTypeKey)


# --------- Prohibited models ------------


# class BuilderModel(BaseModel):
#     """
#     FIXME Does not exist in metadata....
#     """
#
#     BuilderModelKey = models.BigIntegerField(primary_key=True)
#     BuilderModelName = models.CharField(max_length=50, null=True)
#     BuilderModelRelatedBuilderModelKey = models.CharField(max_length=255, null=True)
#     BuilderModelStatus = models.CharField(max_length=255, null=True)
#     BuilderModelCounty = models.CharField(max_length=255, null=True)
#     BuilderModelModificationTimestamp = models.DateTimeField(null=True)
#
#     class Meta:
#         pass
#
#     def __str__(self) -> str:
#         return str(self.BuilderModelName)
#
#
# class BusinessHistoryDeletions(BaseModel):
#     """
#     FIXME: Not persist in metadata
#     """
#
#     DelUchHistChangeKey = models.BigIntegerField(primary_key=True)
#     DelUchHistSystemLocale = models.CharField(max_length=255, null=True)
#     DelUchHistSubSystemLocale = models.CharField(max_length=255, null=True)
#     DelUchHistDeletedTimestamp = models.DateTimeField(null=True)
#
#     class Meta:
#         pass
#
#     def __str__(self) -> str:
#         return str(self.DelUchHistChangeKey)
#
#
# class LisBusinessHistory(BaseModel):
#     """
#     FIXME Does not exist in metadata....
#     """
#
#     UchPropHistChangeKey = models.BigIntegerField(primary_key=True)
#     UchPropHistListingKey = models.CharField(max_length=255, null=True)
#     UchPropHistPartyKey = models.CharField(max_length=255, null=True)
#     UchPropHistChangeType = models.CharField(max_length=20, null=True)
#     UchPropHistChangeTypePckItemKey = models.CharField(max_length=255, null=True)
#     UchPropHistChangeTimestamp = models.DateTimeField(null=True)
#     SystemName = models.CharField(max_length=50, null=True)
#     PropHistColumnName = models.CharField(max_length=64, null=True)
#     TableName = models.CharField(max_length=30, null=True)
#     TableSchemaKey = models.CharField(max_length=255, null=True)
#     UchPropHistOriginalColumnValue = models.CharField(max_length=4000, null=True)
#     UchPropHistNewColumnValue = models.CharField(max_length=4000, null=True)
#     UchPropHistOriginalPickListValue = models.CharField(max_length=80, null=True)
#     UchPropHistNewPickListValue = models.CharField(max_length=80, null=True)
#     UchPropHistItemNumber = models.IntegerField(null=True)
#     UchPropHistSubSystemLocale = models.CharField(max_length=255, null=True)
#     UchPropHistSystemLocale = models.CharField(max_length=255, null=True)
#     BasicListingID = models.CharField(max_length=20, null=True)
#     FullStreetAddress = models.CharField(max_length=80, null=True)
#     UchPropHistCreationTimestamp = models.DateTimeField(null=True)
#     UchPropHistModificationTimestamp = models.DateTimeField(null=True)
#
#     class Meta:
#         pass
#
#     def __str__(self) -> str:
#         return str(self.UchPropHistChangeKey)
#
#
# class ListingSubscription(BaseModel):
#     """
#     FIXME: Does not exist in metadata
#     """
#
#     LsubKey = models.BigIntegerField(primary_key=True)
#     LsubListingKey = models.CharField(max_length=255, null=True)
#     LsubRequestedClassKey = models.CharField(max_length=255, null=True)
#     LsubClassKey = models.CharField(max_length=255, null=True)
#     ReqSubscriptionClassServiceKey = models.CharField(max_length=255, null=True)
#     County = models.CharField(max_length=255, null=True)
#
#     class Meta:
#         pass
#
#     def __str__(self) -> str:
#         return str(self.LsubKey)
#
#
# class PartyProfileOption(BaseModel):
#     """
#     Fixme: Not persist in metadata
#     """
#
#     POName = models.CharField(max_length=50, null=True)
#     PPOCharValue = models.CharField(max_length=4000, null=True)
#     PPODateValue = models.DateField(null=True)
#     PPOKey = models.BigIntegerField(primary_key=True)
#     PPONumValue = models.CharField(max_length=255, null=True)
#     PPOPartyKey = models.CharField(max_length=255, null=True)
#     PPOPOIKey = models.CharField(max_length=255, null=True)
#     PPOUserCustomizableFlag = models.BooleanField(null=True)
#     PPOClobValue = models.CharField(max_length=255, null=True)
#
#     class Meta:
#         pass
#
#     def __str__(self) -> str:
#         return str(self.PPOKey)
