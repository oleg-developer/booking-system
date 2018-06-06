from django.contrib import admin
from apps.users.models import Chief, Access, StaffAccess
from apps.users.models.staff import Staff
from apps.users.models import User

admin.site.register(User)
admin.site.register(Chief)
admin.site.register(Staff)

admin.site.register(Access)
admin.site.register(StaffAccess)

