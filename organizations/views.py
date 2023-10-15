from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserAccount
from common.constants import ORGANIZATION_IS_ACTIVE

from .models import Organization
from .permissions import IsAuthenticatedOwner
from .serializers import OrganizationSerializer


# Create your views here.
class OrganizationListCreateView(ListCreateAPIView):
    queryset = Organization.objects.filter(status=ORGANIZATION_IS_ACTIVE)
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    @property
    def allowed_methods(self):
        allowed_methods = super().allowed_methods

        if self.request and not self.request.path_info.endswith("organizations/"):
            allowed_methods = [method for method in allowed_methods if method != "POST"]

        return allowed_methods

    def get_queryset(self):
        if self.request and self.request.path_info.endswith("owned/"):
            authenticated_user_account: UserAccount = self.request.user
            queryset = Organization.objects.filter(
                owner_user_account_id=authenticated_user_account.id
            )
            return queryset

        return super().get_queryset()

    def perform_create(self, serializer: OrganizationSerializer):
        authenticated_user_account: UserAccount = self.request.user
        serializer.validated_data["owner_user_account"] = authenticated_user_account
        super().perform_create(serializer)


class OrganizationDetailsUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticatedOwner]
    lookup_field = "uuid"

    def perform_destroy(self, instance: Organization):
        instance.status = "I"
        instance.save()
