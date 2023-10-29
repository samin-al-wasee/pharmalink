from rest_framework.permissions import IsAuthenticated

from common.utils import get_path_objects

from .models import Organization
from .permissions import IsOrganizationOwner


class OwnerPermissionMixin:
    """
    Add organization ownership related permission functionalities.
    """

    def get_permissions(self):
        organization = self.kwarg_objects.get("organization_uuid") if hasattr(self, "kwarg_objects") else None
        authenticated_user = self.request.user
        return [
            IsAuthenticated(),
            IsOrganizationOwner(organization=organization, user=authenticated_user),
        ]
