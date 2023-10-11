from django.contrib import admin
from .models import UserAccount
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.


@admin.register(UserAccount)
class UserAccountAdmin(UserAdmin):
    fieldsets = (
        (_("Credentials"), {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "username",
                    "name",
                    "photo",
                    "height_cm",
                    "weight_kg",
                    "blood_group",
                    "gender",
                    "address",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("date_of_birth",)}),
    )
    add_fieldsets = (
        (
            "Credentials",
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "email", "is_superuser", "created_at")
    list_filter = ("is_superuser", "blood_group", "gender", "groups")
