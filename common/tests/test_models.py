from django.test import TestCase

from ..models import Address


class AddressTests(TestCase):
    def setUp(self) -> None:
        self.address: Address = Address.objects.create(
            city="Dhaka", postal_code="1212", country="BD"
        )

    def test_create_success(self):
        self.assertEquals(self.address.unit_no, "")
        self.assertEquals(self.address.street_no, "")
        self.assertEquals(self.address.line_1, "")
        self.assertEquals(self.address.line_2, "")
        self.assertEquals(self.address.city, "Dhaka")
        self.assertEquals(self.address.region, "")
        self.assertEquals(self.address.postal_code, "1212")
        self.assertEquals(self.address.country, "BD")
