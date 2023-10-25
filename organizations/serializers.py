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

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):  # Needs REFACTOR
        request: Request = self.context.get("request")
        add_data = {"owner": request.user}
        validated_data.update(add_data)
        nested_fields = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data_final = create_nested_objects(
            data=validated_data,
            fields=nested_fields,
            serializer_classes=serializer_classes,
        )
        return super().create(validated_data_final)

    def update(self, instance, validated_data):  # Needs REFACTOR
        nested_fields = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data_final = create_nested_objects(
            data=validated_data,
            fields=nested_fields,
            serializer_classes=serializer_classes,
        )
        return super().update(instance, validated_data_final)


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
        add_data = {
            "organization": instance.organization,
            "user": self.instance.user,
        }
        validated_data.update(add_data)
        return super().update(instance, validated_data)


class OrganizationUserSerializerForOwner(OrganizationUserBaseSerializer):
    class Meta(OrganizationUserBaseSerializer.Meta):
        read_only_fields = ("organization",)

    user = SlugRelatedField(
        queryset=get_user_model().objects.filter(), slug_field="uuid"
    )

    def create(self, validated_data):
        request = self.context.get("request")
        org_uuid = request.parser_context.get("kwargs").get("org_uuid")
        organization = Organization.objects.get(uuid=org_uuid)
        add_data = {"organization": organization}
        validated_data.update(add_data)
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
        auth_user = request.user
        add_data = {"user": auth_user}
        validated_data.update(add_data)
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError({"user": "The user already exists in organization."})
