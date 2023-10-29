# Generated by Django 4.1.12 on 2023-10-29 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="information",
            field=models.TextField(
                default="No information available.", verbose_name="information"
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="status",
            field=models.CharField(
                choices=[
                    ("active", "Currently active."),
                    ("inactive", "Currently inactive."),
                    ("disbanded", "Has disbanded."),
                    ("unknown", "No information."),
                ],
                default="unknown",
                max_length=128,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="organizationhasuserwithrole",
            name="role",
            field=models.CharField(
                choices=[
                    ("staff", "Is a staff."),
                    ("doctor", "Is a registered doctor."),
                    ("patient", "Is a patient."),
                    ("other", "Is a generic user."),
                ],
                default="other",
                max_length=128,
                verbose_name="user's role",
            ),
        ),
    ]