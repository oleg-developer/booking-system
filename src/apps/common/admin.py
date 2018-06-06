from django.contrib import admin

from apps.common.models import Country
from apps.common.models import Phone


admin.site.register(Country)
admin.site.register(Phone)

