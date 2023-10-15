from django.forms.models import model_to_dict
from django.test import TestCase

from ..models import Organization


class OrganizationTests(TestCase):
    def setUp(self) -> None:
        self.organization = Organization.objects.create(email="advdvavdavad")
        print(model_to_dict(self.organization))
        print(self.organization.uuid)

    def test_create_success(self):
        pass
