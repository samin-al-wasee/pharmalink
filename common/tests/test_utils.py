from django.test import TestCase
from ..utils import (
    exclude_fields_from_data,
    replace_nested_dict_with_objects,
    _get_nested_object_deserialized,
)
from ..serializers import AddressSerializer
from ..models import Address


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
        data = exclude_fields_from_data(data=self.data, fields=fields)
        try:
            repeated_password = data["repeated_password"]
        except KeyError:
            self.assertTrue(True)

    def test_replace_nested_dict_with_objects(self):
        fields = ("address",)
        serializer_classes = (AddressSerializer,)
        data = replace_nested_dict_with_objects(
            data=self.data, fields=fields, serializer_classes=serializer_classes
        )
        self.assertIsInstance(data.get("address"), list)
        self.assertIsInstance(data.get("address")[0], Address)

    def test__get_nested_object_deserialized(self):
        pass
