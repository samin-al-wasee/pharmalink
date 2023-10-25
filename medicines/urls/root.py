from django.urls import path

from ..views import MedicineBrandListForUser, MedicineGenericListForUser

urlpatterns = [
    path(
        "/medicines/brands",
        MedicineBrandListForUser.as_view(),
        name="medicine-brand-list-user",
    ),
    path(
        "/medicines/brands/search",
        MedicineBrandListForUser.as_view(),
        name="medicine-brand-list-user",
    ),
    path(
        "/medicines/generics",
        MedicineGenericListForUser.as_view(),
        name="medicine-generic-list-user",
    ),
    path(
        "/medicines/generics/search",
        MedicineGenericListForUser.as_view(),
        name="medicine-generic-search",
    ),
]
