# Generated by Django 4.1.12 on 2023-10-19 05:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("organizations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MedicineGeneric",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, unique=True, verbose_name="name"),
                ),
                (
                    "slug",
                    models.SlugField(editable=False, unique=True, verbose_name="slug"),
                ),
                (
                    "pharmacology",
                    models.TextField(
                        default="Not available.", verbose_name="pharmacology"
                    ),
                ),
                (
                    "indications",
                    models.TextField(
                        default="No known indications.", verbose_name="indications"
                    ),
                ),
                (
                    "interactions",
                    models.TextField(
                        default="No known interactions.", verbose_name="interactions"
                    ),
                ),
                (
                    "side_effects",
                    models.TextField(
                        default="No known side effects.", verbose_name="side effects"
                    ),
                ),
            ],
            options={
                "verbose_name": "medicine generic",
                "verbose_name_plural": "medicine generics",
            },
        ),
        migrations.CreateModel(
            name="MedicineBrand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, unique=True, verbose_name="name"),
                ),
                (
                    "slug",
                    models.SlugField(editable=False, unique=True, verbose_name="slug"),
                ),
                (
                    "generic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medicines.medicinegeneric",
                    ),
                ),
                (
                    "manufacturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organizations.organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "medicine brands",
                "verbose_name_plural": "medicine brands",
            },
        ),
        migrations.CreateModel(
            name="MedicineBrandHasDosageFormWithInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dosage_form",
                    models.CharField(
                        choices=[
                            ("T", "Tablet"),
                            ("S", "Capsule"),
                            ("O", "Ointment"),
                            ("I", "Injection"),
                        ],
                        max_length=128,
                        verbose_name="dosage form",
                    ),
                ),
                (
                    "instructions",
                    models.TextField(
                        default="As prescribed by the doctor.",
                        verbose_name="dosage instructions",
                    ),
                ),
                (
                    "unit_price",
                    models.IntegerField(default=-1, verbose_name="unit price"),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medicines.medicinebrand",
                    ),
                ),
            ],
            options={
                "verbose_name": "dosage form",
                "verbose_name_plural": "dosage forms",
                "unique_together": {("brand", "dosage_form")},
            },
        ),
    ]
