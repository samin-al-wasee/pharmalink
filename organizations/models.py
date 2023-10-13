from django.db import models
from common.models import CommonModel, ModelHasName, ModelHasAddress
from django.utils.translation import gettext_lazy as _
from common.constants import (
    MODEL_CHARFIELD_MAX_LENGTH,
    MODEL_CHARFIELD_MIN_LENGTH,
    ORGANIZATION_IS_ACTIVE,
    ORGANIZATION_IS_INACTIVE,
    ORGANIZATION_STATUS_UNKNOWN,
    ORGANIZATION_STATUS,
)


# Create your models here.
class Organization(CommonModel, ModelHasName, ModelHasAddress):
    information = models.TextField(
        verbose_name=_("organization information"), default="No information available."
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
        help_text=_("Required. 128 characters or fewer."),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    status = models.CharField(
        verbose_name=_("organization status"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        choices=ORGANIZATION_STATUS,
        default=ORGANIZATION_STATUS_UNKNOWN,
    )

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
