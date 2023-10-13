MODEL_CHARFIELD_MIN_LENGTH = 8
MODEL_CHARFIELD_MAX_LENGTH = 128
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
