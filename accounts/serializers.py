from django.contrib.auth.validators import ASCIIUsernameValidator
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    DateField,
    EmailField,
    ImageField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    Serializer,
)
from rest_framework.validators import UniqueValidator, ValidationError

from common.constants import *
from common.models import Address
from .models import UserAccount


class UserAccountCreateSerializer(ModelSerializer):
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

    repeated_password = CharField(
        min_length=MODEL_CHARFIELD_MIN_LENGTH,
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True,
    )
    address = PrimaryKeyRelatedField(
        queryset=Address.objects.all(), allow_null=True, required=False, default=None
    )

    # Following two methods need fixing. Validation logics related to two or more fields should be in the validate() method.

    def validate_password(self, value):
        if value != self.initial_data["repeated_password"]:
            raise ValidationError("Passwords do not match.")
        return value

    def validate_repeated_password(self, value):
        if value != self.initial_data["password"]:
            raise ValidationError("Passwords do not match.")
        return value

    def save(self, **kwargs):
        self.validated_data.pop("repeated_password")
        return super().save(**kwargs)
