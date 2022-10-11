from django.db import models
from crum import get_current_user
from account.models import User, Clinic
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, InlinePanel, \
    FieldRowPanel, MultiFieldPanel, HelpPanel, TabbedInterface


class Activities(models.Model):
    name = models.CharField('Nama Activity', max_length=50)
    code = models.CharField('Kode Activity', max_length=5)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name=_('Owner'),
        null=True
    )

    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.SET_NULL,
        verbose_name=_('Klinik'),
        null=True
    )

    panels = [
        MultiFieldPanel([
            HelpPanel(content='Kode Activity maximum 5 karakter'),
            FieldRowPanel([FieldPanel('name'), FieldPanel('code')]),
        ])
    ]

    class Meta:
        db_table = 'activities'
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        if self.user is None:
            current_user = get_current_user()
            self.user = current_user
            self.clinic = current_user.clinic

        return super(Activities, self).save()

