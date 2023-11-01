from django.contrib import admin

from .models import MedicineBrand, MedicineBrandHasDosageForm, MedicineGeneric

# Register your models here.
admin.site.register(
    model_or_iterable=(
        MedicineGeneric,
        MedicineBrand,
        MedicineBrandHasDosageForm,
    )
)
