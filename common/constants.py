"""
Generic model-related constants
"""
MIN_LENGTH = 8
MAX_LENGTH = 128

"""
Constants and choices for User model
"""
MALE = "male"
FEMALE = "female"
OTHER = "other"
A_POSITIVE = "a+"
A_NEGATIVE = "a-"
B_POSITIVE = "b+"
B_NEGATIVE = "b-"
AB_POSITIVE = "ab+"
AB_NEGATIVE = "ab-"
O_POSITIVE = "o+"
O_NEGATIVE = "o-"
UNKNOWN = "unknown"
NOT_SET = -1

GENDERS = [
    (MALE, "Male"),
    (FEMALE, "Female"),
    (OTHER, "Other"),
    (UNKNOWN, "Unknown"),
]

BLOOD_GROUPS = [
    (A_POSITIVE, "A+"),
    (A_NEGATIVE, "A-"),
    (B_POSITIVE, "B-"),
    (B_NEGATIVE, "B-"),
    (AB_POSITIVE, "AB+"),
    (AB_NEGATIVE, "AB-"),
    (O_POSITIVE, "O+"),
    (O_NEGATIVE, "O-"),
    (UNKNOWN, "Unknown"),
]

"""
Constants and choices for Organization model
"""
ACTIVE = "active"
INACTIVE = "inactive"
DISBANDED = "disbanded"

ORGANIZATION_STATUSES = [
    (ACTIVE, "Currently active."),
    (INACTIVE, "Currently inactive."),
    (DISBANDED, "Has disbanded."),
    (UNKNOWN, "No information."),
]

"""
Constants and choices for OrganizationHasUserWithRole model
"""

STAFF = "staff"
DOCTOR = "doctor"
PATIENT = "patient"

USER_ROLES = [
    (STAFF, "Is a staff."),
    (DOCTOR, "Is a registered doctor."),
    (PATIENT, "Is a patient."),
    (OTHER, "Is a generic user."),
]

"""
Constants and choices for MedicineGeneric, MedicineBrand, MedicineBrandHasDosageWithInfo models
"""

TABLET = "tablet"
CAPSULE = "capsule"
OINTMENT = "ointment"
INJECTION = "injection"

DOSAGE_FORMS = [
    (TABLET, "Tablet."),
    (CAPSULE, "Capsule."),
    (OINTMENT, "Ointment."),
    (INJECTION, "Injection."),
]


"""
Constants and choices for Feedback model
"""

ZERO = 0
ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5

RATINGS = [
    (ONE, "1 Star."),
    (TWO, "2 Stars."),
    (THREE, "3 Stars."),
    (FOUR, "4 Stars."),
    (FIVE, "5 Stars."),
]
