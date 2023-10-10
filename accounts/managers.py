from typing import Any
from django.contrib.auth import get_user_model
from common.models import Address
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password


class UserAccountManager(UserManager):
    def create_superuser(
        self, email: str | None, password: str | None, **extra_fields: Any
    ) -> Any:
        UserModel = get_user_model()
        superuser = UserModel(
            username="superuser",
            email=email,
            password=make_password(password),
            is_superuser=True,
        )
        superuser.save()
        return superuser
