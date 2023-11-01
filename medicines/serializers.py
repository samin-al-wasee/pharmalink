from collections import OrderedDict

from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ListField,
    ModelSerializer,
    SerializerMethodField,
    SlugRelatedField,
)

from common.utils import create_nested_objects, extract_fields, remove_blank_or_null
from organizations.models import Organization

from .models import MedicineBrand, MedicineBrandHasDosageForm, MedicineGeneric


class DosageFormSerializer(ModelSerializer):
    class Meta:
        model = MedicineBrandHasDosageForm
        fields = (
            "brand",
            "dosage_form",
            "instructions",
            "unit_price",
        )
        extra_kwargs = {"brand": {"write_only": True, "required": False}}


class MedicineBrandSerializer(ModelSerializer):
    class Meta:
        model = MedicineBrand
        fields = (
            "name",
            "slug",
            "manufacturer",
            "generic",
            "dosage_forms_write_only",
            "dosage_forms",
        )
        read_only_fields = ("slug", "manufacturer", "dosage_forms")

    manufacturer = SlugRelatedField(slug_field="uuid", read_only=True)
    generic = SlugRelatedField(
        queryset=MedicineGeneric.objects.filter(), slug_field="slug"
    )
    dosage_forms_write_only = ListField(allow_empty=False, write_only=True)
    dosage_forms = SerializerMethodField(read_only=True)

    def get_dosage_forms(self, obj):  # Need FIX
        if not isinstance(obj, OrderedDict):
            dosage_forms = MedicineBrandHasDosageForm.objects.filter(brand_id=obj.id)
            serializer = DosageFormSerializer(dosage_forms, many=True)
            return serializer.data

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        to_exclude = ("dosage_forms_write_only",)
        validated_data, extracted_data = extract_fields(
            data=validated_data, fields=to_exclude
        )
        request = self.context.get("request")
        organization_uuid = request.parser_context.get("kwargs").get(
            "organization_uuid"
        )
        organization = Organization.objects.get(uuid=organization_uuid)
        additional_data = {"manufacturer": organization}
        validated_data.update(additional_data)
        instance = super().create(validated_data)

        # Following code snippet needs checking and refactoring for a better solution
        dosage_forms = extracted_data.get("dosage_forms_write_only")[0]
        dosage_forms = [dict(dosage_form) for dosage_form in dosage_forms]
        additional_data = {"brand": instance.id}

        for dosage_form in dosage_forms:
            dosage_form.update(additional_data)
        ##############################################################################

        additional_data = {"dosage_forms": dosage_forms}
        nested_fields = ("dosage_forms",)
        serializer_classes = (DosageFormSerializer,)
        try:
            create_nested_objects(
                data=additional_data,
                fields=nested_fields,
                serializer_classes=serializer_classes,
            )
        except IntegrityError:
            raise ValidationError(
                {
                    "dosage_forms": {
                        "dosage_form": "Dosage form already exists for medicine brand."
                    }
                }
            )
        return instance

    def update(self, instance, validated_data):
        to_exclude = ("dosage_forms_write_only",)
        validated_data, extracted_data = extract_fields(
            data=validated_data, fields=to_exclude
        )
        additional_data = {"manufacturer": instance.manufacturer}
        validated_data.update(additional_data)
        instance = super().update(instance, validated_data)

        try:
            # Following code snippet needs checking and refactoring for a better solution
            dosage_forms = extracted_data.get("dosage_forms_write_only")[0]
            dosage_forms = [dict(dosage_form) for dosage_form in dosage_forms]
            additional_data = {"brand": instance.id}

            for dosage_form in dosage_forms:
                dosage_form.update(additional_data)
            ##############################################################################

            additional_data = {"dosage_forms": dosage_forms}
            nested_fields = ("dosage_forms",)
            serializer_classes = (DosageFormSerializer,)
            MedicineBrandHasDosageForm.objects.filter(brand_id=instance.id).delete()
            try:
                create_nested_objects(
                    data=additional_data,
                    fields=nested_fields,
                    serializer_classes=serializer_classes,
                )
            except IntegrityError:
                raise ValidationError(
                    {
                        "dosage_forms": {
                            "dosage_form": "Dosage form already exists for medicine brand."
                        }
                    }
                )
        except TypeError:
            pass
        return instance


class MedicineGenericSerializer(ModelSerializer):
    class Meta:
        model = MedicineGeneric
        fields = (
            "name",
            "slug",
            "pharmacology",
            "indications",
            "interactions",
            "side_effects",
        )
