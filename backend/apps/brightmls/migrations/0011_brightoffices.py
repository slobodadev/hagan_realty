# Generated by Django 5.1.2 on 2024-10-29 14:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("brightmls", "0010_deletion"),
    ]

    operations = [
        migrations.CreateModel(
            name="BrightOffices",
            fields=[
                ("FranchiseAffiliation", models.CharField(max_length=50, null=True)),
                ("IDXOfficeParticipationYN", models.BooleanField(null=True)),
                ("MainOfficeKey", models.BigIntegerField(null=True)),
                ("MainOfficeMlsId", models.CharField(max_length=25, null=True)),
                ("ModificationTimestamp", models.CharField(max_length=255, null=True)),
                (
                    "OfficeAssociationPrimary",
                    models.CharField(max_length=255, null=True),
                ),
                ("OfficeAddress1", models.CharField(max_length=50, null=True)),
                ("OfficeAddress2", models.CharField(max_length=50, null=True)),
                ("OfficeBoxNumber", models.CharField(max_length=10, null=True)),
                ("OfficeBranchType", models.CharField(max_length=255, null=True)),
                (
                    "OfficeBrokerAcceptedPortalTermsOfUseYN",
                    models.BooleanField(null=True),
                ),
                (
                    "OfficeBrokerAcceptedPortalTermsOfUseVersion",
                    models.CharField(max_length=10, null=True),
                ),
                ("OfficeBrokerKey", models.BigIntegerField(null=True)),
                ("OfficeBrokerLeadEmail", models.CharField(max_length=128, null=True)),
                (
                    "OfficeBrokerLeadPhoneNumber",
                    models.CharField(max_length=128, null=True),
                ),
                ("OfficeBrokerMlsId", models.CharField(max_length=25, null=True)),
                ("OfficeCity", models.CharField(max_length=50, null=True)),
                ("OfficeCountry", models.CharField(max_length=255, null=True)),
                ("OfficeCounty", models.CharField(max_length=255, null=True)),
                ("OfficeDateAdded", models.CharField(max_length=255, null=True)),
                ("OfficeDateTerminated", models.CharField(max_length=255, null=True)),
                ("OfficeEmail", models.CharField(max_length=80, null=True)),
                ("OfficeFax", models.CharField(max_length=16, null=True)),
                (
                    "OfficeKey",
                    models.BigIntegerField(primary_key=True, serialize=False),
                ),
                ("OfficeManagerKey", models.BigIntegerField(null=True)),
                ("OfficeLatitude", models.CharField(max_length=255, null=True)),
                ("OfficeLeadToListingAgentYN", models.BooleanField(null=True)),
                ("OfficeLongitude", models.CharField(max_length=255, null=True)),
                ("OfficeManagerEmail", models.CharField(max_length=3000, null=True)),
                ("OfficeManagerMlsId", models.CharField(max_length=25, null=True)),
                ("OfficeManagerName", models.CharField(max_length=80, null=True)),
                ("OfficeMlsId", models.CharField(max_length=25, null=True)),
                ("OfficeName", models.CharField(max_length=80, null=True)),
                (
                    "OfficeNationalAssociationId",
                    models.CharField(max_length=25, null=True),
                ),
                ("OfficeNumViolations", models.BigIntegerField(null=True)),
                ("OfficePhone", models.CharField(max_length=16, null=True)),
                ("OfficePhoneExt", models.BigIntegerField(null=True)),
                ("OfficePhoneOther", models.CharField(max_length=10, null=True)),
                ("OfficePostalCode", models.CharField(max_length=10, null=True)),
                ("OfficePostalCodePlus4", models.CharField(max_length=4, null=True)),
                ("OfficeRoleList", models.CharField(max_length=4000, null=True)),
                ("OfficeStateOrProvince", models.CharField(max_length=255, null=True)),
                ("OfficeStatus", models.CharField(max_length=255, null=True)),
                ("OfficeStreetDirSuffix", models.CharField(max_length=255, null=True)),
                ("OfficeStreetException", models.CharField(max_length=10, null=True)),
                ("OfficeStreetName", models.CharField(max_length=50, null=True)),
                ("OfficeStreetNumber", models.BigIntegerField(null=True)),
                ("OfficeStreetSuffix", models.CharField(max_length=255, null=True)),
                ("OfficeTradingAs", models.CharField(max_length=50, null=True)),
                ("OfficeType", models.CharField(max_length=255, null=True)),
                ("OfficeUnitDesignation", models.CharField(max_length=255, null=True)),
                ("OfficeUnitNumber", models.CharField(max_length=20, null=True)),
                ("OfficeUserName", models.CharField(max_length=30, null=True)),
                ("OfficeSubSystemLocale", models.CharField(max_length=255, null=True)),
                ("OfficeSystemLocale", models.CharField(max_length=255, null=True)),
                (
                    "SocialMediaBlogUrlOrId",
                    models.CharField(max_length=8000, null=True),
                ),
                (
                    "SocialMediaFacebookUrlOrId",
                    models.CharField(max_length=8000, null=True),
                ),
                (
                    "SocialMediaLinkedInUrlOrId",
                    models.CharField(max_length=8000, null=True),
                ),
                (
                    "SocialMediaTwitterUrlOrId",
                    models.CharField(max_length=8000, null=True),
                ),
                (
                    "SocialMediaWebsiteUrlOrId",
                    models.CharField(max_length=8000, null=True),
                ),
                (
                    "SocialMediaYouTubeUrlOrId",
                    models.CharField(max_length=8000, null=True),
                ),
                (
                    "OfficeSourceBusinessPartner",
                    models.CharField(max_length=255, null=True),
                ),
                ("OfficeSourceRecordKey", models.BigIntegerField(null=True)),
                ("SyndicateAgentOption", models.CharField(max_length=255, null=True)),
                ("SyndicateTo", models.CharField(max_length=255, null=True)),
                ("OfficeSourceRecordID", models.CharField(max_length=128, null=True)),
                ("OfficeBrightConvertedYN", models.BooleanField(null=True)),
                ("OfficeSourceInput", models.CharField(max_length=255, null=True)),
                ("OfficeSourceTransport", models.CharField(max_length=255, null=True)),
                ("MainOfficeName", models.CharField(max_length=50, null=True)),
                (
                    "OfficeAssociationsFullList",
                    models.CharField(max_length=255, null=True),
                ),
                ("OfficeValidationStatus", models.CharField(max_length=255, null=True)),
                ("OfficeCorporateLicense", models.CharField(max_length=50, null=True)),
                (
                    "SourceModificationTimestamp",
                    models.CharField(max_length=255, null=True),
                ),
                ("OfficeStreetDirPrefix", models.CharField(max_length=255, null=True)),
            ],
        ),
    ]