from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

__all__ = [
    'Address', 'LocationType', 'StreetType', 'DistanceType'
]


class Address(TimeStampedModel):
    """
    Address
    """
    city = models.CharField(_('city'), default='', max_length=64, )
    location_type = models.ForeignKey('hotels.LocationType',
                                      verbose_name=_('location type'),
                                      related_name='hotel_addresses',
                                      null=True, blank=True)
    street_type = models.ForeignKey('hotels.StreetType',
                                    verbose_name=_('street type'),
                                    related_name='+', null=True, blank=True)
    street = models.CharField(_('street'), default='', max_length=64,
                              null=True, blank=True)
    distance_type = models.ForeignKey('hotels.DistanceType',
                                      verbose_name=_('distance type'),
                                      related_name='+', null=True, blank=True)
    distance = models.FloatField(_('distance'), default=0.0, null=True,
                                 blank=True)
    latitude = models.CharField(_('latitude'), max_length=64, default='',
                                null=True, blank=True)
    longitude = models.CharField(_('longitude'), max_length=64, default='',
                                 null=True, blank=True)
    house = models.CharField(_('house'), max_length=16, default='', null=True,
                             blank=True)
    building = models.CharField(_('building'), max_length=8, default='',
                                null=True, blank=True)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    def __str__(self):
        return '{}, {} {}'.format(self.city, self.street_type.label,
                                  self.street)


class LocationType(TimeStampedModel):
    """
     Location type
    """
    label = models.CharField(_('label'), max_length=32, default='')
    value = models.CharField(_('value'), max_length=32, default='')

    class Meta:
        verbose_name = _('location type')
        verbose_name_plural = _('location types')

    def __str__(self):
        return self.label


class StreetType(TimeStampedModel):
    """
    Street type
    """
    label = models.CharField(_('label'), max_length=32, default='')
    value = models.CharField(_('value'), max_length=32, default='')

    class Meta:
        verbose_name = _('street type')
        verbose_name_plural = _('street types')

    def __str__(self):
        return self.label


class DistanceType(TimeStampedModel):
    """
    Distance type
    """
    label = models.CharField(_('label'), max_length=32, default='')
    value = models.CharField(_('value'), max_length=32, default='')

    class Meta:
        verbose_name = _('distance type')
        verbose_name_plural = _('distance types')

    def __str__(self):
        return self.label
