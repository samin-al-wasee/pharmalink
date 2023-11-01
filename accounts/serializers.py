from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, ModelSerializer, Serializer
from rest_framework.validators import ValidationError

from common.constants import MAX_LENGTH, MIN_LENGTH
from common.serializers import AddressSerializer
from common.utils import create_nested_objects, extract_fields, remove_blank_or_null
from organizations.serializers import (
    OrganizationUserSerializerForUser,
    OrganizationSerializer,
)


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "uuid",
            "username",
            "email",
            "password",
            "repeated_password",
            "name",
            "photo",
            "height_cm",
            "weight_kg",
            "blood_group",
            "gender",
            "date_of_birth",
            "address",
            "created_at",
            "last_login",
            "is_superuser",
        )
        read_only_fields = ("last_login", "is_superuser")
        extra_kwargs = {"password": {"write_only": True}}

    repeated_password = CharField(
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
        write_only=True,
    )
    address = AddressSerializer(allow_null=True, required=False)

    def validate(self, attrs):
        password = attrs.get("password")
        repeated_password = attrs.get("repeated_password")

        if password != repeated_password:
            raise ValidationError(
                {
                    "password": "Passwords do not match.",
                    "repeated_password": "Passwords do not match.",
                }
            )

        return attrs

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):  # Needs REFACTOR
        """
        Following steps are performed before calling the actual "create()" method to deserialize given data:

        - Repeated password field is removed
        - Checks if any data present for the address field
        - If present raise appropriate validation errors
        - Otherwise create a new address object and save
        - Finally proceed to create the actual user object
        """
        to_exclude = ("repeated_password",)
        validated_data = extract_fields(data=validated_data, fields=to_exclude)[0]
        to_convert = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data = create_nested_objects(
            data=validated_data,
            fields=to_convert,
            serializer_classes=serializer_classes,
        )
        return super().create(validated_data)


class RegistrationSerializer(Serializer):
    user = UserSerializer()
    join = OrganizationUserSerializerForUser()
    create = OrganizationSerializer()

    def validate(self, attrs):
        join_data = attrs.get("join", {})
        create_data = attrs.get("create", {})
        if join_data and create_data:
            raise ValidationError(
                {
                    "join": "Join and create not possible together.",
                    "create": "Join and create not possible together.",
                }
            )
        return super().validate(attrs)
    
    def create(self, validated_data):
        
        return super().create(validated_data)
