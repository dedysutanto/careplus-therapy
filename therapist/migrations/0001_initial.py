# Generated by Django 3.2.6 on 2022-10-10 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Therapists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nama')),
                ('dob', models.DateField(verbose_name='Tanggal Lahir')),
                ('pob', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tempat Lahir')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('mobile', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nomor HP')),
                ('religion', models.CharField(blank=True, choices=[('CHRISTIAN', 'Kristen'), ('CATHOLIC', 'Katholik'), ('ORTHODOX', 'Orthodox'), ('ISLAM', 'Islam'), ('HINDU', 'Hindu'), ('BUDDHA', 'Budha')], default='CHRISTIAN', max_length=50, null=True, verbose_name='Agama')),
                ('education', models.CharField(blank=True, max_length=200, null=True, verbose_name='Pendidikan')),
                ('clinic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.clinic', verbose_name='Klinik')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Therapist',
                'verbose_name_plural': 'Therapist',
                'db_table': 'therapist',
            },
        ),
    ]
