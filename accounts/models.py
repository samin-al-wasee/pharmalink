from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.constants import BLOOD_GROUPS, GENDERS, MAX_LENGTH, MIN_LENGTH, UNKNOWN
from common.models import ModelHasAddress, ModelHasEmail, ModelHasRandomID

from .managers import UserManager_


# Create your models here.
class User(
    AbstractBaseUser,
    PermissionsMixin,
    ModelHasRandomID,
    ModelHasEmail,
    ModelHasAddress,
):
    username = models.CharField(
        verbose_name=_("username"),
        max_length=MAX_LENGTH,
        unique=True,
        help_text=_(
            "Required. 128 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[
            ASCIIUsernameValidator(),
            MinLengthValidator(MIN_LENGTH),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    name = models.CharField(
        _("name"),
        max_length=MAX_LENGTH,
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
        max_length=MAX_LENGTH,
        choices=BLOOD_GROUPS,
        default=UNKNOWN,
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=MAX_LENGTH,
        choices=GENDERS,
        default=UNKNOWN,
    )
    objects: UserManager_ = UserManager_()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

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
