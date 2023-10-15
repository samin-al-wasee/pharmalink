from rest_framework.permissions import IsAuthenticated
from .models import Organization


class IsAuthenticatedOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj: Organization):
        authenticated_user_account = request.user

        return obj.owner_user_account.id == authenticated_user_account.id
