from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.constants import RATINGS
from common.models import CommonModel
from medicines.models import MedicineBrand
from organizations.models import Organization


# Create your models here.
class ModelHasContent(models.Model):
    content = models.TextField(verbose_name=_("feedback or message"))

    class Meta:
        abstract = True


class ModelLinksUserOrganization(CommonModel, ModelHasContent):
    user_account = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ModelLinksUsersPatientDoctor(CommonModel):
    user_account_patient = models.ForeignKey(
        to=get_user_model(),
        related_name="model_set_as_patient",
        on_delete=models.CASCADE,
    )
    user_account_doctor = models.ForeignKey(
        to=get_user_model(),
        related_name="model_set_as_doctor",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class FeedbackForOrganization(ModelLinksUserOrganization):  # Possible REFACTOR
    rating = models.IntegerField(choices=RATINGS)

    class Meta:
        verbose_name = "user feedback"
        verbose_name_plural = "user feedbacks"

    def __str__(self) -> str:
        return (
            f"{str(self.user_account)} to {str(self.organization)} at {self.created_at}"
        )


class MessageBetweenUserOrganization(ModelLinksUserOrganization):
    is_from_user_to_organization = models.BooleanField()

    class Meta:
        verbose_name = "messages"
        verbose_name_plural = "messages"

    def __str__(self) -> str:
        sender = (
            str(self.user_account)
            if self.is_from_user_to_organization
            else str(self.organization)
        )
        receiver = (
            str(self.organization)
            if self.is_from_user_to_organization
            else str(self.user_account)
        )
        return f"{sender} to {receiver} at {self.created_at}"


class Prescription(ModelLinksUsersPatientDoctor):
    is_done = models.BooleanField()

    class Meta:
        verbose_name = "prescription"
        verbose_name_plural = "prescriptions"


class PrescriptionHasInteraction(CommonModel, ModelHasContent):
    in_prescription = models.ForeignKey(to=Prescription, on_delete=models.CASCADE)
    from_user_account = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    is_from_doctor = models.BooleanField()

    class Meta:
        abstract = True


class PrescriptionFeedback(PrescriptionHasInteraction):
    rating = models.IntegerField(choices=RATINGS)

    class Meta:
        verbose_name = "prescription feedback"
        verbose_name_plural = "prescription feedbacks"


class PrescriptionMessage(PrescriptionHasInteraction):
    class Meta:
        verbose_name = "prescription messages"
        verbose_name_plural = "prescription messages"


class PrescriptionHasMedicine(models.Model):
    in_prescription = models.ForeignKey(to=Prescription, on_delete=models.CASCADE)
    medicine_brand = models.ForeignKey(to=MedicineBrand, on_delete=models.PROTECT)
    dosage_instructions = models.TextField(
        verbose_name=_("prescribed directions for the medicine"),
    )

    class Meta:
        verbose_name = "medicines and dosage instructions for prescription"
        verbose_name_plural = "medicines and dosage instructions for prescriptions"
