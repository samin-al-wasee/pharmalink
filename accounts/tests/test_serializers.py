from django.test import TestCase

from ..serializers import UserSerializer


class UserAccountCreateSerializerTests(TestCase):
    def setUp(self) -> None:
        self.invalid_data = {
            "username": "saminalwasee",
            "email": "samin@example.com",
            "password": "saminsaminsa",
            "repeated_password": "saminsaminsa",
            "address": {
                "unit_no": "",
                "street_no": "",
                "line_1": "",
                "line_2": "",
                "city": "",
                "region": "",
                "postal_code": "",
                "country": "",
            },
        }
        self.valid_data = {
            "username": "saminalwasee",
            "name": "Samin AL Wasee",
            "email": "samin@example.com",
            "password": "saminsaminsa",
            "repeated_password": "saminsaminsa",
            "address": {
                "unit_no": "",
                "street_no": "",
                "line_1": "",
                "line_2": "",
                "city": "city",
                "region": "",
                "postal_code": "1111",
                "country": "BD",
            },
        }

        self.invalid_account_serializer = UserSerializer(data=self.invalid_data)
        self.valid_account_serializer = UserSerializer(data=self.valid_data)

    def test_serializer_data(self):
        self.assertFalse(self.invalid_account_serializer.is_valid())
        self.assertTrue(self.valid_account_serializer.is_valid(raise_exception=True))
