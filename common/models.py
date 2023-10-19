from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import Country, CountryField
from django.contrib.auth import get_user_model

from .constants import MAX_LENGTH


# Create your models here.
class ModelHasRandomID(models.Model):
    """An abstract model for common information that multiple models can inherit such as UUID, creation time."""

    uuid = models.UUIDField(default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ModelHasUniqueName(models.Model):
    name = models.CharField(
        _("name"),
        max_length=MAX_LENGTH,
        unique=True,
    )

    class Meta:
        abstract = True


class ModelHasEmail(models.Model):
    """An abstract model for models, which have the email attribute."""

    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
        help_text=_("Required. 128 characters or fewer."),
        error_messages={
            "unique": _("This email already exists."),
        },
    )

    class Meta:
        abstract = True


class Address(models.Model):
    """
    Address model is used to create all the addresses in the system.
    Only city, postal code and country is required.
    Each address, as a whole including all the fields, should be unique.
    """

    unit_no = models.CharField(max_length=MAX_LENGTH, blank=True)
    street_no = models.CharField(max_length=MAX_LENGTH, blank=True)
    line_1 = models.CharField(max_length=MAX_LENGTH, blank=True)
    line_2 = models.CharField(max_length=MAX_LENGTH, blank=True)
    city = models.CharField(max_length=MAX_LENGTH)
    region = models.CharField(max_length=MAX_LENGTH, blank=True)
    postal_code = models.CharField(max_length=MAX_LENGTH)
    country: Country = CountryField(blank_label=_("Select country"))

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")
        ordering = ["country"]
        unique_together = [
            "unit_no",
            "street_no",
            "line_1",
            "line_2",
            "city",
            "region",
            "postal_code",
            "country",
        ]

    def clean(self) -> None:
        """
        This method will add an extra step for the validation of the country field.
        Value of the country code remains blank ("") if no country is selected.
        Raise a validation error manually to ensure that a country is selected
        """
        super().clean()
        if self.country.code == "":
            raise ValidationError({"country": "Country can not be blank."})

    def __str__(self) -> str:
        return f"{self.city}, {self.country.name} | {self.line_1}, {self.line_2}"


class ModelHasAddress(models.Model):
    """
    An abstract model for models, which have the address attribute.
    Address can be empty or none.
    If an address is referenced in any model objects, the address can not be deleted.
    """

    address = models.ForeignKey(
        to=Address, on_delete=models.PROTECT, blank=True, null=True
    )

    class Meta:
        abstract = True
