# Generated by Django 5.1.2 on 2024-10-29 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("brightmls", "0015_alter_brightoffices_officesourcerecordkey"),
    ]

    operations = [
        migrations.CreateModel(
            name="SysPartyLicense",
            fields=[
                (
                    "SysPartyLicenseKey",
                    models.BigIntegerField(primary_key=True, serialize=False),
                ),
                ("SysPartyLicenseState", models.CharField(max_length=255, null=True)),
                ("SysPartyLicenseNumber", models.CharField(max_length=20, null=True)),
                (
                    "SysPartyLicenseExpirationDate",
                    models.CharField(max_length=255, null=True),
                ),
                ("SysPartyLicensePartyKey", models.BigIntegerField(null=True)),
                ("SysPartyLicenseType", models.CharField(max_length=255, null=True)),
                (
                    "SysPartyLicenseModificationTimestamp",
                    models.CharField(max_length=255, null=True),
                ),
                (
                    "SysPartyLicenseSystemLocale",
                    models.CharField(max_length=255, null=True),
                ),
                (
                    "SysPartyLicenseSubSystemLocale",
                    models.CharField(max_length=255, null=True),
                ),
            ],
        ),
    ]
