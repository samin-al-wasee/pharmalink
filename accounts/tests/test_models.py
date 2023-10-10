from django.test import TestCase
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.utils import timezone
from ..models import UserAccount
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


class AccountUserTests(TestCase):
    def setUp(self) -> None:
        self.user_model: UserAccount = get_user_model()
        # self.test_user_account = self.user_model.objects.create(
        #     uuid=uuid4(),
        #     username="test_user_account",
        #     email="test_user_account@example.com",
        #     photo=None,
        #     password="test_user_acc_pass",
        #     date_of_birth="1999-01-17",
        #     height_cm=200,
        #     weight_kg=100,
        #     created_at=timezone.now(),
        #     last_login=timezone.now(),
        #     is_active=True,
        #     is_superuser=False,
        #     gender="M",
        #     blood_group="AB-",
        #     address_id=None,
        # )

    def test_user_model_is_correct(self):
        self.assertIsNot(self.user_model, AbstractBaseUser)
        self.assertIsNot(self.user_model, AbstractUser)
        self.assertIs(self.user_model, UserAccount)
        print("Test User Model Correct: PASSED")
