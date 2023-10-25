from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.constants import RATINGS
from common.models import ModelHasRandomID
from medicines.models import MedicineBrand
from organizations.models import ModelLinksUserOrganization, Organization


# Create your models here.
class ModelHasContent(ModelHasRandomID):
    content = models.TextField(verbose_name=_("feedback or message"))

    class Meta:
        abstract = True


class FeedbackToOrganization(
    ModelHasContent, ModelLinksUserOrganization
):  # Possible REFACTOR
    rating = models.IntegerField(choices=RATINGS)

    class Meta:
        verbose_name = "user feedback"
        verbose_name_plural = "user feedbacks"

    def __str__(self) -> str:
        return f"{str(self.user)} to {str(self.organization)} at {self.created_at}"


class MessageBetweenUserOrganization(ModelHasContent, ModelLinksUserOrganization):
    from_user = models.BooleanField(default=True)

    class Meta:
        verbose_name = "message"
        verbose_name_plural = "messages"

    def __str__(self) -> str:
        sender = str(self.user) if self.from_user else str(self.organization)
        receiver = str(self.organization) if self.from_user else str(self.user)
        return f"{sender} to {receiver} at {self.created_at}"


class Prescription(ModelHasRandomID):
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    patient = models.ForeignKey(
        to=get_user_model(),
        related_name="prescriptions_patient",
        on_delete=models.CASCADE,
    )
    doctor = models.ForeignKey(
        to=get_user_model(),
        related_name="prescriptions_doctor",
        on_delete=models.CASCADE,
    )
    done = models.BooleanField(default=False)

    class Meta:
        verbose_name = "prescription"
        verbose_name_plural = "prescriptions"


class PrescriptionHasInteraction(ModelHasContent):
    prescription = models.ForeignKey(to=Prescription, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    from_doctor = models.BooleanField()

    class Meta:
        abstract = True


class PrescriptionFeedback(PrescriptionHasInteraction):
    rating = models.IntegerField(choices=RATINGS)

    class Meta:
        verbose_name = "prescription feedback"
        verbose_name_plural = "prescription feedbacks"


class PrescriptionMessage(PrescriptionHasInteraction):
    class Meta:
        verbose_name = "prescription message"
        verbose_name_plural = "prescription messages"


class PrescriptionHasMedicine(models.Model):
    prescription = models.ForeignKey(to=Prescription, on_delete=models.CASCADE)
    brand = models.ForeignKey(to=MedicineBrand, on_delete=models.PROTECT)
    instructions = models.TextField(
        verbose_name=_("prescribed directions"),
    )

    class Meta:
        verbose_name = "prescribed medicine"
        verbose_name_plural = "prescribed medicines"
