from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from accounts.models import UserAccount
from common.constants import ORGANIZATION_IS_ACTIVE

from .models import Organization, OrganizationHasUserWithRole
from .permissions import IsAuthenticatedOwner
from .serializers import OrganizationSerializer, OrganizationUserSerializer


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


class OrganizationUserListCreateView(ListCreateAPIView):
    queryset = OrganizationHasUserWithRole.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticatedOwner]

    def check_permissions(self, request: Request):
        organization_uuid = request.parser_context["kwargs"]["uuid"]
        try:
            organization = get_object_or_404(klass=Organization, uuid=organization_uuid)
        except Http404:
            raise NotFound

        if organization.owner_user_account.id != request.user.id:
            raise PermissionDenied(
                "Only the organization owner can see the organization's users' list"
            )

        return super().check_permissions(request)

    def get_queryset(self):
        queryset = super().get_queryset()
        organization_uuid = self.request.parser_context["kwargs"]["uuid"]
        queryset = queryset.filter(organization__uuid=organization_uuid)
        return queryset


class OrganizationUserDetailsUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = OrganizationHasUserWithRole.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticatedOwner]
    lookup_field = "user_account__uuid"
    lookup_url_kwarg = "user_uuid"

    def check_permissions(self, request):
        organization_uuid = request.parser_context["kwargs"]["organization_uuid"]
        try:
            get_object_or_404(klass=Organization, uuid=organization_uuid)
        except Http404:
            raise NotFound("Organization not found.")
        return super().check_permissions(request)

    def get_queryset(self):
        queryset = super().get_queryset()
        organization_uuid = self.request.parser_context["kwargs"]["organization_uuid"]
        queryset = queryset.filter(organization__uuid=organization_uuid)
        return queryset
