from django.urls import include, path

from ..views import (MedicineBrandDetailsUpdateDelete,
                     MedicineBrandListCreateForOwner)

urlpatterns = [
    path(
        "/",
        MedicineBrandListCreateForOwner.as_view(),
        name="med-brand-list-create-owner",
    ),
    path(
        "/<slug:med_slug>",
        MedicineBrandDetailsUpdateDelete.as_view(),
        name="med-brand-detail-update-delete",
    ),
]
