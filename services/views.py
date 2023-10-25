from django.contrib.auth import get_user_model
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, ListCreateAPIView,
                                     RetrieveDestroyAPIView)
from rest_framework.permissions import NOT, IsAuthenticated

from common.constants import DOCTOR, PATIENT
from common.utils import get_path_objects
from organizations.models import Organization

from .models import (FeedbackToOrganization, MessageBetweenUserOrganization,
                     Prescription, PrescriptionMessage)
from .permissions import HasPrescriptionAccess, HasPrescriptionRole, HasRole
from .serializers import (FeedbackSerializer, MessageSerializer,
                          PrescriptionDetailSerializer,
                          PrescriptionFeedbackSerializer,
                          PrescriptionMessageSerializer,
                          PrescriptionSerializer)


# Create your views here.
class FeedbackListCreate(ListCreateAPIView):
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        organization = self.kwarg_objects.get("org_uuid")
        auth_user = self.request.user
        if self.request.method == "GET":
            return [
                IsAuthenticated(),
                NOT(HasRole(organization=organization, user=auth_user, role=PATIENT)),
            ]
        elif self.request.method == "POST":
            return [
                IsAuthenticated(),
                HasRole(organization=organization, user=auth_user, role=PATIENT),
            ]
        else:
            return [IsAuthenticated()]

    def check_permissions(self, request):  # Should REFACTOR
        path_vars = ("org_uuid",)
        model_classes = (Organization,)
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs, path_vars=path_vars, model_classes=model_classes
        )
        return super().check_permissions(request)

    def get_queryset(self):
        organization = self.kwarg_objects.get("org_uuid")
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
        org_uuid = self.kwargs.get("org_uuid")
        if org_uuid:
            organization = self.kwarg_objects.get("org_uuid", None)
            auth_user = self.request.user
            return [
                IsAuthenticated(),
                NOT(HasRole(organization=organization, user=auth_user, role=PATIENT)),
            ]
        else:
            return [IsAuthenticated()]

    def check_permissions(self, request):
        org_uuid = self.kwargs.get("org_uuid", None)
        if org_uuid:
            path_vars = ("org_uuid",)
            model_classes = (Organization,)
            self.kwarg_objects = get_path_objects(
                request_kwargs=self.kwargs,
                path_vars=path_vars,
                model_classes=model_classes,
            )
        return super().check_permissions(request)

    def get_queryset(self):
        org_uuid = self.kwargs.get("org_uuid")
        if org_uuid:
            organization = self.kwarg_objects.get("org_uuid", None)
            queryset = (
                MessageBetweenUserOrganization.objects.select_related()
                .filter(organization_id=organization.id)
                .order_by("-created_at")
            )
            return queryset
        else:
            auth_user = self.request.user
            queryset = (
                MessageBetweenUserOrganization.objects.select_related()
                .filter(user_id=auth_user.id)
                .order_by("-created_at")
            )
            return queryset


class MessageListCreate(ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_permissions(self):
        recepient = self.kwarg_objects.get("user_uuid", None)
        organization = self.kwarg_objects.get("org_uuid")
        auth_user = self.request.user
        if recepient:
            return [
                IsAuthenticated(),
                NOT(HasRole(organization=organization, user=auth_user, role=PATIENT)),
                HasRole(organization=organization, user=recepient, role=PATIENT),
            ]
        else:
            return [
                IsAuthenticated(),
                HasRole(organization=organization, user=auth_user, role=PATIENT),
            ]

    def check_permissions(self, request):
        user_uuid = self.kwargs.get("user_uuid", None)
        if user_uuid:
            path_vars = ("org_uuid", "user_uuid")
            model_classes = (Organization, get_user_model())
        else:
            path_vars = ("org_uuid",)
            model_classes = (Organization,)
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs,
            path_vars=path_vars,
            model_classes=model_classes,
        )
        return super().check_permissions(request)

    def get_queryset(self):
        recepient = self.kwarg_objects.get("user_uuid", None)
        organization = self.kwarg_objects.get("org_uuid", None)
        auth_user = self.request.user
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
                .filter(organization_id=organization.id, user_id=auth_user.id)
                .order_by("-created_at")
            )
            return queryset


class PrescriptionListCreate(ListCreateAPIView):
    serializer_class = PrescriptionSerializer

    def get_permissions(self):
        organization = self.kwarg_objects.get("org_uuid", None)
        auth_user = self.request.user
        return [
            IsAuthenticated(),
            HasRole(organization=organization, user=auth_user, role=DOCTOR),
        ]

    def check_permissions(self, request):
        path_vars = ("org_uuid",)
        model_classes = (Organization,)
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs,
            path_vars=path_vars,
            model_classes=model_classes,
        )
        return super().check_permissions(request)

    def get_queryset(self):
        organization = self.kwarg_objects.get("org_uuid", None)
        auth_user = self.request.user
        queryset = Prescription.objects.select_related().filter(
            organization_id=organization.id, doctor_id=auth_user.id
        )
        return queryset


class PrescriptionListForPatient(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        auth_user = self.request.user
        queryset = Prescription.objects.select_related().filter(patient_id=auth_user.id)
        return queryset


class PrescriptionDetailsDelete(RetrieveDestroyAPIView):
    queryset = Prescription.objects.filter()
    serializer_class = PrescriptionDetailSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "presc_uuid"

    def get_permissions(self):
        org_uuid = self.kwargs.get("org_uuid")
        if org_uuid:
            organization = self.kwarg_objects.get("org_uuid", None)
            auth_user = self.request.user
            return [
                IsAuthenticated(),
                HasRole(organization=organization, user=auth_user, role=DOCTOR),
                HasPrescriptionAccess(),
            ]
        else:
            return [
                IsAuthenticated(),
                HasPrescriptionAccess(),
            ]

    def check_permissions(self, request):
        org_uuid = self.kwargs.get("org_uuid", None)
        if org_uuid:
            path_vars = ("org_uuid",)
            model_classes = (Organization,)
            self.kwarg_objects = get_path_objects(
                request_kwargs=self.kwargs,
                path_vars=path_vars,
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
        organization = self.kwarg_objects.get("org_uuid")
        prescription = self.kwarg_objects.get("presc_uuid")
        auth_user = self.request.user
        if organization:
            return [
                IsAuthenticated(),
                HasPrescriptionRole(
                    prescription=prescription, user=auth_user, role=DOCTOR
                ),
            ]
        else:
            return [
                IsAuthenticated(),
                HasPrescriptionRole(
                    prescription=prescription, user=auth_user, role=PATIENT
                ),
            ]

    def check_permissions(self, request):
        org_uuid = self.kwargs.get("org_uuid", None)
        if org_uuid:
            path_vars = ("org_uuid", "presc_uuid")
            model_classes = (Organization, Prescription)
        else:
            path_vars = ("presc_uuid",)
            model_classes = (Prescription,)
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs,
            path_vars=path_vars,
            model_classes=model_classes,
        )
        return super().check_permissions(request)


class PrescriptionChatListCreate(ListCreateAPIView):
    serializer_class = PrescriptionMessageSerializer

    def get_permissions(self):
        organization = self.kwarg_objects.get("org_uuid")
        prescription = self.kwarg_objects.get("presc_uuid")
        auth_user = self.request.user
        if organization:
            return [
                IsAuthenticated(),
                HasPrescriptionRole(
                    prescription=prescription, user=auth_user, role=DOCTOR
                ),
            ]
        else:
            return [
                IsAuthenticated(),
                HasPrescriptionRole(
                    prescription=prescription, user=auth_user, role=PATIENT
                ),
            ]

    def check_permissions(self, request):
        org_uuid = self.kwargs.get("org_uuid", None)
        if org_uuid:
            path_vars = ("org_uuid", "presc_uuid")
            model_classes = (Organization, Prescription)
        else:
            path_vars = ("presc_uuid",)
            model_classes = (Prescription,)
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs,
            path_vars=path_vars,
            model_classes=model_classes,
        )
        return super().check_permissions(request)

    def get_queryset(self):
        prescription = self.kwarg_objects.get("presc_uuid")
        queryset = (
            PrescriptionMessage.objects.select_related("prescription")
            .filter(prescription__id=prescription.id)
            .order_by("-created_at")
        )
        return queryset
