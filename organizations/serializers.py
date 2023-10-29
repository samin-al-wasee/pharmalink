from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from rest_framework.validators import ValidationError

from common.constants import ACTIVE
from common.serializers import AddressSerializer
from common.utils import create_nested_objects, remove_blank_or_null

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
    owner = SlugRelatedField(slug_field="uuid", read_only=True)

    def create(self, validated_data):  # Needs REFACTOR
        request: Request = self.context.get("request")
        additional_data = {"owner": request.user}
        validated_data.update(additional_data)
        nested_fields = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data = create_nested_objects(
            data=validated_data,
            fields=nested_fields,
            serializer_classes=serializer_classes,
        )
        return super().create(validated_data)

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
        model = OrganizationHasUserWithRole
        fields = (
            "organization",
            "user",
            "role",
        )
        read_only_fields = (
            "organization",
            "user",
        )

    organization = SlugRelatedField(slug_field="uuid", read_only=True)
    user = SlugRelatedField(slug_field="uuid", read_only=True)

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

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

    def create(self, validated_data):
        request = self.context.get("request")
        authenticated_user = request.user
        additional_data = {"user": authenticated_user}
        validated_data.update(additional_data)
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError({"user": "The user already exists in organization."})
