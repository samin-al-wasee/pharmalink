from typing import Any

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .models import Organization


class IsAuthenticatedOwner(IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj: Organization | Any):
        authenticated_user_account = request.user

        if type(obj) is Organization:
            return obj.owner_user_account.id == authenticated_user_account.id
        else:
            organization = Organization.objects.get(
                uuid=request.parser_context["kwargs"]["organization_uuid"]
            )
            return organization.owner_user_account.id == authenticated_user_account.id
