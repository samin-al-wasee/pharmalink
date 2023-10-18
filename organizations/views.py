from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from common.constants import ORGANIZATION_IS_ACTIVE, ORGANIZATION_IS_INACTIVE

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
class OrganizationListViewOnlyOwned(ListAPIView):  # DONE
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        authenticated_user_account: get_user_model() = self.request.user
        queryset = Organization.objects.select_related().filter(
            owner_user_account_id=authenticated_user_account.id
        )
        return queryset


class OrganizationListCreateView(ListCreateAPIView):  # DONE
    queryset = Organization.objects.filter(status=ORGANIZATION_IS_ACTIVE)
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]


class OrganizationDetailsUpdateView(RetrieveUpdateDestroyAPIView):  # DONE
    queryset = Organization.objects.filter()
    serializer_class = OrganizationSerializer
    permission_classes = [IsOrganizationOwner]
    lookup_field = "uuid"
    lookup_url_kwarg = "org_uuid"

    def perform_destroy(self, instance: Organization):  # Possible REFACTOR
        instance.status = ORGANIZATION_IS_INACTIVE
        instance.save()


class OrganizationUserCreateViewForUser(CreateAPIView):  # DONE
    serializer_class = OrganizationUserSerializerForUser
    permission_classes = [IsAuthenticated]


class OrganizationUserListCreateViewForOwner(ListCreateAPIView):  # DONE
    serializer_class = OrganizationUserSeralizerForOwner
    permission_classes = [IsOrganizationOwner]

    def get_queryset(self):
        organization_uuid = self.request.parser_context.get("kwargs").get("org_uuid")
        queryset = OrganizationHasUserWithRole.objects.select_related().filter(
            organization__uuid=organization_uuid
        )
        return queryset


class OrganizationUserDetailsUpdateDeleteView(RetrieveUpdateDestroyAPIView):  # DONE
    permission_classes = [IsOrganizationOwner]
    lookup_field = "user_account__uuid"
    lookup_url_kwarg = "user_uuid"

    def get_queryset(self):
        organization_uuid = self.request.parser_context.get("kwargs").get("org_uuid")
        queryset = OrganizationHasUserWithRole.objects.select_related().filter(
            organization__uuid=organization_uuid
        )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return OrganizationUserBaseSerializer
        else:
            return OrganizationUserSerializer
