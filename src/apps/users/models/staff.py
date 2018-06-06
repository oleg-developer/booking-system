from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from apps.users.models.access import Access, StaffAccess
from apps.users.models.profile import AbstractProfile


class Staff(AbstractProfile):
    """
    Hotel staff (employee)
    """
    chief = models.ForeignKey('users.Chief', verbose_name=_('chief'))
    is_locked = models.BooleanField(_('is_locked'), default=False)
    position = models.CharField(_('position'), max_length=32, default='')

    class Meta:
        verbose_name = _('staff')
        verbose_name_plural = _('staffs')

    def __str__(self):
        return self.user.get_full_name()


@receiver(post_save, sender=Staff)
def create_staff_accesses(sender, instance, **kwargs):
    """
    Adding access (permissions) for hotel staff
    """
    if not StaffAccess.objects.filter(staff=instance).exists():
        accesses = Access.objects.all()

        staff_acceses = [
            StaffAccess(staff=instance, access=access, active=False)
            for access in accesses]

        StaffAccess.objects.bulk_create(staff_acceses)
