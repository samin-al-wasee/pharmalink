from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.constants import (
    MAX_LENGTH,
    ORGANIZATION_STATUSES,
    STATUS_UNKNOWN,
    OTHER,
    USER_ROLES,
)
from common.models import (
    ModelHasRandomID,
    ModelHasAddress,
    ModelHasEmail,
    ModelHasUniqueName,
)


# Create your models here.
class Organization(
    ModelHasRandomID, ModelHasUniqueName, ModelHasEmail, ModelHasAddress
):
    information = models.TextField(
        verbose_name=_("organization information"), default="No information available."
    )

    status = models.CharField(
        verbose_name=_("organization status"),
        max_length=MAX_LENGTH,
        choices=ORGANIZATION_STATUSES,
        default=STATUS_UNKNOWN,
    )
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def __str__(self) -> str:
        return f"{self.name}"


class ModelLinksUserOrganization(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class OrganizationHasUserWithRole(ModelLinksUserOrganization):
    role = models.CharField(
        verbose_name=_("user's role"),
        max_length=MAX_LENGTH,
        choices=USER_ROLES,
        default=OTHER,
    )

    class Meta:
        verbose_name = _("user role")
        verbose_name_plural = _("user roles")
        unique_together = ["organization", "user"]

    def __str__(self) -> str:  # Needs REFACTOR
        return f"{str(self.user)}({self.role}) @ {self.organization.name}"
