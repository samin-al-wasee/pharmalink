from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import UserAccount
from common.constants import (
    MODEL_CHARFIELD_MAX_LENGTH,
    ORGANIZATION_STATUS,
    ORGANIZATION_STATUS_UNKNOWN,
    OTHER,
    USER_ROLES_IN_ORGANIZATION,
)
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

    def __str__(self) -> str:
        return f"{self.name}"


class OrganizationHasUserWithRole(models.Model):
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    user_account = models.ForeignKey(to=UserAccount, on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name=_("user's role"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        choices=USER_ROLES_IN_ORGANIZATION,
        default=OTHER,
    )

    class Meta:
        verbose_name = _("organization has user with role")
        verbose_name_plural = _("organizations have users with roles")

    def __str__(self) -> str:
        return f"{str(self.user_account)}({self.role}) @ {self.organization.name}"
