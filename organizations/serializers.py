from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserAccountSerializer
from common.serializers import AddressSerializer
from common.utils import get_nested_object_deserialized, remove_blank_or_null

from .models import Organization, OrganizationHasUserWithRole


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "uuid",
            "name",
            "email",
            "information",
            "status",
            "address",
            "owner_user_account",
            "created_at",
        )
        read_only_fields = ("owner_user_account",)

    address = AddressSerializer(allow_null=True, required=False)
    owner_user_account = UserAccountSerializer(read_only=True)

    def is_valid(self, *, raise_exception=False):  # Needs REFACTOR
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):  # Needs REFACTOR
        organization_address: dict = validated_data.pop("address", None)
        if organization_address is not None:
            validated_data["address"] = get_nested_object_deserialized(
                data=organization_address, serializer_class=AddressSerializer
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):  # Needs REFACTOR
        organization_address: dict = validated_data.pop("address", None)
        if organization_address is not None:
            validated_data["address"] = get_nested_object_deserialized(
                data=organization_address,
                serializer_class=AddressSerializer,
            )
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        return super().save(**kwargs)


class OrganizationUserSerializer(ModelSerializer):
    class Meta:
        model = OrganizationHasUserWithRole
        fields = "__all__"
        read_only = ("organization",)

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)
