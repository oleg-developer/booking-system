from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class HotelRoom(TimeStampedModel):
    """
    Hotel room
    """
    type = models.ForeignKey('RoomType', verbose_name=_('type'),
                             related_name='rooms', default=None, null=True)
    hotel = models.ForeignKey('hotels.Hotel', verbose_name=_('hotel'),
                              related_name='rooms')
    number = models.CharField(_('number'), default='', max_length=16)
    price = models.FloatField(_('price'), default=0.0)
    title = models.CharField(_('title'), default='', max_length=32, null=True,
                             blank=True)
    building = models.CharField(_('building'), default='', max_length=16,
                                null=True, blank=True)
    floor = models.IntegerField(_('floor'), default=1)
    number_group = models.CharField(_('number_group'), default='',
                                    max_length=16)
    photo = models.ImageField(_('photo'), default=None, null=True, blank=True)
    single_bed = models.PositiveIntegerField(_('single bed count'), default=0)
    double_bed = models.PositiveIntegerField(_('double bed count'), default=0)
    bunk_bed = models.PositiveIntegerField(_('bunk bed count'), default=0)
    rooms_count = models.IntegerField(_('rooms count'), default=1)
    area = models.FloatField(_('area'), default=0.0)
    description = models.CharField(_('description'), max_length=1024,
                                   default='', null=True, blank=True)
    capacity = models.PositiveSmallIntegerField(_('capacity'), default=0)

    class Meta:
        verbose_name = _('hotel room')
        verbose_name_plural = _('hotel rooms')

    def __str__(self):
        return self.number


class RoomType(TimeStampedModel):
    """
    Room type
    """
    abbreviation = models.CharField(_('abbreviation'), max_length=16,
                                    default='', blank=True, null=True)
    name = models.CharField(_('name'), max_length=32, default='')
    capacity = models.PositiveSmallIntegerField(_('capacity'), default=0,
                                                blank=True, null=True)
    english_name = models.CharField(_('english name'), max_length=32,
                                    default='')
    description = models.CharField(_('description'), max_length=1024,
                                   default='', null=True, blank=True)

    class Meta:
        verbose_name = _('room type')
        verbose_name_plural = _('room types')

    def __str__(self):
        return self.name
