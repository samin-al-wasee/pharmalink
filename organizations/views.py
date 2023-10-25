from django.contrib.auth import get_user_model
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from common.constants import ACTIVE, INACTIVE

from .mixins import OwnerPermissionMixin
from .models import Organization, OrganizationHasUserWithRole
from .serializers import (OrganizationSerializer,
                          OrganizationUserBaseSerializer,
                          OrganizationUserSerializerForOwner,
                          OrganizationUserSerializerForUser)


# Create your views here.
class OrganizationListOnlyOwned(ListAPIView):
    """
    Return only owned organizations by authenticated user regardless of status.
    """

    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        auth_user: get_user_model() = self.request.user
        queryset = Organization.objects.select_related().filter(owner_id=auth_user.id)
        return queryset


class OrganizationListCreate(ListCreateAPIView):
    """
    Return all active organizations regardless of owner.
    Create organization for authenticated user.
    """

    queryset = Organization.objects.filter(status=ACTIVE)
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]


class OrganizationDetailsUpdate(OwnerPermissionMixin, RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.filter()
    serializer_class = OrganizationSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "org_uuid"

    def perform_destroy(self, instance: Organization):  # Possible REFACTOR
        instance.status = INACTIVE
        instance.save()


class OrganizationUserCreateForUser(CreateAPIView):
    serializer_class = OrganizationUserSerializerForUser
    permission_classes = [IsAuthenticated]


class OrganizationUserListCreateForOwner(OwnerPermissionMixin, ListCreateAPIView):
    serializer_class = OrganizationUserSerializerForOwner

    def get_queryset(self):
        org_uuid = self.request.parser_context.get("kwargs").get("org_uuid")
        queryset = OrganizationHasUserWithRole.objects.select_related().filter(
            organization__uuid=org_uuid
        )
        return queryset


class OrganizationUserDetailsUpdateDelete(
    OwnerPermissionMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = OrganizationUserBaseSerializer
    lookup_field = "user__uuid"
    lookup_url_kwarg = "user_uuid"

    def get_queryset(self):
        org_uuid = self.kwargs.get("org_uuid")
        queryset = OrganizationHasUserWithRole.objects.select_related().filter(
            organization__uuid=org_uuid
        )
        return queryset
