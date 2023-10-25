from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from medicines.models import MedicineBrand, MedicineGeneric
from organizations.models import Organization

from ..models import Prescription
from ..serializers import (PrescriptionHasMedicineSerializer,
                           PrescriptionSerializer)


class PrescriptionMedicineSeralizerTests(TestCase):
    def setUp(self) -> None:
        self.owner = get_user_model().objects.create(
            **{
                "username": "testowner",
                "email": "testowner@example.com",
                "password": "testownerpass",
                "name": "Test Owner",
                "height_cm": 180,
                "weight_kg": 60,
                "blood_group": "A+",
                "gender": "M",
                "date_of_birth": "2023-10-24",
            }
        )
        self.doctor = get_user_model().objects.create(
            **{
                "username": "testdoctor",
                "email": "testdoctor@example.com",
                "password": "testdoctorpass",
                "name": "Test Doctor",
                "height_cm": 180,
                "weight_kg": 60,
                "blood_group": "A+",
                "gender": "M",
                "date_of_birth": "2023-10-24",
            }
        )
        self.patient = get_user_model().objects.create(
            **{
                "username": "testpatient",
                "email": "testpatient@example.com",
                "password": "testpatientpass",
                "name": "Test Patient",
                "height_cm": 180,
                "weight_kg": 60,
                "blood_group": "A+",
                "gender": "M",
                "date_of_birth": "2023-10-24",
            }
        )
        self.org = Organization.objects.create(
            **{
                "name": "Test Org",
                "email": "testorg@example.com",
                "information": "string",
                "status": "A",
                "owner": self.owner,
            }
        )
        self.org2 = Organization.objects.create(
            **{
                "name": "Test Org 2",
                "email": "testorg2@example.com",
                "information": "string",
                "status": "A",
                "owner": self.owner,
            }
        )
        self.prescription = Prescription.objects.create(
            **{
                "organization": self.org,
                "doctor": self.doctor,
                "patient": self.patient,
            }
        )
        self.generic = MedicineGeneric.objects.create(
            **{
                "name": "Test Generic",
            }
        )
        self.brand = MedicineBrand.objects.create(
            **{
                "name": "Test Brand",
                "manufacturer": self.org2,
                "generic": self.generic,
            }
        )
        self.request_factory = APIRequestFactory()
        self.httprequest = self.request_factory.get("/prescriptions/")
        self.parser_context = {"kwargs": {"org_uuid": self.org.uuid}}
        self.request = Request(self.httprequest, parser_context=self.parser_context)
        self.request.user = self.doctor

    def test_create(self):
        med_data = {
            "prescription": self.prescription.id,
            "brand": "test-brand",
            "instructions": "Instructions",
        }
        data = {
            "patient": self.patient.uuid,
            "prescribed_medicines": med_data,
            "done": False,
        }

        serializer = PrescriptionSerializer(data=data)
        serializer.context["request"] = self.request
        self.assertRaises(NotFound, serializer.is_valid)
