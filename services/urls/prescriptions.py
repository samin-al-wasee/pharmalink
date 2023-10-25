from django.urls import include, path

from ..views import (PrescriptionChatListCreate, PrescriptionDetailsDelete,
                     PrescriptionFeedbackCreate, PrescriptionListCreate,
                     PrescriptionListForPatient, PrescriptionMarkAsDone)

urlpatterns = [
    path(
        "/organizations/<uuid:org_uuid>/services/prescriptions",
        PrescriptionListCreate.as_view(),
        name="prescription-list-create-doctor",
    ),
    path(
        "/organizations/<uuid:org_uuid>/services/prescriptions/<uuid:presc_uuid>",
        PrescriptionDetailsDelete.as_view(),
        name="prescription-details-delete-doctor",
    ),
    path(
        "/organizations/<uuid:org_uuid>/services/prescriptions/<uuid:presc_uuid>/mark-as-done",
        PrescriptionMarkAsDone.as_view(),
        name="prescription-mark-as-done-doctor",
    ),
    path(
        "/organizations/<uuid:org_uuid>/services/prescriptions/<uuid:presc_uuid>/feedbacks",
        PrescriptionFeedbackCreate.as_view(),
        name="prescription-feedback-for-doctor",
    ),
    path(
        "/organizations/<uuid:org_uuid>/services/prescriptions/<uuid:presc_uuid>/chat",
        PrescriptionChatListCreate.as_view(),
        name="prescription-chat-for-doctor",
    ),
    path(
        "/accounts/me/prescriptions",
        PrescriptionListForPatient.as_view(),
        name="prescription-list-patient",
    ),
    path(
        "/accounts/me/prescriptions/<uuid:presc_uuid>",
        PrescriptionDetailsDelete.as_view(),
        name="prescription-details-delete-patient",
    ),
    path(
        "/accounts/me/prescriptions/<uuid:presc_uuid>/mark-as-done",
        PrescriptionMarkAsDone.as_view(),
        name="prescription-mark-as-done-patient",
    ),
    path(
        "/accounts/me/prescriptions/<uuid:presc_uuid>/feedbacks",
        PrescriptionFeedbackCreate.as_view(),
        name="prescription-feedback-for-patient",
    ),
    path(
        "/accounts/me/prescriptions/<uuid:presc_uuid>/chat",
        PrescriptionChatListCreate.as_view(),
        name="prescription-chat-for-patient",
    ),
]
