from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, UUIDField
from rest_framework.validators import ValidationError

from accounts.models import UserAccount
from accounts.serializers import UserAccountSerializer
from common.serializers import AddressSerializer
from common.utils import remove_blank_or_null, replace_nested_dict_with_objects

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

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):  # Needs REFACTOR
        request: Request = self.context.get("request")
        authenticated_user_account: UserAccount = request.user
        validated_data["owner_user_account"] = authenticated_user_account
        fields_to_convert = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data_replaced_final = replace_nested_dict_with_objects(
            data=validated_data,
            fields=fields_to_convert,
            serializer_classes=serializer_classes,
        )
        return super().create(validated_data_replaced_final)

    def update(self, instance, validated_data):  # Needs REFACTOR
        fields_to_convert = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data_replaced_final = replace_nested_dict_with_objects(
            data=validated_data,
            fields=fields_to_convert,
            serializer_classes=serializer_classes,
        )
        return super().update(instance, validated_data_replaced_final)

    def save(self, **kwargs):
        return super().save(**kwargs)


class OrganizationUserBaseSerializer(ModelSerializer):
    class Meta:
        model = OrganizationHasUserWithRole
        fields = ("role",)

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def replace_object_uuid_with_object(
        self,
        data,
        object_uuid,
        object_uuid_field_name,
        object_field_name,
        model_class,
    ):
        if object_uuid is not None:
            try:
                object_ = get_object_or_404(klass=model_class, uuid=object_uuid)
                data[object_field_name] = object_
                return data
            except Http404:
                raise ValidationError(
                    {
                        object_uuid_field_name: f"No {model_class._meta.model_name} with the given uuid found."
                    }
                )

    def update(self, instance, validated_data):
        data_to_update = {
            "organization": instance.organization,
            "user_account": instance.user_account,
        }
        validated_data.update(data_to_update)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        data_to_update = {
            "organization": instance.organization.uuid,
            "user_account": instance.user_account.uuid,
        }
        representation.update(data_to_update)
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
            request: Request = self.context.get("request")
            authenticated_user_account: UserAccount = request.user
            validated_data["user_account"] = authenticated_user_account
            organization_uuid = validated_data.pop("organization_uuid", None)
            validated_data = self.replace_object_uuid_with_object(
                data=validated_data,
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
            request: Request = self.context.get("request")
            organization_uuid = request.parser_context.get("kwargs").get("org_uuid")
            organization: Organization = Organization.objects.get(
                uuid=organization_uuid
            )
            validated_data["organization"] = organization
            user_account_uuid = validated_data.pop("user_account_uuid", None)
            validated_data_replaced_final = self.replace_object_uuid_with_object(
                data=validated_data,
                object_uuid=user_account_uuid,
                object_uuid_field_name="user_account_uuid",
                object_field_name="user_account",
                model_class=UserAccount,
            )
            return super().create(validated_data_replaced_final)
        except IntegrityError:
            raise ValidationError(
                {
                    "user_account_uuid": "This user already exists in this organization. Update the role instead."
                }
            )
