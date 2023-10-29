from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin

from common.constants import ACTIVE, INACTIVE

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


# Create your views here.
class OrganizationList(ListAPIView):
    queryset = Organization.objects.select_related("owner", "address").filter()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "address__city", "address__country"]
    search_fields = [
        "name",
        "information",
    ]


class OrganizationListOnlyOwned(OrganizationList):
    """
    Return only owned organizations by authenticated user regardless of status.
    """

    def get_queryset(self):
        authenticated_user: get_user_model() = self.request.user
        queryset = self.queryset.filter(owner_id=authenticated_user.id)
        return queryset


class OrganizationListCreate(CreateModelMixin, OrganizationList):
    """
    Return all active organizations regardless of owner.
    Create organization for authenticated user.
    """

    filterset_fields = ["status", "owner__name", "address__city", "address__country"]


class OrganizationDetailsUpdate(OwnerPermissionMixin, RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.filter()
    serializer_class = OrganizationSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "organization_uuid"

    def perform_destroy(self, instance: Organization):  # Possible REFACTOR
        instance.status = INACTIVE
        instance.save()


class OrganizationUserCreateForUser(CreateAPIView):
    serializer_class = OrganizationUserSerializerForUser
    permission_classes = [IsAuthenticated]


class OrganizationUserListCreateForOwner(OwnerPermissionMixin, ListCreateAPIView):
    serializer_class = OrganizationUserSerializerForOwner

    def get_queryset(self):
        organization_uuid = self.request.parser_context.get("kwargs").get(
            "organization_uuid"
        )
        queryset = OrganizationHasUserWithRole.objects.select_related().filter(
            organization__uuid=organization_uuid
        )
        return queryset


class OrganizationUserDetailsUpdateDelete(
    OwnerPermissionMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = OrganizationUserBaseSerializer
    lookup_field = "user__uuid"
    lookup_url_kwarg = "user_uuid"

    def get_queryset(self):
        organization_uuid = self.kwargs.get("organization_uuid")
        queryset = OrganizationHasUserWithRole.objects.select_related().filter(
            organization__uuid=organization_uuid
        )
        return queryset
