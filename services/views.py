from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import NOT, IsAuthenticated

from common.constants import DOCTOR, PATIENT
from common.utils import get_path_objects
from organizations.models import Organization

from .models import (
    FeedbackToOrganization,
    MessageBetweenUserOrganization,
    Prescription,
    PrescriptionMessage,
)
from .permissions import HasPrescriptionAccess, HasPrescriptionRole, HasRole
from .serializers import (
    FeedbackSerializer,
    MessageSerializer,
    PrescriptionDetailSerializer,
    PrescriptionFeedbackSerializer,
    PrescriptionMessageSerializer,
    PrescriptionSerializer,
)


# Create your views here.
class FeedbackListCreate(ListCreateAPIView):
    serializer_class = FeedbackSerializer

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

    def check_permissions(self, request):  # Should REFACTOR
        path_variables = ("organization_uuid",)
        model_classes = (Organization,)
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs,
            path_variables=path_variables,
            model_classes=model_classes,
        )
        return super().check_permissions(request)

    def get_queryset(self):
        organization = self.kwarg_objects.get("organization_uuid")
        queryset = (
            FeedbackToOrganization.objects.select_related()
            .filter(organization_id=organization.id)
            .order_by("-created_at")
            .distinct()
        )
        return queryset


class ConversationList(ListAPIView):
    serializer_class = MessageSerializer

    def get_permissions(self):
        organization_uuid = self.kwargs.get("organization_uuid")
        if organization_uuid:
            organization = self.kwarg_objects.get("organization_uuid", None)
            authenticated_user = self.request.user
            return [
                IsAuthenticated(),
                NOT(
                    HasRole(
                        organization=organization, user=authenticated_user, role=PATIENT
                    )
                ),
            ]
        else:
            return [IsAuthenticated()]

    def check_permissions(self, request):
        organization_uuid = self.kwargs.get("organization_uuid", None)
        if organization_uuid:
            path_variables = ("organization_uuid",)
            model_classes = (Organization,)
            self.kwarg_objects = get_path_objects(
                request_kwargs=self.kwargs,
                path_variables=path_variables,
                model_classes=model_classes,
            )
        return super().check_permissions(request)

    def get_queryset(self):
        organization_uuid = self.kwargs.get("organization_uuid")
        if organization_uuid:
            organization = self.kwarg_objects.get("organization_uuid", None)
            queryset = (
                MessageBetweenUserOrganization.objects.select_related()
                .filter(organization_id=organization.id)
                .order_by("-created_at")
            )
            return queryset
        else:
            authenticated_user = self.request.user
            queryset = (
                MessageBetweenUserOrganization.objects.select_related()
                .filter(user_id=authenticated_user.id)
                .order_by("-created_at")
            )
            return queryset


class MessageListCreate(ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_permissions(self):
        recepient = self.kwarg_objects.get("user_uuid", None)
        organization = self.kwarg_objects.get("organization_uuid")
        authenticated_user = self.request.user
        if recepient:
            return [
                IsAuthenticated(),
                NOT(
                    HasRole(
                        organization=organization, user=authenticated_user, role=PATIENT
                    )
                ),
                HasRole(organization=organization, user=recepient, role=PATIENT),
            ]
        else:
            return [
                IsAuthenticated(),
                HasRole(
                    organization=organization, user=authenticated_user, role=PATIENT
                ),
            ]

    def check_permissions(self, request):
        user_uuid = self.kwargs.get("user_uuid", None)
        if user_uuid:
            path_variables = ("organization_uuid", "user_uuid")
            model_classes = (Organization, get_user_model())
        else:
            path_variables = ("organization_uuid",)
            model_classes = (Organization,)
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs,
            path_variables=path_variables,
            model_classes=model_classes,
        )
        return super().check_permissions(request)

    def get_queryset(self):
        recepient = self.kwarg_objects.get("user_uuid", None)
        organization = self.kwarg_objects.get("organization_uuid", None)
        authenticated_user = self.request.user
        if recepient:
            queryset = (
                MessageBetweenUserOrganization.objects.select_related()
                .filter(organization_id=organization.id, user_id=recepient.id)
                .order_by("-created_at")
            )
            return queryset
        else:
            queryset = (
                MessageBetweenUserOrganization.objects.select_related()
                .filter(organization_id=organization.id, user_id=authenticated_user.id)
                .order_by("-created_at")
            )
            return queryset


class PrescriptionListCreate(ListCreateAPIView):
    serializer_class = PrescriptionSerializer

    def get_permissions(self):
        organization = self.kwarg_objects.get("organization_uuid", None)
        authenticated_user = self.request.user
        return [
            IsAuthenticated(),
            HasRole(organization=organization, user=authenticated_user, role=DOCTOR),
        ]

    def check_permissions(self, request):
        path_variables = ("organization_uuid",)
        model_classes = (Organization,)
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs,
            path_variables=path_variables,
            model_classes=model_classes,
        )
        return super().check_permissions(request)

    def get_queryset(self):
        organization = self.kwarg_objects.get("organization_uuid", None)
        authenticated_user = self.request.user
        queryset = Prescription.objects.select_related().filter(
            organization_id=organization.id, doctor_id=authenticated_user.id
        )
        return queryset


class PrescriptionListForPatient(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        authenticated_user = self.request.user
        queryset = Prescription.objects.select_related().filter(
            patient_id=authenticated_user.id
        )
        return queryset


class PrescriptionDetailsDelete(RetrieveDestroyAPIView):
    queryset = Prescription.objects.filter()
    serializer_class = PrescriptionDetailSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "prescription_uuid"

    def get_permissions(self):
        organization_uuid = self.kwargs.get("organization_uuid")
        if organization_uuid:
            organization = self.kwarg_objects.get("organization_uuid", None)
            authenticated_user = self.request.user
            return [
                IsAuthenticated(),
                HasRole(
                    organization=organization, user=authenticated_user, role=DOCTOR
                ),
                HasPrescriptionAccess(),
            ]
        else:
            return [
                IsAuthenticated(),
                HasPrescriptionAccess(),
            ]

    def check_permissions(self, request):
        organization_uuid = self.kwargs.get("organization_uuid", None)
        if organization_uuid:
            path_variables = ("organization_uuid",)
            model_classes = (Organization,)
            self.kwarg_objects = get_path_objects(
                request_kwargs=self.kwargs,
                path_variables=path_variables,
                model_classes=model_classes,
            )
        return super().check_permissions(request)


class PrescriptionMarkAsDone(DestroyAPIView):
    queryset = Prescription.objects.filter()
    serializer_class = PrescriptionDetailSerializer

    def get_permissions(self):
        return [
            IsAuthenticated(),
            HasPrescriptionAccess(),
        ]

    def perform_destroy(self, instance):
        instance.done = True
        instance.save()


class PrescriptionFeedbackCreate(CreateAPIView):
    serializer_class = PrescriptionFeedbackSerializer

    def get_permissions(self):
        organization = self.kwarg_objects.get("organization_uuid")
        prescription = self.kwarg_objects.get("prescription_uuid")
        authenticated_user = self.request.user
        if organization:
            return [
                IsAuthenticated(),
                HasPrescriptionRole(
                    prescription=prescription, user=authenticated_user, role=DOCTOR
                ),
            ]
        else:
            return [
                IsAuthenticated(),
                HasPrescriptionRole(
                    prescription=prescription, user=authenticated_user, role=PATIENT
                ),
            ]

    def check_permissions(self, request):
        organization_uuid = self.kwargs.get("organization_uuid", None)
        if organization_uuid:
            path_variables = ("organization_uuid", "prescription_uuid")
            model_classes = (Organization, Prescription)
        else:
            path_variables = ("prescription_uuid",)
            model_classes = (Prescription,)
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs,
            path_variables=path_variables,
            model_classes=model_classes,
        )
        return super().check_permissions(request)


class PrescriptionChatListCreate(ListCreateAPIView):
    serializer_class = PrescriptionMessageSerializer

    def get_permissions(self):
        organization = self.kwarg_objects.get("organization_uuid")
        prescription = self.kwarg_objects.get("prescription_uuid")
        authenticated_user = self.request.user
        if organization:
            return [
                IsAuthenticated(),
                HasPrescriptionRole(
                    prescription=prescription, user=authenticated_user, role=DOCTOR
                ),
            ]
        else:
            return [
                IsAuthenticated(),
                HasPrescriptionRole(
                    prescription=prescription, user=authenticated_user, role=PATIENT
                ),
            ]

    def check_permissions(self, request):
        organization_uuid = self.kwargs.get("organization_uuid", None)
        if organization_uuid:
            path_variables = ("organization_uuid", "prescription_uuid")
            model_classes = (Organization, Prescription)
        else:
            path_variables = ("prescription_uuid",)
            model_classes = (Prescription,)
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs,
            path_variables=path_variables,
            model_classes=model_classes,
        )
        return super().check_permissions(request)

    def get_queryset(self):
        prescription = self.kwarg_objects.get("prescription_uuid")
        queryset = (
            PrescriptionMessage.objects.select_related("prescription")
            .filter(prescription__id=prescription.id)
            .order_by("-created_at")
        )
        return queryset
