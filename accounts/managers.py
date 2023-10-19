from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class UserManager_(UserManager):
    def create_user(
        self,
        username: str,
        email: str | None = ...,
        password: str | None = ...,
        **extra_fields: Any
    ) -> Any:
        """
        Used for creating new user. This method will be called from within "create()" method.
        By default this method ensures that the newly created user through this method is not a superuser.
        """

        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self, email: str | None, password: str | None, **extra_fields: Any
    ) -> Any:
        """
        Calling this method is the only way to create a superuser for the admin panel.
        Only callable through the management command "createsuperuser" by default.
        """

        user_model = get_user_model()
        superuser = user_model(
            username="superuser",
            email=email,
            password=make_password(password),
            is_superuser=True,
        )
        superuser.save(using=self._db)
        return superuser

    def create(self, **kwargs: Any) -> Any:
        """
        This is the method called by the serializer by default when creating a new user instance.
        By default does not provide password hashing hence "create_user()" method is called.
        This method receives the entire user data and passes appropriate values for the parameters of "create_user()" method.
        """
        username = kwargs.pop("username")
        email = kwargs.pop("email")
        password = kwargs.pop("password")
        return self.create_user(
            username=username, email=email, password=password, **kwargs
        )
