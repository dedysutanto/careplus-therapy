# Generated by Django 3.2.6 on 2022-10-10 05:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='clinic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.clinic', verbose_name='Klinic'),
        ),
        migrations.AddField(
            model_name='students',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
