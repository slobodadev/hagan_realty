# Generated by Django 5.1.2 on 2024-10-29 14:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "brightmls",
            "0006_brightmedia_squashed_0008_alter_brightmedia_mediaurl_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                (
                    "TeamMemberKey",
                    models.BigIntegerField(primary_key=True, serialize=False),
                ),
                ("TeamMemberTeamKey", models.BigIntegerField(null=True)),
                ("TeamMemberMemberKey", models.BigIntegerField(null=True)),
                ("TeamMemberRelationshipKey", models.BigIntegerField(null=True)),
                ("TeamMemberRelationshipActiveFlag", models.BooleanField(null=True)),
                (
                    "TeamMemberRelationshipName",
                    models.CharField(max_length=80, null=True),
                ),
                (
                    "TeamMemberModificationTimestamp",
                    models.CharField(max_length=255, null=True),
                ),
            ],
        ),
    ]
