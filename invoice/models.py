from django.db import models
from django.utils.timezone import now
from django.db.models import Sum
from django.core.exceptions import ValidationError
from crum import get_current_user
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel
from account.models import User, Clinic
from student.models import Students
from data_support.models import InvoiceItems


class InvoicesForm(WagtailAdminPageForm):
    class Meta:
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        is_invoice_item = False
        for form in self.formsets['related_invoice_item'].forms:

            if form.is_valid():
                cleaned_form_data = form.clean()
                item = cleaned_form_data.get('item')
                if item:
                    is_invoice_item = True

        if is_invoice_item:
            return cleaned_data
        else:
            raise ValidationError('Item Invoice harus ada. Silakan ditambahkan Invoice Item')


class Invoices(ClusterableModel):
    def limit_choices_to_current_user():
        user = get_current_user()
        if not user.is_superuser:
            return {'user': user}
        else:
            return {}

    number = models.CharField(_('Nomor Invoice'), max_length=12, unique=True)
    datetime = models.DateTimeField(_('Tanggal'), default=now)
    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
        verbose_name='Siswa',
        limit_choices_to=limit_choices_to_current_user
    )

    additional_info = models.TextField('Keterangan', blank=True, null=True)

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
        FieldPanel('additional_info'),
        FieldPanel('is_paid'),
    ]

    base_form_class = InvoicesForm

    class Meta:
        db_table = 'invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    '''
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

        if len(str(self.number)) != 12:
            #number = Invoices.objects.filter(user=self.user, student=self.student).count() + 1
            last_invoice = Invoices.objects.filter(user=self.user, student=self.student).last()
            #print(last_invoice.number)
            if last_invoice:
                last_number = int(last_invoice.number[9:])
                print("Last Invoice Number", last_number)
            else:
                last_number = 0

            prefix = 'INV{:03d}{:03d}'.format(self.user.id, self.student.id)
            #self.number = '{}{:03d}'.format(prefix, number)
            self.number = '{}{:03d}'.format(prefix, last_number + 1)
            print('Invoice', self.number)

            '''
            is_no_number = False
            counter = 1
            while not is_no_number
                try:
                    Invoices.objects.get(number=self.number)
                    counter += 1
                    self.number = '{}{:03d}'.format(prefix, last_number + counter)
                    print('Invoice', self.number)
                except ObjectDoesNotExist:
                    is_no_number = True
            '''

        return super(Invoices, self).save()

    def calculate_total(self):
        total_text = 0
        total = InvoiceForItems.objects.filter(invoice=self).aggregate(Sum('sub_total'))
        if total['sub_total__sum']:
            total_text = total['sub_total__sum']
        return 'Rp. {:,}'.format(total_text).replace(',', '.')
    calculate_total.short_description = 'Total'


class InvoiceForItems(Orderable):
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
        return super(InvoiceForItems, self).save()
