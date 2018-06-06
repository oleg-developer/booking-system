import os
import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

__all__ = [
    'AbstractProfile'
]


# TODO: do a generic method for upload_logo
def upload_file(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = '{name}.{ext}'.format(name=str(uuid.uuid4()), ext=ext)
    return os.path.join('profile', 'photo', new_filename)


class AbstractProfile(TimeStampedModel):
    """
    Common user info
    """
    user = models.OneToOneField('users.User', related_name='%(class)s')
    first_name = models.CharField(_('first_name'), default='', max_length=64,
                                  null=True, blank=True)
    second_name = models.CharField(_('second_name'), default='', max_length=64,
                                   null=True, blank=True)
    last_name = models.CharField(_('last_name'), default='', max_length=64,
                                 null=True, blank=True)
    photo = models.ImageField(_('photo'), default=None, upload_to=upload_file,
                              blank=True, null=True)
    # TODO: move to Chief model
    email_confirmed = models.BooleanField(_('email_confirmed'), default=False)
    phones = GenericRelation('common.Phone')

    class Meta:
        abstract = True

    @property
    def full_name(self):
        if any([self.first_name, self.second_name, self.last_name]):
            return '{last} {first} {second}' \
                .format(last=self.last_name or '', first=self.first_name or '',
                        second=self.second_name or '') \
                .strip()
        return self.user.username
