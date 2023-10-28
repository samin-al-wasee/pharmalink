# Generated by Django 4.1.12 on 2023-10-23 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0001_initial"),
        (
            "services",
            "0002_rename_feedbackfororganization_feedbacktoorganization_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="prescription",
            name="organization",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="organizations.organization",
            ),
            preserve_default=False,
        ),
    ]