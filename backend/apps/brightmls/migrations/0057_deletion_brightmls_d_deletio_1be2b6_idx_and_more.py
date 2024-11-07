# Generated by Django 5.1.2 on 2024-11-05 07:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("brightmls", "0056_brightmedia_brightmls_b_mediamo_37c6f2_idx_and_more"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="deletion",
            index=models.Index(
                fields=["DeletionTimestamp"], name="brightmls_d_Deletio_1be2b6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="greenverification",
            index=models.Index(
                fields=["GreenVerificationModificationTimestamp"],
                name="brightmls_g_GreenVe_ee0228_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="lookup",
            index=models.Index(
                fields=["ModificationTimestamp"], name="brightmls_l_Modific_105392_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="partypermissions",
            index=models.Index(
                fields=["PartyPermModificationTimestamp"],
                name="brightmls_p_PartyPe_568fe1_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="propertyarea",
            index=models.Index(
                fields=["PropAreaModificationTimestamp"],
                name="brightmls_p_PropAre_71fbd1_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="relatedlookup",
            index=models.Index(
                fields=["ModificationTimestamp"], name="brightmls_r_Modific_b204b0_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="room",
            index=models.Index(
                fields=["RoomModificationTimestamp"],
                name="brightmls_r_RoomMod_dcc065_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="school",
            index=models.Index(
                fields=["SchoolModificationTimestamp"],
                name="brightmls_s_SchoolM_912cc0_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="schooldistrict",
            index=models.Index(
                fields=["SchoolDistrictModificationTimestamp"],
                name="brightmls_s_SchoolD_788796_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="subdivision",
            index=models.Index(
                fields=["LoSubdivisionModificationTimestamp"],
                name="brightmls_s_LoSubdi_566ace_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="sysagentmedia",
            index=models.Index(
                fields=["SysMediaModificationTimestamp"],
                name="brightmls_s_SysMedi_2ea098_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="sysofficemedia",
            index=models.Index(
                fields=["SysMediaModificationTimestamp"],
                name="brightmls_s_SysMedi_80b6ab_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="syspartylicense",
            index=models.Index(
                fields=["SysPartyLicenseModificationTimestamp"],
                name="brightmls_s_SysPart_5bd7b9_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="team",
            index=models.Index(
                fields=["TeamModificationTimestamp"],
                name="brightmls_t_TeamMod_08e22e_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="teammember",
            index=models.Index(
                fields=["TeamMemberModificationTimestamp"],
                name="brightmls_t_TeamMem_253fa9_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="unit",
            index=models.Index(
                fields=["PropUnitModificationTimestamp"],
                name="brightmls_u_PropUni_40cc1c_idx",
            ),
        ),
    ]
