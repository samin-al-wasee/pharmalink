from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin

from common.constants import ACTIVE, DISBANDED

from .mixins import OwnerPermissionMixin
from .models import Organization, OrganizationHasUserWithRole
from .serializers import (
    OrganizationSerializer,
    OrganizationUserBaseSerializer,
    OrganizationUserSerializerForOwner,
    OrganizationUserSerializerForUser,
)
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from common.mixins import PathValidationMixin


# Create your views here.
class _OrganizationList(ListAPIView):
    queryset = Organization.objects.select_related("owner", "address").filter()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "address__city", "address__country"]
    search_fields = [
        "name",
        "information",
    ]


class OrganizationListOnlyOwned(_OrganizationList):
    """
    List organizations owned only by the authenticated user.
    """

    def get_queryset(self):
        authenticated_user: get_user_model() = self.request.user
        owned_queryset = self.queryset.filter(owner_id=authenticated_user.id)
        joined_ids = (
            OrganizationHasUserWithRole.objects
            .filter(user_id=authenticated_user.id)
            .values("organization")
        )
        joined_queryset = self.queryset.filter(id__in=joined_ids)
        queryset = owned_queryset | joined_queryset
        return queryset


class OrganizationListCreate(CreateModelMixin, _OrganizationList):
    """
    List all organizations.
    Create organization for authenticated user.
    """

    filterset_fields = ["status", "owner__name", "address__city", "address__country"]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrganizationDetailsUpdate(OwnerPermissionMixin, RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.filter()
    serializer_class = OrganizationSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "organization_uuid"

    def perform_destroy(self, instance: Organization):  # Possible REFACTOR
        instance.status = DISBANDED
        instance.save()


class OrganizationUserCreateForUser(CreateAPIView):
    serializer_class = OrganizationUserSerializerForUser
    permission_classes = [IsAuthenticated]


class OrganizationUserListCreateForOwner(
    OwnerPermissionMixin, PathValidationMixin, ListCreateAPIView
):
    serializer_class = OrganizationUserSerializerForOwner
    path_variables = ("organization_uuid",)
    model_classes = (Organization,)
    kwarg_objects = {}

    def get_queryset(self):
        organization_uuid = self.kwargs.get("organization_uuid")
        queryset = OrganizationHasUserWithRole.objects.select_related(
            "organization", "user"
        ).filter(organization__uuid=organization_uuid)
        return queryset


class OrganizationUserDetailsUpdateDelete(
    OwnerPermissionMixin, PathValidationMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = OrganizationUserBaseSerializer
    path_variables = ("organization_uuid",)
    model_classes = (Organization,)
    kwarg_objects = {}
    lookup_field = "user__uuid"
    lookup_url_kwarg = "user_uuid"

    def get_queryset(self):
        organization_uuid = self.kwargs.get("organization_uuid")
        queryset = OrganizationHasUserWithRole.objects.select_related(
            "organization", "user"
        ).filter(organization__uuid=organization_uuid)
        return queryset
