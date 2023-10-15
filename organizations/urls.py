from django.urls import path
from .views import OrganizationListCreateView, OrganizationDetailsUpdateView

urlpatterns = [
    path(
        "",
        OrganizationListCreateView.as_view(),
        name="organizations-list-all-create",
    ),
    path(
        "<str:uuid>",
        OrganizationDetailsUpdateView.as_view(),
        name="organization-details-update",
    ),
    path(
        "owned/",
        OrganizationListCreateView.as_view(),
        name="organizations-list-owned",
    ),
]
