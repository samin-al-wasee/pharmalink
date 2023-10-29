from .permissions import HasPrescriptionRole
from common.constants import DOCTOR, PATIENT


class PrescriptionDoctorPermissionMixin:
    def get_permissions(self):
        permissions = super().get_permissions()
        prescription = self.kwarg_objects.get("prescription_uuid")
        authenticated_user = self.request.user
        permissions.append(
            HasPrescriptionRole(
                prescription=prescription, user=authenticated_user, role=DOCTOR
            ),
        )
        return permissions


class PrescriptionPatientPermissionMixin:
    def get_permissions(self):
        permissions = super().get_permissions()
        prescription = self.kwarg_objects.get("prescription_uuid")
        authenticated_user = self.request.user
        permissions.append(
            HasPrescriptionRole(
                prescription=prescription, user=authenticated_user, role=PATIENT
            ),
        )
        return permissions
