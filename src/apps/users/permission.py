from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.permissions import BasePermission


class StaffPermission(BasePermission):
    """
    Checking whether the user is an employee or hotel owner
    """
    message = _("User is not the owner or staff")

    def has_permission(self, request, view):

        try:
            return request.user.chief
        except ObjectDoesNotExist:
            pass

        try:
            return request.user.staff
        except ObjectDoesNotExist:
            pass

        return False
