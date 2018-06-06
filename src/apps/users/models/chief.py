from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.users.models.profile import AbstractProfile


class Chief(AbstractProfile):
    """
    Hotel chief
    """
    country = models.ForeignKey('common.Country', verbose_name=_('country'),
                                related_name='chiefs')

    class Meta:
        verbose_name = _('chief')
        verbose_name_plural = _('chiefs')

    def __str__(self):
        return self.user.get_full_name()
