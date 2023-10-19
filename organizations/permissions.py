from typing import Any

from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from .models import Organization


class IsOrganizationOwner(BasePermission):
    def __init__(self) -> None:
        super().__init__()
        self.user = None
        self.organization = None

    def get_user_and_organization(
        self, request: Request, view, obj=None
    ) -> (
        tuple
    ):  # Needs REFACTOR (Extra conditionals not needed, qurysets are lazily evaluated)
        self.user: get_user_model() = request.user if self.user is None else self.user
        try:
            self.organization: Organization = (
                Organization.objects.select_related().get(
                    uuid=request.parser_context.get("kwargs").get("org_uuid")
                )
                if self.organization is None
                else self.organization
            )
        except Organization.DoesNotExist:
            raise NotFound("Organization does not exist.")

        return self.user, self.organization

    def has_permission(self, request: Request, view):
        user, organization = self.get_user_and_organization(
            request=request, view=view
        )
        return user.is_authenticated and organization.owner.id == user.id

    def has_object_permission(self, request: Request, view, obj: Organization | Any):
        user, organization = self.get_user_and_organization(
            request=request, view=view, obj=obj
        )
        if type(obj) is Organization:
            return obj.owner.id == user.id
        else:
            return organization.owner.id == user.id
