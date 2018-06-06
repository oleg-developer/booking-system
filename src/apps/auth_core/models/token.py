from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel

from apps.auth_core.utils import generate_string

__all__ = [
    'AuthToken'
]


class AuthToken(TimeStampedModel):
    """
    Authorization Token
    """

    PLATFORM_CHOICES = Choices(
        ('web', 'WEB', _('Web')),
        ('ios', 'IOS', _('IOS')),
        ('android', 'ANDROID', _('Android')),
    )

    key = models.CharField(_('key'), max_length=128, primary_key=True,
                           default=generate_string, editable=False)

    platform = models.SlugField(_('platform'), choices=PLATFORM_CHOICES,
                                default=PLATFORM_CHOICES.WEB)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             related_name='tokens', default=None, blank=True,
                             null=True)

    version = models.FloatField(_('version'), default=1.0)

    client = models.CharField(_('client'), max_length=1024, default='')

    class Meta:
        verbose_name = _('auth token')
        verbose_name_plural = _('auth tokens')

    def __str__(self):
        return 'Token value: {}'.format(self.key)
