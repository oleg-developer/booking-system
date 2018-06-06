from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Phone(TimeStampedModel):
    """
    Phone
    """
    main = models.CharField(_("main"), default='', max_length=32, )
    option = models.CharField(_("option"), default='', max_length=8, null=True,
                              blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    profile = GenericForeignKey()

    class Meta:
        verbose_name = _("phone")
        verbose_name_plural = _("phones")

    def __str__(self):
        return self.main
