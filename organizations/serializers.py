from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from rest_framework.validators import ValidationError

from common.constants import ACTIVE, OWNER
from common.serializers import AddressSerializer
from common.utils import (create_nested_objects, extract_fields,
                          remove_blank_or_null)

from .models import Organization, OrganizationHasUser


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
            "created_at",
        )

    address = AddressSerializer(allow_null=True, required=False)

    def is_valid(self, *, raise_exception=False):
        to_exclude = ("user",)
        self.initial_data, extracted_data = extract_fields(
            data=self.initial_data, fields=to_exclude
        )
        result = super().is_valid(raise_exception=raise_exception)
        self.validated_data.update(extracted_data)
        return result

    def create(self, validated_data):  # Needs REFACTOR
        user = validated_data.pop("user", None)
        if not user:
            request = self.context.get("request")
            authenticated_user = request.user
            additional_data = {"user": authenticated_user, "default": False}
        else:
            additional_data = {"user": user, "default": True}
        nested_fields = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data = create_nested_objects(
            data=validated_data,
            fields=nested_fields,
            serializer_classes=serializer_classes,
        )
        instance = super().create(validated_data)
        connector_data = {"organization": instance, "role": OWNER}
        connector_data.update(additional_data)
        connector_data = {"organization_user_role": connector_data}
        nested_fields = ("organization_user_role",)
        serializer_classes = (OrganizationUserSerializerForUser,)
        create_nested_objects(
            data=connector_data,
            nested_fields=nested_fields,
            serializer_classes=serializer_classes,
        )
        return instance

    def update(self, instance, validated_data):  # Needs REFACTOR
        nested_fields = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data = create_nested_objects(
            data=validated_data,
            fields=nested_fields,
            serializer_classes=serializer_classes,
        )
        return super().update(instance, validated_data)


class OrganizationUserBaseSerializer(ModelSerializer):
    class Meta:
        model = OrganizationHasUser
        fields = (
            "organization",
            "user",
            "role",
            "default",
        )
        read_only_fields = (
            "organization",
            "user",
        )

    organization = SlugRelatedField(slug_field="uuid", read_only=True)
    user = SlugRelatedField(slug_field="uuid", read_only=True)

    def update(self, instance, validated_data):
        additional_data = {
            "organization": instance.organization,
            "user": self.instance.user,
        }
        validated_data.update(additional_data)
        return super().update(instance, validated_data)


class OrganizationUserSerializerForOwner(OrganizationUserBaseSerializer):
    class Meta(OrganizationUserBaseSerializer.Meta):
        read_only_fields = ("organization",)

    user = SlugRelatedField(
        queryset=get_user_model().objects.filter(), slug_field="uuid"
    )

    def create(self, validated_data):
        request = self.context.get("request")
        organization_uuid = request.parser_context.get("kwargs").get(
            "organization_uuid"
        )
        organization = Organization.objects.get(uuid=organization_uuid)
        additional_data = {"organization": organization}
        validated_data.update(additional_data)
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError(
                {"organization": "The user already exists in organization."}
            )


class OrganizationUserSerializerForUser(OrganizationUserBaseSerializer):
    class Meta(OrganizationUserBaseSerializer.Meta):
        read_only_fields = ("user",)

    organization = SlugRelatedField(
        queryset=Organization.objects.filter(status=ACTIVE), slug_field="uuid"
    )

    def is_valid(self, *, raise_exception=False):
        to_exclude = ("user",)
        self.initial_data, extracted_data = extract_fields(
            data=self.initial_data, fields=to_exclude
        )
        result = super().is_valid(raise_exception=raise_exception)
        self.validated_data.update(extracted_data)
        return result

    def create(self, validated_data):
        user = validated_data.get("user", None)
        if not user:
            request = self.context.get("request")
            authenticated_user = request.user
            additional_data = {"user": authenticated_user}
        else:
            additional_data = {"default": True}
        validated_data.update(additional_data)

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError({"user": "The user already exists in organization."})
