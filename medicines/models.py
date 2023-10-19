from collections.abc import Iterable
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from common.constants import DOSAGE_FORMS, MAX_LENGTH
from organizations.models import Organization
from common.models import ModelHasUniqueName


# Create your models here.
class ModelHasNameToSlug(ModelHasUniqueName):
    slug = models.SlugField(verbose_name=_("slug"), unique=True, editable=False)

    class Meta:
        abstract = True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(force_insert, force_update, using, update_fields)


class MedicineGeneric(
    ModelHasNameToSlug
):  # Needs more research about model fields and REFACTOR
    pharmacology = models.TextField(
        verbose_name=_("pharmacology"), default="Not available."
    )
    indications = models.TextField(
        verbose_name=_("indications"),
        default="No known indications.",
    )
    interactions = models.TextField(
        verbose_name=_("interactions"),
        default="No known interactions.",
    )
    side_effects = models.TextField(
        verbose_name=_("side effects"),
        default="No known side effects.",
    )

    class Meta:
        verbose_name = _("medicine generic")
        verbose_name_plural = _("medicine generics")

    def __str__(self) -> str:
        return self.name


class MedicineBrand(ModelHasNameToSlug):
    manufacturer = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    generic = models.ForeignKey(to=MedicineGeneric, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("medicine brands")
        verbose_name_plural = _("medicine brands")

    def __str__(self) -> str:
        return self.name


class MedicineBrandHasDosageFormWithInfo(models.Model):
    brand = models.ForeignKey(to=MedicineBrand, on_delete=models.CASCADE)
    dosage_form = models.CharField(
        verbose_name=_("dosage form"),
        max_length=MAX_LENGTH,
        choices=DOSAGE_FORMS,
    )
    instructions = models.TextField(
        verbose_name=_("dosage instructions"),
        default="As prescribed by the doctor.",
    )
    unit_price = models.IntegerField(_("unit price"), default=-1)

    class Meta:
        verbose_name = _("dosage form")
        verbose_name_plural = _("dosage forms")
        unique_together = ["brand", "dosage_form"]

    def __str__(self):
        return f"{str(self.brand)} | {self.dosage_form}"
