"""
Generic model-related constants
"""
MIN_LENGTH = 8
MAX_LENGTH = 128

"""
Constants and choices for User model
"""
MALE = "Male"
FEMALE = "Female"
OTHER = "Other"
A_POSITIVE = "A+"
A_NEGATIVE = "A-"
B_POSITIVE = "B+"
B_NEGATIVE = "B-"
AB_POSITIVE = "AB+"
AB_NEGATIVE = "AB-"
O_POSITIVE = "O+"
O_NEGATIVE = "O-"
UNKNOWN = "U"
NOT_SET = -1

GENDERS = [
    (MALE, "Male"),
    (FEMALE, "Female"),
    (OTHER, "Other"),
    (UNKNOWN, "Unknown"),
]

BLOOD_GROUPS = [
    (A_POSITIVE, "A Positive"),
    (A_NEGATIVE, "A Negative"),
    (B_POSITIVE, "B Positive"),
    (B_NEGATIVE, "B Negative"),
    (AB_POSITIVE, "AB Positive"),
    (AB_NEGATIVE, "AB Negative"),
    (O_POSITIVE, "O Positive"),
    (O_NEGATIVE, "O Negative"),
    (UNKNOWN, "Unknown"),
]

"""
Constants and choices for Organization model
"""
ACTIVE = "Active"
INACTIVE = "Inactive"
DISBANDED = "Disbanded"
STATUS_UNKNOWN = "Unknown"

ORGANIZATION_STATUSES = [
    (ACTIVE, "This organization is currently active."),
    (INACTIVE, "This organization is currently inactive."),
    (DISBANDED, "This organization is no longer functioning"),
    (STATUS_UNKNOWN, "No information about this organization's status."),
]

"""
Constants and choices for OrganizationHasUserWithRole model
"""

STAFF = "Staff"
DOCTOR = "Doctor"
PATIENT = "Patient"
OWNER = "Owner"

USER_ROLES = [
    (STAFF, "Is a staff."),
    (DOCTOR, "Is a registered doctor."),
    (PATIENT, "Is a patient."),
    (OWNER, "Is the owner."),
]

"""
Constants and choices for MedicineGeneric, MedicineBrand, MedicineBrandHasDosageWithInfo models
"""

TABLET = "Tablet"
CAPSULE = "Capsule"
OINTMENT = "Ointment"
INJECTION = "Injection"

DOSAGE_FORMS = [
    (TABLET, "Tablet"),
    (CAPSULE, "Capsule"),
    (OINTMENT, "Ointment"),
    (INJECTION, "Injection"),
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
    (ONE, "1 Star"),
    (TWO, "2 Stars"),
    (THREE, "3 Stars"),
    (FOUR, "4 Stars"),
    (FIVE, "5 Stars"),
]
