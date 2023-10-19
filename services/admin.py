from django.contrib import admin
from .models import (
    FeedbackForOrganization,
    MessageBetweenUserOrganization,
    Prescription,
    PrescriptionFeedback,
    PrescriptionMessage,
    PrescriptionHasMedicine,
)

# Register your models here.
admin.site.register(
    model_or_iterable=(
        FeedbackForOrganization,
        MessageBetweenUserOrganization,
        Prescription,
        PrescriptionFeedback,
        PrescriptionMessage,
        PrescriptionHasMedicine,
    )
)
