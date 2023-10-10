from typing import Any
from django.contrib.auth import get_user_model
from common.models import Address
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password


class UserAccountManager(UserManager):
    def create_superuser(
        self,
        username: str | None,
        email: str | None,
        password: str | None,
        **extra_fields: Any
    ) -> Any:
        UserModel = get_user_model()
        superuser_address: Address = Address.objects.create(
            unit_no="1A",
            street_no="1",
            line_1="Superuser Street",
            line_2="Superuser Avenue",
            city="Fictional",
            region="Fictional",
            country="BD",
        )
        superuser = UserModel(
            username="superuser",
            email=email,
            password=make_password(password),
            name="Super User",
            date_of_birth="1999-01-17",
            height_cm=175,
            weight_kg=65,
            blood_group="AB-",
            gender="M",
            address=superuser_address,
            is_superuser=True,
        )
        superuser.save()
        return superuser
