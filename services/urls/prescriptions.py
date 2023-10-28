from django.urls import path

from ..views import (
    PrescriptionChatListCreate,
    PrescriptionDetailsDelete,
    PrescriptionFeedbackCreate,
    PrescriptionListCreate,
    PrescriptionListForPatient,
    PrescriptionMarkAsDone,
)

urlpatterns = [
    path(
        "/organizations/<uuid:organization_uuid>/prescriptions",
        PrescriptionListCreate.as_view(),
        name="prescription-list-create-doctor",
    ),
    path(
        "/organizations/<uuid:organization_uuid>/prescriptions/<uuid:prescription_uuid>",
        PrescriptionDetailsDelete.as_view(),
        name="prescription-details-delete-doctor",
    ),
    path(
        "/organizations/<uuid:organization_uuid>/prescriptions/<uuid:prescription_uuid>/mark-as-done",
        PrescriptionMarkAsDone.as_view(),
        name="prescription-mark-as-done-doctor",
    ),
    path(
        "/organizations/<uuid:organization_uuid>/prescriptions/<uuid:prescription_uuid>/feedbacks",
        PrescriptionFeedbackCreate.as_view(),
        name="prescription-feedback-for-doctor",
    ),
    path(
        "/organizations/<uuid:organization_uuid>/prescriptions/<uuid:prescription_uuid>/chat",
        PrescriptionChatListCreate.as_view(),
        name="prescription-chat-for-doctor",
    ),
    path(
        "/me/prescriptions",
        PrescriptionListForPatient.as_view(),
        name="prescription-list-patient",
    ),
    path(
        "/me/prescriptions/<uuid:prescription_uuid>",
        PrescriptionDetailsDelete.as_view(),
        name="prescription-details-delete-patient",
    ),
    path(
        "/me/prescriptions/<uuid:prescription_uuid>/mark-as-done",
        PrescriptionMarkAsDone.as_view(),
        name="prescription-mark-as-done-patient",
    ),
    path(
        "/me/prescriptions/<uuid:prescription_uuid>/feedbacks",
        PrescriptionFeedbackCreate.as_view(),
        name="prescription-feedback-for-patient",
    ),
    path(
        "/me/prescriptions/<uuid:prescription_uuid>/chat",
        PrescriptionChatListCreate.as_view(),
        name="prescription-chat-for-patient",
    ),
]