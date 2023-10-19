from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from common.constants import ACTIVE, INACTIVE

from .models import Organization, OrganizationHasUserWithRole
from .permissions import IsOrganizationOwner
from .serializers import (
    OrganizationSerializer,
    OrganizationUserBaseSerializer,
    OrganizationUserSeralizerForOwner,
    OrganizationUserSerializer,
    OrganizationUserSerializerForUser,
)


# Create your views here.
class OrganizationListOnlyOwned(ListAPIView):  # DONE
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        auth_user: get_user_model() = self.request.user
        queryset = Organization.objects.select_related().filter(owner_id=auth_user.id)
        return queryset


class OrganizationListCreate(ListCreateAPIView):  # DONE
    queryset = Organization.objects.filter(status=ACTIVE)
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]


class OrganizationDetailsUpdate(RetrieveUpdateDestroyAPIView):  # DONE
    queryset = Organization.objects.filter()
    serializer_class = OrganizationSerializer
    permission_classes = [IsOrganizationOwner]
    lookup_field = "uuid"
    lookup_url_kwarg = "org_uuid"

    def perform_destroy(self, instance: Organization):  # Possible REFACTOR
        instance.status = INACTIVE
        instance.save()


class OrganizationUserCreateForUser(CreateAPIView):  # DONE
    serializer_class = OrganizationUserSerializerForUser
    permission_classes = [IsAuthenticated]


class OrganizationUserListCreateForOwner(ListCreateAPIView):  # DONE
    serializer_class = OrganizationUserSeralizerForOwner
    permission_classes = [IsOrganizationOwner]

    def get_queryset(self):
        org_uuid = self.request.parser_context.get("kwargs").get("org_uuid")
        queryset = OrganizationHasUserWithRole.objects.select_related().filter(
            organization__uuid=org_uuid
        )
        return queryset


class OrganizationUserDetailsUpdateDelete(RetrieveUpdateDestroyAPIView):  # DONE
    permission_classes = [IsOrganizationOwner]
    lookup_field = "user__uuid"
    lookup_url_kwarg = "user_uuid"

    def get_queryset(self):
        org_uuid = self.request.parser_context.get("kwargs").get("org_uuid")
        queryset = OrganizationHasUserWithRole.objects.select_related().filter(
            organization__uuid=org_uuid
        )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return OrganizationUserBaseSerializer
        else:
            return OrganizationUserSerializer
