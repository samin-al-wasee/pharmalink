from typing import Any

from rest_framework.serializers import ModelSerializer

from .models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        exclude = ("id",)
        extra_kwargs = {
            "unit_no": {"required": False},
            "street_no": {"required": False},
            "line_1": {"required": False},
            "line_2": {"required": False},
            "region": {"required": False},
        }
