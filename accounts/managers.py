from typing import Any
from django.contrib.auth import get_user_model
from common.models import Address
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password


class UserAccountManager(UserManager):
    def create_user(
        self,
        username: str,
        email: str | None = ...,
        password: str | None = ...,
        **extra_fields: Any
    ) -> Any:
        print("Hello, I am create_user()!")
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

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
        superuser.save(using=self._db)
        return superuser

    def create(self, **kwargs: Any) -> Any:
        return super().create(**kwargs)
