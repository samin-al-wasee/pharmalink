from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserAccount
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
        authenticated_user_account: UserAccount = self.request.user
        queryset = Organization.objects.select_related().filter(
            owner_user_account_id=authenticated_user_account.id
        )
        return queryset


class OrganizationListCreateView(ListCreateAPIView):  # DONE
    queryset = Organization.objects.filter(status=ORGANIZATION_IS_ACTIVE)
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: OrganizationSerializer):
        authenticated_user_account: UserAccount = self.request.user
        serializer.validated_data["owner_user_account"] = authenticated_user_account
        super().perform_create(serializer)


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

    def perform_create(
        self, serializer: OrganizationUserSerializerForUser
    ):  # Possible REFACTOR
        user_account: UserAccount = self.request.user
        serializer.validated_data["user_account"] = user_account
        return super().perform_create(serializer)


class OrganizationUserListCreateViewForOwner(ListCreateAPIView):  # DONE
    serializer_class = OrganizationUserSeralizerForOwner
    permission_classes = [IsOrganizationOwner]

    def get_queryset(self):
        organization_uuid = self.request.parser_context["kwargs"]["org_uuid"]
        queryset = OrganizationHasUserWithRole.objects.select_related().filter(
            organization__uuid=organization_uuid
        )
        return queryset

    def perform_create(self, serializer):  # Possible REFACTOR
        organization_uuid = self.request.parser_context["kwargs"]["org_uuid"]
        organization: Organization = Organization.objects.get(uuid=organization_uuid)
        serializer.validated_data["organization"] = organization
        return super().perform_create(serializer)


class OrganizationUserDetailsUpdateDeleteView(RetrieveUpdateDestroyAPIView):  # DONE
    permission_classes = [IsOrganizationOwner]
    lookup_field = "user_account__uuid"
    lookup_url_kwarg = "user_uuid"

    def get_queryset(self):
        organization_uuid = self.request.parser_context["kwargs"]["org_uuid"]
        queryset = OrganizationHasUserWithRole.objects.select_related().filter(
            organization__uuid=organization_uuid
        )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return OrganizationUserBaseSerializer
        else:
            return OrganizationUserSerializer

    def perform_update(self, serializer: OrganizationUserBaseSerializer):
        organization_user_with_role: OrganizationHasUserWithRole = serializer.instance
        serializer.validated_data[
            "organization"
        ] = organization_user_with_role.organization
        serializer.validated_data[
            "user_account"
        ] = organization_user_with_role.user_account
        return super().perform_update(serializer)
