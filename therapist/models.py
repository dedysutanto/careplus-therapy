from django.db import models
from account.models import User, Clinic
from django.utils.translation import gettext_lazy as _
from crum import get_current_user
from wagtail.admin.panels import FieldPanel, InlinePanel, \
    FieldRowPanel, MultiFieldPanel, HelpPanel, TabbedInterface
from student.models import RELIGION


class Therapists(models.Model):
    name = models.CharField('Nama', max_length=100)
    dob = models.DateField(verbose_name=_('Tanggal Lahir'))
    pob = models.CharField(_('Tempat Lahir'), max_length=50, blank=True, null=True)
    address = models.TextField(verbose_name=_('Address'), blank=True, null=True)
    mobile = models.CharField(_('Nomor HP'), max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50,
                                verbose_name=_('Agama'),
                                choices=RELIGION,
                                default='CHRISTIAN', blank=True, null=True)

    education = models.CharField('Pendidikan', max_length=200, blank=True, null=True)
    additional_info = models.TextField('Keterangan', blank=True, null=True)

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
            FieldPanel('name'),
            FieldRowPanel([FieldPanel('pob'), FieldPanel('dob')]),
            FieldPanel('mobile'),
            FieldPanel('address'),
            FieldPanel('education'),
            FieldPanel('additional_info')
        ])
    ]

    class Meta:
        db_table = 'therapist'
        verbose_name = 'Therapist'
        verbose_name_plural = 'Therapist'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        if self.user is None:
            current_user = get_current_user()
            self.user = current_user
            self.clinic = current_user.clinic

        return super(Therapists, self).save()



