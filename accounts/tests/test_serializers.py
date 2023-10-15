from django.test import TestCase

from ..serializers import AddressCreateSerializer, UserAccountCreateSerializer


class UserAccountCreateSerializerTests(TestCase):
    def setUp(self) -> None:
        self.data = {
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

        self.account_create_serializer = UserAccountCreateSerializer(data=self.data)

        print(self.account_create_serializer.is_valid())
        print(self.account_create_serializer.validated_data)
        print(self.account_create_serializer.save())

    def test_serializer_data(self):
        pass
