from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.models import TimeStampedModel


class RoomFoodInfo(TimeStampedModel):
    """
    Food info
    """
    type = models.ForeignKey('hotels.FoodType', verbose_name=_('type'),
                             related_name='rooms_food_info')
    cost_info = models.ForeignKey('hotels.FoodCost',
                                  verbose_name=_('cost info'),
                                  related_name='rooms_food_info')

    class Meta:
        verbose_name = _('room food info')
        verbose_name_plural = _('room food info')

    def __str__(self):
        return self.type.name


class FoodTime(TimeStampedModel):
    """
    Food time
    """
    FOOD_CHOICES = Choices(
        ('BREAKFAST', _('Breakfast')),
        ('BRUNCH', _('Brunch')),
        ('DINNER', _('Dinner'))
    )

    start = models.TimeField(_('start'))
    end = models.TimeField(_('end'))
    type = models.CharField(_('type'), max_length=32,
                            default=FOOD_CHOICES.BREAKFAST,
                            choices=FOOD_CHOICES)
    room_food_info = models.ForeignKey('hotels.RoomFoodInfo',
                                       verbose_name=_('room food info'),
                                       related_name='times', null=True)

    class Meta:
        verbose_name = _('food time')
        verbose_name_plural = _('food times')

    def __str__(self):
        return self.type


class FoodCost(TimeStampedModel):
    """
    Food cost
    """
    name = models.CharField(_('name'), max_length=64, default='')
    price = models.IntegerField(_('price'), default=0)

    class Meta:
        verbose_name = _('food cost')
        verbose_name_plural = _('food сosts')

    def __str__(self):
        return '{}: {}'.format(self.name, self.price)


class FoodType(TimeStampedModel):
    """
    Food type
    """
    name = models.CharField(_('name'), max_length=32, default='')

    class Meta:
        verbose_name = _('food type')
        verbose_name_plural = _('food types')

    def __str__(self):
        return self.name
