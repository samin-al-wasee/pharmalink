# Generated by Django 4.1.12 on 2023-10-11 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['country']},
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together={('unit_no', 'street_no', 'line_1', 'line_2', 'city', 'region', 'postal_code', 'country')},
        ),
    ]
