from rest_framework.serializers import CharField, ModelSerializer
from rest_framework.validators import ValidationError

from common.constants import MODEL_CHARFIELD_MAX_LENGTH, MODEL_CHARFIELD_MIN_LENGTH
from common.serializers import AddressSerializer
from common.utils import (
    replace_nested_dict_with_objects,
    remove_blank_or_null,
    exclude_fields_from_data,
)

from .models import UserAccount


class UserAccountSerializer(ModelSerializer):
    class Meta:
        model = UserAccount
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
        min_length=MODEL_CHARFIELD_MIN_LENGTH,
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
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
        fields_to_exclude = ("repeated_password",)
        validated_data_without_unnecessary_fields = exclude_fields_from_data(
            data=validated_data, fields=fields_to_exclude
        )
        fields_to_convert = ("address",)
        serializer_classes = (AddressSerializer,)
        validated_data_replaced_final = replace_nested_dict_with_objects(
            data=validated_data_without_unnecessary_fields,
            fields=fields_to_convert,
            serializer_classes=serializer_classes,
        )
        return super().create(validated_data_replaced_final)
