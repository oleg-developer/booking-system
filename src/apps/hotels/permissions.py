from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import BasePermission


class HotelRequired(BasePermission):
    """
    Check if the user has contact with the hotel
    """
    message = _("For the user is not defined hotel")

    def has_permission(self, request, view):
        return request.user.get_hotel()
