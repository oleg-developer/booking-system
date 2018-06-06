from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import BasePermission


class TokenRequired(BasePermission):
    """
    Checking the Authorization Token 
    """
    message = _("No authorization token")

    def has_permission(self, request, view):
        return request.auth


class IsAuthenticated(BasePermission):
    """
    Verify user authorization
    """
    message = _("User not authorized")

    def has_permission(self, request, view):
        return request.user.is_authenticated()
