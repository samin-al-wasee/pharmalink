from django.db.models import Q
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request

from organizations.mixins import OwnerPermissionMixin

from .models import MedicineBrand, MedicineGeneric
from .serializers import MedicineBrandSerializer, MedicineGenericSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from common.mixins import PathValidationMixin
from organizations.models import Organization


# Create your views here.
class MedicineBrandListForUser(ListAPIView):
    queryset = MedicineBrand.objects.select_related("generic", "manufacturer").filter()
    serializer_class = MedicineBrandSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["generic__name", "manufacturer__name"]
    search_fields = [
        "name",
        "slug",
        "generic__name",
        "generic__slug",
        "generic__pharmacology",
        "generic__indications",
        "generic__interactions",
        "generic__side_effects",
        "manufacturer__name",
    ]


class MedicineBrandListCreateForOwner(OwnerPermissionMixin, PathValidationMixin, ListCreateAPIView):
    serializer_class = MedicineBrandSerializer
    path_variables = ("organization_uuid",)
    model_classes = (Organization,)
    kwarg_objects = {}

    def get_queryset(self):
        organization_uuid = self.kwargs.get("organization_uuid")
        queryset = MedicineBrand.objects.filter(manufacturer__uuid=organization_uuid)
        return queryset


class MedicineBrandDetailsUpdateDelete(
    OwnerPermissionMixin, PathValidationMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = MedicineBrandSerializer
    path_variables = ("organization_uuid",)
    model_classes = (Organization,)
    kwarg_objects = {}
    lookup_field = "slug"
    lookup_url_kwarg = "medicine_slug"

    def get_queryset(self):
        organization_uuid = self.kwargs.get("organization_uuid")
        queryset = MedicineBrand.objects.select_related().filter(
            manufacturer__uuid=organization_uuid
        )
        return queryset


class MedicineGenericListForUser(ListAPIView):
    queryset = MedicineGeneric.objects.filter()
    serializer_class = MedicineGenericSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = [
        "name",
        "slug",
        "pharmacology",
        "indications",
        "interactions",
        "side_effects",
    ]
