from django.urls import path

from .views import (
    OrganizationDetailsUpdate,
    OrganizationListCreate,
    OrganizationListOnlyOwned,
    OrganizationUserCreateForUser,
    OrganizationUserDetailsUpdateDelete,
    OrganizationUserListCreateForOwner,
)

urlpatterns = [
    path(
        "",
        OrganizationListCreate.as_view(),
        name="org-list-all-create",
    ),
    path(
        "owned/",
        OrganizationListOnlyOwned.as_view(),
        name="org-list-owned",
    ),
    path(
        "join",
        OrganizationUserCreateForUser.as_view(),
        name="org-user-create-for-user",
    ),
    path(
        "<str:org_uuid>",
        OrganizationDetailsUpdate.as_view(),
        name="org-details-update",
    ),
    path(
        "<str:org_uuid>/users/",
        OrganizationUserListCreateForOwner.as_view(),
        name="org-user-list-create-for-owner",
    ),
    path(
        "<str:org_uuid>/users/<str:user_uuid>",
        OrganizationUserDetailsUpdateDelete.as_view(),
        name="org-user-details-update-delete",
    ),
]
