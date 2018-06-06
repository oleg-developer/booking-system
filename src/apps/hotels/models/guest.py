from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Guest(TimeStampedModel):
    """
    Guest
    """
    hotel = models.ForeignKey('hotels.Hotel', verbose_name=_('hotel'),
                              related_name='guests')
    first_name = models.CharField(_('first_name'), default='', max_length=64)
    second_name = models.CharField(_('second_name'), default='', max_length=64,
                                   null=True, blank=True)
    last_name = models.CharField(_('last_name'), default='', max_length=64,
                                 null=True, blank=True)
    email = models.EmailField(_('email'), default='', max_length=64, null=True,
                              blank=True)
    agent = models.CharField(_('agent'), default='', max_length=64, null=True,
                             blank=True)
    information = models.CharField(_('information'), default='',
                                   max_length=512, null=True, blank=True)

    class Meta:
        verbose_name = _('guest')
        verbose_name_plural = _('guests')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return '{} {} {}'.format(self.first_name, self.second_name,
                                 self.last_name)
