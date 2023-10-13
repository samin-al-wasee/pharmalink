from typing import Any
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import MinLengthValidator
from common.constants import *
from common.models import *
from .managers import UserAccountManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserAccount(
    AbstractBaseUser, PermissionsMixin, CommonModel, ModelHasName, ModelHasAddress
):
    username = models.CharField(
        verbose_name=_("username"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        unique=True,
        help_text=_(
            "Required. 128 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[
            ASCIIUsernameValidator(),
            MinLengthValidator(MODEL_CHARFIELD_MIN_LENGTH),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
        help_text=_("Required. 128 characters or fewer."),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    date_of_birth = models.DateField(
        verbose_name=_("date of birth"), blank=True, null=True
    )

    def _rename_photo(instance, filename: str):
        """Rename the user uploaded photo befire saving it into the media directory.

        - Separate the file extension
        - Concat username and the file extension to get a unique name for the photo
        """

        extension = filename.split(sep=".")[-1]
        return f"user_photos/{instance.username}.{extension}"

    photo = models.ImageField(
        verbose_name=_("user photo"), upload_to=_rename_photo, blank=True, null=True
    )
    height_cm = models.IntegerField(_("height in centimetres"), default=-1)
    weight_kg = models.IntegerField(_("weight in kilograms"), default=-1)
    blood_group = models.CharField(
        verbose_name=_("blood group"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        choices=BLOOD_GROUPS,
        default=UNKNOWN,
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        choices=GENDERS,
        default=UNKNOWN,
    )
    objects: UserAccountManager = UserAccountManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user account")
        verbose_name_plural = _("user accounts")

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self) -> str:
        return f"{self.username} | {self.email}"

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self) -> str:
        return self.name

    def email_user(self) -> Any:
        """
        Could be implemented later for user verification purpose.
        """

        pass
