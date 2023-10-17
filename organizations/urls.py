from django.urls import path

from .views import (
    OrganizationDetailsUpdateView,
    OrganizationListCreateView,
    OrganizationListViewOnlyOwned,
    OrganizationUserCreateViewForUser,
    OrganizationUserDetailsUpdateDeleteView,
    OrganizationUserListCreateViewForOwner,
)

urlpatterns = [
    path(
        "",
        OrganizationListCreateView.as_view(),
        name="organizations-list-all-create",
    ),
    path(
        "owned/",
        OrganizationListViewOnlyOwned.as_view(),
        name="organizations-list-owned",
    ),
    path(
        "join",
        OrganizationUserCreateViewForUser.as_view(),
        name="organization-user-create-as-user",
    ),
    path(
        "<str:org_uuid>",
        OrganizationDetailsUpdateView.as_view(),
        name="organization-details-update",
    ),
    path(
        "<str:org_uuid>/users/",
        OrganizationUserListCreateViewForOwner.as_view(),
        name="organization-user-list-create-as-owner",
    ),
    path(
        "<str:org_uuid>/users/<str:user_uuid>",
        OrganizationUserDetailsUpdateDeleteView.as_view(),
        name="organization-user-details-update-delete",
    ),
]
