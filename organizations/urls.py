from django.urls import include, path

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
        "/me/organizations",
        OrganizationListOnlyOwned.as_view(),
        name="org-list-owned",
    ),
    path(
        "/we",
        OrganizationListCreate.as_view(),
        name="org-list-all-create",
    ),
    path(
        "/we/join",
        OrganizationUserCreateForUser.as_view(),
        name="org-user-create-for-user",
    ),
    path(
        "/we/<uuid:organization_uuid>",
        OrganizationDetailsUpdate.as_view(),
        name="org-details-update",
    ),
    path(
        "/we/<uuid:organization_uuid>/medicines",
        include("medicines.urls.org-medicines"),
    ),
    path(
        "/we/<uuid:organization_uuid>/services",
        include("services.urls.root"),
    ),
    path(
        "/we/<uuid:organization_uuid>/users",
        OrganizationUserListCreateForOwner.as_view(),
        name="org-user-list-create-for-owner",
    ),
    path(
        "/we/<uuid:organization_uuid>/users/<uuid:user_uuid>",
        OrganizationUserDetailsUpdateDelete.as_view(),
        name="org-user-details-update-delete",
    ),
]
