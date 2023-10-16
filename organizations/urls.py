from django.urls import path

from .views import (
    OrganizationDetailsUpdateView,
    OrganizationListCreateView,
    OrganizationUserDetailsUpdateDeleteView,
    OrganizationUserListCreateView,
)

urlpatterns = [
    path(
        "",
        OrganizationListCreateView.as_view(),
        name="organizations-list-all-create",
    ),
    path(
        "owned/",
        OrganizationListCreateView.as_view(),
        name="organizations-list-owned",
    ),
    path(
        "<str:uuid>",
        OrganizationDetailsUpdateView.as_view(),
        name="organization-details-update",
    ),
    path(
        "<str:uuid>/users/",
        OrganizationUserListCreateView.as_view(),
        name="organization-user-list-create",
    ),
    path(
        "<str:organization_uuid>/users/<str:user_uuid>",
        OrganizationUserDetailsUpdateDeleteView.as_view(),
        name="organization-user-details-update-delete",
    ),
]
