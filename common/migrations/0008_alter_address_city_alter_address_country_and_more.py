# Generated by Django 4.1.12 on 2023-10-12 12:31

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0007_alter_address_country"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="city",
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name="address",
            name="country",
            field=django_countries.fields.CountryField(max_length=2),
        ),
        migrations.AlterField(
            model_name="address",
            name="postal_code",
            field=models.CharField(max_length=128),
        ),
    ]
