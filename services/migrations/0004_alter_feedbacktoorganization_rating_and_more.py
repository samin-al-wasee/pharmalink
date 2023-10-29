# Generated by Django 4.1.12 on 2023-10-29 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0003_prescription_organization"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedbacktoorganization",
            name="rating",
            field=models.IntegerField(
                choices=[
                    (1, "1 Star."),
                    (2, "2 Stars."),
                    (3, "3 Stars."),
                    (4, "4 Stars."),
                    (5, "5 Stars."),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="prescriptionfeedback",
            name="rating",
            field=models.IntegerField(
                choices=[
                    (1, "1 Star."),
                    (2, "2 Stars."),
                    (3, "3 Stars."),
                    (4, "4 Stars."),
                    (5, "5 Stars."),
                ]
            ),
        ),
    ]
