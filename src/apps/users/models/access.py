from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Access(TimeStampedModel):
    """
    Staff Access
    """
    name = models.CharField(_("name"), max_length=32, default='')
    label = models.CharField(_("label"), max_length=32, default='')
    logo = models.ImageField(_("logo"), default=None)

    class Meta:
        verbose_name = _("access")
        verbose_name_plural = _("accesses")

    def __str__(self):
        return self.name


class StaffAccess(TimeStampedModel):
    """
    Staff and Access relation
    """
    staff = models.ForeignKey('users.Staff', verbose_name=_("staff"),
                              related_name='accesses')
    access = models.ForeignKey('users.Access', verbose_name=_("access"),
                               related_name='+')
    active = models.BooleanField(_("active"), default=False)

    class Meta:
        verbose_name = _("staff access")
        verbose_name_plural = _("staff accesses")

    def __str__(self):
        return "{}: {}".format(self.staff, self.access.name)
