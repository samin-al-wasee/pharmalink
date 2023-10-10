from django.test import TestCase
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.utils import timezone
from ..models import UserAccount
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


class AccountUserTests(TestCase):
    def setUp(self) -> None:
        self.user_model: UserAccount = get_user_model()
        self.superuser: UserAccount = self.user_model.objects.create_superuser(
            username=None, email="superuser@example.com", password="superuser_pass"
        )

    def test_user_model_is_correct(self):
        self.assertIsNot(self.user_model, AbstractBaseUser)
        self.assertIsNot(self.user_model, AbstractUser)
        self.assertIs(self.user_model, UserAccount)

    def test_superuser_create_success(self):
        self.assertIsInstance(self.superuser, self.user_model)
        self.assertTrue(self.superuser.is_superuser)
