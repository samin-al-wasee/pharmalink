# Generated by Django 4.1.12 on 2023-10-11 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_alter_address_options_alter_address_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='region',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
