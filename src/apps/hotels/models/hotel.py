from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

from apps.hotels.models.equipment import HotelEquipmentItem, EquipmentItem


class Hotel(TimeStampedModel):
    """
    Hotel
    """

    chief = models.OneToOneField('users.Chief', verbose_name=_('chief'),
                                 related_name='hotel')
    name = models.CharField(_('name'), max_length=64, default='')
    address = models.OneToOneField('hotels.Address',
                                   verbose_name=_('hotel address'))
    registration_from = models.DateTimeField(_('registration from'),
                                             default=None, null=True,
                                             blank=True)
    registration_to = models.DateTimeField(_('registration to'), default=None,
                                           null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=32, default='', null=True,
                             blank=True)
    email = models.EmailField(_('email'), default='', null=True, blank=True)
    website = models.CharField(_('website'), max_length=64, default='',
                               null=True, blank=True)
    description = models.CharField(_('description'), max_length=1024,
                                   default='', null=True, blank=True)
    rating = models.PositiveIntegerField(_('rating'), default=0, null=True,
                                         blank=True)
    rating_confirmed = models.BooleanField(_('rating confirmed'),
                                           default=False)

    class Meta:
        verbose_name = _('hotel')
        verbose_name_plural = _('hotels')

    def __str__(self):
        return self.name


@receiver(post_save, sender=Hotel)
def create_hotel_items(sender, instance, **kwargs):
    """
    Adding equipment to the hotel
    """
    if not HotelEquipmentItem.objects.filter(hotel=instance).exists():
        items = EquipmentItem.objects.all()

        hotel_items = [
            HotelEquipmentItem(hotel=instance,equipment_item=item, active=False)
            for item in items]

        HotelEquipmentItem.objects.bulk_create(hotel_items)
