from django.test import TestCase

from ..serializers import OrganizationSerializer


class OrganizationSerializerTests(TestCase):
    def setUp(self) -> None:
        self.data = {
            "name": "Organization 6",
            "email": "org6@example.com",
            "information": "",
            "status": None,
            "address": {
                "unit_no": "6A",
                "street_no": "6",
                "line_1": "Line 1",
                "line_2": "Line 2",
                "city": "Dhaka",
                "region": "",
                "postal_code": "1211",
                "country": "BD",
            },
        }

    def test_is_valid(self):
        org_ser = OrganizationSerializer(data=self.data)
        self.assertTrue(org_ser.is_valid())
