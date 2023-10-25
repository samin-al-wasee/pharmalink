from django.contrib import admin

from .models import (FeedbackToOrganization, MessageBetweenUserOrganization,
                     Prescription, PrescriptionFeedback,
                     PrescriptionHasMedicine, PrescriptionMessage)

# Register your models here.
admin.site.register(
    model_or_iterable=(
        FeedbackToOrganization,
        MessageBetweenUserOrganization,
        Prescription,
        PrescriptionFeedback,
        PrescriptionMessage,
        PrescriptionHasMedicine,
    )
)
