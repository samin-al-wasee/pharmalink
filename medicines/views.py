from django.db.models import Q
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request

from organizations.mixins import OwnerPermissionMixin

from .models import MedicineBrand, MedicineGeneric
from .serializers import MedicineBrandSerializer, MedicineGenericSerializer


# Create your views here.
class MedicineBrandListForUser(ListAPIView):
    queryset = MedicineBrand.objects.filter()
    serializer_class = MedicineBrandSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        request: Request = self.request
        query_params = request.query_params
        if query_params:
            query = Q()
            query_param_mapper = {
                "name": "name",
                "generic": "generic__name",
                "pharmacology": "generic__pharmacology",
                "indications": "generic__indications",
                "interactions": "generic__indications",
                "sideeffects": "generic__side_effects",
                "manufacturer": "manufacturer__name",
            }
            for param, keywords in query_params.items():
                keywords = query_params.get(param).split("%")
                field = query_param_mapper.get(param)
                for word in keywords:
                    query |= Q(**{field + "__icontains": word})
            queryset = MedicineBrand.objects.select_related(
                "generic", "manufacturer"
            ).filter(query)
            return queryset
        return super().get_queryset()


class MedicineBrandListCreateForOwner(OwnerPermissionMixin, ListCreateAPIView):
    serializer_class = MedicineBrandSerializer

    def get_queryset(self):
        org_uuid = self.kwargs.get("org_uuid")
        queryset = MedicineBrand.objects.filter(manufacturer__uuid=org_uuid)
        return queryset


class MedicineBrandDetailsUpdateDelete(
    OwnerPermissionMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = MedicineBrandSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "med_slug"

    def get_queryset(self):
        org_uuid = self.kwargs.get("org_uuid")
        queryset = MedicineBrand.objects.select_related().filter(
            manufacturer__uuid=org_uuid
        )
        return queryset


class MedicineGenericListForUser(ListAPIView):
    queryset = MedicineGeneric.objects.filter()
    serializer_class = MedicineGenericSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        request: Request = self.request
        query_params = request.query_params
        if query_params:
            keywords = query_params.get("name").split("%")
            query = Q()
            for word in keywords:
                query |= Q(slug__icontains=word)
            queryset = MedicineGeneric.objects.filter(query)
            return queryset
        return super().get_queryset()
