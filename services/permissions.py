from rest_framework.permissions import BasePermission

from common.constants import DOCTOR, PATIENT
from organizations.models import Organization, OrganizationHasUserWithRole
from .models import Prescription


class HasRole(BasePermission):
    def __init__(self, organization, user, role) -> None:
        self.organization = organization
        self.user = user
        self.role = role
        super().__init__()

    def has_permission(self, request, view):
        relation = OrganizationHasUserWithRole.objects.get(
            organization_id=self.organization.id, user_id=self.user.id
        )
        return relation.role == self.role

    def has_object_permission(self, request, view, obj):
        return (
            self.has_permission(request=request, view=view)
            if not isinstance(obj, Organization)
            else OrganizationHasUserWithRole.objects.get(
                organization_id=self.organization.id, user_id=self.user.id
            ).role
            == self.role
        )


class HasPrescriptionRole(BasePermission):
    def __init__(self, prescription, user, role) -> None:
        self.prescription = prescription
        self.user = user
        self.role = role
        super().__init__()

    def has_permission(self, request, view):
        if self.role == DOCTOR:
            return self.prescription.doctor.id == self.user.id
        if self.role == PATIENT:
            return self.prescription.patient.id == self.user.id

    def has_object_permission(self, request, view, obj):
        return True


class HasPrescriptionAccess(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        authenticated_user = request.user
        return (
            obj.doctor.id == authenticated_user.id
            or obj.patient.id == authenticated_user.id
        )


class IsDone(BasePermission):
    def __init__(self, prescription=None) -> None:
        self.prescription = prescription
        super().__init__()

    def has_permission(self, request, view):
        return self.prescription.done if self.prescription else True

    def has_object_permission(self, request, view, obj):
        return (
            self.has_permission()
            if not isinstance(obj, Prescription)
            else obj.prescription.done
        )
