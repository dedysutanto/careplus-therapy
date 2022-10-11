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

'''
class Packages(models.Model):
    name = models.CharField('Nama Paket', max_length=50)
    price = models.IntegerField('Harga Paket')
    session = models.IntegerField('Jumlah Sesi')

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
            #HelpPanel(content='Kode Activity maximum 5 karakter'),
            FieldRowPanel([FieldPanel('name'), FieldPanel('session')]),
            FieldPanel('price')
        ])
    ]

    class Meta:
        db_table = 'packages'
        verbose_name = 'Paket'
        verbose_name_plural = 'Paket'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        if self.user is None:
            current_user = get_current_user()
            self.user = current_user
            self.clinic = current_user.clinic

        return super(Activities, self).save()
'''


class InvoiceItems(models.Model):
    name = models.CharField('Nama Item', max_length=50)
    price = models.IntegerField('Harga Item')
    #discount = models.FloatField('Diskon (%)', default=0)
    #final_price = models.IntegerField('Harga Akhir', default=0)
    session = models.IntegerField('Jumlah Sesi', default=0)
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
            # HelpPanel(content='Kode Activity maximum 5 karakter'),
            FieldPanel('name'),
            # FieldRowPanel([FieldPanel('price'), FieldPanel('discount'), FieldPanel('session')]),
            FieldRowPanel([FieldPanel('price'), FieldPanel('session')]),
            FieldPanel('additional_info')
        ])
    ]

    class Meta:
        db_table = 'invoice_items_setting'
        verbose_name = 'Daftar Item'
        verbose_name_plural = 'Daftar Item'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        if self.user is None:
            current_user = get_current_user()
            self.user = current_user
            self.clinic = current_user.clinic

        # self.final_price = self.price * (1 - self.discount/100)

        return super(InvoiceItems, self).save()