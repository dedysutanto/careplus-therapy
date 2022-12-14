# Generated by Django 3.2.6 on 2022-10-13 03:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import invoice.models
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('data_support', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=12, unique=True, verbose_name='Nomor Invoice')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Tanggal')),
                ('additional_info', models.TextField(blank=True, null=True, verbose_name='Keterangan')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Sudah Dibayar')),
                ('clinic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.clinic', verbose_name='Klinik')),
                ('student', models.ForeignKey(limit_choices_to=invoice.models.Invoices.limit_choices_to_current_user, on_delete=django.db.models.deletion.CASCADE, to='student.students', verbose_name='Siswa')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'db_table': 'invoices',
            },
        ),
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('sub_total', models.IntegerField()),
                ('invoice', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_invoice_item', to='invoice.invoices')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_support.invoiceitems')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Item',
                'db_table': 'invoice_items',
            },
        ),
    ]
