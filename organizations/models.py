from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import UserAccount
from common.constants import (MODEL_CHARFIELD_MAX_LENGTH,
                              MODEL_CHARFIELD_MIN_LENGTH,
                              ORGANIZATION_IS_ACTIVE, ORGANIZATION_IS_INACTIVE,
                              ORGANIZATION_STATUS, ORGANIZATION_STATUS_UNKNOWN)
from common.models import CommonModel, ModelHasAddress, ModelHasEmail


# Create your models here.
class Organization(CommonModel, ModelHasEmail, ModelHasAddress):
    name = models.CharField(_("name"), max_length=MODEL_CHARFIELD_MAX_LENGTH)
    information = models.TextField(
        verbose_name=_("organization information"), default="No information available."
    )

    status = models.CharField(
        verbose_name=_("organization status"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        choices=ORGANIZATION_STATUS,
        default=ORGANIZATION_STATUS_UNKNOWN,
    )
    owner_user_account = models.ForeignKey(to=UserAccount, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
