from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer, UUIDField
from rest_framework.validators import ValidationError

from accounts.models import UserAccount
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


class OrganizationUserBaseSerializer(ModelSerializer):
    class Meta:
        model = OrganizationHasUserWithRole
        fields = ("role",)

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def replace_object_uuid_with_object(
        self,
        validated_data,
        object_uuid,
        object_uuid_field_name,
        object_field_name,
        model_class,
    ):
        validated_data_ = validated_data.copy()

        if object_uuid is not None:
            try:
                object_ = get_object_or_404(klass=model_class, uuid=object_uuid)
                validated_data_[object_field_name] = object_
                return validated_data_
            except Http404:
                raise ValidationError(
                    {
                        object_uuid_field_name: f"No {model_class._meta.model_name} with the given uuid found."
                    }
                )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["organization"] = instance.organization.uuid
        representation["user_account"] = instance.user_account.uuid
        return representation


class OrganizationUserSerializer(OrganizationUserBaseSerializer):
    class Meta(OrganizationUserBaseSerializer.Meta):
        fields = (
            "organization",
            "user_account",
            "user_account_uuid",
        ) + OrganizationUserBaseSerializer.Meta.fields
        read_only_fields = ("organization", "user_account")

    user_account_uuid = UUIDField(write_only=True)


class OrganizationUserSerializerForUser(OrganizationUserBaseSerializer):
    class Meta(OrganizationUserBaseSerializer.Meta):
        fields = (
            "organization",
            "organization_uuid",
            "user_account",
        ) + OrganizationUserBaseSerializer.Meta.fields
        read_only_fields = ("organization", "user_account")

    organization_uuid = UUIDField(write_only=True)

    def create(self, validated_data):
        try:
            organization_uuid = validated_data.pop("organization_uuid", None)
            validated_data = self.replace_object_uuid_with_object(
                validated_data=validated_data,
                object_uuid=organization_uuid,
                object_uuid_field_name="organization_uuid",
                object_field_name="organization",
                model_class=Organization,
            )
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError(
                {
                    "organization_uuid": "You already exist in this organization. Contact owner to update the role instead."
                }
            )


class OrganizationUserSeralizerForOwner(OrganizationUserBaseSerializer):
    class Meta(OrganizationUserBaseSerializer.Meta):
        fields = (
            "organization",
            "user_account",
            "user_account_uuid",
        ) + OrganizationUserBaseSerializer.Meta.fields
        read_only_fields = ("organization", "user_account")

    user_account_uuid = UUIDField(write_only=True)

    def create(self, validated_data):
        try:
            user_account_uuid = validated_data.pop("user_account_uuid", None)
            validated_data = self.replace_object_uuid_with_object(
                validated_data=validated_data,
                object_uuid=user_account_uuid,
                object_uuid_field_name="user_account_uuid",
                object_field_name="user_account",
                model_class=UserAccount,
            )
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError(
                {
                    "user_account_uuid": "This user already exists in this organization. Update the role instead."
                }
            )
