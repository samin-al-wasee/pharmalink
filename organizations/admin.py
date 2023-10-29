from django.contrib import admin

from .models import Organization, OrganizationHasUser

# Register your models here.
admin.site.register(model_or_iterable=(Organization, OrganizationHasUser))
