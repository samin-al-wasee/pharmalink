from rest_framework.serializers import ModelSerializer
from .models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        exclude = ("id",)
