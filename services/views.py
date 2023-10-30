from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import NOT, IsAuthenticated
from .mixins import (
    PrescriptionDoctorPermissionMixin,
    PrescriptionPatientPermissionMixin,
)

from common.constants import DOCTOR, PATIENT
from organizations.models import Organization

from .models import (
    FeedbackToOrganization,
    MessageBetweenUserOrganization,
    Prescription,
    PrescriptionMessage,
)
from .permissions import (
    HasPrescriptionAccess,
    HasRole,
    IsDone,
)
from .serializers import (
    FeedbackSerializer,
    MessageSerializer,
    PrescriptionDetailSerializer,
    PrescriptionFeedbackSerializer,
    PrescriptionMessageSerializer,
    PrescriptionSerializer,
)
from common.mixins import PathValidationMixin


# Create your views here.
class FeedbackListCreate(PathValidationMixin, ListCreateAPIView):
    serializer_class = FeedbackSerializer
    path_variables = ("organization_uuid",)
    model_classes = (Organization,)
    kwarg_objects = {}

    def get_permissions(self):
        organization = self.kwarg_objects.get("organization_uuid")
        authenticated_user = self.request.user
        if self.request.method == "GET":
            return [
                IsAuthenticated(),
                NOT(
                    HasRole(
                        organization=organization, user=authenticated_user, role=PATIENT
                    )
                ),
            ]
        elif self.request.method == "POST":
            return [
                IsAuthenticated(),
                HasRole(
                    organization=organization, user=authenticated_user, role=PATIENT
                ),
            ]
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        organization = self.kwarg_objects.get("organization_uuid")
        queryset = (
            FeedbackToOrganization.objects.select_related("user", "organization")
            .filter(organization_id=organization.id)
            .order_by("-created_at")
            .distinct()
        )
        return queryset


class _ConversationList(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = MessageBetweenUserOrganization.objects.select_related(
        "user", "organization"
    ).filter()


class ConversationListForPatient(_ConversationList):
    def get_queryset(self):
        authenticated_user = self.request.user
        queryset = self.queryset.filter(user_id=authenticated_user.id).order_by(
            "-created_at"
        )
        return queryset


class ConversationListForOrganization(PathValidationMixin, _ConversationList):
    path_variables = ("organization_uuid",)
    model_classes = (Organization,)
    kwarg_objects = {}

    def get_permissions(self):
        permissions = super().get_permissions()
        organization = self.kwarg_objects.get("organization_uuid", None)
        authenticated_user = self.request.user
        permissions.append(
            NOT(
                HasRole(
                    organization=organization, user=authenticated_user, role=PATIENT
                )
            )
        )
        return permissions

    def get_queryset(self):
        organization = self.kwarg_objects.get("organization_uuid", None)
        queryset = self.queryset.filter(organization_id=organization.id).order_by(
            "-created_at"
        )
        return queryset


class _MessageListCreate(PathValidationMixin, ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = MessageBetweenUserOrganization.objects.select_related(
        "user", "organization"
    ).filter()
    path_variables = ("organization_uuid",)
    model_classes = (Organization,)
    kwarg_objects = {}


class MessageListCreateForPatient(_MessageListCreate):
    def get_permissions(self):
        permissions = super().get_permissions()
        organization = self.kwarg_objects.get("organization_uuid", None)
        authenticated_user = self.request.user
        permissions.append(
            HasRole(organization=organization, user=authenticated_user, role=PATIENT),
        )
        return permissions

    def get_queryset(self):
        organization = self.kwarg_objects.get("organization_uuid", None)
        authenticated_user = self.request.user
        queryset = self.queryset.filter(
            organization_id=organization.id, user_id=authenticated_user.id
        ).order_by("-created_at")
        return queryset


class MessageListCreateForOrganization(_MessageListCreate):
    path_variables = ("organization_uuid", "user_uuid")
    model_classes = (Organization, get_user_model())

    def get_permissions(self):
        permissions = super().get_permissions()
        organization = self.kwarg_objects.get("organization_uuid", None)
        authenticated_user = self.request.user
        permissions.append(
            NOT(
                HasRole(
                    organization=organization, user=authenticated_user, role=PATIENT
                )
            ),
        )
        return permissions

    def get_queryset(self):
        organization = self.kwarg_objects.get("organization_uuid", None)
        recepient = self.kwarg_objects.get("user_uuid", None)
        queryset = self.queryset.filter(
            organization_id=organization.id, user_id=recepient.id
        ).order_by("-created_at")
        return queryset


class PrescriptionListCreate(PathValidationMixin, ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    path_variables = ("organization_uuid",)
    model_classes = (Organization,)
    kwarg_objects = {}

    def get_permissions(self):
        organization = self.kwarg_objects.get("organization_uuid", None)
        authenticated_user = self.request.user
        return [
            IsAuthenticated(),
            HasRole(organization=organization, user=authenticated_user, role=DOCTOR),
        ]

    def get_queryset(self):
        organization = self.kwarg_objects.get("organization_uuid", None)
        authenticated_user = self.request.user
        queryset = Prescription.objects.select_related(
            "organization", "patient", "doctor"
        ).filter(organization_id=organization.id, doctor_id=authenticated_user.id)
        return queryset


class PrescriptionListForPatient(ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        authenticated_user = self.request.user
        queryset = Prescription.objects.select_related(
            "organization", "patient", "doctor"
        ).filter(patient_id=authenticated_user.id)
        return queryset


class _PrescriptionDetailsDelete(RetrieveDestroyAPIView):
    queryset = Prescription.objects.select_related(
        "organization", "patient", "doctor"
    ).filter()
    serializer_class = PrescriptionDetailSerializer
    permission_classes = [IsAuthenticated, HasPrescriptionAccess]
    lookup_field = "uuid"
    lookup_url_kwarg = "prescription_uuid"


class PrescriptionDetailsDeleteForPatient(_PrescriptionDetailsDelete):
    pass


class PrescriptionDetailsDeleteForDoctor(
    PathValidationMixin, _PrescriptionDetailsDelete
):
    path_variables = ("organization_uuid",)
    model_classes = (Organization,)
    kwarg_objects = {}

    def get_permissions(self):
        permissions = super().get_permissions()
        organization = self.kwarg_objects.get("organization_uuid", None)
        authenticated_user = self.request.user
        permissions.append(
            HasRole(organization=organization, user=authenticated_user, role=DOCTOR)
        )
        return permissions


class PrescriptionMarkAsDone(DestroyAPIView):
    queryset = Prescription.objects.filter()
    serializer_class = PrescriptionDetailSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "prescription_uuid"

    def get_permissions(self):
        return [
            IsAuthenticated(),
            HasPrescriptionAccess(),
        ]

    def perform_destroy(self, instance):
        instance.done = True
        instance.save()


class _PrescriptionFeedbackCreate(PathValidationMixin, CreateAPIView):
    serializer_class = PrescriptionFeedbackSerializer
    path_variables = ("prescription_uuid",)
    model_classes = (Prescription,)
    kwarg_objects = {}

    def get_permissions(self):
        prescription = self.kwarg_objects.get("prescription_uuid")
        return [
            IsAuthenticated(),
            NOT(IsDone(prescription=prescription)),
        ]


class PrescriptionFeedbackCreateForPatient(
    PrescriptionPatientPermissionMixin, _PrescriptionFeedbackCreate
):
    pass


class PrescriptionFeedbackCreateForDoctor(
    PrescriptionDoctorPermissionMixin, _PrescriptionFeedbackCreate
):
    path_variables = ("organization_uuid", "prescription_uuid")
    model_classes = (
        Organization,
        Prescription,
    )


class _PrescriptionChatListCreate(PathValidationMixin, ListCreateAPIView):
    serializer_class = PrescriptionMessageSerializer
    path_variables = ("prescription_uuid",)
    model_classes = (Prescription,)
    kwarg_objects = {}

    def get_permissions(self):
        prescription = self.kwarg_objects.get("prescription_uuid")
        return [
            IsAuthenticated(),
            NOT(IsDone(prescription=prescription)),
        ]

    def get_queryset(self):
        prescription = self.kwarg_objects.get("prescription_uuid")
        queryset = (
            PrescriptionMessage.objects.select_related("prescription")
            .filter(prescription__id=prescription.id)
            .order_by("-created_at")
        )
        return queryset


class PrescriptionChatListCreateForPatient(
    PrescriptionPatientPermissionMixin, _PrescriptionChatListCreate
):
    pass


class PrescriptionChatListCreateforDoctor(
    PrescriptionDoctorPermissionMixin, _PrescriptionChatListCreate
):
    path_variables = ("organization_uuid", "prescription_uuid")
    model_classes = (
        Organization,
        Prescription,
    )
