from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, UUIDField
from rest_framework.validators import ValidationError

from accounts.serializers import UserSerializer
from common.serializers import AddressSerializer
from common.utils import remove_blank_or_null, create_nested_objects

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
            "owner",
            "created_at",
        )
        read_only_fields = ("owner",)

    address = AddressSerializer(allow_null=True, required=False)
    owner = UserSerializer(read_only=True)

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):  # Needs REFACTOR
        request: Request = self.context.get("request")
        auth_user: get_user_model() = request.user
        validated_data["owner"] = auth_user
        to_convert = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data_final = create_nested_objects(
            data=validated_data,
            fields=to_convert,
            serializer_classes=serializer_classes,
        )
        return super().create(validated_data_final)

    def update(self, instance, validated_data):  # Needs REFACTOR
        to_convert = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data_final = create_nested_objects(
            data=validated_data,
            fields=to_convert,
            serializer_classes=serializer_classes,
        )
        return super().update(instance, validated_data_final)

    def save(self, **kwargs):
        return super().save(**kwargs)


class OrganizationUserBaseSerializer(ModelSerializer):
    class Meta:
        model = OrganizationHasUserWithRole
        fields = ("role",)

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def replace_uuid_with_object(
        self,
        data,
        uuid,
        uuid_field,
        object_field,
        model_class,
    ):
        if uuid is not None:
            try:
                object_ = get_object_or_404(klass=model_class, uuid=uuid)
                data[object_field] = object_
                return data
            except Http404:
                raise ValidationError(
                    {
                        uuid_field: f"No {model_class._meta.model_name} with the given uuid found."
                    }
                )

    def update(self, instance, validated_data):
        new_data = {
            "organization": instance.organization,
            "user": instance.user,
        }
        validated_data.update(new_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        new_data = {
            "organization": instance.organization.uuid,
            "user": instance.user.uuid,
        }
        representation.update(new_data)
        return representation


class OrganizationUserSerializer(OrganizationUserBaseSerializer):
    class Meta(OrganizationUserBaseSerializer.Meta):
        fields = (
            "organization",
            "user",
            "user_uuid",
        ) + OrganizationUserBaseSerializer.Meta.fields
        read_only_fields = ("organization", "user")

    user_uuid = UUIDField(write_only=True)


class OrganizationUserSerializerForUser(OrganizationUserBaseSerializer):
    class Meta(OrganizationUserBaseSerializer.Meta):
        fields = (
            "organization",
            "org_uuid",
            "user",
        ) + OrganizationUserBaseSerializer.Meta.fields
        read_only_fields = ("organization", "user")

    org_uuid = UUIDField(write_only=True)

    def create(self, validated_data):
        try:
            request: Request = self.context.get("request")
            auth_user: get_user_model() = request.user
            validated_data["user"] = auth_user
            org_uuid = validated_data.pop("org_uuid", None)
            validated_data = self.replace_uuid_with_object(
                data=validated_data,
                uuid=org_uuid,
                uuid_field="org_uuid",
                object_field="organization",
                model_class=Organization,
            )
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError(
                {
                    "org_uuid": "You already exist in this organization. Contact owner to update the role instead."
                }
            )


class OrganizationUserSeralizerForOwner(OrganizationUserBaseSerializer):
    class Meta(OrganizationUserBaseSerializer.Meta):
        fields = (
            "organization",
            "user",
            "user_uuid",
        ) + OrganizationUserBaseSerializer.Meta.fields
        read_only_fields = ("organization", "user")

    user_uuid = UUIDField(write_only=True)

    def create(self, validated_data):
        try:
            request: Request = self.context.get("request")
            org_uuid = request.parser_context.get("kwargs").get("org_uuid")
            organization: Organization = Organization.objects.get(uuid=org_uuid)
            validated_data["organization"] = organization
            user_uuid = validated_data.pop("user_uuid", None)
            validated_data_final = self.replace_uuid_with_object(
                data=validated_data,
                uuid=user_uuid,
                uuid_field="user_uuid",
                object_field="user",
                model_class=get_user_model(),
            )
            return super().create(validated_data_final)
        except IntegrityError:
            raise ValidationError(
                {
                    "user_uuid": "This user already exists in this organization. Update the role instead."
                }
            )
