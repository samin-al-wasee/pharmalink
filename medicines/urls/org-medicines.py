from django.urls import path

from ..views import MedicineBrandDetailsUpdateDelete, MedicineBrandListCreateForOwner

urlpatterns = [
    path(
        "",
        MedicineBrandListCreateForOwner.as_view(),
        name="med-brand-list-create-owner",
    ),
    path(
        "/<slug:medicine_slug>",
        MedicineBrandDetailsUpdateDelete.as_view(),
        name="med-brand-detail-update-delete",
    ),
]
