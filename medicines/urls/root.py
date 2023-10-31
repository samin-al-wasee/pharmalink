from django.urls import path

from ..views import MedicineBrandListForUser, MedicineGenericListForUser

urlpatterns = [
    path(
        "/medicines",
        MedicineBrandListForUser.as_view(),
        name="medicine-brand-list-user",
    ),
    path(
        "/generics",
        MedicineGenericListForUser.as_view(),
        name="medicine-generic-list-user",
    ),
]
