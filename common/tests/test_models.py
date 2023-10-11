from django.test import TestCase
from ..models import Address


class AddressTests(TestCase):
    def setUp(self) -> None:
        self.address: Address = Address.objects.create()

    def test_create_success(self):
        self.assertEquals(self.address.unit_no, "")
        self.assertEquals(self.address.country, "NZ")
