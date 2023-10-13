"""
Generic model-related constants
"""
MODEL_CHARFIELD_MIN_LENGTH = 8
MODEL_CHARFIELD_MAX_LENGTH = 128

"""
Constants and choices for the UserAccount model
"""
MALE = "M"
FEMALE = "F"
OTHER = "O"
A_POSITIVE = "A+"
A_NEGATIVE = "A-"
B_POSITIVE = "B+"
B_NEGATIVE = "B-"
AB_POSITIVE = "AB+"
AB_NEGATIVE = "AB-"
O_POSITIVE = "O+"
O_NEGATIVE = "O-"
UNKNOWN = "U"

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
ORGANIZATION_IS_ACTIVE = "A"
ORGANIZATION_IS_INACTIVE = "I"
ORGANIZATION_STATUS_UNKNOWN = "U"

ORGANIZATION_STATUS = [
    (ORGANIZATION_IS_ACTIVE, "This organization is currently active."),
    (ORGANIZATION_IS_INACTIVE, "This organization is currently inactive."),
    (ORGANIZATION_STATUS_UNKNOWN, "No information about this organization's status."),
]
