from collections.abc import Iterable

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from common.constants import DOSAGE_FORMS, MODEL_CHARFIELD_MAX_LENGTH
from organizations.models import Organization


# Create your models here.
class ModelHasNameAndSlug(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("slug generated from name"), unique=True, editable=False
    )

    class Meta:
        abstract = True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(force_insert, force_update, using, update_fields)


class MedicineGeneric(
    ModelHasNameAndSlug
):  # Needs more research about model fields and REFACTOR
    pharmacology = models.TextField(
        verbose_name=_("medicine generic pharmacology"), default="Not available."
    )
    indications = models.TextField(
        verbose_name=_("medicine generic indications"),
        default="No known indications.",
    )
    interactions = models.TextField(
        verbose_name=_("medicine generic interactions"),
        default="No known interactions.",
    )
    side_effects = models.TextField(
        verbose_name=_("medicine generic side effects"),
        default="No known side effects.",
    )

    class Meta:
        verbose_name = _("medicine generic")
        verbose_name_plural = _("medicine generics")

    def __str__(self) -> str:
        return self.name


class MedicineBrand(ModelHasNameAndSlug):
    owner_organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    medicine_generic = models.ForeignKey(to=MedicineGeneric, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("medicine brands")
        verbose_name_plural = _("medicine brands")

    def __str__(self) -> str:
        return self.name


class MedicineBrandHasDosageFormWithInfo(models.Model):
    medicine_brand = models.ForeignKey(to=MedicineBrand, on_delete=models.CASCADE)
    dosage_form = models.CharField(
        verbose_name=_("medicine brand dosage form"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        choices=DOSAGE_FORMS,
    )
    dosage_instructions = models.TextField(
        verbose_name=_("medicine brand dosage instructions"),
        default="As prescribed by the doctor.",
    )
    unit_price = models.IntegerField(_("unit price in bdt"), default=-1)

    class Meta:
        verbose_name = _("medicine brand has dosage form with info")
        verbose_name_plural = _("medicine brands have dosage forms with info")
        unique_together = ["medicine_brand", "dosage_form"]

    def __str__(self):
        return f"{str(self.medicine_brand)} | {self.dosage_form}"
