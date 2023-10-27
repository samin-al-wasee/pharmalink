from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Organization


class OrganizationTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@example.com",
            password="test_user_pass",
        )
        self.organization = Organization.objects.create(
            name="Org 1", email="org1@example.com", owner=self.user
        )

    def test_create_success(self):
        self.assertIsInstance(self.organization, Organization)
        self.assertIs(self.organization.owner, self.user)
