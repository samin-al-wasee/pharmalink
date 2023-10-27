from django.test import TestCase

from ..models import Address
from ..serializers import AddressSerializer
from ..utils import create_nested_objects, extract_fields


class UtilTests(TestCase):
    def setUp(self) -> None:
        self.data = {
            "username": "username",
            "email": "user@example.com",
            "password": "password",
            "repeated_password": "password",
            "name": "Test User",
            "photo": None,
            "height_cm": 180,
            "weight_kg": 60,
            "blood_group": "AB-",
            "gender": "M",
            "date_of_birth": "1999-01-17",
            "address": [
                {
                    "unit_no": "1A",
                    "street_no": "1",
                    "line_1": "Line 1",
                    "line_2": "Line 2",
                    "city": "City",
                    "region": "Region",
                    "postal_code": "4216",
                    "country": "BD",
                },
                {
                    "unit_no": "1A",
                    "street_no": "11",
                    "line_1": "Line 1",
                    "line_2": "Line 2",
                    "city": "City",
                    "region": "Region",
                    "postal_code": "4226",
                    "country": "BD",
                },
            ],
        }

    def test_exclude_fields_from_data(self):
        fields = ("repeated_password",)
        data = extract_fields(data=self.data, fields=fields)[0]
        repeated_password = data.get("repeated_password")
        self.assertIsNone(repeated_password)

    def test_replace_nested_dict_with_objects(self):
        fields = ("address",)
        serializer_classes = (AddressSerializer,)
        data = create_nested_objects(
            data=self.data, fields=fields, serializer_classes=serializer_classes
        )
        self.assertIsInstance(data.get("address"), list)
        self.assertIsInstance(data.get("address")[0], Address)

    def test__get_nested_object_deserialized(self):
        pass
