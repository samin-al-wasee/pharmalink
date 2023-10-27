from rest_framework.permissions import IsAuthenticated

from common.utils import get_path_objects

from .models import Organization
from .permissions import IsOrganizationOwner


class OwnerPermissionMixin:
    """
    Add organization ownership related permission functionalities.
    """

    def get_permissions(self):
        organization = self.kwarg_objects.get("organization_uuid")
        authenticated_user = self.request.user
        return [
            IsAuthenticated(),
            IsOrganizationOwner(organization=organization, user=authenticated_user),
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
