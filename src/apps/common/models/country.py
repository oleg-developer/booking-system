import os
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

__all__ = [
    'Country'
]


def upload_logo(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = '{name}.{ext}'.format(name=str(uuid.uuid4()), ext=ext)
    return os.path.join('countries', 'logo', new_filename)


class Country(TimeStampedModel):
    """
    Country
    """
    code = models.CharField(_('code'), max_length=4, default='', blank=True,
                            null=True)
    name = models.CharField(_('name'), max_length=32, default='')
    # TODO: use thumbnail
    logo = models.ImageField(_('logo'), default=None, upload_to=upload_logo,
                             blank=True, null=True)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self):
        return self.name
