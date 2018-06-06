from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.models import TimeStampedModel


class Order(TimeStampedModel):
    """
    Order/booking 
    """
    STATUS_CHOICES = Choices(
        ('booking_confirmed', 'BOOKING_CONFIRMED', _('booking confirmed')),
        ('booking_not_confirmed', 'BOOKING_NOT_CONFIRMED',
         _('booking not confirmed')),
        ('occupied', 'OCCUPIED', _('occupied')),
        ('alert', 'ALERT', _('alert'))
    )

    room = models.ForeignKey('hotels.HotelRoom', verbose_name=_('room'),
                             related_name='orders')
    guest = models.ForeignKey('hotels.Guest', verbose_name=_('guest'),
                              related_name='orders')
    arrival_date = models.DateTimeField(_('arrival date'), default=None,
                                        null=True, blank=True)
    leave_date = models.DateTimeField(_('leave date'), default=None, null=True,
                                      blank=True)
    payment_status = models.CharField(_('payment status'), max_length=32,
                                      default=STATUS_CHOICES.BOOKING_NOT_CONFIRMED,
                                      choices=STATUS_CHOICES)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return '{number}: {arrival} - {leave}'.format(number=self.room.number,
                                                      arrival=self.arrival_date,
                                                      leave=self.leave_date)

    def get_total_price(self):
        """
        Get total price
        :return: 
        """
        # TODO: Implement this method
        return 0.0
