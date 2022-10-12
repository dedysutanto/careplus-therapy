from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from config.utils import calculate_age
from wagtail.admin.panels import FieldPanel, InlinePanel, \
    FieldRowPanel, MultiFieldPanel, HelpPanel, TabbedInterface
from account.models import User, Clinic
from crum import get_current_user
from student.models import Students
from data_support.models import InvoiceItems
from django.utils.timezone import now
from django.db.models import Sum
from django.core.exceptions import ValidationError


class Invoices(ClusterableModel):
    def limit_choices_to_current_user():
        user = get_current_user()
        if not user.is_superuser:
            return {'user': user}
        else:
            return {}

    datetime = models.DateTimeField(_('Tanggal'), default=now)
    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
        verbose_name='Siswa',
        limit_choices_to=limit_choices_to_current_user
    )

    is_paid = models.BooleanField(_('Sudah Dibayar'), default=False)
    #is_cancel = models.BooleanField(_('Batal'), default=False)

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
        FieldRowPanel([FieldPanel('student'), FieldPanel('datetime')]),
        InlinePanel('related_invoice_item', heading='Items', label='Detail Item'),
        FieldPanel('is_paid'),
    ]

    class Meta:
        db_table = 'invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def clean(self):
        invoice_item = InvoiceItems.objects.filter(invoice=self)

        if not invoice_item:
            raise ValidationError('Item Invoice harus ada. Silakan ditambahkan Invoice Item')

    '''
    def save(self):
        if self.user is None:
            current_user = get_current_user()
            self.user = current_user
            self.clinic = current_user.clinic

        return super(Invoices, self).save()
    '''

    def calculate_total(self):
        total_text = 0
        total = InvoiceItems.objects.filter(invoice=self).aggregate(Sum('sub_total'))
        if total['sub_total__sum']:
            total_text = total['sub_total__sum']
        return 'Rp. {:,}'.format(total_text).replace(',', '.')
    calculate_total.short_description = 'Total'


class InvoiceItems(Orderable):
    item = models.ForeignKey(
        InvoiceItems,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(blank=True, null=True)
    sub_total = models.IntegerField()

    invoice = ParentalKey('Invoices', on_delete=models.CASCADE, related_name='related_invoice_item')

    panels = [
        FieldRowPanel([
            FieldPanel('item'),
            FieldPanel('quantity'),
            FieldPanel('price', widget=forms.TextInput(attrs={"disabled": True}))
        ])
    ]

    class Meta:
        db_table = 'invoice_items'
        verbose_name = 'Item'
        verbose_name_plural = 'Item'

    def save(self):
        self.price = self.item.price
        self.sub_total = self.quantity * self.price
        return super(InvoiceItems, self).save()