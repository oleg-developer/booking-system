from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class EquipmentSection(TimeStampedModel):
    """
    Equipment category
    """
    title = models.CharField(_('title'), max_length=32, default='')
    label = models.CharField(_('label'), max_length=128, default='')

    class Meta:
        verbose_name = _('equipment section')
        verbose_name_plural = _('equipment sections')

    def __str__(self):
        return self.label


class EquipmentItem(TimeStampedModel):
    """
    Element of hotel equipment
    """
    section = models.ForeignKey('hotels.EquipmentSection',
                                verbose_name=_('section'),
                                related_name='items')
    label = models.CharField(_('label'), max_length=64, default='')

    class Meta:
        verbose_name = _('equipment item')
        verbose_name_plural = _('equipment items')

    def __str__(self):
        return '{} ({})'.format(self.label, self.section.label)


class HotelEquipmentItem(TimeStampedModel):
    """
    Relation of the equipment element with the hotel
    """
    hotel = models.ForeignKey('hotels.Hotel', verbose_name=_('hotel'),
                              related_name='equipment_items')
    equipment_item = models.ForeignKey('hotels.EquipmentItem',
                                       verbose_name=_('equipment item'),
                                       related_name='+')
    active = models.BooleanField(_('active'), default=False)

    class Meta:
        verbose_name = _('hotel equipment item')
        verbose_name_plural = _('hotel equipment item')

    def __str__(self):
        return '{}: {}'.format(self.hotel, self.hotel.name)
