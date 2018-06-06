from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication

from apps.auth_core.models.token import AuthToken


class TokenAuthentication(BaseTokenAuthentication):
    """
    Аутентификация по токену
    """
    model = AuthToken

    def authenticate(self, request):
        return super(TokenAuthentication, self).authenticate(request)

    def authenticate_credentials(self, key):

        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if token.user and not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.user or AnonymousUser(), token
