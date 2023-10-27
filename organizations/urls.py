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
        "/organizations",
        OrganizationListCreate.as_view(),
        name="org-list-all-create",
    ),
    path(
        "/organizations/owned",
        OrganizationListOnlyOwned.as_view(),
        name="org-list-owned",
    ),
    path(
        "/organizations/join",
        OrganizationUserCreateForUser.as_view(),
        name="org-user-create-for-user",
    ),
    path(
        "/organizations/<uuid:organization_uuid>",
        OrganizationDetailsUpdate.as_view(),
        name="org-details-update",
    ),
    path(
        "/organizations/<uuid:organization_uuid>/medicines",
        include("medicines.urls.org-medicines"),
    ),
    path(
        "/organizations/<uuid:organization_uuid>/services",
        include("services.urls.root"),
    ),
    path(
        "/organizations/<uuid:organization_uuid>/users",
        OrganizationUserListCreateForOwner.as_view(),
        name="org-user-list-create-for-owner",
    ),
    path(
        "/organizations/<uuid:organization_uuid>/users/<uuid:user_uuid>",
        OrganizationUserDetailsUpdateDelete.as_view(),
        name="org-user-details-update-delete",
    ),
]
