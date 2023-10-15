from uuid import UUID, uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.test import TestCase
from django.utils import timezone

from ..models import UserAccount


class AccountUserTests(TestCase):
    def setUp(self) -> None:
        self.user_model: UserAccount = get_user_model()
        self.superuser: UserAccount = self.user_model.objects.create_superuser(
            username=None, email="superuser@example.com", password="superuser_pass"
        )
        self.user: UserAccount = self.user_model.objects.create_user(
            username="test_user",
            email="test_user@example.com",
            password="test_user_pass",
        )

    def test_user_model_correct(self):
        self.assertIsNot(self.user_model, AbstractBaseUser)
        self.assertIsNot(self.user_model, AbstractUser)
        self.assertIs(self.user_model, UserAccount)

    def test_create_superuser_success(self):
        self.assertIsInstance(self.superuser, self.user_model)
        self.assertTrue(self.superuser.is_superuser)
        self.assertIsInstance(self.superuser.uuid, UUID)
        self.assertEquals(self.superuser.name, "")
        self.assertIsNone(self.superuser.address)
        self.assertEquals(self.superuser.username, "superuser")
        self.assertEquals(self.superuser.email, "superuser@example.com")
        self.assertIsNone(self.superuser.date_of_birth)
        self.assertEquals(self.superuser.height_cm, -1)
        self.assertEquals(self.superuser.weight_kg, -1)
        self.assertEquals(self.superuser.blood_group, "U")
        self.assertEquals(self.superuser.gender, "U")

    def test_create_user_success(self):
        self.assertIsInstance(self.user, self.user_model)
        # self.assertEquals(self.user.password, "test_user_pass")

    def test_create_success(self):
        self.assertEquals(self.user.blood_group, "U")
        self.assertEquals(self.user.gender, "U")
        self.assertEquals(self.user.height_cm, -1)
        self.assertEquals(self.user.weight_kg, -1)
        self.assertEquals(self.user.photo, None)
