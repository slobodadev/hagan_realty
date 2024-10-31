# Generated by Django 5.1.2 on 2024-10-29 14:25

from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ("brightmls", "0001_initial"),
        ("brightmls", "0002_alter_sysofficemedia_sysmediadisplayorder_and_more"),
    ]

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SysOfficeMedia",
            fields=[
                ("SysMediaObjectKey", models.BigIntegerField(null=True)),
                (
                    "SysMediaKey",
                    models.BigIntegerField(primary_key=True, serialize=False),
                ),
                ("SysMediaType", models.CharField(max_length=255, null=True)),
                ("SysMediaExternalKey", models.BigIntegerField(null=True)),
                ("SysMediaItemNumber", models.BigIntegerField(null=True)),
                ("SysMediaDisplayOrder", models.BigIntegerField(null=True)),
                ("SysMediaSize", models.CharField(max_length=255, null=True)),
                ("SysMediaMimeType", models.CharField(max_length=255, null=True)),
                ("SysMediaBytes", models.CharField(max_length=255, null=True)),
                ("SysMediaFileName", models.CharField(max_length=3000, null=True)),
                ("SysMediaCaption", models.CharField(max_length=50, null=True)),
                ("SysMediaDescription", models.CharField(max_length=4000, null=True)),
                ("SysMediaURL", models.URLField(null=True)),
                (
                    "SysMediaCreationTimestamp",
                    models.CharField(max_length=255, null=True),
                ),
                (
                    "SysMediaModificationTimestamp",
                    models.CharField(max_length=255, null=True),
                ),
                ("SysMediaSystemLocale", models.CharField(max_length=255, null=True)),
                (
                    "SysMediaSubSystemLocale",
                    models.CharField(max_length=255, null=True),
                ),
                (
                    "SysMediaProcessingStatus",
                    models.CharField(max_length=255, null=True),
                ),
                (
                    "SysMediaPendingFileName",
                    models.CharField(max_length=3000, null=True),
                ),
                (
                    "SysMediaExtSysProcessingCode",
                    models.CharField(max_length=100, null=True),
                ),
                ("SysMediaExtSysProcessingTime", models.BigIntegerField(null=True)),
                ("SysMediaExtSysResizeTime", models.BigIntegerField(null=True)),
                (
                    "SysMediaExtSysTotalBytes",
                    models.CharField(max_length=255, null=True),
                ),
                ("SysMediaExtSysWriteTime", models.BigIntegerField(null=True)),
                (
                    "SysMediaExtSysErrorMessage",
                    models.CharField(max_length=4000, null=True),
                ),
                ("SysMediaObjectID", models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
